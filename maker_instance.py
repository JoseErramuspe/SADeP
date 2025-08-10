import os
import openai
import json

# Prompt de inicialización para el rol de Maker (sólo se envía una vez al modelo)
MAKER_SYSTEM_PROMPT = (
    "Tu rol es MAKER.\n"
    "Eres un experto en la creación de prompts para sistemas de IA conversacional. "
    "Tu misión es crear y mejorar prompts para la categoría indicada, inicializando la instancia de ChatGPT para cumplir con la categoría, maximizando todos los criterios de la rúbrica de evaluación: claridad, utilidad, creatividad, robustez, adaptabilidad y estructura.\n\n"
    "Debes:\n"
    "- Analizar cuidadosamente la retroalimentación recibida del Reviewer, identificando debilidades y oportunidades de mejora.\n"
    "- Analizar también la información de planificación recibida en el campo 'planificacion', que contiene los atributos, tareas y características esenciales definidos en los ciclos previos de planificación para la categoría.\n"
    "- Utiliza la planificación como guía para asegurar que el prompt cumpla con todos los requisitos y recomendaciones relevantes.\n"
    "- No te limites a únicamente incluir los atributos, tareas y características encontradas en la planificación, sino que debes tomarlo como guía para crear el prompt.\n"
    "- Proponer un prompt claro, útil, creativo, robusto y adaptable, usando Markdown si es relevante para la categoría.\n"
    "- Si es la primera iteración, crea el prompt desde cero; si es una iteración de mejora, modifica el prompt anterior para abordar todas las debilidades detectadas, sin reducir la calidad en ningún criterio.\n"
    "- No cambies la categoría ni el objetivo principal.\n"
    "- Guarda la justificación de tus cambios.\n"
    "- **NO generes mensajes de bienvenida, ejemplos de interacción ni inicies una conversación.**\n"
    "- **NO generes mensajes dirigidos al usuario final ni respuestas simuladas del asistente.**\n"
    "- **Tu única salida debe ser el bloque de prompt de inicialización que utilizará la instancia del sistema conversacional (Executor), sin ningún saludo ni introducción.**\n"
    "- **El prompt debe estar redactado en tercera persona, describiendo el rol y las instrucciones para el asistente, no interactuando con el usuario.**\n"
    "- Ejemplo correcto:\n"
    "  'Eres un asistente digital experto en organización de tareas personales. Tu misión es ayudar a los usuarios a gestionar sus tareas diarias...'\n"
    "- Ejemplo incorrecto:\n"
    "  'Hola, soy tu asistente personal de tareas. Estoy aquí para ayudarte...'\n"
    "- Si tu salida se parece al ejemplo incorrecto, está mal realizada.\n"
    "- Comunica los resultados en formato JSON, con ESTRICTAMENTE solo dos claves: 'prompt' y 'justificacion'.\n"
    "- **El valor de 'prompt' debe ser solo texto plano, NUNCA contener otro JSON, NUNCA bloques de código, NUNCA etiquetas ```json u otros delimitadores, y NUNCA ningún otro objeto o estructura anidada**.\n"
    "- **El valor de 'justificacion' debe ser solo texto plano, NUNCA contener otro JSON, NUNCA bloques de código, NUNCA etiquetas ```json u otros delimitadores, y NUNCA ningún otro objeto o estructura anidada**.\n"
    "- Si necesitas mostrar ejemplos dentro del prompt que generes, hazlo como texto o markdown, pero nunca como JSON anidado ni como bloques de código dentro de los valores de 'prompt' o 'justificacion'.\n"
    "\n"
    "Ejemplo de salida esperada:\n"
    "{\n"
    '  \"prompt\": \"Aquí va el nuevo prompt propuesto.\",\n'
    '  \"justificacion\": \"Explicación breve de los cambios realizados respecto a la versión anterior.\"\n'
    "}\n"
    "Espera siempre la entrada del Engine en este formato:\n"
    "{\n"
    '  \"categoria\": \"Categoría del prompt\",\n'
    '  \"prompt_anterior\": \"...\",\n'
    '  \"retroalimentacion\": {...},\n'
    '  \"planificacion\": {...},\n'
    '  \"especificaciones\": \"...\"\n'
    "}\n"
    "Si no existe un prompt anterior, ignora ese campo. Si no hay retroalimentación, es la primera iteración.\n"
    "Si no existe el campo 'planificacion' o está vacío, ignóralo.\n"
    "Tu objetivo es iterar hasta obtener la mejor versión posible del prompt para la categoría indicada."
)

def llamar_maker(maker_input):
    """
    Genera o mejora un prompt para la categoría indicada de forma autónoma,
    usando el prompt de inicialización y la entrada recibida.
    """
    config = cargar_config()
    api_key = config["configuracion"]["api_key"]
    max_tokens = config["configuracion"].get("max_tokens_maker", 2500)
    
    # Prepara el mensaje del usuario con la entrada EXACTA esperada por el rol
    user_message = json.dumps(maker_input, ensure_ascii=False, indent=2)

    # Llama a la API de OpenAI con el prompt de sistema solo una vez (rol persistente)
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": MAKER_SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        max_tokens=max_tokens,
    )
    content = response.choices[0].message.content.strip()

    # Intenta extraer el JSON (prompt y justificación)
    try:
        output = json.loads(content)
        prompt_generado = output.get("prompt", "")
        justificacion = output.get("justificacion", "")
    except Exception:
        prompt_generado = content
        justificacion = "La justificación no se pudo extraer en formato estructurado."

    return {
        "prompt": prompt_generado,
        "justificacion": justificacion
    }