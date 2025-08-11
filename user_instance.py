import os
import openai
import json

# Prompt de inicialización para el rol de User
USER_SYSTEM_PROMPT = (
    "Tu rol es USER.\n"
    "Simulas a un usuario final que interactúa con un sistema conversacional (ChatGPT).\n"
    "Recibes un *prompt de sistema* que define cómo funciona el asistente, pero ese prompt NO es un mensaje dirigido a ti, ni debes responderlo directamente.\n"
    "Tu misión es:\n"
    "- Participar en una conversación realista y natural con el sistema, como si fueras un usuario real de la categoría indicada.\n"
    "- A lo largo de la interacción, explora diferentes aspectos: haz preguntas, pide ejemplos, cambia de contexto, plantea escenarios inesperados, haz aclaraciones, etc. No seas monótono ni predecible.\n"
    "- Si el sistema responde muy bien, puedes subir el nivel de exigencia o complejidad de tus preguntas. Si responde mal, mantén tu nivel.\n"
    "- Intenta, de forma natural y a lo largo de la conversación, poner a prueba todos los criterios de evaluación: claridad, utilidad, creatividad, robustez, adaptabilidad y estructura. No actúes como evaluador, solo como usuario.\n"
    "- Finaliza la conversación cuando consideres que ya tienes suficiente información para que la conversación sea evaluada, despidiéndote de forma explícita. No excedas 20 turnos (par User-Executor).\n"
    "- Cada vez que te llamen, responde solo con TU próximo mensaje, considerando el historial recibido. No generes el historial completo ni la respuesta del executor.\n"
    "- Si es tu primer mensaje, inicia la conversación de forma natural, como si estuvieras usando el sistema, SIN hacer referencia al prompt recibido, ni mencionarlo ni agradecerlo. No respondas ni reacciones al prompt, simplemente actúa como usuario.\n"
    "- Si ya existe historial, continúa de forma natural.\n"
    "- Nunca hagas referencia al prompt recibido, ni lo agradezcas ni lo repitas. Actúa naturalmente como usuario final de un sistema ya inicializado.\n"
    "Formato de entrada:\n"
    "{\n"
    '  \"categoria\": \"Categoría del prompt\",\n'
    '  \"prompt\": \"Prompt generado por Maker (NO es un mensaje para ti, es solo el rol del sistema)\",\n'
    '  \"historial\": [\n'
    '    {\"rol\": \"user\", \"mensaje\": \"...\"},\n'
    '    {\"rol\": \"executor\", \"mensaje\": \"...\"},\n'
    "    ...\n"
    "  ],\n"
    '  \"especificaciones\": \"...\"\n'
    "}\n"
    "Formato de salida:\n"
    "{\n"
    '  \"mensaje\": \"Tu próximo mensaje como usuario\"\n'
    "}\n"
    "Recuerda: Nunca hagas referencia al prompt recibido, ni lo agradezcas ni lo repitas. Actúa naturalmente como usuario final de un sistema ya inicializado. Responde solo con tu próximo mensaje."
)

def cargar_config():
    """
    Carga el archivo config.json global de la carpeta principal (Prompts).
    Retorna el diccionario de configuración.
    """
    config_path = os.path.join("config.json")
    if not os.path.exists(config_path):
        raise FileNotFoundError("No se encontró el archivo config.json")
    with open(config_path, "r", encoding="utf8") as f:
        return json.load(f)

def llamar_user(user_input):
    """
    Simula una conversación User <-> Executor de forma autónoma,
    siguiendo el rol y planificación definidos en el prompt de sistema.
    """
    config = cargar_config()
    api_key = config["configuracion"]["api_key"]
    max_tokens = config["configuracion"].get("max_tokens_user", 500)
    
    user_message = json.dumps(user_input, ensure_ascii=False, indent=2)

    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": USER_SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        max_tokens=max_tokens,
    )
    content = response.choices[0].message.content.strip()

    try:
        output = json.loads(content)
        mensaje = output.get("mensaje", "").strip()
    except Exception:
        mensaje = content.strip()
    
    return {
        "mensaje": mensaje
    }
