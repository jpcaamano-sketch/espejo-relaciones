import os

def _get(key, default=""):
    return os.environ.get(key, default)

SUPABASE_URL   = _get("SUPABASE_URL")
SUPABASE_KEY   = _get("SUPABASE_KEY")
RESEND_API_KEY = _get("RESEND_API_KEY")
GOOGLE_API_KEY = _get("GOOGLE_API_KEY")
BASE_URL       = _get("BASE_URL", "http://localhost:8546")
FROM_EMAIL     = "El Espejo de tus Relaciones <noreply@escuelayocreo.cl>"
AGENDA_URL     = _get("AGENDA_URL", "https://jpecoachdevida.cl/agendar-sesion")
