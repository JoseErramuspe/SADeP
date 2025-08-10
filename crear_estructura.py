import os
import json

def crear_estructura(nombre_experimento):
    base = os.path.join("experimentos", nombre_experimento)
    ciclos_dir = os.path.join(base, "ciclos")
    planificacion_dir = os.path.join(base, "planificacion")

    # Crear carpetas principales
    os.makedirs(ciclos_dir, exist_ok=True)
    os.makedirs(planificacion_dir, exist_ok=True)
    
    # Crear archivo config.json de ejemplo si no existe
    config_path = os.path.join(base, "config.json")
    if not os.path.exists(config_path):
        config = {
            "categoria": "Ejemplo de categoría", # Categoría del experimento
            "contexto": "Ejemplo de contexto",  # Contexto del experimento
            "puntaje_objetivo": 95, # Puntaje objetivo del prompt
            "max_ciclos": 10, # Limitar cantidad de ciclos del experimento
            "max_turnos": 20  # Limitar turnos de conversación User-Executor
        }
        with open(config_path, "w", encoding="utf8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"Archivo creado: {config_path}")
    else:
        print(f"Ya existe: {config_path}")

    # Crear archivos vacíos de historial y mejor_prompt si no existen
    historial_path = os.path.join(base, "historial_completo.json")
    mejor_prompt_path = os.path.join(base, "mejor_prompt.json")
    if not os.path.exists(historial_path):
        with open(historial_path, "w", encoding="utf8") as f:
            json.dump([], f)
        print(f"Archivo creado: {historial_path}")
    else:
        print(f"Ya existe: {historial_path}")

    if not os.path.exists(mejor_prompt_path):
        with open(mejor_prompt_path, "w", encoding="utf8") as f:
            json.dump({}, f)
        print(f"Archivo creado: {mejor_prompt_path}")
    else:
        print(f"Ya existe: {mejor_prompt_path}")

    print(f"Estructura creada correctamente en {base}")

if __name__ == "__main__":
    nombre = input("Nombre del experimento: ").strip()
    if not nombre:
        print("Debes ingresar un nombre para el experimento.")
    else:
        crear_estructura(nombre)