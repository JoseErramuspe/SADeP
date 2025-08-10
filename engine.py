import os
import json
from pathlib import Path
from maker_instance import llamar_maker
from user_instance import llamar_user
from executor_instance import llamar_executor
from reviewer_instance import llamar_reviewer
from planifier_instance import llamar_planifier
from utils import extract_reviewer_output, extract_executor_output

EXPERIMENTOS_DIR = os.path.join(os.path.dirname(__file__), "experimentos")

def cargar_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf8") as f:
        return json.load(f)

def guardar_json(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def siguiente_ciclo(ciclos_dir):
    existentes = list(Path(ciclos_dir).glob("ciclo_*"))
    if not existentes:
        return 1
    return 1 + max(int(p.name.split("_")[1]) for p in existentes)

def promedio_eval(evaluacion):
    if not evaluacion or "evaluacion" not in evaluacion:
        return 0
    keys = ["claridad", "utilidad", "creatividad", "robustez", "adaptabilidad", "estructura"]
    puntajes = []
    for k in keys:
        try:
            puntajes.append(evaluacion["evaluacion"][k]["puntaje"])
        except (KeyError, TypeError):
            puntajes.append(0)
    if puntajes:
        return sum(puntajes) / len(puntajes)
    else:
        return 0

def main():
    # --- Parámetros base ---
    nombre_experimento = input("Nombre del experimento: ").strip()
    base = os.path.join(EXPERIMENTOS_DIR, nombre_experimento)
    ciclos_dir = os.path.join(base, "ciclos")
    config_path = os.path.join(base, "config.json")
    # Ruta a config.json global (carpeta principal)
    config_global_path = os.path.join(os.path.dirname(__file__), "config.json")
    config_global = cargar_json(config_global_path)
    historial_path = os.path.join(base, "historial_completo.json")
    mejor_prompt_path = os.path.join(base, "mejor_prompt.json")

    # --- Carga de configuración ---
    if not os.path.exists(config_path):
        print("No existe config.json. Ejecuta primero el script de creación de estructura.")
        return
    config = cargar_json(config_path)
    categoria = config.get("categoria") or input("Categoría del prompt: ").strip()
    contexto = config.get("contexto")
    puntaje_objetivo = config.get("puntaje_objetivo", 100)
    max_ciclos = config.get("max_ciclos", 10)
    max_turnos = config.get("max_turnos", 20)

    ciclo = siguiente_ciclo(ciclos_dir)
    prompt_anterior = ""
    retroalimentacion = {}
    mejor_prompt = None
    mejor_evaluacion = None
    historial_ciclos = cargar_json(historial_path) if os.path.exists(historial_path) else []

    # --- PLANIFICACIÓN PREVIA (3 ciclos de planificación antes de iniciar los ciclos de maker) ---
    planificacion_dir = os.path.join(base, "planificacion")
    planificaciones_previas = []
    for plan_ciclo in range(1, 4):
        ciclo_plan_dir = os.path.join(planificacion_dir, f"ciclo_{plan_ciclo:03d}")
        os.makedirs(ciclo_plan_dir, exist_ok=True)
        planifier_input = {
            "categoria": categoria,
            "contexto": contexto,
            "planificaciones_previas": planificaciones_previas,
            "especificaciones": config_global.get("especificaciones", {}).get("planifier", {})
        }
        print(f"\n--- PLANIFICACIÓN CICLO {plan_ciclo:03d} ---")
        print(f"Categoría: {categoria}")
        print(f"Contexto: {contexto}")
        planificacion = llamar_planifier(planifier_input)
        planificacion_path = os.path.join(ciclo_plan_dir, "planificacion.json")
        guardar_json(planificacion, planificacion_path)
        for bloque in ["Atributos", "Tareas", "Características"]:
            print(f"\n[{bloque.upper()}]")
            for obj in planificacion.get(bloque, []):
                print(f"- {obj.get('titulo', '')}: {obj.get('descripcion', '')}")
        planificaciones_previas.append(planificacion)

    # --- INICIO DE CICLOS DE MAKER, USER, EXECUTOR Y REVIEWER ---
    while ciclo <= max_ciclos:
        print(f"\n<===-- CICLO {ciclo} --===>")
        ciclo_dir = os.path.join(ciclos_dir, f"ciclo_{ciclo:03d}")
        os.makedirs(ciclo_dir, exist_ok=True)

        # 1. MAKER
        maker_input = {
            "categoria": categoria,
            "prompt_anterior": prompt_anterior,
            "retroalimentacion": retroalimentacion,
            "planificacion": planificaciones_previas[-1] if planificaciones_previas else None,
            "especificaciones": config_global.get("especificaciones", {}).get("maker", {})
        }
        guardar_json(maker_input, os.path.join(ciclo_dir, "maker_input.json"))
        maker_output = llamar_maker(maker_input)
        guardar_json(maker_output, os.path.join(ciclo_dir, "maker_output.json"))
        prompt_actual = maker_output["prompt"]
        print(f"\n[PROMPT GENERADO POR MAKER]\n{prompt_actual}\n")

        print(f"\n=== Conversación User <-> Executor ===")
        # 2. Conversación User <-> Executor
        historial = []
        user_turn = False
        turnos = 0
        mensaje_user = None
        mensaje_executor = None
        despedida = False

        while turnos < max_turnos:
            if user_turn:
                user_input = {
                    "categoria": categoria,
                    "prompt": prompt_actual,
                    "historial": historial
                    "especificaciones": config_global.get("especificaciones", {}).get("user", {})
                }
                user_output = llamar_user(user_input)
                mensaje_user = user_output.get("mensaje", "").strip()
                if not mensaje_user:
                    print("User no generó mensaje. Fin de la conversación.")
                    break
                print(f"[USER]: {mensaje_user}")
                historial.append({"rol": "user", "mensaje": mensaje_user})
                if "despedida" in mensaje_user.lower() or "adiós" in mensaje_user.lower() or "hasta luego" in mensaje_user.lower():
                    despedida = True
                    break
            else:
                executor_input = {
                    "prompt": prompt_actual,
                    "mensaje_user": mensaje_user,
                    "historial": historial
                    "especificaciones": config_global.get("especificaciones", {}).get("executor", {})
                }
                raw_executor_output = llamar_executor(executor_input)
                mensaje_executor = extract_executor_output(raw_executor_output)  # <--- EXTRACTOR ROBUSTO
                if not mensaje_executor:
                    print("Executor no generó mensaje. Fin de la conversación.")
                    break
                print(f"[EXECUTOR]: {mensaje_executor}")
                historial.append({"rol": "executor", "mensaje": mensaje_executor})
            user_turn = not user_turn
            turnos += 1

        # Guarda la conversación del ciclo
        guardar_json(historial, os.path.join(ciclo_dir, "historial.json"))

        # 3. USER_OUTPUT para compatibilidad con reviewer
        user_output_json = {"historial": historial}
        guardar_json(user_output_json, os.path.join(ciclo_dir, "user_output.json"))

        # 4. REVIEWER
        reviewer_input = {
            "prompt": prompt_actual,
            "categoria": categoria,
            "historial": historial,
            "evaluacion_previa": mejor_evaluacion["evaluacion"] if mejor_evaluacion and "evaluacion" in mejor_evaluacion else {}
            "especificaciones": config_global.get("especificaciones", {}).get("reviewer", {})
        }
        guardar_json(reviewer_input, os.path.join(ciclo_dir, "reviewer_input.json"))
        raw_reviewer_output = llamar_reviewer(reviewer_input)
        guardar_json(raw_reviewer_output, os.path.join(ciclo_dir, "reviewer_output_raw.json"))  # Guarda crudo para depuración

        # --- USAR EXTRACTOR ---
        reviewer_output = extract_reviewer_output(
            raw_reviewer_output if isinstance(raw_reviewer_output, str) else json.dumps(raw_reviewer_output, ensure_ascii=False, indent=2)
        )
        guardar_json(reviewer_output, os.path.join(ciclo_dir, "reviewer_output.json"))

        print(f"\n=== Resumen de puntajes por categoría ===")
        # Resumen de puntajes por categoría (si existen)
        if "evaluacion" in reviewer_output:
            print("\n[PUNTAJE POR CATEGORÍA DE REVIEWER]:")
            for categoria, detalle in reviewer_output["evaluacion"].items():
                print(f"  {categoria.capitalize()}: {detalle.get('puntaje', 'N/A')}")
        else:
            print("\n[REVIEWER]: No se encontraron detalles de evaluación por categoría.")

        # Resumen final
        print(f"\n[EVALUACIÓN FINAL]: {reviewer_output.get('resumen', 'Sin resumen')}")

        # 5. Actualiza historial y mejores resultados
        entry = {
            "ciclo": ciclo,
            "prompt": prompt_actual,
            "evaluacion": reviewer_output,
            "justificacion": maker_output.get("justificacion", "")
        }
        historial_ciclos.append(entry)
        guardar_json(historial_ciclos, historial_path)

        promedio = reviewer_output.get("promedio") or promedio_eval(reviewer_output)
        print(f"\n[PROMEDIO DE PUNTUACIÓN]: {promedio:.2f}")
        if (not mejor_evaluacion) or (promedio > (mejor_evaluacion.get("promedio") or promedio_eval(mejor_evaluacion))):
            mejor_prompt = prompt_actual
            mejor_evaluacion = reviewer_output
            guardar_json({
                "prompt": mejor_prompt,
                "evaluacion": mejor_evaluacion
            }, mejor_prompt_path)

        # 6. Condición de parada
        if promedio >= puntaje_objetivo:
            print(f"¡Condición de parada: puntaje objetivo alcanzado ({promedio})!")
            break
        if ciclo == max_ciclos:
            print("¡Condición de parada: máximo de ciclos alcanzado!")
            break

        # 7. Prepara siguiente ciclo
        prompt_anterior = prompt_actual
        retroalimentacion = reviewer_output
        ciclo += 1

    print("\n==== RESULTADO FINAL ====")
    print("Mejor prompt:", mejor_prompt)
    print("Evaluación final:", mejor_evaluacion.get("resumen", "Sin resumen"))
    print(f"Historial de ciclos guardado en {historial_path}")

if __name__ == "__main__":
    main()
