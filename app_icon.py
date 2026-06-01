import sys
import tkinter as tk
from pathlib import Path

BASE_DIR = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
ICON_ICO = ASSETS_DIR / "logo.ico"
ICON_PNG = ASSETS_DIR / "logo.png"
ICON_ICNS = ASSETS_DIR / "logo.icns"


def _set_iconphoto(root, icon_path):
    try:
        icon = tk.PhotoImage(file=str(icon_path))
    except Exception:
        return False

    try:
        root.iconphoto(True, icon)
    except Exception:
        try:
            root.iconphoto(False, icon)
        except Exception:
            return False

    root._app_icon = icon
    return True


def carregar_icone(root):
    """Carrega o ícone do aplicativo para a janela Tkinter informada."""
    if not hasattr(root, "tk"):
        return False

    loaded = False
    if sys.platform.startswith("win") and ICON_ICO.exists():
        try:
            root.iconbitmap(str(ICON_ICO))
            loaded = True
        except Exception:
            loaded = False

    if ICON_PNG.exists():
        loaded = _set_iconphoto(root, ICON_PNG) or loaded
    elif sys.platform.startswith("win") and ICON_ICO.exists():
        loaded = _set_iconphoto(root, ICON_ICO) or loaded

    return loaded
