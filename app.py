import streamlit as st
import random
import time
import json
import re
from core.questions import (PREGUNTAS_ESCALA, PREGUNTAS_ABIERTAS,
                             PREGUNTAS_EXTERNAS_ESCALA, PREGUNTAS_EXTERNAS_ABIERTAS,
                             IDS_ESCALA, IDS_ABIERTAS, IDS_EXTERNAS_ESCALA,
                             IDS_EXTERNAS_ABIERTAS, ESCALA_LABELS, HERIDAS_INFO,
                             get_intensidad)

st.set_page_config(
    page_title="El Espejo de tus Relaciones",
    page_icon="🪞",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── CSS ─────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbarActions"], [data-testid="stDeployButton"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
header[data-testid="stHeader"] { background: transparent !important; border-bottom: none !important; box-shadow: none !important; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
  background: #4E32AD !important;
}
[data-testid="stAppViewContainer"] > .main { background: #4E32AD; }
[data-testid="stVerticalBlock"] { background: transparent !important; }
section[data-testid="stSidebar"] { display: none !important; }
.block-container { max-width: 700px; padding: 2rem 1.5rem; }

* { font-family: 'Inter', sans-serif !important; }
h1, h2, h3 { color: #DCFE77 !important; }
p, li { color: #F0ECFF !important; }

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
  background: rgba(255,255,255,.1) !important;
  color: #F0ECFF !important;
  border: 1px solid rgba(255,255,255,.2) !important;
  border-radius: 8px !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
  border-color: rgba(220,254,119,.5) !important;
  box-shadow: 0 0 0 2px rgba(220,254,119,.1) !important;
}

[data-testid="stRadio"] label { color: rgba(240,236,255,.8) !important; }

[data-testid="stButton"] > button {
  background: #FF6B4E !important; color: #fff !important;
  border: none !important; border-radius: 8px !important;
  font-weight: 700 !important; font-size: 15px !important;
  padding: 12px 32px !important; width: 100% !important; transition: .2s !important;
}
[data-testid="stButton"] > button:hover { background: #ff8570 !important; transform: translateY(-1px) !important; }
[data-testid="stButton"] > button:disabled { background: #2B1D8A !important; color: rgba(240,236,255,.4) !important; }

[data-testid="stDownloadButton"] > button {
  background: #2B1D8A !important; color: #DCFE77 !important;
  border: 1px solid rgba(220,254,119,.3) !important; border-radius: 8px !important; width: 100%;
}

[data-testid="stProgress"] > div { background: #2B1D8A !important; border-radius: 6px; }
[data-testid="stProgress"] > div > div { background: #FF6B4E !important; border-radius: 6px; }

hr { border-color: rgba(255,255,255,.1) !important; }
</style>
""", unsafe_allow_html=True)


# ─── Estado ───────────────────────────────────────────────────────────────────

def init_state():
    defaults = {
        "etapa": "inicio",
        "proceso_id": None,
        "nombre": "",
        "correo": "",
        "orden_preguntas": [],
        "q_idx": 0,
        "a_idx": 0,
        "respuestas": {},
        "analisis": None,
        "scores": None,
        "herida_primaria": None,
        "herida_secundaria": None,
        "evaluadores_form": [{"nombre": "", "correo": ""}] * 3,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def ir_a(etapa, **kwargs):
    st.session_state.etapa = etapa
    for k, v in kwargs.items():
        st.session_state[k] = v
    st.rerun()


# ─── Helpers de UI ────────────────────────────────────────────────────────────

def box(html: str, border_color: str = "rgba(220,254,119,.15)"):
    st.markdown(
        f'<div style="background:#2B1D8A;border:1px solid {border_color};'
        f'border-radius:10px;padding:20px 24px;margin-bottom:16px;">{html}</div>',
        unsafe_allow_html=True)


def herida_badge(h_id: str, score: int = None):
    info = HERIDAS_INFO[h_id]
    score_txt = f" — {score} pts" if score is not None else ""
    return (f'<span style="background:{info["color"]}22;border:1px solid {info["color"]}66;'
            f'color:{info["color"]};padding:4px 12px;border-radius:4px;font-size:14px;">'
            f'{info["icono"]} {info["nombre"]}{score_txt}</span>')


# ─── Página: Inicio ───────────────────────────────────────────────────────────

def page_inicio():
    st.markdown("""
<div style="text-align:center;padding:40px 0 20px;">
  <div style="font-size:52px;margin-bottom:16px;">🪞</div>
  <h1 style="font-size:30px;margin-bottom:8px;">El Espejo de tus Relaciones</h1>
  <p style="color:#FF6B4E;font-size:16px;font-style:italic;margin-bottom:24px;">
    Descubre qué herida emocional está guiando tu forma de relacionarte
  </p>
  <p style="color:rgba(240,236,255,.8);font-size:14px;max-width:520px;margin:0 auto 32px;line-height:1.8;">
    Basado en el marco de las 5 heridas de Lise Bourbeau e integrado con la filosofía
    de Alejandro Jodorowsky. Dos fases: tu propio diagnóstico y, si quieres,
    el espejo de quienes te conocen.
  </p>
  <p style="color:rgba(240,236,255,.55);font-size:13px;">⏱️ Fase 1: 10 a 15 minutos · Fase 2 (opcional): invitas a 3-5 personas cercanas</p>
</div>
""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        nombre = st.text_input("Tu nombre", placeholder="¿Cómo te llamas?", key="inp_nombre")
        correo = st.text_input("Tu correo", placeholder="Para recibir tu reporte", key="inp_correo")

        st.markdown("""
<div style="background:#2B1D8A;border:1px solid rgba(220,254,119,.15);border-radius:8px;
            padding:12px 16px;margin:16px 0;font-size:12px;color:rgba(240,236,255,.6);line-height:1.7;">
<strong style="color:#FF6B4E;">Aviso importante:</strong><br>
Esta herramienta es un ejercicio de autoconocimiento basado en modelos de desarrollo personal.
No es un diagnóstico clínico ni reemplaza la atención de un profesional de salud mental.
Si estás viviendo una crisis emocional, te recomendamos buscar apoyo profesional.
</div>
""", unsafe_allow_html=True)

        if st.button("🪞 Comenzar mi diagnóstico"):
            if not nombre.strip():
                st.error("Por favor ingresa tu nombre.")
                return
            if not correo.strip() or "@" not in correo:
                st.error("Por favor ingresa un correo válido.")
                return
            orden = IDS_ESCALA.copy()
            random.shuffle(orden)
            from core.database import create_proceso
            proceso = create_proceso(nombre.strip(), correo.strip().lower(), orden)
            ir_a("instrucciones",
                 proceso_id=proceso["id"],
                 nombre=nombre.strip(),
                 correo=correo.strip().lower(),
                 orden_preguntas=orden)


# ─── Página: Instrucciones ────────────────────────────────────────────────────

def page_instrucciones():
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown("""
<div style="text-align:center;padding:20px 0 32px;">
  <h2 style="font-size:22px;">Antes de comenzar</h2>
</div>
""", unsafe_allow_html=True)

        box("""
<p style="color:#c9859a;font-size:15px;line-height:1.8;margin-bottom:14px;">
  Responde desde lo que realmente sientes — no desde lo que crees que deberías sentir.
</p>
<p style="color:#b899c8;font-size:14px;line-height:1.8;margin-bottom:14px;">
  Vas a responder <strong style="color:#f5eef8;">20 afirmaciones de escala</strong>
  sobre cómo vives y reaccionas en tus relaciones.
  Después, 4 preguntas de reflexión abierta (opcionales).
</p>
<p style="color:#b899c8;font-size:14px;line-height:1.8;">
  No hay respuestas correctas ni incorrectas.
  Lo que sientes — aunque no te guste — es la información más valiosa.
</p>
""", "#3d2040")

        st.markdown("""
<div style="background:#1c1535;border-left:3px solid #c9859a;padding:14px 18px;
            border-radius:0 6px 6px 0;margin:8px 0 24px;">
  <p style="color:#7d6690;font-size:13px;margin:0;line-height:1.7;">
    <strong style="color:#b899c8;">Escala de respuestas:</strong><br>
    1 = No me identifica &nbsp;·&nbsp; 2 = Poco &nbsp;·&nbsp; 3 = A veces
    &nbsp;·&nbsp; 4 = Bastante &nbsp;·&nbsp; 5 = Me describe completamente
  </p>
</div>
""", unsafe_allow_html=True)

        if st.button("Entendido, comenzar →"):
            ir_a("cuestionario", q_idx=0)


# ─── Página: Cuestionario (escala) ────────────────────────────────────────────

def page_cuestionario():
    idx = st.session_state.q_idx
    orden = st.session_state.orden_preguntas
    total = len(orden)
    q_id = orden[idx]

    col1, col2, col3 = st.columns([1, 5, 1])
    with col2:
        st.progress(idx / total)
        st.markdown(
            f'<p style="color:#7d6690;font-size:12px;text-align:center;margin:4px 0 20px;">'
            f'Pregunta {idx + 1} de {total}</p>',
            unsafe_allow_html=True)

        st.markdown(
            f'<p style="color:#f5eef8;font-size:16px;line-height:1.7;'
            f'text-align:center;margin:20px 0 28px;">'
            f'{PREGUNTAS_ESCALA[q_id]["usuario"]}</p>',
            unsafe_allow_html=True)

        prev = st.session_state.respuestas.get(q_id)
        prev_idx = (prev - 1) if prev else None

        seleccion = st.radio(
            "Tu respuesta:",
            options=list(range(1, 6)),
            format_func=lambda x: f"{x} — {ESCALA_LABELS[x-1]}",
            index=prev_idx,
            key=f"radio_q{q_id}",
            label_visibility="collapsed",
        )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Continuar →"):
            if seleccion is None:
                st.error("Por favor selecciona una respuesta.")
                return
            st.session_state.respuestas[q_id] = seleccion
            from core.database import save_respuesta
            save_respuesta(st.session_state.proceso_id, q_id, valor_escala=seleccion)

            if idx + 1 < total:
                ir_a("cuestionario", q_idx=idx + 1)
            else:
                ir_a("reflexion", a_idx=0)


# ─── Página: Reflexión abierta ────────────────────────────────────────────────

def page_reflexion():
    idx = st.session_state.a_idx
    pid = IDS_ABIERTAS[idx]

    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.progress(1.0)
        st.markdown(
            f'<p style="color:#7d6690;font-size:12px;text-align:center;margin:4px 0 20px;">'
            f'Reflexión {idx + 1} de 4 — opcional</p>',
            unsafe_allow_html=True)

        st.markdown(
            f'<p style="color:#c9859a;font-size:15px;line-height:1.7;'
            f'text-align:center;font-style:italic;margin:20px 0 16px;">'
            f'Una pregunta para reflexionar</p>',
            unsafe_allow_html=True)
        st.markdown(
            f'<p style="color:#f5eef8;font-size:15px;line-height:1.7;'
            f'text-align:center;margin:0 0 24px;">'
            f'{PREGUNTAS_ABIERTAS[pid]}</p>',
            unsafe_allow_html=True)

        prev = st.session_state.respuestas.get(pid, "")
        respuesta = st.text_area(
            "Tu respuesta (puedes dejarla en blanco):",
            value=str(prev) if prev else "",
            key=f"open_a{pid}",
            height=100,
            placeholder="Tómate el tiempo que necesites...",
            label_visibility="collapsed",
        )

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Omitir"):
                _avanzar_reflexion(idx)
        with c2:
            if st.button("Continuar →"):
                if respuesta.strip():
                    st.session_state.respuestas[pid] = respuesta.strip()
                    from core.database import save_respuesta
                    save_respuesta(st.session_state.proceso_id, pid, texto=respuesta.strip())
                _avanzar_reflexion(idx)


def _avanzar_reflexion(idx: int):
    if idx + 1 < len(IDS_ABIERTAS):
        ir_a("reflexion", a_idx=idx + 1)
    else:
        ir_a("transicion")


# ─── Página: Transición ───────────────────────────────────────────────────────

def page_transicion():
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        placeholder = st.empty()
        mensajes = [
            ("🪞", "El espejo está tomando forma..."),
            ("💫", "Leyendo los patrones de tus respuestas..."),
            ("🌿", "Preparando tu reporte personalizado..."),
        ]
        for icono, msg in mensajes:
            placeholder.markdown(f"""
<div style="text-align:center;padding:80px 20px;">
  <div style="font-size:52px;margin-bottom:24px;">{icono}</div>
  <p style="color:#c9859a;font-size:18px;font-style:italic;">{msg}</p>
</div>""", unsafe_allow_html=True)
            time.sleep(1.2)
        placeholder.empty()

        with st.spinner("Generando tu análisis..."):
            from core.scoring import calcular_puntajes, determinar_heridas
            from core.report import generar_analisis, generar_grafico, generar_pdf
            from core.database import completar_fase1
            from core.email_service import enviar_reporte
            from core.config import BASE_URL

            respuestas = st.session_state.respuestas
            scores = calcular_puntajes(respuestas)
            herida_prim, herida_sec, co_dom = determinar_heridas(scores)
            intensidad, _ = get_intensidad(scores[herida_prim])

            analisis = generar_analisis(
                st.session_state.nombre, scores,
                herida_prim, herida_sec, intensidad, respuestas, co_dom)

            grafico = generar_grafico(scores, herida_prim, herida_sec)
            pdf = generar_pdf(
                st.session_state.nombre, scores, herida_prim, herida_sec,
                intensidad, analisis, grafico, respuestas)

            completar_fase1(st.session_state.proceso_id, herida_prim, herida_sec,
                            intensidad, scores, analisis)

            link = f"{BASE_URL}/?resultado={st.session_state.proceso_id}"
            try:
                enviar_reporte(st.session_state.nombre, st.session_state.correo, link, pdf)
            except Exception:
                pass

            st.session_state.analisis = analisis
            st.session_state.scores = scores
            st.session_state.herida_primaria = herida_prim
            st.session_state.herida_secundaria = herida_sec
            st.session_state.grafico = grafico
            st.session_state.pdf = pdf

        ir_a("resultado")


# ─── Página: Resultado ────────────────────────────────────────────────────────

def page_resultado(proceso=None, scores=None, analisis=None,
                   grafico=None, pdf=None, respuestas=None, evaluadores_data=None):
    if scores is None:
        scores   = st.session_state.scores
        analisis = st.session_state.analisis
        grafico  = st.session_state.grafico
        pdf      = st.session_state.pdf
        respuestas = st.session_state.respuestas

    if proceso is None:
        from core.database import get_proceso
        proceso = get_proceso(st.session_state.proceso_id)

    nombre = proceso["nombre"] if proceso else st.session_state.nombre
    herida_prim = proceso["herida_primaria"] if proceso else st.session_state.herida_primaria
    herida_sec  = proceso["herida_secundaria"] if proceso else st.session_state.herida_secundaria
    intensidad  = proceso["intensidad_primaria"] if proceso else ""

    if not scores or not analisis:
        st.error("No se encontró el reporte.")
        return

    h_info = HERIDAS_INFO[herida_prim]
    _, intensidad_desc = get_intensidad(scores[herida_prim])

    st.markdown(f"""
<div style="text-align:center;padding:24px 0 16px;">
  <div style="font-size:44px;margin-bottom:12px;">🪞</div>
  <h1 style="font-size:26px;margin-bottom:8px;">El Espejo de tus Relaciones</h1>
  <p style="color:#7d6690;font-size:14px;">Reporte de {nombre}</p>
  <p style="color:#c9859a;font-size:13px;font-style:italic;margin:8px 0 0;">
    "Este espejo es tuyo. Lo que ves en él es el punto de partida, no el destino."
  </p>
</div>
""", unsafe_allow_html=True)

    st.divider()

    st.markdown("<h2 style='font-size:18px;'>🗺️ Mapa de tus Heridas</h2>", unsafe_allow_html=True)
    st.image(grafico, use_container_width=True)

    st.divider()

    st.markdown("<h2 style='font-size:18px;'>💔 Tu Herida Principal</h2>", unsafe_allow_html=True)

    box(f"""
<p style="margin:0 0 8px;">{herida_badge(herida_prim, scores[herida_prim])}</p>
<p style="color:#c9859a;font-size:12px;text-transform:uppercase;letter-spacing:1px;margin:8px 0 4px;">
  Intensidad: {intensidad.upper()}
</p>
<p style="color:#b899c8;font-size:13px;font-style:italic;margin:0 0 14px;">{intensidad_desc}</p>
<p style="color:#f5eef8;font-size:14px;font-style:italic;margin:0;">
  &ldquo;{h_info['mensaje']}&rdquo;
</p>
""", h_info["color"])

    descripcion = analisis.get("herida_primaria", {}).get("descripcion", "")
    if descripcion:
        st.markdown(f'<p style="color:#b899c8;font-size:14px;line-height:1.8;">{descripcion}</p>',
                    unsafe_allow_html=True)

    manifestaciones = analisis.get("herida_primaria", {}).get("manifestaciones", [])
    if manifestaciones:
        st.markdown("<p style='color:#c9859a;font-size:13px;margin-bottom:6px;'>Cómo se manifiesta en tus relaciones:</p>",
                    unsafe_allow_html=True)
        for m in manifestaciones:
            st.markdown(f'<p style="color:#b899c8;font-size:13px;padding-left:16px;'
                        f'border-left:2px solid #2d2040;margin-bottom:6px;">· {m}</p>',
                        unsafe_allow_html=True)

    msg_personal = analisis.get("herida_primaria", {}).get("mensaje_personal", "")
    if msg_personal:
        box(f'<p style="color:#f5eef8;font-size:14px;line-height:1.8;margin:0;">{msg_personal}</p>',
            "#c9859a")

    que_protege = analisis.get("herida_primaria", {}).get("que_protege", "")
    if que_protege:
        st.markdown(f'<p style="color:#7d6690;font-size:13px;font-style:italic;'
                    f'padding-left:16px;border-left:2px solid #2d2040;">'
                    f'Lo que protegió: {que_protege}</p>',
                    unsafe_allow_html=True)

    st.divider()

    h_sec_info = HERIDAS_INFO[herida_sec]
    st.markdown("<h2 style='font-size:18px;'>🔮 Herida Secundaria</h2>", unsafe_allow_html=True)
    box(f"""
<p style="margin:0 0 10px;">{herida_badge(herida_sec, scores[herida_sec])}</p>
<p style="color:#b899c8;font-size:13px;line-height:1.7;margin:0 0 8px;">
  {analisis.get('herida_secundaria', {}).get('descripcion_breve', '')}
</p>
<p style="color:#7d6690;font-size:13px;font-style:italic;margin:0;">
  {analisis.get('herida_secundaria', {}).get('relacion', '')}
</p>
""")

    st.divider()

    orientacion = analisis.get("orientacion", {})
    st.markdown("<h2 style='font-size:18px;'>🌿 Orientación de Sanación</h2>", unsafe_allow_html=True)
    for key in ["parrafo1", "parrafo2", "parrafo3"]:
        p = orientacion.get(key, "")
        if p:
            st.markdown(f'<p style="color:#b899c8;font-size:14px;line-height:1.8;margin-bottom:12px;">{p}</p>',
                        unsafe_allow_html=True)
    primer_paso = orientacion.get("primer_paso", "")
    if primer_paso:
        box(f'<p style="color:#c9859a;font-size:14px;font-weight:bold;margin:0 0 4px;">Un primer paso:</p>'
            f'<p style="color:#f5eef8;font-size:14px;margin:0;">{primer_paso}</p>', "#c9859a")

    abiertas_resp = [(pid, respuestas.get(pid)) for pid in IDS_ABIERTAS
                     if respuestas.get(pid) and str(respuestas.get(pid)).strip()]
    if abiertas_resp:
        st.divider()
        st.markdown("<h2 style='font-size:18px;'>🪞 Lo que ya sabías</h2>", unsafe_allow_html=True)
        sintesis = analisis.get("sintesis_reflexiones", "")
        if sintesis:
            st.markdown(f'<p style="color:#b899c8;font-size:14px;line-height:1.8;margin-bottom:16px;">{sintesis}</p>',
                        unsafe_allow_html=True)
        from core.questions import PREGUNTAS_ABIERTAS as PA
        for pid, texto in abiertas_resp:
            st.markdown(
                f'<p style="color:#7d6690;font-size:13px;font-style:italic;margin-bottom:4px;">{PA[pid]}</p>'
                f'<p style="color:#f5eef8;font-size:14px;margin-bottom:16px;padding-left:16px;'
                f'border-left:2px solid #2d2040;">{texto}</p>',
                unsafe_allow_html=True)

    if evaluadores_data and evaluadores_data.get("completados", 0) >= 3:
        _mostrar_espejo_externo(evaluadores_data)

    st.divider()

    st.markdown("""
<div style="text-align:center;padding:20px 0 10px;">
  <p style="color:#c9859a;font-size:15px;font-style:italic;margin-bottom:16px;">
    "Este diagnóstico es el primer paso.<br>Si quieres acompañamiento para sanar esta herida,<br>
    puedo caminar contigo. — Juan Pablo"
  </p>
</div>
""", unsafe_allow_html=True)

    from core.config import AGENDA_URL
    st.link_button("Agendar una conversación con Juan Pablo", AGENDA_URL)

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if pdf:
            st.download_button(
                label="⬇️ Descargar reporte PDF",
                data=pdf,
                file_name=f"espejo_relaciones_{nombre.lower().replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
    with col2:
        if proceso and proceso.get("estado") in ("fase1_completa",) and not proceso.get("fase2_activada"):
            if st.button("✨ Activar el Espejo Externo", use_container_width=True):
                ir_a("espejo_form")
        elif proceso and proceso.get("fase2_activada"):
            from core.database import get_evaluadores
            evals = get_evaluadores(proceso["id"])
            completados = sum(1 for e in evals if e["estado"] == "completado")
            total_inv   = len(evals)
            st.markdown(
                f'<p style="color:#7d6690;font-size:13px;text-align:center;">'
                f'Espejo externo: {completados}/{total_inv} personas han respondido</p>',
                unsafe_allow_html=True)
            if completados < 3:
                st.info("Cuando 3 o más personas respondan, el espejo externo se integrará al reporte.")


def _mostrar_espejo_externo(evaluadores_data: dict):
    st.divider()
    st.markdown("<h2 style='font-size:18px;'>👁️ El Espejo Externo</h2>", unsafe_allow_html=True)
    st.markdown(
        f'<p style="color:#7d6690;font-size:13px;margin-bottom:16px;">'
        f'Perspectiva de {evaluadores_data["completados"]} personas cercanas.</p>',
        unsafe_allow_html=True)

    divergencias = evaluadores_data.get("divergencias", [])
    if divergencias:
        for d in divergencias:
            h_nom = HERIDAS_INFO[d["herida"]]["nombre"]
            color = HERIDAS_INFO[d["herida"]]["color"]
            if d["tipo"] == "no_reconocida":
                msg = (f"Quienes te conocen perciben la herida de <b>{h_nom}</b> con más "
                       f"intensidad de lo que tú reconoces.")
            else:
                msg = (f"Percibes la herida de <b>{h_nom}</b> con más intensidad "
                       f"de lo que ven quienes te rodean.")
            box(f'<p style="color:{color};font-size:13px;margin:0 0 4px;">{h_nom}</p>'
                f'<p style="color:#b899c8;font-size:13px;margin:0;">{msg}</p>', color)

    citas = evaluadores_data.get("citas_abiertas", [])
    if citas:
        st.markdown("<p style='color:#c9859a;font-size:13px;margin-bottom:8px;'>Lo que sienten cerca de ti:</p>",
                    unsafe_allow_html=True)
        for cita in citas:
            st.markdown(
                f'<p style="color:#b899c8;font-size:14px;font-style:italic;'
                f'padding:12px 16px;border-left:3px solid #c9859a;margin-bottom:10px;">'
                f'"{cita}"</p>',
                unsafe_allow_html=True)


# ─── Resultado desde DB (link permanente) ────────────────────────────────────

def page_resultado_from_db(proceso_id: str):
    if not re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
                        proceso_id.lower()):
        st.error("Enlace inválido.")
        return

    from core.database import get_proceso, get_respuestas, get_respuestas_externas, get_evaluadores
    from core.scoring import calcular_puntajes, calcular_promedios_externos, detectar_divergencias
    from core.report import generar_grafico, generar_pdf

    proceso = get_proceso(proceso_id)
    if not proceso or proceso["estado"] == "fase1_pendiente":
        st.error("Reporte no disponible.")
        return

    respuestas = get_respuestas(proceso_id)
    scores     = json.loads(proceso["puntajes"]) if proceso.get("puntajes") else calcular_puntajes(respuestas)
    analisis   = json.loads(proceso["analisis"]) if proceso.get("analisis") else {}

    scores = {k: int(v) for k, v in scores.items()}

    herida_prim = proceso["herida_primaria"]
    herida_sec  = proceso["herida_secundaria"]
    grafico = generar_grafico(scores, herida_prim, herida_sec)

    evaluadores_data = None
    if proceso.get("fase2_activada"):
        evals = get_evaluadores(proceso_id)
        completados = sum(1 for e in evals if e["estado"] == "completado")
        resp_ext = get_respuestas_externas(proceso_id)
        if completados >= 3:
            promedios = calcular_promedios_externos(resp_ext)
            divergencias = detectar_divergencias(scores, promedios)
            citas = [r["texto_respuesta"] for r in resp_ext
                     if r["pregunta_id"] in (206, 207) and r.get("texto_respuesta")]
            evaluadores_data = {
                "completados": completados,
                "divergencias": divergencias,
                "citas_abiertas": citas,
            }

    pdf = generar_pdf(proceso["nombre"], scores, herida_prim, herida_sec,
                      proceso.get("intensidad_primaria", ""), analisis, grafico,
                      respuestas, evaluadores_data)

    st.session_state.proceso_id = proceso_id
    st.session_state.respuestas = respuestas
    page_resultado(proceso=proceso, scores=scores, analisis=analisis,
                   grafico=grafico, pdf=pdf, respuestas=respuestas,
                   evaluadores_data=evaluadores_data)


# ─── Activar Espejo Externo ────────────────────────────────────────────────────

def page_espejo_form():
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown("""
<div style="text-align:center;padding:16px 0 24px;">
  <h2 style="font-size:22px;">El Espejo Externo</h2>
  <p style="color:#7d6690;font-size:13px;font-style:italic;">
    Invita a entre 3 y 5 personas cercanas a responderte de forma anónima
  </p>
</div>
""", unsafe_allow_html=True)

        box("""
<p style="color:#b899c8;font-size:14px;line-height:1.7;margin-bottom:10px;">
  Las personas que invites recibirán un link único y anónimo. Responderán 7 preguntas
  sobre cómo te perciben — sin saber qué respondiste tú, sin atribución individual.
</p>
<p style="color:#b899c8;font-size:14px;line-height:1.7;margin:0;">
  Tu reporte se enriquecerá automáticamente cuando 3 o más personas respondan.
</p>
""", "#3d2040")

        proceso_correo = st.session_state.correo

        evaluadores = []
        for i in range(5):
            st.markdown(f"<p style='color:#c9859a;font-size:14px;margin:12px 0 4px;'>"
                        f"Persona {i+1} {'(requerida)' if i < 3 else '(opcional)'}</p>",
                        unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                nom = st.text_input("Nombre", key=f"ev_nom_{i}", placeholder="Su nombre")
            with c2:
                cor = st.text_input("Correo", key=f"ev_cor_{i}", placeholder="su@correo.com")
            evaluadores.append({"nombre": nom.strip(), "correo": cor.strip().lower()})

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Volver al reporte"):
                ir_a("resultado")
        with c2:
            if st.button("Enviar invitaciones →"):
                requeridos = evaluadores[:3]
                if any(not e["nombre"] or not e["correo"] or "@" not in e["correo"]
                       for e in requeridos):
                    st.error("Completa los datos de al menos 3 personas (nombre y correo válido).")
                    return

                validos = [e for e in evaluadores
                           if e["nombre"] and e["correo"] and "@" in e["correo"]]

                correos_usados = {proceso_correo}
                correos_vistos = set()
                hay_duplicado  = False
                for e in validos:
                    if e["correo"] in correos_usados or e["correo"] in correos_vistos:
                        st.error(f"Correo duplicado o igual al tuyo: {e['correo']}")
                        hay_duplicado = True
                        break
                    correos_vistos.add(e["correo"])
                if hay_duplicado:
                    return

                from core.database import create_evaluador, activar_fase2
                from core.email_service import enviar_invitacion_evaluador
                from core.config import BASE_URL

                activar_fase2(st.session_state.proceso_id)
                for e in validos:
                    ev = create_evaluador(st.session_state.proceso_id, e["nombre"], e["correo"])
                    try:
                        enviar_invitacion_evaluador(
                            st.session_state.nombre, e["nombre"], e["correo"],
                            ev["token"], BASE_URL)
                    except Exception:
                        pass

                ir_a("espejo_confirmado", n_invitados=len(validos))


# ─── Confirmación espejo ──────────────────────────────────────────────────────

def page_espejo_confirmado():
    n = st.session_state.get("n_invitados", 3)
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown(f"""
<div style="text-align:center;padding:60px 20px;">
  <div style="font-size:44px;margin-bottom:24px;">✉️</div>
  <h2 style="font-size:22px;">Invitaciones enviadas</h2>
  <p style="color:#b899c8;font-size:15px;line-height:1.8;max-width:420px;margin:16px auto 32px;">
    {n} personas recibieron tu invitación.<br>
    Cuando 3 o más respondan, tu reporte se enriquecerá automáticamente.
  </p>
</div>
""", unsafe_allow_html=True)
        if st.button("Ver mi reporte →"):
            ir_a("resultado")


# ─── Evaluador externo ────────────────────────────────────────────────────────

def page_evaluador(token: str):
    if not re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
                        token.lower()):
        st.error("Enlace inválido.")
        return

    from core.database import get_evaluador_by_token, get_proceso, save_respuesta_externa, completar_evaluador

    evaluador = get_evaluador_by_token(token)
    if not evaluador:
        st.error("Este enlace no es válido.")
        return

    if evaluador["estado"] == "completado":
        st.markdown("""
<div style="text-align:center;padding:80px 20px;">
  <div style="font-size:44px;margin-bottom:20px;">✅</div>
  <h2>Ya respondiste</h2>
  <p style="color:#b899c8;">Gracias por tu tiempo. Ya registramos tu respuesta anteriormente.</p>
</div>""", unsafe_allow_html=True)
        return

    proceso = get_proceso(evaluador["proceso_id"])
    if not proceso:
        st.error("Proceso no encontrado.")
        return

    nombre_eval = proceso["nombre"]

    st.markdown(f"""
<div style="text-align:center;padding:32px 0 24px;">
  <div style="font-size:44px;margin-bottom:16px;">🪞</div>
  <h1 style="font-size:24px;margin-bottom:8px;">El Espejo de tus Relaciones</h1>
  <p style="color:#b899c8;font-size:15px;line-height:1.8;max-width:500px;margin:0 auto;">
    <strong style="color:#f5eef8;">{nombre_eval}</strong> te ha pedido que le ayudes
    a conocerse mejor. Tus respuestas serán completamente anónimas.<br>
    Son solo 7 preguntas — toma menos de 3 minutos.
  </p>
</div>
""", unsafe_allow_html=True)

    st.divider()

    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        key_prefix = f"ext_{token[:8]}"
        respuestas_ext = {}

        for pid in IDS_EXTERNAS_ESCALA:
            pinfo = PREGUNTAS_EXTERNAS_ESCALA[pid]
            texto = pinfo["texto"].replace("[nombre]", nombre_eval)
            st.markdown(
                f'<p style="color:#f5eef8;font-size:15px;line-height:1.7;'
                f'text-align:center;margin:20px 0 12px;">{texto}</p>',
                unsafe_allow_html=True)
            st.markdown(
                f'<p style="color:#7d6690;font-size:12px;text-align:center;margin-bottom:12px;">'
                f'1 = {pinfo["escala_min"]} &nbsp;·&nbsp; 5 = {pinfo["escala_max"]}</p>',
                unsafe_allow_html=True)
            val = st.radio(
                texto,
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: str(x),
                key=f"{key_prefix}_e{pid}",
                horizontal=True,
                label_visibility="collapsed",
            )
            respuestas_ext[pid] = val
            st.markdown("<br>", unsafe_allow_html=True)

        for pid in IDS_EXTERNAS_ABIERTAS:
            texto = PREGUNTAS_EXTERNAS_ABIERTAS[pid].replace("[nombre]", nombre_eval)
            st.markdown(
                f'<p style="color:#c9859a;font-size:14px;font-style:italic;'
                f'text-align:center;margin:16px 0 8px;">Pregunta abierta (opcional)</p>',
                unsafe_allow_html=True)
            st.markdown(
                f'<p style="color:#f5eef8;font-size:15px;text-align:center;margin:0 0 12px;">{texto}</p>',
                unsafe_allow_html=True)
            resp = st.text_area("Tu respuesta:", key=f"{key_prefix}_a{pid}",
                                height=80, placeholder="Escribe libremente...",
                                label_visibility="collapsed")
            respuestas_ext[pid] = resp.strip() if resp.strip() else None

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Enviar mi respuesta →"):
            ev_id = evaluador["id"]
            for pid in IDS_EXTERNAS_ESCALA:
                save_respuesta_externa(ev_id, pid, valor_escala=respuestas_ext[pid])
            for pid in IDS_EXTERNAS_ABIERTAS:
                if respuestas_ext.get(pid):
                    save_respuesta_externa(ev_id, pid, texto=respuestas_ext[pid])
            completar_evaluador(ev_id)
            ir_a("gracias_evaluador")


def page_gracias_evaluador():
    st.markdown("""
<div style="text-align:center;padding:80px 20px;">
  <div style="font-size:52px;margin-bottom:24px;">🙏</div>
  <h2 style="font-size:24px;">Gracias por tu honestidad</h2>
  <p style="color:#b899c8;font-size:15px;line-height:1.8;max-width:460px;margin:16px auto;">
    Tu respuesta fue registrada y se integrará de forma anónima al reporte.<br>
    Este pequeño acto de honestidad puede ser un regalo enorme.
  </p>
  <p style="color:#7d6690;font-size:13px;font-style:italic;margin-top:24px;">
    "El espejo solo muestra lo que ya estaba ahí."
  </p>
</div>
""", unsafe_allow_html=True)


# ─── Router ───────────────────────────────────────────────────────────────────

def main():
    init_state()

    token     = st.query_params.get("token")
    resultado = st.query_params.get("resultado")

    if token:
        if st.session_state.etapa == "gracias_evaluador":
            page_gracias_evaluador()
        else:
            page_evaluador(token)
        return

    if resultado:
        page_resultado_from_db(resultado)
        return

    etapa = st.session_state.etapa

    if etapa == "inicio":
        page_inicio()
    elif etapa == "instrucciones":
        page_instrucciones()
    elif etapa == "cuestionario":
        page_cuestionario()
    elif etapa == "reflexion":
        page_reflexion()
    elif etapa == "transicion":
        page_transicion()
    elif etapa == "resultado":
        page_resultado()
    elif etapa == "espejo_form":
        page_espejo_form()
    elif etapa == "espejo_confirmado":
        page_espejo_confirmado()
    elif etapa == "gracias_evaluador":
        page_gracias_evaluador()
    else:
        ir_a("inicio")


if __name__ == "__main__":
    main()
