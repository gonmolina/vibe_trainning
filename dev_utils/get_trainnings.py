import requests
import json
import os
from datetime import datetime

# Cargar configuración desde JSON
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "..", "strava_config.json")

if not os.path.exists(CONFIG_PATH):
    raise FileNotFoundError(f"No se encontró el archivo de configuración en: {CONFIG_PATH}")

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

CLIENT_ID = config["client_id"]
CLIENT_SECRET = config["client_secret"]
REFRESH_TOKEN = config["refresh_token"]
OUTPUT_DIR = config["output_dir"]


def get_new_access_token():
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }
    response = requests.post("https://www.strava.com/oauth/token", data=payload)
    
    if response.status_code != 200:
        print(f"❌ Error al refrescar token ({response.status_code}): {response.text}")
        return None
        
    data = response.json()
    return data["access_token"]


def download_activities():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    token = get_new_access_token()
    if not token:
        return
        
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        "https://www.strava.com/api/v3/athlete/activities",
        headers=headers,
        params={"per_page": 50},
    )

    if response.status_code != 200:
        print(f"❌ Error en la API de Strava ({response.status_code}): {response.text}")
        return

    activities = response.json()
    if not isinstance(activities, list):
        print(f"❌ Respuesta inesperada de la API: {activities}")
        return

    count_new = 0
    for activity in activities:
        if count_new >= 20:
            break

        fecha_str = activity["start_date_local"].split("T")[0]
        fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d")
        año, semana, _ = fecha_obj.isocalendar()
        
        # Crear subcarpeta por semana
        semana_dir = os.path.join(OUTPUT_DIR, f"semana_{año}-{semana:02d}")
        if not os.path.exists(semana_dir):
            os.makedirs(semana_dir)
            
        id_act = activity["id"]
        nombre = activity["name"]

        # Nombres de archivo
        json_path = os.path.join(semana_dir, f"{fecha_str}_{id_act}.json")
        laps_path = os.path.join(semana_dir, f"{fecha_str}_{id_act}_laps.json")
        md_path = os.path.join(semana_dir, f"{fecha_str}_{id_act}.md")

        # Verificar si ya existe
        if os.path.exists(json_path):
            print(f"⏭️  Omitiendo (ya existe): {fecha_str} - {nombre}")
            continue

        count_new += 1

        # 🔄 Obtener Laps (Vueltas)
        laps_response = requests.get(
            f"https://www.strava.com/api/v3/activities/{id_act}/laps",
            headers=headers
        )
        laps = laps_response.json() if laps_response.status_code == 200 else []

        # Datos básicos
        distancia_km = round(activity["distance"] / 1000, 2)
        desnivel_m = activity["total_elevation_gain"]
        minutos = int(activity["moving_time"] // 60)
        segundos = int(activity["moving_time"] % 60)

        # 📝 Generar Tabla de Laps para el Markdown
        laps_table = ""
        if laps and len(laps) > 1:
            laps_table = "\n## ⏱️ Vueltas (Laps)\n"
            laps_table += "| Lap | Distancia | Tiempo | Ritmo | FC Med |\n"
            laps_table += "| :--- | :--- | :--- | :--- | :--- |\n"
            for i, lap in enumerate(laps):
                d_lap = round(lap["distance"] / 1000, 2)
                m_lap = int(lap["moving_time"] // 60)
                s_lap = int(lap["moving_time"] % 60)
                # Ritmo min/km
                ritmo_seg = lap["moving_time"] / (lap["distance"] / 1000) if lap["distance"] > 0 else 0
                r_min = int(ritmo_seg // 60)
                r_seg = int(ritmo_seg % 60)
                fc = lap.get("average_heartrate", "--")
                laps_table += f"| {i+1} | {d_lap} km | {m_lap}:{s_lap:02d} | {r_min}:{r_seg:02d} | {fc} |\n"

        # 📝 Generar contenido Markdown
        md_content = f"""# 🏃‍♂️ {nombre}
**Fecha:** {fecha_str}
**ID Strava:** [{id_act}](https://www.strava.com/activities/{id_act})

## 📊 Estadísticas Clave
- **Distancia:** {distancia_km} km
- **Desnivel Positivo:** {desnivel_m} m 🏔️
- **Tiempo en movimiento:** {minutos}:{segundos:02d}
- **Tipo de actividad:** {activity["type"]}
{laps_table}
---
*Generado automáticamente vía API de Strava.*
"""

        # Guardar archivos
        with open(json_path, "w") as f:
            json.dump(activity, f, indent=4)
        
        if laps:
            with open(laps_path, "w") as f:
                json.dump(laps, f, indent=4)

        with open(md_path, "w") as f:
            f.write(md_content)

        print(f"✅ Procesado por semana: {fecha_str} - {nombre}")


if __name__ == "__main__":
    download_activities()
