import streamlit as st
import json
from pathlib import Path
from datetime import datetime, date, time
from zoneinfo import ZoneInfo

st.set_page_config(page_title="Convertidor de Horas", layout="centered")

ZONAS_PATH = Path(__file__).parent / "zonas.json"
ZONAS = json.loads(ZONAS_PATH.read_text(encoding="utf-8"))

st.title("🕒 Convertidor de horas")
st.caption("Convierte una hora local a otros lugares del mundo.")

labels = list(ZONAS.keys())

# Selección de origen y destinos
origen = st.selectbox("Origen", labels, index=labels.index("Chile") if "Chile" in labels else 0)
destinos = st.multiselect(
    "Destinos",
    [x for x in labels if x != origen],
    default=[x for x in ["Tijuana", "Valencia"] if x in labels and x != origen],
)

st.divider()

# Fecha
modo_fecha = st.radio("Fecha", ["Hoy", "Elegir fecha"], horizontal=True)
if modo_fecha == "Hoy":
    fecha = date.today()
else:
    fecha = st.date_input("Fecha", value=date.today())

# Hora
hora = st.time_input("Hora (del origen)", value=time(9, 0))

st.divider()

def convertir(origen, fecha, hora, destinos):
    tz_origen = ZoneInfo(ZONAS[origen])
    dt_origen = datetime.combine(fecha, hora).replace(tzinfo=tz_origen)

    resultados = []
    for d in destinos:
        tz_dest = ZoneInfo(ZONAS[d])
        dt_dest = dt_origen.astimezone(tz_dest)
        resultados.append({
            "Lugar": d,
            "Fecha": dt_dest.strftime("%Y-%m-%d"),
            "Hora": dt_dest.strftime("%H:%M"),
        })
    return resultados

if st.button("Convertir", type="primary", use_container_width=True):
    if not destinos:
        st.warning("Selecciona al menos un destino.")
    else:
        resultados = convertir(origen, fecha, hora, destinos)
        st.subheader("Equivalencias horarias")
        st.dataframe(resultados, hide_index=True, use_container_width=True)

        # Texto simple para copiar/pegar
        texto = [f"Hora base ({origen}): {fecha} {hora.strftime('%H:%M')}"]
        for r in resultados:
            texto.append(f"{r['Lugar']}: {r['Fecha']} {r['Hora']}")
        st.text_area("Copiar / pegar", value="\n".join(texto), height=120)

