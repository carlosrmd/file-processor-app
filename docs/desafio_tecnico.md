## Desafío técnico

### Lectura del archivo

Clases implementadas:
-**FileFormatter**:  Clase abstracta sin implementación. La clase que la implemente debe implementar el método **format**, quien le dará formato a cada línea leída.
-**CsvFileFormatter**: Implementación de **FileFormatter**. Responsabilidad de interpretar cada línea en formato CSV y utiliza el separador leido de la configuración.
-**FileReader**: Responsabilidad de lectura de archivos por chunks. Implementa el método generador **chunk_reader** que dado el tamaño (nro de líneas) abre el archivo, lee las N cantidad de líneas solicitadas y hace yield del set de líneas, con el formato dado por el FileFormatter del cual depende.
-**FileProcessor**: Responsabilidad de tomar los chunks de **FileReader** y utilizar el **ApiManager** para realizar la tarea. Se inicializa con ambos objetos de los cuales depende y realiza el trabajo en el método **process**.

Dependencias:
FileReader <- FileFormatter
FileProcessor <- (FileReader, ApiManager)

### Consulta de las API

Clases implementadas:
-**ApiManager**: Clase abstracta sin implementación. Quien la implemente debe hacer override al método **download_and_store_items**.
-**MeliApiManager**: Implementación de **ApiManager**. Responsabilidad de, para un set de líneas formateadas dadas, realizar las consultas al API de Mercado Libre y guardar los resultados en la base de datos. 

La implementación se hizo con la librería concurrent.future, que implementa la clase ThreadPoolExecutor.

El objeto ThreadPoolExecutor se crea con un límite de 30 workers, ejecuta las tareas de consultar la API de Item, obtiene la información relevante y luego crea tres subthreads más de la misma manera para consultar las otras tres APIs solicitadas. Una vez recopilada toda la información de un Item, el thread inserta el objeto en la base de datos.

### Base de Datos

Clases implementadas:
-**Item**: Clase para almacenar un registro de información de un item particular, para poder ser almacenado en la base de datos.
-**MysqlDatabaseManager**: Clase que inicializa y almacena un pool de conexiones a la base de datos MySQL. Implementa el método store_record que recibe un objeto Item, abre conexión mediante el pool y lo almacena en la base de datos.

Se escogió el motor relacional MySQL dado que es muy popular, altamente usado, con trayectoria, sólido y open source.

La conexión es accesible desde cualquier parte del programa, pero solo el ApiManager tiene la responsabilidad de usarla para insertar los elementos a medida que obtiene la información completa para cada uno.

Esta implementación significó un bottleneck en la ejecución ya que el Pool solo admite 32 conexiones simultáneas, y cualquier intento de conexión una vez lleno era rechazada por la librería.

### Logger

Clases implementadas:
-**Logger**: Clase abstracta para un logger. Quien la implemente de hacer override al método **log**.
-**FileLogger**: Implementación de **Logger**. En el método **log** recibe un texto y hace log del mismo a un archivo especificado en la configuración. Este logger es accesible desde todo el código pero sólo lo utiliza ApiManager.

### Docker

Se utilizó Docker y docker-compose para mayor facilidad al construir/levantar/bajar los containers.

Se utiliza un container tanto para la app y otro container para la base de datos.

En el directorio "docker" del repo se encuentran ambos Dockerfile y, para el caso de la base de datos, un script SQL que crea la tabla al momento de levantar el container.