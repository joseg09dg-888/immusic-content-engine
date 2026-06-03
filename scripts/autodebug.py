"""
IM Music Content Engine — AutoDebug Hook
Corre pytest automaticamente despues de editar cualquier .py del proyecto.
Si los tests fallan, le avisa a Claude con el traceback exacto.
"""
import sys
import json
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\jose-\projects\immusic-content-engine")


def main():
    # Leer el JSON del hook desde stdin
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    # Extraer el path del archivo modificado
    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path", "") or tool_input.get("filePath", "")

    if not file_path:
        sys.exit(0)

    fp = Path(file_path)

    # Solo actuar en archivos .py dentro del proyecto
    if fp.suffix != ".py":
        sys.exit(0)

    try:
        fp.resolve().relative_to(PROJECT_ROOT.resolve())
    except ValueError:
        sys.exit(0)  # No es del proyecto

    # Correr pytest
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q", "--tb=short", "--no-header"],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
        timeout=180,
        env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"},
    )

    if result.returncode != 0:
        # Tests fallaron — reportar a Claude para que corrija
        last_output = (result.stdout + result.stderr)[-3000:]
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": (
                    f"AUTODEBUG ALERT — tests FALLARON despues de editar {fp.name}:\n\n"
                    f"{last_output}\n\n"
                    "Corrige el error inmediatamente antes de continuar."
                ),
            }
        }
        print(json.dumps(output))
        sys.exit(2)  # exit 2 = asyncRewake wakes Claude with the message

    # Tests pasan — silencio (Claude sigue trabajando)
    sys.exit(0)


if __name__ == "__main__":
    main()
