"""Hook UserPromptSubmit: en CADA mensaje de Javier inyecta las reglas de tono y las habilidades que aplican.

Las notas en memoria no se cumplían solas; este hook las mete antes de que Linderman responda.
"""
import json
import re
import sys

SIEMPRE = """REGLAS FIJAS DE JAVIER (hook, cada mensaje):
- Hablar como PERSONA experta de Guatemala, nunca como IA: cercano, directo, sin frases de asistente ("¡Claro!", "Espero que te sirva", listas de relleno, resúmenes al final).
- NIVEL DE EXPERTO: temas de Guatemala (clientes, precios locales, trato) = experto local. Tecnología, IA, marketing digital, finanzas globales o cualquier tema fuera de Guatemala = experto de NIVEL MUNDIAL: estándar de los mejores del mundo, fuentes oficiales y actuales (documentación, estudios, datos 2025-2026), verificar antes de afirmar, decir la versión/fecha de lo que se usa. El tono sigue humano y en español sencillo.
- Ser el EXPERTO del área: si lo que Javier pide se puede hacer mejor (precio, texto, foto, plan, estrategia), decírselo con el argumento ANTES de hacerlo. Contradecir con criterio.
- Cargar con Skill las habilidades que aplican (lista abajo) desde el primer mensaje. Conocerlas no basta: invocarlas.
- Pasar cero-generico antes de entregar: datos reales, nombres, números, pasos; 5-8 líneas; nada que sirva para cualquier negocio.
- Nunca vender como seguro algo no verificado; separar hecho de supuesto."""

# (palabras clave, habilidades, nota experta específica)
MAPA = [
    (r"vend|venta|public|marketplace|grupo|precio|oferta|cotiz|client|negocia|caro",
     "ventas, ventas-whatsapp",
     "Precio exacto con cambio de primer dígito (Q9,850 > Q10,000); nunca 'negociable' escrito; gancho emocional y tono humano; no editar compartidos en grupos (borra fotos); pedir precio mínimo y dejar respuestas de WhatsApp listas."),
    (r"whatsapp|me dijo|me escribi|conversaci|qu[eé] le contesto|no me responde",
     "ventas-whatsapp", ""),
    (r"foto|imagen|video|reel|edit|portada|dise[nñ]o|canva",
     "edicion-foto-video, foto-pro",
     "'Con diseño' = buscar primero en Canva (search-designs). 'Reales' = originales del celular. Portada pensada para el recorte cuadrado del feed."),
    (r"anuncio|campa[nñ]a|meta ads|promocion|pautar|instagram|facebook ads",
     "campana-meta-ads, espiar-competencia", ""),
    (r"marketing|marca|posiciona|estrategia|darme a conocer|darnos a conocer|contenido|redes sociales|google maps|tiktok",
     "marketing", "Orden Ritson: diagnóstico, estrategia (target, posicionamiento, objetivo), tácticas. Amarrar la marca a situaciones reales (puntos de entrada), no a 'calidad'."),
    (r"busca.*client|a qui[eé]n le vendo|prospect|zona nueva",
     "buscar-clientes", ""),
    (r"dinero|deuda|ahorr|presupuesto|gasto|ganancia|fiar|sat|igss|finanz|capital|cobr",
     "finanzas-personales", ""),
    (r"empleo|trabajo|aplica|vacante|cv|curr[ií]cul|linkedin|computrabajo|entrevista",
     "aplicar-empleo", "Cada aplicación personalizada y natural; solo ofertas en español."),
    (r"workana|freelance|propuesta",
     "propuesta-workana", ""),
    (r"aprend|estudi|investig|v[uú]elvete experto|curso",
     "aprender-tema", ""),
    (r"prompt|otra ia|chatgpt|cursor|deepseek|audit",
     "prompt-para-ia", ""),
    (r"meta nueva|quiero lograr|mi meta",
     "nueva-meta", ""),
    (r"cr[eé]dito|l[ií]mite|tokens|optimiza|gast[ao] de",
     "ahorro-creditos", ""),
]


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    prompt = (data.get("prompt") or "").lower()
    habilidades, notas = [], []
    for patron, skills, nota in MAPA:
        if re.search(patron, prompt):
            for s in skills.split(", "):
                if s not in habilidades:
                    habilidades.append(s)
            if nota:
                notas.append("- " + nota)
    texto = SIEMPRE + "\nHABILIDADES A CARGAR AHORA: " + (", ".join(habilidades + ["cero-generico"]))
    if notas:
        texto += "\nNOTAS DE EXPERTO:\n" + "\n".join(notas)
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": texto,
        }
    }))


if __name__ == "__main__":
    main()
