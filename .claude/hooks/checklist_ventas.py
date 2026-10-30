"""Hook UserPromptSubmit: si Javier habla de vender/publicar, inyecta el checklist obligatorio.

Las notas en memoria no se cumplían solas; este hook las mete en cada mensaje que aplique.
"""
import json
import re
import sys

PALABRAS = r"vend|public|marketplace|grupo|precio|anuncio|client|foto|oferta|cotiz|whatsapp|promocion|campa"

CHECKLIST = """CHECKLIST OBLIGATORIO (hook de ventas, regla de Javier 2026-10-29). Antes de responder o actuar:
1. CARGAR con Skill, desde el primer mensaje, TODAS las que apliquen: ventas, ventas-whatsapp, cero-generico, foto-pro / edicion-foto-video (si hay fotos), campana-meta-ads (si hay anuncios). No basta con conocerlas: invocarlas.
2. CONTRADECIR COMO EXPERTO antes de publicar: revisar precio (precio exacto y cambio de primer dígito: Q9,850 > Q10,000), nunca escribir 'negociable/platicables', gancho, portada cuadrada, tono humano (no técnico ni de IA). Si lo que pidió Javier se puede mejorar, decírselo con el argumento ANTES de hacerlo.
3. Fotos 'con diseño' = buscar primero en Canva (search-designs). Fotos 'reales' = originales del celular.
4. Marketplace: nunca EDITAR un compartido en grupo (borra las fotos). Revisar bandeja marketplace/inbox antes de diagnosticar.
5. Pedir precio mínimo y dejar respuestas de WhatsApp listas (objeciones) al publicar.
6. Pasar cero-generico antes de entregar: concreto, corto, sin frases de libro."""


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    prompt = (data.get("prompt") or "").lower()
    if re.search(PALABRAS, prompt):
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": CHECKLIST,
            }
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
