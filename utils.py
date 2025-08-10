import json
import re

def extract_reviewer_output(raw_output):
    """
    Extrae la estructura de evaluación del reviewer de forma robusta.
    Permite que la salida del reviewer sea texto plano, JSON crudo, o JSON anidado en texto.
    Devuelve un dict con formato estándar:
    {
        "evaluacion": {categoria: {"puntaje": int, "justificacion": str, "mejora": str}, ...},
        "promedio": float,
        "resumen": str
    }
    """
    CATEGORIAS = ["claridad", "utilidad", "creatividad", "robustez", "adaptabilidad", "estructura"]
    resultado = {
        "evaluacion": {cat: {"puntaje": 0, "justificacion": "", "mejora": ""} for cat in CATEGORIAS},
        "promedio": 0,
        "resumen": ""
    }

    # 1. Intentar cargar el bloque JSON (aunque esté dentro de texto)
    json_regex = re.compile(r"\{[\s\S]*\}", re.MULTILINE)
    match = json_regex.search(raw_output)
    if match:
        try:
            reviewer_json = json.loads(match.group())
            for cat in CATEGORIAS:
                if cat not in reviewer_json.get("evaluacion", {}):
                    reviewer_json.setdefault("evaluacion", {})
                    reviewer_json["evaluacion"][cat] = {"puntaje": 0, "justificacion": "", "mejora": ""}
            resultado.update({
                "evaluacion": reviewer_json.get("evaluacion", resultado["evaluacion"]),
                "promedio": reviewer_json.get("promedio", 0),
                "resumen": reviewer_json.get("resumen", "")
            })
            return resultado
        except Exception:
            pass

    # 2. Si no hay JSON, buscar puntajes y justificaciones en texto plano
    for cat in CATEGORIAS:
        pattern = rf"{cat.capitalize()}\s*:\s*(\d+)[^\n]*([\s\S]*?)(?:\n\s*[A-Z][a-z]+:|\n*$)"
        m = re.search(pattern, raw_output, re.IGNORECASE)
        if m:
            resultado["evaluacion"][cat]["puntaje"] = int(m.group(1))
            justif = m.group(2).strip(" -:\n")
            if justif and justif.lower()[:11] != "puntaje bajo":
                resultado["evaluacion"][cat]["justificacion"] = justif

    resumen_match = re.search(r"resumen\s*[:\-]?\s*(.*)", raw_output, re.IGNORECASE)
    if resumen_match:
        resultado["resumen"] = resumen_match.group(1).strip()
    else:
        parrafos = [p.strip() for p in raw_output.split("\n\n") if len(p.strip()) > 30]
        if parrafos:
            resultado["resumen"] = parrafos[-1]

    puntajes = [v["puntaje"] for v in resultado["evaluacion"].values() if isinstance(v["puntaje"], int)]
    if puntajes and any(puntajes):
        resultado["promedio"] = sum(puntajes) / len(puntajes)
    else:
        resultado["promedio"] = 0

    return resultado

def extract_executor_output(raw_output):
    """
    Extrae el mensaje de la salida del executor de forma robusta.
    - Si es un JSON válido con campo 'mensaje', devuelve ese string.
    - Si es un string con bloque JSON, lo intenta extraer.
    - Si es texto plano, devuelve el texto tal como está.
    - Si el mensaje está anidado (ej: {"mensaje": {"mensaje": ...}}), desempaqueta.
    """
    # 1. Si es ya un dict con 'mensaje'
    if isinstance(raw_output, dict):
        mensaje = raw_output.get("mensaje")
        # Si está anidado
        if isinstance(mensaje, dict) and "mensaje" in mensaje:
            return mensaje["mensaje"]
        if mensaje:
            return mensaje

    # 2. Si es string, buscar bloque JSON
    if isinstance(raw_output, str):
        # Busca bloque JSON en texto
        json_regex = re.compile(r"\{[\s\S]*?\}", re.MULTILINE)
        match = json_regex.search(raw_output)
        if match:
            try:
                data = json.loads(match.group())
                mensaje = data.get("mensaje")
                if isinstance(mensaje, dict) and "mensaje" in mensaje:
                    return mensaje["mensaje"]
                if mensaje:
                    return mensaje
            except Exception:
                pass
        # Si no encuentra JSON, devuelve el texto plano quitando posibles comillas de bloque
        texto = raw_output.strip()
        if texto.startswith("```json"):
            texto = texto.replace("```json", "").replace("```", "").strip()
        return texto

    # 3. Si nada funcionó, devuelve como string
    return str(raw_output)