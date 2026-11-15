Análisis de seguridad de una arquitectura NoSQL: MongoDB y Elasticsearch
1. Descripción del proyecto

Este proyecto corresponde a una actividad de análisis de seguridad de una arquitectura NoSQL basada en MongoDB y Elasticsearch, integrada mediante una API desarrollada con FastAPI y desplegada utilizando Docker Compose.

El objetivo es identificar vulnerabilidades derivadas de configuraciones inseguras, evaluar sus posibles impactos y aplicar medidas correctoras para mejorar la seguridad del entorno.

La actividad se desarrolla mediante dos configuraciones diferenciadas:

Entorno vulnerable: configuración inicial con mecanismos de seguridad deshabilitados o insuficientes, utilizada para identificar y demostrar las vulnerabilidades.
Entorno securizado: configuración modificada para incorporar autenticación, control de accesos, reducción de servicios expuestos y otras medidas de protección.
2. Tecnologías utilizadas
Componente	Tecnología
API	FastAPI
Lenguaje	Python 3.11
Base de datos NoSQL	MongoDB 7
Motor de búsqueda	Elasticsearch 7.17.10
Contenedores	Docker
Orquestación	Docker Compose
Reconocimiento	Nmap
Pruebas HTTP	curl
Entorno de desarrollo	Eclipse / editores de código
3. Estructura del proyecto

El repositorio presenta la siguiente organización:

text
.
├── docker-compose-insecure.yml
├── docker-compose.yml
├── fastapi-app
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── README.md
└── scripts
    ├── init_elastic.sh
    └── init_mongo.js

Descripción de los archivos
Archivo	Función
docker-compose-insecure.yml	Configuración inicial del entorno vulnerable.
docker-compose.yml	Configuración del entorno con las medidas de seguridad aplicadas.
fastapi-app/Dockerfile	Construcción de la imagen Docker de FastAPI.
fastapi-app/main.py	Código fuente de la API y sus endpoints.
fastapi-app/requirements.txt	Dependencias Python necesarias para ejecutar la aplicación.
scripts/init_elastic.sh	Script de inicialización de Elasticsearch.
scripts/init_mongo.js	Script de inicialización de MongoDB y creación de usuarios.
4. Requisitos previos

Para desplegar el entorno es necesario disponer de:

Docker Desktop o Docker Engine.
Docker Compose.
Git (opcional).
curl para realizar las pruebas HTTP.
Nmap para las pruebas de reconocimiento.
5. Despliegue del entorno vulnerable

Esta configuración permite reproducir las condiciones iniciales de la actividad y analizar las vulnerabilidades existentes antes de aplicar las medidas correctoras.

Desde el directorio raíz del proyecto, ejecutar:

bash
docker compose -f docker-compose-insecure.yml up --build -d


Para comprobar el estado de los contenedores:

bash
docker compose -f docker-compose-insecure.yml ps


Para consultar los registros:

bash
docker compose -f docker-compose-insecure.yml logs


En esta fase se analizan especialmente:

Exposición de los puertos 8000, 9200 y 27017.
Acceso anónimo a MongoDB.
Acceso anónimo a Elasticsearch.
Posibles vulnerabilidades de inyección NoSQL.
Ausencia o insuficiencia de mecanismos de autenticación y autorización.
6. Despliegue del entorno securizado

Una vez identificadas las vulnerabilidades, se utiliza el archivo docker-compose.yml, que incorpora las modificaciones realizadas durante las fases de defensa mínima y endurecimiento ampliado.

Para iniciar el entorno:

bash
docker compose up --build -d


Comprobar el estado de los servicios:

bash
docker compose ps


Consultar los registros:

bash
docker compose logs


Entre las medidas de seguridad aplicadas se encuentran:

Habilitación de autenticación en MongoDB mediante --auth.
Creación de un usuario específico con permisos de lectura y escritura.
Activación de los mecanismos de seguridad de Elasticsearch mediante xpack.security.enabled.
Eliminación de la publicación directa del puerto 9200 en el host.
Validación de entradas en la API.
Restricción de parámetros de búsqueda y resultados.
Incorporación de TLS y cabeceras de seguridad HTTP.
Limitación de solicitudes mediante rate limiting.
Configuración de un repositorio local de snapshots en Elasticsearch.
Revisión de los registros de actividad de los contenedores.
7. Inicialización de las bases de datos

Los scripts de la carpeta scripts/ permiten preparar los servicios para las pruebas.

MongoDB

El archivo scripts/init_mongo.js contiene las instrucciones para:

Seleccionar la base de datos de trabajo.
Insertar usuarios de prueba.
Crear un usuario específico para la aplicación.
Asignar permisos de lectura y escritura.
Insertar un pedido inicial de prueba.

La creación del usuario específico permite aplicar el principio de mínimo privilegio.

Elasticsearch

El archivo scripts/init_elastic.sh contiene las operaciones necesarias para la inicialización del servicio, según la configuración definida para el entorno.

8. Pruebas de funcionamiento y seguridad

Una vez desplegados los servicios, se realizan comprobaciones para verificar su disponibilidad y comportamiento.

Comprobación de contenedores
bash
docker compose ps

Comprobación de la API FastAPI
bash
curl -i http://localhost:8000/

Consulta de registros
bash
docker compose logs fastapi


El nombre del servicio debe corresponder al definido en el archivo Docker Compose.

Pruebas de reconocimiento

Se utiliza Nmap para comprobar la exposición de los puertos del entorno de laboratorio.

Se presta especial atención a los puertos:

8000: API FastAPI.
9200: Elasticsearch.
27017: MongoDB.

Las pruebas de acceso a las bases de datos se realizan teniendo en cuenta la configuración de autenticación de cada entorno.

9. Verificación de las medidas correctoras

Tras aplicar las medidas de seguridad se comprueba:

Que MongoDB exige autenticación.
Que el usuario de aplicación dispone únicamente de los permisos asignados.
Que Elasticsearch incorpora mecanismos de autenticación y seguridad.
Que el puerto 9200 deja de estar publicado directamente en el host.
Que FastAPI continúa comunicándose con los servicios mediante la red interna de Docker.
Que las solicitudes incorrectas de autenticación devuelven respuestas HTTP adecuadas.
Que el mecanismo de limitación de solicitudes responde ante peticiones repetitivas.
Que se pueden consultar los registros de actividad de los contenedores.
10. Detención del entorno

Para detener el entorno securizado:

bash
docker compose down


Para detener el entorno vulnerable:

bash
docker compose -f docker-compose-insecure.yml down


Si se desea eliminar también los volúmenes asociados:

bash
docker compose down -v


Advertencia: la opción -v elimina los volúmenes gestionados por Docker Compose y puede provocar la pérdida de los datos almacenados.

11. Consideraciones de seguridad

Este proyecto tiene fines exclusivamente educativos y experimentales.

Las configuraciones vulnerables se utilizan únicamente para demostrar los riesgos asociados a una arquitectura NoSQL insuficientemente protegida.

Las pruebas deben realizarse exclusivamente en el entorno de laboratorio autorizado.

Las contraseñas, claves privadas y demás credenciales reales no deben almacenarse en el repositorio.

12. Resultado de la actividad

La actividad permite analizar y comparar el comportamiento de una arquitectura NoSQL antes y después de aplicar diferentes medidas de seguridad.

Se demuestra la importancia de la autenticación, la autorización, la validación de entradas, el cifrado de comunicaciones, la reducción de la superficie de exposición y la monitorización para proteger los servicios y la información almacenada.
