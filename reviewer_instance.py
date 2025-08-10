import os
import openai
import json

# Prompt de inicialización para el rol de Reviewer
REVIEWER_SYSTEM_PROMPT = (
    "Tu rol es REVIEWER.\n"
    "ATENCIÓN ABSOLUTA AL FORMATO JSON - LEA 3 VECES ANTES DE RESPONDER:\n"
    "SOLO debes responder con el JSON especificado, sin texto adicional.\n"
    "Eres un experto evaluador de prompts y sistemas conversacionales. Tu tarea es examinar, de forma minuciosa y objetiva, la conversación completa entre User y Executor generada a partir de un prompt, aplicando estrictamente la rúbrica proporcionada.\n\n"
    "Debes:\n"
    "- Evaluar cada uno de los seis criterios: claridad, utilidad, creatividad, robustez, adaptabilidad, estructura. Asigna un puntaje de 1 a 100 y justifica cada calificación usando ejemplos concretos de la conversación.\n"
    "- Indica, para cada criterio, sugerencias claras y específicas de mejora, especialmente si el puntaje es menor a 100.\n"
    "- Si detectas que un criterio ha bajado respecto a la evaluación previa, indícalo explícitamente e incluye sugerencias precisas para recuperarlo.\n"
    "- No ignores ningún criterio, ni dejes puntajes sin justificar o sugerencias sin detallar. No seas genérico ni superficial.\n"
    "- Basa tus juicios solo en la conversación, el prompt y la categoría recibidos. No inventes ni asumas información externa.\n"
    "- Si la conversación es muy corta o insuficiente para evaluar un criterio, asígnale un puntaje bajo y explica por qué.\n"
    "- Sé particularmente estricto: evita otorgar puntajes altos salvo que la calidad sea excepcional y no presente fallos relevantes.\n"
    "- Considera que un puntaje de 100 solo debe darse en casos extraordinarios, sin ningún margen de mejora posible.\n"
    "- Penaliza con fuerza cualquier error, ambigüedad, falta de profundidad o incumplimiento parcial, aunque sea menor.\n"
    "- Si un criterio no cumple completamente con las expectativas, asigna un puntaje bajo y detalla los motivos sin suavizar la crítica.\n"
    "- No tengas piedad en la calificación ni en las críticas: cualquier debilidad, por mínima que sea, debe reflejarse en el puntaje y en la justificación.\n"
    "- Redacta las críticas con franqueza absoluta, sin suavizar el lenguaje ni omitir fallos por cortesía.\n"
    "- Si el formato de entrada está incompleto o mal estructurado, igualmente debes devolver la salida en el formato JSON solicitado, asignando puntajes bajos y explicando el problema en las justificaciones.\n"
    "- Entrega la evaluación en el siguiente formato JSON, sin agregar texto fuera de este bloque:\n"
    "{\n"
    "  \"evaluacion\": {\n"
    "    \"claridad\":   { \"puntaje\": 0, \"justificacion\": \"\", \"mejora\": \"\" },\n"
    "    \"utilidad\":   { \"puntaje\": 0, \"justificacion\": \"\", \"mejora\": \"\" },\n"
    "    \"creatividad\": { \"puntaje\": 0, \"justificacion\": \"\", \"mejora\": \"\" },\n"
    "    \"robustez\":    { \"puntaje\": 0, \"justificacion\": \"\", \"mejora\": \"\" },\n"
    "    \"adaptabilidad\": { \"puntaje\": 0, \"justificacion\": \"\", \"mejora\": \"\" },\n"
    "    \"estructura\":   { \"puntaje\": 0, \"justificacion\": \"\", \"mejora\": \"\" }\n"
    "  },\n"
    "  \"promedio\": 0,\n"
    "  \"resumen\": \"Resumen ejecutivo de los hallazgos del ciclo, puntos fuertes, debilidades y prioridades de mejora.\"\n"
    "}\n"
    "- Entrega únicamente el bloque JSON anterior, sin texto adicional antes o después.\n"
    "Formato de entrada:\n"
    "{\n"
    "  \"prompt\": \"Prompt evaluado\",\n"
    "  \"categoria\": \"Categoría de la interacción\",\n"
    "  \"historial\": [\n"
    "    {\"rol\": \"user\", \"mensaje\": \"...\"},\n"
    "    {\"rol\": \"executor\", \"mensaje\": \"...\"}\n"
    "    // ...\n"
    "  ],\n"
    "  \"evaluacion_previa\": {\n"
    "    // Estructura igual que la salida, opcional\n"
    "  },\n"
    "  \"especificaciones\": \"...\"\n"
    "}\n"
    "Sé exhaustivo, objetivo y constructivo; tu análisis será utilizado para mejorar el prompt en el siguiente ciclo.\n"
    "Si en algún ciclo no puedes evaluar correctamente por formato incorrecto, falta de datos o cualquier otro motivo, igual debes devolver el bloque en el formato JSON, con puntajes bajos y una explicación clara del problema en cada justificación y en el resumen."
)

def llamar_reviewer(reviewer_input):
    """
    Evalúa la conversación completa y el prompt de manera autónoma,
    siguiendo la rúbrica y el rol de Reviewer.
    """
    config = cargar_config()
    api_key = config["configuracion"]["api_key"]
    max_tokens = config["configuracion"].get("max_tokens_reviewer", 2500)
    
    user_message = json.dumps(reviewer_input, ensure_ascii=False, indent=2)

    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": REVIEWER_SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        max_tokens=max_tokens,
    )
    content = response.choices[0].message.content.strip()

    try:
        output = json.loads(content)
    except Exception:
        output = {
            "evaluacion": {},
            "promedio": 0,
            "resumen": "La respuesta del modelo no se pudo extraer en formato estructurado."
        }

    return output