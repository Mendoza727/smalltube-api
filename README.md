# Django Backend Project

![Django](https://img.shields.io/badge/Django-v3.2-blue)
![Python](https://img.shields.io/badge/Python-v3.9-green)
![Docker](https://img.shields.io/badge/Docker-v20.10.7-blue)
![License](https://img.shields.io/badge/License-MIT-blue)

Este es un backend desarrollado en **Django** que proporciona una API RESTful. En este README se explica cómo clonar el repositorio, configurar un entorno virtual, y ejecutar el proyecto en un contenedor Docker. (SMALLTUBE)

## Requisitos previos

Antes de comenzar, asegúrate de tener instalados los siguientes requisitos en tu máquina:

- [Python](https://www.python.org/) (versión 3.9 o superior)
- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/)

## Clonar el Repositorio

Clona este repositorio en tu máquina local:

```bash
git clone https://github.com/Mendoza727/smalltube-api
cd smalltube-api
```

# Configuración del Entorno Virtual
# Ejecución en un Entorno Virtual (sin Docker)
1. Crear un Entorno Virtual
Si no tienes un entorno virtual, crea uno con el siguiente comando:

```bash
python -m venv venv
```

2. Activar el Entorno Virtual

```bash
source venv/bin/activate
cd .\venv\Scripts\activate
```
3. Instalar las Dependencias
Una vez activado el entorno virtual, instala las dependencias del proyecto con:

```bash
pip install -r requirements.txt
```

4. Configurar la Base de Datos
Ejecuta las migraciones para configurar la base de datos:

```bash
python manage.py migrate
```

5. Ejecutar el Servidor de Desarrollo
Inicia el servidor de desarrollo de Django:

```bash
python manage.py runserver
El servidor estará disponible en http://127.0.0.1:8000/.
```

# Ejecución con Docker
Si prefieres usar Docker, sigue estos pasos.

1. Crear los Contenedores Docker
Construye y ejecuta el contenedor Docker con el siguiente comando:

```bash
docker-compose up --build
```
- Este comando descargará las dependencias, construirá la imagen y ejecutará el contenedor.

2. Ejecutar Migraciones dentro del Contenedor Docker
Para aplicar las migraciones dentro del contenedor Docker, ejecuta:

```bash
docker-compose exec django_app python manage.py migrate
```
3. Cargar Datos Iniciales (si es necesario)
Si deseas cargar datos iniciales, puedes hacerlo con:

4. Acceder al Proyecto en el Navegador
Una vez que el contenedor esté corriendo, el servidor de desarrollo estará disponible en http://localhost:8000/.

# Licencia
Este proyecto está bajo la licencia Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).

- Condiciones:

Atribución: Debes dar crédito a los autores originales.
No Comercial: No puedes utilizar el material para fines comerciales.
Compartir Igual: Si adaptas o construyes a partir de este proyecto, debes distribuir tus contribuciones bajo la misma licencia.
Consulta el archivo LICENSE para más detalles.
