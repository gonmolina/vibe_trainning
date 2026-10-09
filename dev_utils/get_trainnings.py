import requests
import json
import os
import time
from datetime import datetime
import gpxpy
import gpxpy.gpx

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
# Redirigir la salida al blog de Hugo (Page Bundles)
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "blog", "content", "entrenamientos")


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


def download_gpx(activity_id, token, save_path):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"keys": "latlng,altitude,time", "key_by_type": "true"}
    response = requests.get(
        f"https://www.strava.com/api/v3/activities/{activity_id}/streams",
        headers=headers,
        params=params
    )
    
    # Reconstruir GPX
    gpx = gpxpy.gpx.GPX()
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    if response.status_code != 200:
        print(f"⚠️ No se pudo obtener el stream para GPX ({activity_id})")
        with open(save_path, "w") as f:
            f.write(gpx.to_xml())
        return False
        
    streams = response.json()
    
    latlng = streams.get("latlng", {}).get("data", [])
    altitudes = streams.get("altitude", {}).get("data", [])
    times = streams.get("time", {}).get("data", [])
    
    # Strava activity start time
    for i in range(len(latlng)):
        lat, lon = latlng[i]
        ele = altitudes[i] if i < len(altitudes) else 0
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon, elevation=ele))
        
    with open(save_path, "w") as f:
        f.write(gpx.to_xml())
    return True


def download_photos(activity_id, token, folder_path):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"https://www.strava.com/api/v3/activities/{activity_id}/photos",
        headers=headers,
        params={"size": 5000}
    )
    
    if response.status_code != 200:
        print(f"⚠️ No se pudieron obtener las fotos ({activity_id})")
        return []
        
    photos_data = response.json()
    downloaded_files = []
    
    for i, photo in enumerate(photos_data):
        if "urls" in photo and "5000" in photo["urls"]:
            url = photo["urls"]["5000"]
        elif "url" in photo:
            url = photo["url"]
        else:
            continue
            
        img_response = requests.get(url)
        if img_response.status_code == 200:
            filename = f"photo_{i}.jpg"
            with open(os.path.join(folder_path, filename), "wb") as f:
                f.write(img_response.content)
            downloaded_files.append(filename)
            
    return downloaded_files


def download_activities():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    token = get_new_access_token()
    if not token:
        return
        
    headers = {"Authorization": f"Bearer {token}"}

    all_activities = []
    page = 1
    print("📥 Obteniendo lista de actividades desde Strava...")
    while True:
        response = requests.get(
            "https://www.strava.com/api/v3/athlete/activities",
            headers=headers,
            params={"per_page": 100, "page": page},
        )

        if response.status_code != 200:
            print(f"❌ Error en la API de Strava ({response.status_code}): {response.text}")
            break

        activities = response.json()
        if not activities or not isinstance(activities, list):
            break

        all_activities.extend(activities)
        print(f"   Página {page}: {len(activities)} actividades encontradas.")
        if len(activities) < 100:
            break

        # Si llegamos a actividades anteriores al 11 de julio de 2026, ya cubrimos todo lo nuevo
        if activities[-1].get("start_date_local", "") < "2026-07-11":
            break

        page += 1
        time.sleep(0.2)

    count_new = 0
    total_found = len(all_activities)
    print(f"🔎 Total de actividades para verificar: {total_found}")

    for activity in all_activities:
        fecha_str = activity["start_date_local"].split("T")[0]
        if fecha_str < "2026-07-11":
            continue

        nombre = activity["name"].replace('"', '\\"')
        id_act = activity["id"]

        # Page Bundle Directory
        activity_dir = os.path.join(OUTPUT_DIR, f"{fecha_str}_{id_act}")
        json_path = os.path.join(activity_dir, "activity.json")
        md_path = os.path.join(activity_dir, "index.md")
        gpx_path = os.path.join(activity_dir, "activity.gpx")

        # Verificar si ya existe
        if os.path.exists(json_path):
            continue

        if not os.path.exists(activity_dir):
            os.makedirs(activity_dir)

        count_new += 1
        print(f"🔄 [{count_new}] Procesando: {fecha_str} - {nombre} (ID: {id_act})")

        has_polyline = bool(activity.get("map", {}).get("summary_polyline"))

        # 🔄 Obtener Laps (Vueltas) si aplica
        laps = []
        if activity.get("type") in ["Run", "TrailRun", "Ride", "Hike", "Walk"]:
            try:
                laps_response = requests.get(
                    f"https://www.strava.com/api/v3/activities/{id_act}/laps",
                    headers=headers
                )
                if laps_response.status_code == 200:
                    laps = laps_response.json()
            except Exception as e:
                print(f"⚠️ Error obteniendo laps: {e}")
            time.sleep(0.15)

        # 🔄 Descargar GPX si tiene ruta, o generar GPX vacío
        if has_polyline:
            download_gpx(id_act, token, gpx_path)
            time.sleep(0.15)
        else:
            gpx = gpxpy.gpx.GPX()
            with open(gpx_path, "w") as f:
                f.write(gpx.to_xml())

        # 🔄 Fotos solo si tiene fotos asociadas
        photos = []
        if activity.get("total_photo_count", 0) > 0:
            photos = download_photos(id_act, token, activity_dir)
            time.sleep(0.15)

        # Datos básicos
        distancia_km = round(activity["distance"] / 1000, 2)
        desnivel_m = activity["total_elevation_gain"]
        minutos = int(activity["moving_time"] // 60)
        segundos = int(activity["moving_time"] % 60)

        # 📝 Generar Tabla de Laps
        laps_table = ""
        if laps and len(laps) > 1:
            laps_table = "\n## ⏱️ Vueltas (Laps)\n"
            laps_table += "| Lap | Distancia | Tiempo | Ritmo | FC Med |\n"
            laps_table += "| :--- | :--- | :--- | :--- | :--- |\n"
            for i, lap in enumerate(laps):
                d_lap = round(lap["distance"] / 1000, 2)
                m_lap = int(lap["moving_time"] // 60)
                s_lap = int(lap["moving_time"] % 60)
                ritmo_seg = lap["moving_time"] / (lap["distance"] / 1000) if lap["distance"] > 0 else 0
                r_min = int(ritmo_seg // 60)
                r_seg = int(ritmo_seg % 60)
                fc = lap.get("average_heartrate", "--")
                laps_table += f"| {i+1} | {d_lap} km | {m_lap}:{s_lap:02d} | {r_min}:{r_seg:02d} | {fc} |\n"

        # 🖼️ Generar sección de fotos
        photos_section = ""
        if photos:
            photos_section = "\n## 📸 Fotos\n"
            for p in photos:
                photos_section += f"![Foto]({p})\n"

        # 🗺️ Mapa GPX
        map_section = "\n## 🗺️ Mapa y Recorrido\n"
        map_section += '{{< gpx "activity.gpx" >}}\n'

        # 📝 Generar contenido Markdown
        md_content = f"""---
title: "{nombre}"
date: {fecha_str}
categories: ["Entrenamiento"]
tags: ["{activity["type"]}", "Strava"]
strava_id: {id_act}
---

## 📊 Estadísticas Clave
- **Distancia:** {distancia_km} km
- **Desnivel Positivo:** {desnivel_m} m 🏔️
- **Tiempo en movimiento:** {minutos}:{segundos:02d}
- **Tipo de actividad:** {activity["type"]}

{map_section}
{laps_table}
{photos_section}

---
*Generado automáticamente vía API de Strava.*
"""

        # Guardar archivos
        with open(json_path, "w") as f:
            json.dump(activity, f, indent=4)
        
        with open(md_path, "w") as f:
            f.write(md_content)

    print(f"✅ Descarga completada: {count_new} actividades nuevas procesadas.")


if __name__ == "__main__":
    download_activities()
