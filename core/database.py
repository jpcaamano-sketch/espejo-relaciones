import json
import uuid
from datetime import datetime, timezone

_client = None


def _db():
    global _client
    if _client is None:
        from core.config import SUPABASE_URL, SUPABASE_KEY
        from supabase import create_client
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client


# ─── Procesos ─────────────────────────────────────────────────────────────────

def create_proceso(nombre: str, correo: str, orden_preguntas: list) -> dict:
    r = _db().table("espejo_procesos").insert({
        "nombre": nombre,
        "correo": correo,
        "orden_preguntas": json.dumps(orden_preguntas),
        "estado": "fase1_pendiente",
    }).execute()
    return r.data[0]


def get_proceso(proceso_id: str) -> dict | None:
    r = _db().table("espejo_procesos").select("*").eq("id", proceso_id).execute()
    return r.data[0] if r.data else None


def update_proceso(proceso_id: str, **kwargs):
    _db().table("espejo_procesos").update(kwargs).eq("id", proceso_id).execute()


def completar_fase1(proceso_id: str, herida_primaria: str, herida_secundaria: str,
                    intensidad: str, puntajes: dict, analisis: dict):
    now = datetime.now(timezone.utc).isoformat()
    update_proceso(
        proceso_id,
        estado="fase1_completa",
        herida_primaria=herida_primaria,
        herida_secundaria=herida_secundaria,
        intensidad_primaria=intensidad,
        puntajes=json.dumps(puntajes),
        analisis=json.dumps(analisis),
        fecha_completado=now,
    )


def activar_fase2(proceso_id: str):
    update_proceso(proceso_id, estado="fase2_activa", fase2_activada=True)


def get_all_procesos() -> list:
    r = _db().table("espejo_procesos").select("*").order("fecha_creacion", desc=True).execute()
    return r.data


# ─── Respuestas propias ───────────────────────────────────────────────────────

def save_respuesta(proceso_id: str, pregunta_id: int, valor_escala=None, texto=None):
    row = {"proceso_id": proceso_id, "pregunta_id": pregunta_id}
    if valor_escala is not None:
        row["valor_escala"] = int(valor_escala)
    if texto:
        row["texto_respuesta"] = str(texto)
    _db().table("espejo_respuestas").upsert(
        row, on_conflict="proceso_id,pregunta_id"
    ).execute()


def get_respuestas(proceso_id: str) -> dict:
    r = _db().table("espejo_respuestas").select("*").eq("proceso_id", proceso_id).execute()
    result = {}
    for row in r.data:
        pid = row["pregunta_id"]
        result[pid] = row["valor_escala"] if row["valor_escala"] is not None else row["texto_respuesta"]
    return result


# ─── Evaluadores externos ─────────────────────────────────────────────────────

def create_evaluador(proceso_id: str, nombre: str, correo: str) -> dict:
    token = str(uuid.uuid4())
    r = _db().table("espejo_evaluadores").insert({
        "proceso_id": proceso_id,
        "nombre": nombre,
        "correo": correo,
        "token": token,
        "estado": "pendiente",
    }).execute()
    return r.data[0]


def get_evaluador_by_token(token: str) -> dict | None:
    r = _db().table("espejo_evaluadores").select("*").eq("token", token).execute()
    return r.data[0] if r.data else None


def get_evaluadores(proceso_id: str) -> list:
    r = _db().table("espejo_evaluadores").select("*").eq("proceso_id", proceso_id).execute()
    return r.data


def completar_evaluador(evaluador_id: str):
    now = datetime.now(timezone.utc).isoformat()
    _db().table("espejo_evaluadores").update({
        "estado": "completado",
        "fecha_completado": now,
    }).eq("id", evaluador_id).execute()


# ─── Respuestas externas ──────────────────────────────────────────────────────

def save_respuesta_externa(evaluador_id: str, pregunta_id: int, valor_escala=None, texto=None):
    row = {"evaluador_id": evaluador_id, "pregunta_id": pregunta_id}
    if valor_escala is not None:
        row["valor_escala"] = int(valor_escala)
    if texto:
        row["texto_respuesta"] = str(texto)
    _db().table("espejo_respuestas_externas").upsert(
        row, on_conflict="evaluador_id,pregunta_id"
    ).execute()


def get_respuestas_externas(proceso_id: str) -> list:
    """Retorna todas las respuestas de evaluadores completados."""
    evaluadores = get_evaluadores(proceso_id)
    completados = [e["id"] for e in evaluadores if e["estado"] == "completado"]
    if not completados:
        return []
    r = _db().table("espejo_respuestas_externas").select("*").in_(
        "evaluador_id", completados
    ).execute()
    return r.data
