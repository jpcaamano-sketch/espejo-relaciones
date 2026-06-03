HERIDAS = ['rechazo', 'abandono', 'humillacion', 'traicion', 'injusticia']

HERIDA_PREGUNTAS = {
    'rechazo':     [1, 6, 11, 16],
    'abandono':    [2, 7, 12, 17],
    'humillacion': [3, 8, 13, 18],
    'traicion':    [4, 9, 14, 19],
    'injusticia':  [5, 10, 15, 20],
}

HERIDAS_INFO = {
    'rechazo': {
        'nombre': 'Rechazo',
        'icono': '🫧',
        'color': '#c9859a',
        'mensaje': 'Me hago pequeño/a para no ser visto — el miedo no es al otro, es a ti mismo/a',
        'orientacion': 'Aprende a habitar tu propio espacio. Mereces estar aquí.',
        'descripcion_corta': 'El miedo a no ser suficiente hace que te retires antes de que te rechacen.',
    },
    'abandono': {
        'nombre': 'Abandono',
        'icono': '🌊',
        'color': '#8b68c4',
        'mensaje': 'Buscas en el otro la seguridad que solo tú puedes darte',
        'orientacion': 'Construye tu propia presencia interna para no necesitar que el otro nunca se vaya.',
        'descripcion_corta': 'El terror a quedarse solo lleva a aferrarse o a anticipar el abandono.',
    },
    'humillacion': {
        'nombre': 'Humillación',
        'icono': '🌿',
        'color': '#68b4a4',
        'mensaje': 'Te sacrificas para no sentirte indigno/a — pero en ese sacrificio te pierdes a ti',
        'orientacion': 'Reconocer tus propias necesidades es un acto de sanación, no de egoísmo.',
        'descripcion_corta': 'El sacrificio constante es un intento de demostrar que mereces estar.',
    },
    'traicion': {
        'nombre': 'Traición',
        'icono': '🔒',
        'color': '#c4945c',
        'mensaje': 'Controlas porque en algún momento alguien no estuvo — y sigues protegiéndote de eso',
        'orientacion': 'Aprender a confiar empieza por confiar en tu propio criterio.',
        'descripcion_corta': 'La necesidad de control es una armadura construida contra la decepción.',
    },
    'injusticia': {
        'nombre': 'Injusticia',
        'icono': '⚖️',
        'color': '#7ab868',
        'mensaje': 'Eres muy duro/a contigo porque aprendiste que sentir era peligroso',
        'orientacion': 'Permitirte sentir no te hace débil — te hace humano/a.',
        'descripcion_corta': 'La autoexigencia y la rigidez son defensas contra lo que se percibe como caos emocional.',
    },
}

# ─── Preguntas de escala (autodiagnóstico) ─────────────────────────────────────

PREGUNTAS_ESCALA = {
    1:  {"usuario": "Cuando siento que alguien podría rechazarme, prefiero alejarme yo primero",
         "externo": "Cuando siente que alguien podría rechazarle, prefiere alejarse primero"},
    2:  {"usuario": "Cuando alguien cercano se distancia, siento una angustia difícil de controlar",
         "externo": "Cuando alguien cercano se distancia, siente una angustia difícil de controlar"},
    3:  {"usuario": "Con frecuencia pongo las necesidades de los demás antes que las mías propias",
         "externo": "Con frecuencia pone las necesidades de los demás antes que las suyas propias"},
    4:  {"usuario": "Me cuesta confiar en que las personas cumplirán sus compromisos conmigo",
         "externo": "Le cuesta confiar en que las personas cumplirán sus compromisos con él/ella"},
    5:  {"usuario": "Soy muy exigente conmigo mismo/a y me cuesta perdonarme los errores",
         "externo": "Es muy exigente consigo mismo/a y le cuesta perdonarse los errores"},
    6:  {"usuario": "Me cuesta creer que las personas me quieran tal como soy",
         "externo": "Le cuesta creer que las personas le quieran tal como es"},
    7:  {"usuario": "Necesito saber que las personas importantes en mi vida están disponibles para mí",
         "externo": "Necesita saber que las personas importantes en su vida están disponibles para él/ella"},
    8:  {"usuario": "Cuando alguien me critica delante de otros, me siento muy pequeño/a",
         "externo": "Cuando alguien le critica delante de otros, se siente muy pequeño/a"},
    9:  {"usuario": "Necesito tener cierto control sobre las situaciones para sentirme seguro/a",
         "externo": "Necesita tener cierto control sobre las situaciones para sentirse seguro/a"},
    10: {"usuario": "Cuando algo es injusto, siento una tensión interna muy intensa",
         "externo": "Cuando algo es injusto, siente una tensión interna muy intensa"},
    11: {"usuario": "Hay momentos en que siento que no merezco estar en ciertos grupos o espacios",
         "externo": "Hay momentos en que siente que no merece estar en ciertos grupos o espacios"},
    12: {"usuario": "Tengo miedo de que las personas que amo me dejen o se vayan",
         "externo": "Tiene miedo de que las personas que ama le dejen o se vayan"},
    13: {"usuario": "Me cuesta pedir cosas para mí porque siento que no debería molestar",
         "externo": "Le cuesta pedir cosas para sí mismo/a porque siente que no debería molestar"},
    14: {"usuario": "Cuando alguien no cumple lo que promete, lo recuerdo durante mucho tiempo",
         "externo": "Cuando alguien no cumple lo que promete, lo recuerda durante mucho tiempo"},
    15: {"usuario": "Me resulta difícil reconocer y expresar lo que siento emocionalmente",
         "externo": "Le resulta difícil reconocer y expresar lo que siente emocionalmente"},
    16: {"usuario": "Me incomoda profundamente ser el centro de atención",
         "externo": "Le incomoda profundamente ser el centro de atención"},
    17: {"usuario": "Me cuesta estar solo/a por períodos prolongados",
         "externo": "Le cuesta estar solo/a por períodos prolongados"},
    18: {"usuario": "Suelo sentir vergüenza con más facilidad que la mayoría de las personas",
         "externo": "Suele sentir vergüenza con más facilidad que la mayoría de las personas"},
    19: {"usuario": "Me cuesta delegar porque temo que otros no harán las cosas bien",
         "externo": "Le cuesta delegar porque teme que otros no harán las cosas bien"},
    20: {"usuario": "Tiendo a reprimir mis emociones para mantener el control y la apariencia",
         "externo": "Tiende a reprimir sus emociones para mantener el control y la apariencia"},
}

IDS_ESCALA = list(range(1, 21))

# ─── Preguntas abiertas (autodiagnóstico) ──────────────────────────────────────

PREGUNTAS_ABIERTAS = {
    101: "¿Qué comportamiento de otras personas te irrita más intensamente?",
    102: "¿Qué situación se repite en tus relaciones que te genera malestar?",
    103: "¿De qué forma crees que tu familia de origen influyó en cómo te relacionas hoy?",
    104: "¿Qué tipo de persona sientes que sigues atrayendo a tu vida?",
}

IDS_ABIERTAS = [101, 102, 103, 104]

# ─── Preguntas externas (evaluadores) ─────────────────────────────────────────

PREGUNTAS_EXTERNAS_ESCALA = {
    201: {
        "texto": "¿En qué momentos percibes que [nombre] se aleja o se hace invisible?",
        "escala_min": "Nunca",
        "escala_max": "Frecuentemente",
        "herida": "rechazo",
    },
    202: {
        "texto": "¿Sientes que [nombre] confía genuinamente en ti?",
        "escala_min": "Muy poco",
        "escala_max": "Completamente",
        "herida": "traicion",
    },
    203: {
        "texto": "¿Percibes que [nombre] se sacrifica demasiado por los demás?",
        "escala_min": "Nunca",
        "escala_max": "Siempre",
        "herida": "humillacion",
    },
    204: {
        "texto": "Cuando algo no sale como espera, ¿cómo reacciona [nombre]?",
        "escala_min": "Con calma",
        "escala_max": "Con mucha dificultad",
        "herida": "injusticia",
    },
    205: {
        "texto": "¿Sientes que [nombre] te necesita de una forma que a veces resulta agotadora?",
        "escala_min": "Nunca",
        "escala_max": "Frecuentemente",
        "herida": "abandono",
    },
}

PREGUNTAS_EXTERNAS_ABIERTAS = {
    206: "¿Qué emoción surge principalmente en ti cuando estás cerca de [nombre]?",
    207: "¿Hay algo que quisieras decirle a [nombre] que sientes que aún no has podido decirle?",
}

IDS_EXTERNAS_ESCALA  = [201, 202, 203, 204, 205]
IDS_EXTERNAS_ABIERTAS = [206, 207]

# Heridas mapeadas a preguntas externas (para comparación)
HERIDA_EXTERNAS = {
    'rechazo':     [201],
    'traicion':    [202, 204],
    'humillacion': [203],
    'abandono':    [205],
    'injusticia':  [204],
}

# ─── Escala ────────────────────────────────────────────────────────────────────

ESCALA_LABELS = [
    "No me identifica",
    "Poco",
    "A veces",
    "Bastante",
    "Me describe completamente",
]


def get_intensidad(score: int) -> tuple:
    """score = suma de 4 preguntas, rango 4-20"""
    if score <= 8:
        return "leve", "Esta herida está presente de forma suave. Puede que no la hayas identificado antes."
    elif score <= 13:
        return "moderado", "Esta herida tiene un peso real en tu forma de relacionarte."
    elif score <= 17:
        return "intenso", "Esta herida está activa y probablemente la reconoces en tu vida cotidiana."
    else:
        return "profundo", "Esta herida es central en tu historia. Hay un trabajo importante de sanación por hacer."
