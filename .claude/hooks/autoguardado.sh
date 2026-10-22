#!/usr/bin/env bash
# Autoguardado de Linderman: al terminar cada respuesta, sube a GitHub todo lo que cambió.
cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}" || exit 0
git add -A
if ! git diff --cached --quiet; then
  git commit -qm "autoguardado Linderman $(date '+%Y-%m-%d %H:%M')"
fi
git push -q 2>/dev/null || true
exit 0
