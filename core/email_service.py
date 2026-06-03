import resend
from core.config import RESEND_API_KEY, FROM_EMAIL


def _send(params: dict):
    resend.api_key = RESEND_API_KEY
    return resend.Emails.send(params)


def enviar_invitacion_evaluador(nombre_evaluado: str, nombre_evaluador: str,
                                correo_evaluador: str, token: str, base_url: str):
    link = f"{base_url}/?token={token}"
    params = {
        "from": FROM_EMAIL,
        "to": [correo_evaluador],
        "subject": f"{nombre_evaluado} te pide un regalo — responder toma 3 minutos",
        "html": f"""
<div style="font-family:Georgia,serif;max-width:560px;margin:0 auto;padding:32px 24px;
            background:#faf8f4;border-radius:12px;">
  <h2 style="color:#c9859a;margin-bottom:16px;">El Espejo de tus Relaciones</h2>
  <p style="color:#444;line-height:1.8;margin-bottom:16px;">
    Hola {nombre_evaluador},
  </p>
  <p style="color:#444;line-height:1.8;margin-bottom:16px;">
    <strong>{nombre_evaluado}</strong> está haciendo un ejercicio de autoconocimiento
    y te pidió que lo/la ayudes — de forma anónima y honesta.
  </p>
  <p style="color:#444;line-height:1.8;margin-bottom:16px;">
    Solo son 7 preguntas breves. Tus respuestas serán completamente anónimas:
    {nombre_evaluado} nunca sabrá qué respondiste tú en particular.
  </p>
  <div style="text-align:center;margin:32px 0;">
    <a href="{link}" style="background:#c9859a;color:#fff;padding:14px 36px;
       border-radius:6px;font-weight:700;font-size:16px;text-decoration:none;">
      Responder ahora →
    </a>
  </div>
  <p style="color:#888;font-size:13px;text-align:center;">
    Este link es único para ti. Responder toma menos de 3 minutos.
  </p>
</div>
""",
    }
    return _send(params)


def enviar_reporte(nombre: str, correo: str, link: str, pdf_bytes: bytes):
    params = {
        "from": FROM_EMAIL,
        "to": [correo],
        "subject": f"Tu reporte — El Espejo de tus Relaciones, {nombre}",
        "html": f"""
<div style="font-family:Georgia,serif;max-width:560px;margin:0 auto;padding:32px 24px;
            background:#faf8f4;border-radius:12px;">
  <h2 style="color:#c9859a;margin-bottom:16px;">Tu reporte está listo, {nombre}</h2>
  <p style="color:#444;line-height:1.8;margin-bottom:16px;">
    Encontrarás tu reporte completo adjunto en PDF.
    También puedes acceder a él en línea en cualquier momento:
  </p>
  <div style="text-align:center;margin:32px 0;">
    <a href="{link}" style="background:#c9859a;color:#fff;padding:14px 36px;
       border-radius:6px;font-weight:700;font-size:16px;text-decoration:none;">
      Ver mi reporte →
    </a>
  </div>
  <p style="color:#888;font-size:13px;text-align:center;font-style:italic;">
    Este espejo es tuyo. Lo que ves en él es el punto de partida, no el destino.
  </p>
</div>
""",
        "attachments": [{
            "filename": f"espejo_relaciones_{nombre.lower().replace(' ', '_')}.pdf",
            "content": list(pdf_bytes),
        }],
    }
    return _send(params)
