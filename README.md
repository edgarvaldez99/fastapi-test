# iCargo BACKEND

Proyecto backend para iCargo desarrollado con [FastAPI](https://fastapi.tiangolo.com/)

## EJECUTAR LOCALMENTE

### Pre-requisitos

- Python 3.8
- Pip 3 `(sudo apt-get install python3-pip)`
- Instalar Poetry. Seguir la [guía para la instalación](https://python-poetry.org/docs/)
- Instalar virtualenv `(sudo apt-get install python3-virtualenv python3-venv)`
- Crear entorno virtual:
    ```
    virtualenv -p `which python3` .venv
    ```
- Activar el entorno virtual:
    ```
    source .venv/bin/activate
    ```
- Instalar las dependencias especificadas en [pyproject.toml]:
    ```
    poetry install --no-root
    ```
- Cree una base de datos con postgres
- Copie y renombre el archivo `.env-example` a `.env` (No reemplace directamente el archivo `.env-example`, cópielo)
- En el archivo `.env` cambie los valores de las variables de la base de datos para que apunten a la base de datos a utilizar.

    Ejemplo:
    ```
    ENV=development
    DATABASE_URL=localhost:5432
    DATABASE_USER=fastapi-test
    DATABASE_PASS=fastapi-test
    DATABASE_NAME=fastapi-test
    DATABASE_TYPE=postgresql
    INSTALL_DEV=true
    SECRET_KEY=secret_key

    ```

### Ejecutar

- Para levantar la aplicación utilice el comando:

    ```
    uvicorn app.main:app --reload
    ```

    **Obs:** Asegúrese de haber activado el virtualenv `(source .venv/bin/activate)`

- El backend estará disponible en `http://localhost:8000`

## EJECUTAR CON DOCKER
- Copie y renombre el archivo `.env-example` a `.env` (No reemplace directamente el archivo `.env-example`, cópielo)
- En el archivo `.env` cambie el valor de la variable `DATABASE_URL` a `db` (nombre del servicio de base datos en el docker-compose). Cambiar el valor del resto de las variables es opcional
- Ejecutar
    ```
    docker-compose up --build
    ```
- El backend estará disponible en `http://localhost:8000`

- Para iniciar una sesión interactiva en el contenedor de backend ejecute:
    ```
    docker-compose exec backend bash
    ```

- Para ver el log utilice:
    ```
    docker-compose logs -f backend
    ```

## SWAGGER
- FastAPI trae integrado un swagger para probar los servicios, disponible en `http://localhost:8000/docs`

## MIGRACIONES
- Las migraciones a la base de datos se realizan con [Alembic](https://alembic.sqlalchemy.org/en/latest/).

    Para correr las migraciones ejecutar:
    ```
    alembic upgrade head
    ```

    Con docker:
    ```
    docker-compose exec backend alembic upgrade head
    ```

- Para que un modelo sea detectado por alembic para la migración asegurese de importarlo en el archivo [app/models/\_\_init\_\_.py]. Ejemplo:
    ```python
    # debe importarse para que alembic pueda detectar y crear las tablas
    from app.database import Base  # noqa

    from .item import Item  # noqa
    # User es el nuevo modelo
    from .user import User  # noqa
    # La palabra "noqa" se agrega al final de cada import para evitar errores de linteo.

    ```


- Asegúrese de crear una "revisión" (archivo de migración) de sus modelos con cada cambio que haga, ya sea agregando una columna nuevo o creando un nuevo modelo, y luego "actualice" su base de datos con esa revisión cada vez, ya que esto es lo que actualizará las tablas en su base de datos, de lo contrario, su aplicación tendrá errores.

    Para ejecutar revisión utilice el comando:
    ```
    alembic revision --autogenerate -m "Add column last_name to User model"
    ```

    Con docker:
    ```
    docker-compose exec backend alembic revision --autogenerate -m "Add column last_name to User model"
    ```

    Este comando crea los archivos para la migración en la carpeta [alembic/versions]

    Luego de ejecutar la revisión debe actualizar la base de datos:
    ```
    alembic upgrade head
    ```

    Con docker:
    ```
    docker-compose exec backend alembic upgrade head
    ```

## ESTRUCTURA
```
.
├── alembic     # Configuración para las migraciones
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
│       └── * migrations_files
├── alembic.ini
├── app
│   ├── audits          # Modulo de auditoría
│   │   └── __init__.py
│   ├── config.py       # Variables de entorno y configuración
│   ├── database        # Paquete de conf de base de datos
│   │   └── __init__.py
│   ├── dependencies    # Paquete de conf de dependencias
│   │   └── __init__.py
│   ├── endpoints       # Paquete donde se configuran las rutas
│   │   └── __init__.py
│   ├── __init__.py
│   ├── logger.py       # Archivo de conf de logger
│   ├── main.py         # Archivo desde donde se levanta el backend
│   ├── middlewares     # Paquete de interceptores de request
│   │   └── __init__.py
│   ├── models          # Paquete de modelado de base de datos
│   │   └── __init__.py
│   ├── repositories    # Paquete de funciones para acceder a base de datos
│   │   └── __init__.py
│   ├── schemas         # Paquete de modelado de datos para el Frontend
│   │   └── __init__.py
│   ├── services        # Paquete de lógica del negocio 
│   │   └── __init__.py
│   ├── tests           # Paquete donde se configuran los tests
│   │   └── tests.py
│   └── utils           # Paquete de funciones utilitarias
│       └── __init__.py
├── docker-compose.yml
├── Dockerfile
├── mypy.ini        # Configuración para lint:tipos
├── noxfile.py      # Script para lint y test
├── poetry.lock     # Archivo para cerrar versiones
├── prestart.sh     # Script previo al inicio (Docker)
├── pyproject.toml  # Configuración y dependencias del proyecto
├── pytest.ini      # Configuración para test
└── README.md

```

### A tener en cuenta.

- El paquete endpoints es la parte más importante del proyecto, ya que es aquí donde se usan a todos los demás paquetes. Los endpoints solo deben encargarse del enrutado y la documentación del proyecto, no meter logica y/o acceder a la base de datos desde los endpoints.

Ejemplo 1:

```python
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import models, schemas, repositories
from app.dependencies import get_current_user, get_db_session

router = APIRouter()


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(get_current_user),  # Las funciones usadas aquí se importan desde el paquete de dependencies
    db: Session = Depends(get_db_session),  # noqa: B008
) -> Any:
    """
    Get a specific user by id.
    """
    user = repositories.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    # ↑ aquí arriba estamos metiendo lógica, esto podría hacerse desde un servicio y llamar al servicio en la linea del return
    return user

```

Si se transladar la lógica a un servicio, por ejemplo: [app/services/user.py]:

```python
from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import repositories
from app.models.user import User


def get_user_by_id(db: Session, *, user_id: int, current_user: User) -> User:
    user = repositories.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user

```

Entonces nuestro endpoint quedaría de la siguiente forma:

```python
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from app import models, schemas, services
from app.dependencies import get_current_user, get_db_session

router = APIRouter()


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(get_current_user),  # Las funciones usadas aquí se importan desde el paquete de dependencies
    db: Session = Depends(get_db_session),  # noqa: B008
) -> Any:
    """
    Get a specific user by id.
    """
    return services.user.get_user_by_id(db, user_id=user_id, current_user=current_user)
```

Los endpoints solo deben tener la responsabilidad de enrutar y documentar.

Mismo ejemplo se aplicaría en caso de que necesitemos acceder a base de datos:

```python
@router.get("/{email}", response_model=schemas.User)
def my_account(email: str) -> Any:
    """
    Retrieve user by email.
    """
    return db.query(User).filter(User.email == email).first() # se accede a base de datos directamente aquí, mejor usamos un repository
```

Para evitar sobrecargar al endpoint con la responsabilidad de acceder a la base de datos mejor creamos una función en archivo [app/repositories/user.py]:
```python
def get_by_email(db: Session, *, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()
```

Entonces nuestro endpoint quedaría de la siguiente manera:

```python
@router.get("/{email}", response_model=schemas.User)
def my_account(email: str) -> Any:
    """
    Retrieve user by email.
    """
    return repositories.user.get_by_email(db, email=email)
```
