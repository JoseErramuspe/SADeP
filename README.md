# 🚀 **SADeP** – *Sistema Automático para Desarrollo de Prompts*

📑 **Tabla de Contenidos**
1. [Título y descripción]
2. [Características principales]
3. [Instalación]
4. [Uso]
5. [Estructura del proyecto]
6. [Ejemplo de flujo de trabajo]
7. [Contribuciones]

## 📜 **1. Título y Descripción**
SADeP es una herramienta diseñada para automatizar el proceso de **planificación, redacción, ejecución y evaluación** de *prompts* de forma iterativa en llamados **experimentos**.
Mediante un sistema de roles virtuales que colaboran entre sí, el programa busca generar *prompts* de alta calidad, optimizados para su uso en modelos de lenguaje.
Su objetivo es **encontrar la mejor versión posible de un prompt** a través de un ciclo continuo de mejora, evaluando criterios como claridad, creatividad, utilidad y adaptabilidad.

El sistema simula un entorno de trabajo colaborativo en el que cada rol aporte una función única y vital para el proceso de desarrollo:
* **Planifier** diseña la estrategia y define las caracteristicas, tareas y atributos del *prompt*.
* **Maker** lo redacta siguiendo la planificación y teniendo en cuenta evaluaciones y resultados previos.
* **User** actúa como el usuario final, probando el *prompt* una vez es ejecutado.
* **Executor** simula el modelo de IA que responde al *prompt* y conversa con User.
* **Reviewer** evalúa la calidad del resultado de la conversación User <=> Executor y determina aspectos para mejorar.

El proceso se repite en ciclos sucesivos, donde cada iteración ajusta y perfecciona el *prompt* hasta alcanzar la mejor versión posible.
Esto logra que a medida que un **experimento** avanza y realiza una mayor cantidad de ciclos, los actores vitales para la creación del *prompt* (**Maker** y **Reviewer**) ganan una mayor fuerza y capacidad de cumplir su rol ya que tienen una mayor disponibilidad de iteraciónes previas repletas de información de la cuale pueden alimentar y nutrir el crecimiento crecimiento de su capacidad para llevar a cabo sus tareas.

SADeP combina **automatización**, **evaluación objetiva** y **retroalimentación continua**, ofreciendo una herramienta potente para *prompt engineering* y experimentación controlada con modelos de lenguaje.
Este sistema está orientado tanto a desarrolladores y *prompt engineers*, como a cualquier persona interesada en perfeccionar la interacción con IA mediante un enfoque estructurado y repetible.

## 🔌 **3. Instalación**
1. Descargar e instalar Python (Este punto puede variar dependiendo del sistema operativo).
2. Instalar la biblioteca de OpenAI para Python ejecutando el comando ```pip install openai``` desde la terminal.
3. Descargar el sistema desde el repositorio haciendo click en el botón "Code" => "Download ZIP".
4. Extraer el ZIP descargado en el directorio de preferencia.
5. Modificar el archivo config.json ubicado en el directorio principal (SADeP - Main\config.json) y agregar la API Key de OpenAI en "api_key:".

## 🔨 **4. Uso**
SADeP funciona estructurado en **experimentos**. Para crear y ejecutar un experimento debes:
1. Abrir la terminal en el directorio del sistema.
2. Ejecutar el script **"crear_estructura.py"** utilizando el comando ```python crear_estructura.py``` desde la terminal.
3. El script procederá a solicitar el nombre del experimento (p.ej. "expermiento01).
4. Navegar y acceder al directorio del experimento (p.ej. SADeP - Main\experimentos\experimento01) y modificar el archivo **config.json** para agregar **categoría** y **contexto** y modificar, opcionalmente, los parametros de **puntaje objetivo**, **ciclos máximos** y **turnos máximos**.
5. Ejecutar el script **engine.py** utilizando el comando ```python engine.py``` desde la terminal.
6. Escribir
