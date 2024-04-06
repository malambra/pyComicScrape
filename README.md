<p align="center">
  <img src="https://github.com/malambra/pyComicScrape/blob/main/pyComicScrape.png" />
</p>

**pyComicScrape** permite obtener datos de **ediciones** o **comics** de Whakoom.

## Qué es pyComicScrape?

**pyComicScrape** permite obtener desde la web de whakom, en formato json, los comics indicados en un rango dado. Estos elementos pueden ser insertados en una base de datos mongodb, para su posterior uso o tratamiento.

## Quick start

```bash
    Uso:
    - python main.py {ediciones,comics} start_id [end_id] [--debug] [--delay] 

    Ejemplos de uso:
    - python main.py ediciones 2216 2219 --debug
    - python main.py ediciones 2216 2219
    - python main.py comics 6gppv --debug
    - python main.py comics 6gppv 

    Primer argumento 'ediciones' o 'comics':
        Indica si iteramos sobre las urls de ediciones o comics.
            - Comics usa id alfanuméricos por lo que no permite iterar sobre ellos y obtiene un único elemento.
            - Ediciones usa id numéricos por lo que permite recibir uno o dos argumentos, dependiendo de si obtenemos un único elemento o todos los elementos de un intervalo.

    Luego, debes proporcionar uno o dos id.
    - Para ediciones los id deben ser enteros
    - Para comcis los id son alfanuméricos.

    Debug: Si incluimos '--debug' se habilitar el modo de depuración y no se realizan inserciones en bbdd
    Delay: Por defecto es 0, pero podemos establecer un delay forzado entre peticiones.
```
    
## Persistencia de datos
Para  la persistencia de datos, **pyComicScrape** requiere de una base de datos sobre la que realizar los insert de los objetos generados de nuestra petición.

- **docker-compose.yml** proporciona una instancia de mongodb para realizar las pruebas de persistencia.
    - Levanta **mongo-express** en el puerto 8081 de localhost (user root1)
    - Levanta **mongo** en el puerto 27017 y lo expone en localhost 27018 (user root)
    ```bash
    docker-compose up -d
    ```

- **initializeDB.py** proporciona un script para inicializar nuestra base de datos y la colección indicada.
    ```bash
    python initializeDB.py comics comiteca
    ```
- **scraper.py** viene preconfigurado para insertar datos en la base de datos local con los parámetros anteriormente comentados.
    ```bash
    def connect_to_db():
        client = pymongo.MongoClient("mongodb://root:example@localhost:27018/")
        db = client["comics"]
        collection = db["comiteca"]
        return collection
    ```
    - bbdd: comics
    - collection: comiteca
    - port 27018
    - user:password: `root:example`

## Next steps.
- Añadir enriquecimiento con:
    - género
    - subgénero
    - referidos