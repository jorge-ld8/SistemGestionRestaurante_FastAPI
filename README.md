# 🍝 Proyecto de Gestión de Restaurantes con FastAPI 🍝

Este proyecto es una aplicación de gestión de restaurantes construida con FastAPI. Este README proporcionará los pasos necesarios para configurar y ejecutar la aplicación.

## Descripción

Esta aplicación permite a los usuarios gestionar las operaciones diarias de un restaurante, incluyendo la gestión de menús, pedidos, inventario y personal.

## Requisitos

- Python 3.8+
- Docker 26+


## Configuración del entorno

1. Clone este repositorio con `git clone https://github.com/jorge-ld8/SistemGestionRestaurante_FastAPI.git`
2. Modificar el .env.template y quitarle el template (debe quedar como .env)
3. Build de las imagenes del docker compose con `docker compose build`
4. Correr el docker compose `docker compose up`
5. Generar la migración. Para esto hay que ejecutar primero `cd backend` y posteriormente `alembic revision --autogenerate -m "migración inicial"`
6. Correr la migración con `alembic upgrade head` (dentro del mismo directorio)


> 💡 Se recomienda utilizar PgAdmin para conectarse con la Base de Datos

## Uso

Una vez que el servidor esté en funcionamiento, puede interactuar con la API a través de `http://0.0.0.0:8000/api/v1`.

## Swagger

Una vez que el servidor esté en funcionamiento, puede interactuar con la documentación de los endpoints a través de `http://0.0.0.0:8000/docs`.

## Contacto

Si tiene alguna pregunta o problema, por favor abra un issue en este repositorio.