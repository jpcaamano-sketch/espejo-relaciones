import io
import re
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                 HRFlowable, Table, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from core.questions import (HERIDAS, HERIDAS_INFO, PREGUNTAS_ABIERTAS,
                             get_intensidad, IDS_ABIERTAS)

_gemini = None


def _get_gemini():
    global _gemini
    if _gemini is None:
        from google import genai
        from core.config import GOOGLE_API_KEY
        _gemini = genai.Client(api_key=GOOGLE_API_KEY)
    return _gemini


def _sanitize_json(text: str) -> str:
    result = []
    in_string = False
    escape_next = False
    for ch in text:
        if escape_next:
            result.append(ch); escape_next = False
        elif ch == '\\' and in_string:
            result.append(ch); escape_next = True
        elif ch == '"':
            in_string = not in_string; result.append(ch)
        elif in_string and ord(ch) < 0x20:
            if ch == '\n': result.append('\\n')
            elif ch == '\r': result.append('\\r')
            elif ch == '\t': result.append('\\t')
        else:
            result.append(ch)
    return ''.join(result)


# ─── Gemini ───────────────────────────────────────────────────────────────────

def generar_analisis(nombre: str, scores: dict, herida_primaria: str,
                     herida_secundaria: str, intensidad: str,
                     respuestas: dict, co_dominante: bool) -> dict:
    h_prim = HERIDAS_INFO[herida_primaria]
    h_sec  = HERIDAS_INFO[herida_secundaria]

    reflexiones = []
    for pid in IDS_ABIERTAS:
        texto = respuestas.get(pid)
        if texto and str(texto).strip():
            reflexiones.append(f"- {PREGUNTAS_ABIERTAS[pid]}\n  {texto}")

    scores_texto = "\n".join(
        f"- {HERIDAS_INFO[h]['nombre']}: {s} pts (rango 4-20)"
        for h, s in sorted(scores.items(), key=lambda x: x[1], reverse=True)
    )

    co_nota = "Las dos primeras heridas tienen puntajes muy similares — ambas deben considerarse como primarias." if co_dominante else ""

    prompt = f"""Eres un guía experto en heridas emocionales, integrando los marcos de Lise Bourbeau y Alejandro Jodorowsky.
Genera el reporte personalizado de {nombre} basándote en su diagnóstico de heridas emocionales.

RESULTADO DEL DIAGNÓSTICO:
- Herida primaria: {h_prim['nombre']} (puntaje: {scores[herida_primaria]}/20, intensidad: {intensidad})
- Herida secundaria: {h_sec['nombre']} (puntaje: {scores[herida_secundaria]}/20)
{co_nota}

TODOS LOS PUNTAJES:
{scores_texto}

REFLEXIONES DE {nombre}:
{chr(10).join(reflexiones) if reflexiones else "No compartió reflexiones abiertas."}

Genera el reporte en JSON con este formato exacto:
{{
  "herida_primaria": {{
    "descripcion": "Párrafo de 4-5 líneas sobre qué es esta herida, cómo se origina en la infancia y qué función tuvo en su momento. Hablar de la herida, no de {nombre}.",
    "manifestaciones": [
      "Patrón específico de comportamiento en relaciones (una línea)",
      "Segundo patrón",
      "Tercer patrón"
    ],
    "mensaje_personal": "Párrafo en segunda persona, cálido, sin juicio. Dirigido a {nombre} directamente. Nombra lo que ve sin juzgarlo. Que sienta que alguien lo/la comprende.",
    "que_protege": "Una o dos frases sobre la función positiva que tuvo esta herida — lo que protegió en su origen."
  }},
  "orientacion": {{
    "parrafo1": "Primer párrafo de orientación de sanación para la herida {h_prim['nombre']}.",
    "parrafo2": "Segundo párrafo — más práctico, más concreto.",
    "parrafo3": "Tercer párrafo — de cierre, con apertura al futuro.",
    "primer_paso": "Un primer paso concreto y accesible. Una frase o dos máximo."
  }},
  "herida_secundaria": {{
    "descripcion_breve": "3-4 líneas describiendo cómo esta herida secundaria se manifiesta.",
    "relacion": "Cómo se relaciona e interactúa con la herida primaria — en 2-3 líneas."
  }},
  "sintesis_reflexiones": "Si hay reflexiones abiertas: un párrafo que las integre como espejo propio — qué patrones revelan, qué tiene sentido ahora. Si no hay reflexiones: una frase de invitación a la reflexión."
}}

Reglas:
- Solo texto plano, sin asteriscos, sin markdown
- Lenguaje cálido, cercano, no clínico
- Segunda persona para el mensaje_personal
- Tercera persona o general para el resto
- Nunca usar lenguaje determinista — siempre apertura y posibilidad
- Responde SOLO el JSON, sin texto adicional"""

    response = _get_gemini().models.generate_content(model="gemini-2.5-flash", contents=prompt)
    texto = response.text.strip()
    texto = re.sub(r"^```json\s*", "", texto)
    texto = re.sub(r"\s*```$", "", texto)
    texto = _sanitize_json(texto)
    return json.loads(texto)


# ─── Gráfico ──────────────────────────────────────────────────────────────────

def generar_grafico(scores: dict, herida_primaria: str, herida_secundaria: str) -> bytes:
    sorted_h = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    nombres  = [HERIDAS_INFO[h]["nombre"] for h, _ in sorted_h]
    valores  = [s for _, s in sorted_h]
    herida_ids = [h for h, _ in sorted_h]

    def bar_color(h):
        if h == herida_primaria:
            return HERIDAS_INFO[h]["color"]
        if h == herida_secundaria:
            return "#8b68c4"
        return "#2d2040"

    colores = [bar_color(h) for h in herida_ids]

    fig, ax = plt.subplots(figsize=(10, 4.5))
    fig.patch.set_facecolor("#0d0a1a")
    ax.set_facecolor("#0d0a1a")

    bars = ax.barh(nombres, valores, color=colores, height=0.55, zorder=3)

    for bar, val in zip(bars, valores):
        if val > 0:
            ax.text(val + 0.3, bar.get_y() + bar.get_height() / 2,
                    str(val), va="center", ha="left",
                    color="#f5eef8", fontsize=9, fontweight="bold")

    ax.set_xlim(0, 22)
    ax.set_xticks([4, 8, 12, 16, 20])
    ax.set_xticklabels(["4", "8", "12", "16", "20"], color="#7d6690", fontsize=8)
    ax.tick_params(axis="y", colors="#c4adcc", labelsize=9)
    ax.spines[:].set_visible(False)
    ax.grid(axis="x", color="#1c1535", linewidth=0.8, zorder=0)
    ax.set_title("Mapa de tus Heridas Emocionales", color="#c9859a", fontsize=11,
                 fontweight="bold", pad=12)

    import matplotlib.patches as mpatches
    p = mpatches.Patch(color=HERIDAS_INFO[herida_primaria]["color"], label="Herida primaria")
    s = mpatches.Patch(color="#8b68c4", label="Herida secundaria")
    o = mpatches.Patch(color="#2d2040", label="Otras heridas")
    ax.legend(handles=[p, s, o], loc="lower right", framealpha=0,
              labelcolor="#c4adcc", fontsize=8)

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight", facecolor="#0d0a1a")
    buf.seek(0)
    img_bytes = buf.read()
    plt.close()
    return img_bytes


# ─── PDF ─────────────────────────────────────────────────────────────────────

def generar_pdf(nombre: str, scores: dict, herida_primaria: str, herida_secundaria: str,
                intensidad: str, analisis: dict, grafico_bytes: bytes,
                respuestas: dict, evaluadores_data: dict | None = None) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    rose   = colors.HexColor("#c9859a")
    violet = colors.HexColor("#8b68c4")
    oscuro = colors.HexColor("#150e2a")
    gris   = colors.HexColor("#555555")
    muted  = colors.HexColor("#7d6690")

    s_titulo  = ParagraphStyle("titulo", parent=styles["Heading1"],
                               textColor=rose, fontSize=22, spaceAfter=4,
                               alignment=TA_CENTER, fontName="Helvetica-Bold")
    s_sub     = ParagraphStyle("sub", parent=styles["Normal"],
                               textColor=muted, fontSize=11, spaceAfter=16,
                               alignment=TA_CENTER)
    s_frase   = ParagraphStyle("frase", parent=styles["Normal"],
                               textColor=rose, fontSize=11, spaceAfter=8,
                               alignment=TA_CENTER, fontName="Helvetica-Oblique")
    s_h2      = ParagraphStyle("h2", parent=styles["Heading2"],
                               textColor=rose, fontSize=13,
                               spaceBefore=18, spaceAfter=8,
                               fontName="Helvetica-Bold")
    s_h3      = ParagraphStyle("h3", parent=styles["Heading3"],
                               textColor=violet, fontSize=11,
                               spaceBefore=12, spaceAfter=6,
                               fontName="Helvetica-Bold")
    s_body    = ParagraphStyle("body", parent=styles["Normal"],
                               fontSize=10, leading=16, spaceAfter=10,
                               textColor=colors.HexColor("#2d2040"),
                               alignment=TA_JUSTIFY)
    s_cita    = ParagraphStyle("cita", parent=styles["Normal"],
                               fontSize=10, leading=16, spaceAfter=10,
                               textColor=colors.HexColor("#2d2040"),
                               leftIndent=20, fontName="Helvetica-Oblique")
    s_label   = ParagraphStyle("label", parent=styles["Normal"],
                               fontSize=9, textColor=muted, spaceAfter=2)

    story = []
    from datetime import date

    story.append(Paragraph("El Espejo de tus Relaciones", s_titulo))
    story.append(Paragraph(f"Reporte de {nombre}  ·  {date.today().strftime('%d/%m/%Y')}", s_sub))
    story.append(Paragraph(
        "<i>Este espejo es tuyo. Lo que ves en él es el punto de partida, no el destino.</i>",
        s_frase))
    story.append(Spacer(1, 0.3*cm))

    graf_buf = io.BytesIO(grafico_bytes)
    img = Image(graf_buf, width=16*cm, height=7.5*cm)
    img.hAlign = "CENTER"
    story.append(img)
    story.append(Spacer(1, 0.3*cm))

    h_info = HERIDAS_INFO[herida_primaria]
    _, intensidad_desc = get_intensidad(scores[herida_primaria])
    story.append(HRFlowable(width="100%", thickness=0.5, color=rose, spaceAfter=8))
    story.append(Paragraph(f"Tu Herida Principal: {h_info['nombre']} {h_info['icono']}", s_h2))
    story.append(Paragraph(f"<b>Intensidad:</b> {intensidad.upper()} — {intensidad_desc}", s_body))
    story.append(Paragraph(analisis.get("herida_primaria", {}).get("descripcion", ""), s_body))

    manifestaciones = analisis.get("herida_primaria", {}).get("manifestaciones", [])
    if manifestaciones:
        story.append(Paragraph("<b>Cómo se manifiesta en tus relaciones:</b>", s_body))
        for m in manifestaciones:
            story.append(Paragraph(f"• {m}", s_body))

    story.append(Paragraph(f"<i>\"{h_info['mensaje']}\"</i>", s_cita))

    msg_personal = analisis.get("herida_primaria", {}).get("mensaje_personal", "")
    if msg_personal:
        story.append(Paragraph(msg_personal, s_body))

    que_protege = analisis.get("herida_primaria", {}).get("que_protege", "")
    if que_protege:
        story.append(Paragraph(f"<b>Lo que esta herida protegió:</b> {que_protege}", s_body))

    h_sec = HERIDAS_INFO[herida_secundaria]
    story.append(HRFlowable(width="100%", thickness=0.5, color=violet, spaceAfter=8))
    story.append(Paragraph(f"Herida Secundaria: {h_sec['nombre']} {h_sec['icono']}", s_h3))
    story.append(Paragraph(
        analisis.get("herida_secundaria", {}).get("descripcion_breve", ""), s_body))
    relacion = analisis.get("herida_secundaria", {}).get("relacion", "")
    if relacion:
        story.append(Paragraph(f"<i>{relacion}</i>", s_cita))

    story.append(HRFlowable(width="100%", thickness=0.5, color=rose, spaceAfter=8))
    story.append(Paragraph("Tu Orientación de Sanación", s_h2))
    orientacion = analisis.get("orientacion", {})
    for key in ["parrafo1", "parrafo2", "parrafo3"]:
        p = orientacion.get(key, "")
        if p:
            story.append(Paragraph(p, s_body))
    primer_paso = orientacion.get("primer_paso", "")
    if primer_paso:
        story.append(Paragraph(f"<b>Un primer paso:</b> {primer_paso}", s_body))

    reflexiones_texto = analisis.get("sintesis_reflexiones", "")
    abiertas_respondidas = [(pid, respuestas[pid]) for pid in IDS_ABIERTAS
                            if pid in respuestas and str(respuestas[pid]).strip()]
    if abiertas_respondidas:
        story.append(HRFlowable(width="100%", thickness=0.5, color=rose, spaceAfter=8))
        story.append(Paragraph("Lo que ya sabías", s_h2))
        if reflexiones_texto:
            story.append(Paragraph(reflexiones_texto, s_body))
        for pid, texto in abiertas_respondidas:
            story.append(Paragraph(f"<i>{PREGUNTAS_ABIERTAS[pid]}</i>", s_label))
            story.append(Paragraph(str(texto), s_cita))

    if evaluadores_data and evaluadores_data.get("completados", 0) >= 3:
        story.append(HRFlowable(width="100%", thickness=0.5, color=violet, spaceAfter=8))
        story.append(Paragraph("El Espejo Externo", s_h2))
        story.append(Paragraph(
            f"Perspectiva de {evaluadores_data['completados']} personas cercanas.", s_body))

        divergencias = evaluadores_data.get("divergencias", [])
        for d in divergencias:
            h_nom = HERIDAS_INFO[d["herida"]]["nombre"]
            if d["tipo"] == "no_reconocida":
                story.append(Paragraph(
                    f"<b>{h_nom}:</b> quienes te conocen perciben esta herida con más intensidad "
                    f"de lo que tú reconoces (externo: {d['score_externo']}/5 vs. tu {d['score_auto_norm']}/5).",
                    s_body))
            else:
                story.append(Paragraph(
                    f"<b>{h_nom}:</b> la percibes con más intensidad de lo que ven quienes te rodean "
                    f"(tú: {d['score_auto_norm']}/5 vs. externo: {d['score_externo']}/5).",
                    s_body))

        citas = evaluadores_data.get("citas_abiertas", [])
        if citas:
            story.append(Paragraph("<b>Lo que sienten cerca de ti:</b>", s_body))
            for cita in citas:
                story.append(Paragraph(f'"{cita}"', s_cita))

    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(
        "<i>Este diagnóstico es el primer paso. Si quieres acompañamiento para sanar esta herida, "
        "puedo caminar contigo. — Juan Pablo</i>",
        s_frase))

    doc.build(story)
    buf.seek(0)
    return buf.read()
