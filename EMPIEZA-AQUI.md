# Linderman · Empieza aquí

Linderman es tu agente de IA personal. Nació en blanco: tú decides en qué es experto y le vas enseñando. Funciona como Hermes Agent: recuerda, aprende y guarda habilidades.

## Cómo abrirlo
1. En VS Code: **Archivo › Abrir carpeta** → elige la carpeta `Linderman`.
2. Abre Claude Code. Desde ese momento hablas con Linderman.

## Los 4 comandos
| Escribe | Para qué |
|---|---|
| `/especialidad renta de maquinaria` | Le dices en qué ser experto. Te hace unas preguntas y lo deja escrito. |
| `/ensenar mi lista de precios es...` | Le enseñas algo: texto, un archivo (arrástralo al chat) o un link. |
| `/habilidad` | Después de que haga algo bien, lo guarda para repetirlo igual la próxima vez. |
| `/que-sabes` | Te muestra todo lo que sabe hasta hoy y qué le falta aprender. |

También aprende solo: si le dices "recuerda que..." lo anota, y cuando termina una tarea larga te ofrece guardarla como habilidad.

## Dónde vive lo que aprende
- `ESPECIALIDAD.md` → en qué es experto.
- `memoria/MEMORIA.md` → datos cortos que recuerda de ti.
- `conocimiento/` → tus documentos, precios, guías y ejemplos.
- `habilidades.md` → lista de lo que ya sabe hacer (los pasos están en `.claude/skills/`).

Todo son archivos normales: puedes abrirlos y corregirlos a mano cuando quieras. Si un día instalamos Hermes Agent de verdad, esta misma carpeta se le pasa y no se pierde nada.
