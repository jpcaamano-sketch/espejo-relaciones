from core.questions import HERIDA_PREGUNTAS, HERIDAS, get_intensidad


def calcular_puntajes(respuestas: dict) -> dict:
    """Suma de 4 preguntas por herida. Rango 4-20."""
    scores = {}
    for herida, ids in HERIDA_PREGUNTAS.items():
        vals = [respuestas[i] for i in ids if i in respuestas and respuestas[i]]
        scores[herida] = sum(vals) if vals else 0
    return scores


def determinar_heridas(scores: dict) -> tuple:
    """Retorna (herida_primaria, herida_secundaria, es_co_dominante)."""
    sorted_h = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primaria  = sorted_h[0][0]
    secundaria = sorted_h[1][0]
    p_score = sorted_h[0][1]
    s_score = sorted_h[1][1]
    co_dominante = abs(p_score - s_score) <= 2
    return primaria, secundaria, co_dominante


def calcular_promedios_externos(respuestas_externas: list) -> dict:
    """
    respuestas_externas: lista de dicts {pregunta_id, valor_escala}
    Retorna {pregunta_id: promedio}
    """
    from collections import defaultdict
    acum = defaultdict(list)
    for r in respuestas_externas:
        if r.get("valor_escala") is not None:
            acum[r["pregunta_id"]].append(r["valor_escala"])
    return {pid: round(sum(vals) / len(vals), 1) for pid, vals in acum.items()}


def detectar_divergencias(scores_auto: dict, promedios_externos: dict) -> list:
    """
    Detecta divergencias significativas entre autopercepción y percepción externa.
    Retorna lista de {herida, score_auto, score_externo, tipo}
    """
    from core.questions import HERIDA_EXTERNAS
    divergencias = []

    # Escala auto: 4-20. Escala externa: 1-5. Normalizo auto a 1-5 dividiendo / 4
    for herida, ext_ids in HERIDA_EXTERNAS.items():
        ext_vals = [promedios_externos[i] for i in ext_ids if i in promedios_externos]
        if not ext_vals:
            continue
        promedio_ext = sum(ext_vals) / len(ext_vals)
        score_auto_norm = scores_auto.get(herida, 0) / 4  # normalizo a escala 1-5

        diff = promedio_ext - score_auto_norm
        if abs(diff) >= 1.0:
            divergencias.append({
                "herida": herida,
                "score_auto_norm": round(score_auto_norm, 1),
                "score_externo": round(promedio_ext, 1),
                "diferencia": round(diff, 1),
                "tipo": "no_reconocida" if diff > 0 else "sobreestimada",
            })
    return divergencias
