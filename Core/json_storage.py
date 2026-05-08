import json
import logging
from pathlib import Path
from typing import Any, Dict, List


LOGGER = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent.parent


def _resolve_path(file_path: str) -> Path:
    path = Path(file_path)
    if path.is_absolute():
        return path
    return BASE_DIR / path


def load_json_list(file_path: str) -> List[Dict[str, Any]]:
    path = _resolve_path(file_path)
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, list):
                raise ValueError("JSON 文件内容应为列表")
            return data
    except (FileNotFoundError, json.JSONDecodeError, OSError, ValueError) as exc:
        LOGGER.warning("加载 JSON 文件失败: %s (%s)", path, exc)
        return []


def save_json_list(file_path: str, data: List[Dict[str, Any]]) -> bool:
    path = _resolve_path(file_path)
    try:
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return True
    except (OSError, TypeError) as exc:
        LOGGER.warning("保存 JSON 文件失败: %s (%s)", path, exc)
        return False
