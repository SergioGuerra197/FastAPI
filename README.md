# FastAPI

Proyecto para practica de Framework de fastAPI, se ejecutará un CRUD con protocolos HTTP, en este caso usando fastAPI, la ejecución sera por medio de uvicorn.

# Ejecucion en Windows

Para la correcta ejecucion de este proyecto se deja las instrucciones en el siguiente segmento del README, estos comandos se ejecutan en la consola de comandos, en la ubicacion en la que se quiera el proyecto, reemplazando URL por el link del repositorio.

```sh
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
git clone URL
python -m  venv venv
venv/Scripts/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 5000
```

Al ejecutar estos comandos, en el navegador, se ingresa la siguiente URL, donde se encontrá con la documentacion, y las secciones creadas en el proyecto, con la opcion de ejecutarlas.

```sh
localhost:5000/docs
```
