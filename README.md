# file-processor-app

## Servicios

### POST /process_file
#### Descripción:

Recibe nombre del archivo a procesar y tamaño de chunk.
El tamaño de chunk va a ser el número de líneas a cargar en memoria y procesar por vez, para evitar el colapso de la misma, hasta que termine el archivo completo.

Request body:
```
{
	"file_name": string,
	"chunk_size": int
}
```
Response:
```
{
	"http_requests_performed": int,
	"more_info": string,
	"total_time_seconds": float
}
```
### GET /logs

Descarga logs generados durante el procesamiento de archivos.

## Instrucciones para ejecutar el programa:

Requisitos:
- Docker
- docker-compose

Descargar repositorio:

`git clone https://github.com/carlosrmd/file-processor-app.git`

Navegar al directorio del repo descargado:

`cd file-processor-app`

Incluir en el directorio el archivo que se desea procesar. Editar `config.py` y agregar las características del archivo a procesar. Los formatos soportados son: 'csv', 'jsonlines' y 'text'.
```python
file_line_separator = ','
file_encoding = 'utf8'
file_format = 'csv'
```
Construir e iniciar los containers:

`docker-compose build && docker-compose up`

Tomar en cuenta que el container de la base de datos puede tardar un poco en iniciar y mientras tanto se mostrará en pantalla errores de conexión. Esperar al mensaje clásico de Flask `* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)` para comenzar a utilizar los servicios.

Es posible conectarse a la base de datos con los mismos datos de conexión que se aprecian en `config.py` pero cambiando `db` por `localhost` en `host`
