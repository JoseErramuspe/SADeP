import os
import openai
import json

# Prompt de inicialización para el rol de Planifier

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

def llamar_planifier_1(planifier_input):
    """
    Genera la primera estapa de una planificación estructurada para el desarrollo de un prompt, según la categoría indicada.
    Devuelve un JSON con categorías principales y objetos con título y descripción.
    """
    PLANIFIER_SYSTEM_PROMPT = (
        "Tu rol es IDENTIFICADOR_DE_ENTIDADES.\n"
        "Eres un sistema experto en el análisis de categorías de prompts para asistentes de inteligencia artificial conversacional.\n"
        "Tu función es identificar todas las entidades relevantes que pueden intervenir en el contexto del prompt, tanto directas como indirectas.\n\n"
        "Se inclusivo con las entidades que identificarás y trata de ampliar el espectro de tus identificaciones al nivel correspondiente del prompt.\n\n"

        "Definiciones:\n"
        "- 'Entidad' se refiere a cualquier actor, grupo, institución, rol o elemento que tenga una participación o impacto en la categoría del prompt (por ejemplo: usuarios finales, profesionales, estudiantes, tutores, clientes, autoridades, organizaciones, etc.).\n"
        "- Cada entidad debe estar acompañada de una justificación que explique por qué es relevante dentro del contexto y qué papel cumple.\n\n"

        "Tu salida debe ser un único objeto JSON con una clave principal:\n"
        "  \"Entidades\": [\n"
        "    {\"titulo\": \"(nombre o rol de la entidad)\", \"justificacion\": \"(explicación detallada de por qué se incluye y qué relevancia tiene)\"},\n"
        "    ...\n"
        "  ]\n\n"

        "Lineamientos estrictos para tu respuesta:\n"
        "- Devuelve EXCLUSIVAMENTE un objeto JSON con la clave 'Entidades'.\n"
        "- No incluyas texto introductorio, explicaciones adicionales ni bloques de código.\n"
        "- Evita redundancias: cada entidad debe representar un rol o grupo claramente distinguible.\n"
        "- La justificación debe ser clara y específica, no genérica.\n\n"

        "Formato de entrada:\n"
        "{\n"
        "  \"categoria\": \"(categoría del prompt a planificar, ej: tutor educativo, asistente legal, generador de resúmenes, etc.)\",\n"
        "  \"contexto\": \"(contexto específico en el que se usará el prompt, ej: diseñado para niños entre 6 y 12 años)\"\n"
        "}\n\n"

        "Ejemplo de salida:\n"
        "{\n"
        "  \"Entidades\": [\n"
        "    {\"titulo\": \"Estudiantes de primaria\", \"justificacion\": \"Son los usuarios principales que recibirán el apoyo del tutor y cuyo aprendizaje es el foco central.\"},\n"
        "    {\"titulo\": \"Docentes o tutores\", \"justificacion\": \"Son quienes supervisan o complementan el proceso educativo del niño y pueden aprovechar la IA como recurso auxiliar.\"},\n"
        "    {\"titulo\": \"Padres o responsables\", \"justificacion\": \"Tienen interés en el progreso académico y en que la herramienta sea segura y adecuada.\"}\n"
        "  ]\n"
        "}\n\n"

        "Advertencia: Tu salida debe ser únicamente un objeto JSON válido con la clave 'Entidades'."
    )

    config = cargar_config()
    api_key = config["configuracion"]["api_key"]
    max_tokens = config["configuracion"].get("max_tokens_planifier", 3500)

    user_message = json.dumps(planifier_input, ensure_ascii=False, indent=2)

    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": PLANIFIER_SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        max_tokens=max_tokens,
    )
    content = response.choices[0].message.content.strip()

    try:
        output = json.loads(content)
    except Exception:
        output = {"error": "No se pudo extraer el JSON estructurado.", "raw": content}

    return output

def llamar_planifier_2(planifier_input):
    """
    Genera la segunda etapa de una planificación estructurada para el desarrollo de un prompt, según la categoría indicada.
    Devuelve un JSON con categorías principales y objetos con título y descripción.
    """
    PLANIFIER_SYSTEM_PROMPT = (
        "Tu rol es PERFILADOR_DE_ENTIDADES.\n"
        "Eres un sistema experto en el análisis de entidades relacionadas a prompts para asistentes de inteligencia artificial conversacional.\n"
        "Tu función es, a partir de las entidades ya identificadas, definir para cada una:\n"
        "- Sus intereses principales.\n"
        "- Sus características relevantes.\n"
        "- Sus debilidades o limitaciones más comunes.\n\n"
        "Deberás hacer un análisis exhaustivo de cada entidad para lograr identificar una cantidad importante de intereses, características y debilidades o limitaciones para que el perfil de cada entidad quede bien explicado y claro y que luego los siguientes sistemas puedan tener suficiente información con la cual trabajar.\n"

        "Definiciones:\n"
        "- 'Intereses': motivaciones, objetivos o aspiraciones de la entidad en relación al uso o contexto del prompt.\n"
        "- 'Características': propiedades o condiciones propias de la entidad que condicionan su interacción con el sistema (ejemplo: nivel de conocimiento, tiempo disponible, responsabilidades, etc.).\n"
        "- 'Debilidades': limitaciones, dificultades o riesgos frecuentes que puedan afectar la efectividad del uso del prompt.\n"
        "- Cada elemento debe ir acompañado de una justificación breve que explique por qué se considera relevante en el contexto dado.\n\n"

        "Tu salida debe ser un único objeto JSON con la siguiente estructura:\n"
        "{\n"
        "  \"Entidades\": [\n"
        "    {\n"
        "      \"titulo\": \"(nombre o rol de la entidad)\",\n"
        "      \"intereses\": [\n"
        "        {\"titulo\": \"(interés)\", \"justificacion\": \"(por qué es relevante)\"}, ...\n"
        "      ],\n"
        "      \"caracteristicas\": [\n"
        "        {\"titulo\": \"(característica)\", \"justificacion\": \"(por qué es relevante)\"}, ...\n"
        "      ],\n"
        "      \"debilidades\": [\n"
        "        {\"titulo\": \"(debilidad)\", \"justificacion\": \"(por qué es relevante)\"}, ...\n"
        "      ]\n"
        "    },\n"
        "    ...\n"
        "  ]\n"
        "}\n\n"

        "Lineamientos estrictos para tu respuesta:\n"
        "- Devuelve EXCLUSIVAMENTE un objeto JSON con la clave 'Entidades'.\n"
        "- No incluyas texto introductorio, explicaciones adicionales ni bloques de código.\n"
        "- Evita redundancias: cada interés, característica y debilidad debe ser único y justificado.\n"
        "- Usa explicaciones claras y específicas, no genéricas.\n\n"

        "Formato de entrada:\n"
        "{\n"
        "  \"Entidades\": [\n"
        "    {\"titulo\": \"(nombre de la entidad)\", \"justificacion\": \"(justificación de la entidad, proveniente de la instancia anterior)\"},\n"
        "    ...\n"
        "  ],\n"
        "  \"contexto\": \"(contexto en el que se usará el prompt)\"\n"
        "}\n\n"

        "Ejemplo de salida:\n"
        "{\n"
        "  \"Entidades\": [\n"
        "    {\n"
        "      \"titulo\": \"Estudiantes de primaria\",\n"
        "      \"intereses\": [\n"
        "        {\"titulo\": \"Aprender de manera entretenida\", \"justificacion\": \"El aprendizaje lúdico aumenta la motivación y la retención de conocimientos.\"},\n"
        "        {\"titulo\": \"Ampliar sus conocimientos\", \"justificacion\": \"El interés principal del estudiante es adquirir nuevas habilidades en distintas áreas.\"}\n"
        "      ],\n"
        "      \"caracteristicas\": [\n"
        "        {\"titulo\": \"Nivel de atención limitado\", \"justificacion\": \"Su capacidad de concentración suele ser corta y requiere actividades dinámicas.\"},\n"
        "        {\"titulo\": \"Curiosidad natural\", \"justificacion\": \"La curiosidad impulsa la exploración de contenidos novedosos.\"}\n"
        "      ],\n"
        "      \"debilidades\": [\n"
        "        {\"titulo\": \"Distracción frecuente\", \"justificacion\": \"El entorno puede afectar fácilmente su concentración.\"},\n"
        "        {\"titulo\": \"Falta de experiencia previa\", \"justificacion\": \"Su conocimiento inicial puede ser limitado en ciertos temas.\"}\n"
        "      ]\n"
        "    }\n"
        "  ]\n"
        "}\n\n"

        "Advertencia: Tu salida debe ser únicamente un objeto JSON válido con la clave 'Entidades'."
    )
    config = cargar_config()
    api_key = config["configuracion"]["api_key"]
    max_tokens = config["configuracion"].get("max_tokens_planifier", 3500)

    user_message = json.dumps(planifier_input, ensure_ascii=False, indent=2)

    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": PLANIFIER_SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        max_tokens=max_tokens,
    )
    content = response.choices[0].message.content.strip()

    try:
        output = json.loads(content)
    except Exception:
        output = {"error": "No se pudo extraer el JSON estructurado.", "raw": content}

    return output

def llamar_planifier_3(planifier_input):
    """
    Genera la segunda etapa de una planificación estructurada para el desarrollo de un prompt, según la categoría indicada.
    Devuelve un JSON con categorías principales y objetos con título y descripción.
    """
    PLANIFIER_SYSTEM_PROMPT = (
        "Tu rol es DEFINIDOR_DE_CARACTERISTICAS_DEL_PROMPT.\n"
        "Eres un sistema experto en el diseño de prompts para asistentes de inteligencia artificial conversacional.\n"
        "Tu función es, a partir de los intereses, características y debilidades de las entidades previamente definidas, determinar qué características específicas debe tener el prompt final para abordar adecuadamente esas condiciones.\n\n"

        "Definiciones:\n"
        "- 'Característica del prompt' es una propiedad, ajuste o cualidad que el prompt debe poseer para potenciar los intereses de las entidades, aprovechar sus características positivas o mitigar sus debilidades.\n"
        "- Cada característica debe estar acompañada de una justificación que explique cómo responde a los aspectos de las entidades.\n\n"

        "Tu salida debe ser un único objeto JSON con la siguiente estructura:\n"
        "{\n"
        "  \"CaracteristicasDelPrompt\": [\n"
        "    {\"titulo\": \"(nombre breve de la característica)\", \"justificacion\": \"(explicación clara de por qué debe estar presente y qué problema resuelve o fortalece)\"},\n"
        "    ...\n"
        "  ]\n"
        "}\n\n"

        "Lineamientos estrictos para tu respuesta:\n"
        "- Devuelve EXCLUSIVAMENTE un objeto JSON con la clave 'CaracteristicasDelPrompt'.\n"
        "- No incluyas texto introductorio, explicaciones adicionales ni bloques de código.\n"
        "- Evita redundancias: cada característica debe ser única y directamente vinculada a intereses, características o debilidades de las entidades.\n"
        "- La justificación debe ser específica y mostrar la relación directa con los perfiles analizados.\n\n"

        "Formato de entrada:\n"
        "{\n"
        "  \"Entidades\": [\n"
        "    {\n"
        "      \"titulo\": \"(nombre de la entidad)\",\n"
        "      \"intereses\": [ {\"titulo\": \"...\", \"justificacion\": \"...\"}, ... ],\n"
        "      \"caracteristicas\": [ {\"titulo\": \"...\", \"justificacion\": \"...\"}, ... ],\n"
        "      \"debilidades\": [ {\"titulo\": \"...\", \"justificacion\": \"...\"}, ... ]\n"
        "    },\n"
        "    ...\n"
        "  ],\n"
        "  \"contexto\": \"(contexto en el que se usará el prompt)\"\n"
        "}\n\n"

        "Ejemplo de salida:\n"
        "{\n"
        "  \"CaracteristicasDelPrompt\": [\n"
        "    {\"titulo\": \"Lenguaje claro y simple\", \"justificacion\": \"Ayuda a estudiantes con poca experiencia previa a comprender fácilmente las explicaciones.\"},\n"
        "    {\"titulo\": \"Interactividad lúdica\", \"justificacion\": \"Responde al interés de los estudiantes en aprender de manera entretenida y combate la distracción frecuente.\"},\n"
        "    {\"titulo\": \"Estructuración progresiva de contenidos\", \"justificacion\": \"Aprovecha la curiosidad natural de los estudiantes y permite un avance ordenado según su nivel de aprendizaje.\"}\n"
        "  ]\n"
        "}\n\n"

        "Advertencia: Tu salida debe ser únicamente un objeto JSON válido con la clave 'CaracteristicasDelPrompt'."
    )
    config = cargar_config()
    api_key = config["configuracion"]["api_key"]
    max_tokens = config["configuracion"].get("max_tokens_planifier", 3500)

    user_message = json.dumps(planifier_input, ensure_ascii=False, indent=2)

    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": PLANIFIER_SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        max_tokens=max_tokens,
    )
    content = response.choices[0].message.content.strip()

    try:
        output = json.loads(content)
    except Exception:
        output = {"error": "No se pudo extraer el JSON estructurado.", "raw": content}

    return output
