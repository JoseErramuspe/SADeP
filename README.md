# 🚀 **SADeP** – *Sistema Automático para Desarrollo de Prompts*

📑 **Tabla de Contenidos**
1. [Título y descripción]
2. [Instalación]
3. [Uso]
4. [Estructura del proyecto]
5. [Ejemplo de flujo de trabajo]
6. [Contribuciones]

## 📜 **1. Título y Descripción**
SADeP es una herramienta diseñada para automatizar el proceso de **planificación, redacción, ejecución y evaluación** de *prompts* de forma iterativa en llamados **experimentos**.
Mediante un sistema de roles virtuales que colaboran entre sí, el programa busca generar *prompts* de alta calidad, optimizados para su uso en modelos de lenguaje.
Su objetivo es **encontrar la mejor versión posible de un prompt** a través de un ciclo continuo de mejora, evaluando criterios como claridad, creatividad, utilidad y adaptabilidad.

El sistema simula un entorno de trabajo colaborativo en el que cada rol aporte una función única y vital para el proceso de desarrollo:
* **Planifier** diseña la estrategia y define las caracteristicas, tareas y atributos del *prompt*.
* **Maker** lo redacta siguiendo la planificación y teniendo en cuenta evaluaciones y resultados previos.
* **User** actúa como el usuario final, probando el *prompt* una vez es ejecutado.
* **Executor** simula el modelo de IA que responde al *prompt* y conversa con User.
* **Reviewer** evalúa la calidad del resultado de la conversación User ↔ Executor y determina aspectos para mejorar.

El proceso se repite en ciclos sucesivos, donde cada iteración ajusta y perfecciona el *prompt* hasta alcanzar la mejor versión posible.
Esto logra que a medida que un **experimento** avanza y realiza una mayor cantidad de ciclos, los actores vitales para la creación del *prompt* (**Maker** y **Reviewer**) ganan una mayor fuerza y capacidad de cumplir su rol ya que tienen una mayor disponibilidad de iteraciónes previas repletas de información de la cuale pueden alimentar y nutrir el crecimiento crecimiento de su capacidad para llevar a cabo sus tareas.

SADeP combina **automatización**, **evaluación objetiva** y **retroalimentación continua**, ofreciendo una herramienta potente para *prompt engineering* y experimentación controlada con modelos de lenguaje.
Este sistema está orientado tanto a desarrolladores y *prompt engineers*, como a cualquier persona interesada en perfeccionar la interacción con IA mediante un enfoque estructurado y repetible.

## 🔌 **2. Instalación**
1. Descargar e instalar Python (Este punto puede variar dependiendo del sistema operativo).
2. Instalar la biblioteca de OpenAI para Python ejecutando el comando ```pip install openai``` desde la terminal.
3. Descargar el sistema desde el repositorio haciendo click en el botón "Code" => "Download ZIP".
4. Extraer el ZIP descargado en el directorio de preferencia.
5. Modificar el archivo config.json ubicado en el directorio principal (SADeP - Main\config.json) y agregar la API Key de OpenAI en "api_key:".

## 🔨 **3. Uso**
SADeP funciona estructurado en **experimentos**. Para crear y ejecutar un experimento debes:
1. Abrir la terminal en el directorio del sistema.
2. Ejecutar el script **"crear_estructura.py"** utilizando el comando ```python crear_estructura.py``` desde la terminal.
3. El script procederá a solicitar el nombre del experimento (p.ej. ```"expermiento01"```).
4. Navegar y acceder al directorio del experimento (p.ej. ```SADeP - Main\experimentos\experimento01```) y modificar el archivo **config.json** para agregar **categoría** y **contexto** y modificar, opcionalmente, los parametros de **puntaje objetivo**, **ciclos máximos** y **turnos máximos**.
5. Ejecutar el script **engine.py** utilizando el comando ```python engine.py``` desde la terminal.
6. Escribir el nombre del experimento a comenzar.
7. Comenzará el desarrollo del **prompt**, todo el feedback y procesos de la IA se pueden ver desde la terminal con la cual se ejecutó el mismo.
8. Una vez finalizado el proceso, dentro de la carpeta del experimento se puede encontrar un archivo llamado **mejor_prompt.json**, en este JSON se encuentra el **prompt** el cual puntuó mas alto durante todo el proceso de desarrollo junto a la evaluación y justificación de sus características.

## 📁 **4. Estructura del Proyecto**
La organización de archivos y carpetas en SADeP fue pensada parafacilitar su comprensión, mantenimiento y escalabilidad.
Cada componente cumple un rol específico dentro del flujo del sistema.

Prompts/

├── experimentos/ ------------ # Directorio el cual alojará los subdirectorios dedicados a cada experimento.

├── config.json ---------------- # Archivo de configuración global. Define parámetros por defecto, ajustes de cada rol y opciones generales.

├── crear_estructura.py ------- # Script auxiliar para generar la estructura base de carpetas y archivos de un nuevo experimento.

├── engine.py ----------------- # Núcleo del sistema. Controla el ciclo de ejecución Planifier → Maker → User <=> Executor → Reviewer.

├── planifier_instance.py ------ # Implementa el rol Planifier: diseña y planifica el contenido y la estrategia del prompt.

├── maker_instance.py -------- # Implementa el rol Maker: redacta el prompt final según las directrices del Planifier.

├── user_instance.py ---------- # Implementa el rol User: simula al usuario final que interactuará con el prompt.

├── executor_instance.py ----- # Implementa el rol Executor: ejecuta el prompt como un modelo de IA y mantiene conversación con el User.

├── reviewer_instance.py ----- # Implementa el rol Reviewer: evalúa la salida generada según criterios predefinidos y propone mejoras.

└── utils.py -------------------- # Funciones auxiliares y utilidades. Incluye manejo de datos, extracción de resultados y operaciones comunes.

Notas:
La carpeta ```experimentos/``` (generada en tiempo de ejecución) contendrá los experimentos creados por el usuario.
Cada experimento tendrá su propio subdirectorio con:

* **config.json** personalizado para ese experimento.
* Carpeta ```ciclos/``` con los registros de cada iteración.
* Archivos de historial y mejores resultados (historial_completo.json, mejor_prompt.json).

Todos los módulos de instancias (*_instance.py) dependen de la configuración central y se ejecutan secuencialmente en el ciclo definido por engine.py.

## 🔁 **5. Flujo de desarrollo**
A continuación se describe el flujo de desarrollo de un experimento en SADeP. El objetivo es que quien lea pueda comprender paso a paso qué hace el sistema, qué resultados tiene y cómo se toman las decisiones en cada iteración del ciclo.

SADeP funciona como una línea de ensamblaje iterativa para prompts: cada ciclo consta de varias etapas que producen, prueban y evalúan prompts. El ciclo completo se repite hasta cumplir una condición de parada (número máximo de ciclos, puntaje objetivo, intervención humana, etc.). Los roles principales son: Planifier → Maker → User ↔ Executor → Reviewer. engine.py orquesta este flujo y persiste los resultados.

#### 🛠 1. Inicialización del experimento
crear_estructura.py crea la carpeta del experimento en ```experimentos/[nombre]``` con subcarpetas estándar:

* ```ciclos/```: directorio donde se aloja la información de cada cilco
* ```config.json```: configuración específica del experimento
* ```historial_completo.json``` historial completo de las conversaciones User ↔ Executor
* ```mejor_prompt.json``` prompt con el mayor puntaje obtenido durante el transcurso de todo el experimento

Se cargan parámetros desde config.json global y el config del experimento (p. ej. max_ciclos, especificaciones por instancia o globales, max_tokens, etc.).

#### 🤖 2. Planifier (planifica el prompt)
Entrada: Categoría y contexto del prompt, información alojada en ```config.json``` del experimento y especificaciones de la instancia.

Salida: Plan estructurado (JSON) con instrucciones para el Maker.

Ejemplo de salida:

```
"Atributos": [
    {
      "titulo": "Claridad del propósito",
      "descripcion": "El prompt debe definir claramente la función de ayuda en la organización y planificación de tareas para que la IA pueda ejecutar sus capacidades de manera óptima."
    },
    {
      "titulo": "Formato estructurado",
      "descripcion": "Debe proporcionar un formato organizado que permita a la IA comprender y desglosar tareas de manera clara y lógica, facilitando su interpretación y ejecución."
    }
  ],
  "Tareas": [
    {
      "titulo": "Organizar tareas",
      "descripcion": "La IA debe ser capaz de listar, categorizar y estructurar tareas siguiendo criterios específicos de prioridad y urgencia."
    },
    {
      "titulo": "Planificar cronogramas",
      "descripcion": "Debe elaborar cronogramas que distribuyan las tareas a lo largo de un periodo determinado, asegurando que se respeten los plazos asignados."
    },
    {
      "titulo": "Recordar plazos",
      "descripcion": "El sistema debe recordar y, si es posible, enviar recordatorios sobre las fechas límite para las tareas programadas, evitando su incumplimiento."
    }
  ],
  "Características": [
    {
      "titulo": "Adaptabilidad a cambios",
      "descripcion": "La IA debe ser capaz de ajustarse a modificaciones o interrupciones en la programación inicial, replanificando cuando sea necesario para mantener la eficiencia."
    },
    {
      "titulo": "Concisión",
      "descripcion": "Las respuestas deben ser breves y directas, proporcionando al usuario la información esencial para la gestión de sus tareas."
    }
  ]
```

#### 🤖 3. Maker (redacta el prompt)
Entrada: Categoría y contexto del prompt, plan generado por Planifier y especificaciones de la instancia.

Salida: El prompt redactado.

Ejemplo de salida:
```
{
  "prompt": "Eres un asistente digital especializado en organización y planificación de tareas. Tu misión es ayudar a los usuarios a gestionar sus tareas diarias con eficiencia y claridad.",
  "justificacion": "Explicación breve del prompt o los cambios hechos."
}
```
#### 🤖 4. Executor (ejecuta el prompt, simula la IA)
Entrada: Prompt hecho por Maker, último mensaje de User, historial y especificaciones de la instancia.

Salida: Mensaje de ejecución del prompt y contestaciones a User.

Ejemplo de salida:
```
{
  "mensaje": "¡Bienvenido! Soy tu asistente digital especializado en organización y planificación de tareas. Estoy aquí para ayudarte a gestionar tus tareas diarias con eficiencia y claridad."/n
              "Para comenzar, por favor, proporciona detalles sobre las tareas que necesitas organizar:"/n
              "- ¿Cuál es el propósito de cada tarea?"/n
              "- ¿Cuáles son sus prioridades y plazos?"/n
              "- ¿Hay algún requisito especial que deba conocer?"
}
```

#### 🤖 5. User (simula al usuario final)
Entrada: Prompt hecho por Maker, categoría del prompt, historial y especificaciones de la instancia.

Salida: Conversacion simulada que representen el uso real de un usuario final.

Ejemplo de salida:
```
{
  "mensaje": "¡Gracias! Tengo algunas tareas en mente:"/n
             "1. **Planificar una reunión de equipo:**"/n
             "- **Propósito:** Discutir los progresos del proyecto y establecer los próximos pasos."/n
             "- **Prioridad:** Alta."/n
             "- **Plazo:** Necesitamos tenerla antes de final de la semana."/n
             "- **Requisitos especiales:** Debo coordinar la disponibilidad de todos los miembros del equipo."/n/n

             "2. **Revisar y aprobar un informe financiero:**"/n
             "- **Propósito:** Asegurar la precisión del reporte antes de enviarlo a la dirección general."/n
             "- **Prioridad:** Media."/n
             "- **Plazo:** Dentro de las próximas dos semanas."
}
```

Nota: en SADeP, User y Executor actúan como interlocutores: Ambos mantienen una conversación real y todas las interacciones quedan registradas.

#### 🤖 6. Reviewer (evalúa resultados)
Entrada: Prompt actual, categoría y contexto del prompt, historial de conversación User ↔ Executor, evaluaciones previas y especificaciones de la instancia.

Salida: Evaluación del prompt, incluyendo criterios, puntaje, justificación y mejora posible en cada uno.

Estructura de salida:
```
{
    "  \"evaluacion\": {\n"
    "    \"claridad\":   { \"puntaje\": 0, \"justificacion\": \"\", \"mejora\": \"\" },\n"
    "    \"utilidad\":   { \"puntaje\": 0, \"justificacion\": \"\", \"mejora\": \"\" },\n"
    "    \"creatividad\": { \"puntaje\": 0, \"justificacion\": \"\", \"mejora\": \"\" },\n"
    "    \"robustez\":    { \"puntaje\": 0, \"justificacion\": \"\", \"mejora\": \"\" },\n"
    "    \"adaptabilidad\": { \"puntaje\": 0, \"justificacion\": \"\", \"mejora\": \"\" },\n"
    "    \"estructura\":   { \"puntaje\": 0, \"justificacion\": \"\", \"mejora\": \"\" }\n"
}"
```

## 🤝 **6. Contribuciones**
Este proyecto fue desarrollado gracias al trabajo y los esfuerzos colaborativo de:

Santiago Boné — Diseño y desarrollo de la arquitectura del sistema, testeo y evaluación del sistema y los resultados, refinamiento de módulos y correción de errores encontrados.

José Erramuspe — Diseño y desarrollo de la arquitectura del sistema, implementación de funciones clave de generación, simulación y evaluación de prompts y desarrollo de instancias.

Ambos trabajaron conjuntamente en la definición del enfoque iterativo, diseño modular, y pruebas para asegurar la reproducibilidad y extensibilidad del sistema. La colaboración se basó en revisiones continuas, validación mutua del código y discusión activa de mejoras.
