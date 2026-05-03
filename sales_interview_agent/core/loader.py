
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]


def _resolve_path(file_path: str) -> Path:
    path = Path(file_path)
    if path.exists():
        return path

    fallback_path = BASE_DIR / path
    if fallback_path.exists():
        return fallback_path

    raise FileNotFoundError(
        f"Dosya bulunamadı: {file_path} "
        f"(kontrol edilen yollar: {path}, {fallback_path})"
    )


def load_roles(file_path: str) -> dict:
    """
    roles.json dosyasını okur ve dictionary olarak döner
    """
    resolved_path = _resolve_path(file_path)

    with resolved_path.open("r", encoding="utf-8") as f:
        roles = json.load(f)

    return roles


def load_knowledge(file_path: str) -> str:
    """
    txt bilgi dosyasını okur ve string olarak döner
    """
    resolved_path = _resolve_path(file_path)

    with resolved_path.open("r", encoding="utf-8") as f:
        content = f.read()

    return content
