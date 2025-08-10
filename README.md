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

## 🔧 **3. Instalación**
