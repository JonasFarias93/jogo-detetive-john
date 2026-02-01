from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


# Pasta base dos chapters: src/jogo/chapters
CHAPTERS_DIR = Path(__file__).resolve().parent


# ---------- Contratos (dados que o registry entrega) ----------

@dataclass(frozen=True)
class EffectsData:
    sono: int = 0
    energia: int = 0
    foco: int = 0
    estresse: int = 0


@dataclass(frozen=True)
class ActionData:
    key: str
    label: str
    goto: str
    effects: EffectsData = EffectsData()
    hint: str = ""  # opcional (Sprint 1)


@dataclass(frozen=True)
class SceneData:
    id: str
    text: str
    image: str  # path resolvido (string) ou ""
    actions: List[ActionData]


# ---------- Erros do registry ----------

class ChapterNotFoundError(FileNotFoundError):
    pass


class ManifestError(ValueError):
    pass


class SceneNotFoundError(KeyError):
    pass


# ---------- Funções públicas (API do registry) ----------

def chapter_dir(chapter_id: str) -> Path:
    d = CHAPTERS_DIR / chapter_id
    if not d.exists() or not d.is_dir():
        raise ChapterNotFoundError(f"Chapter '{chapter_id}' não encontrado em {d}")
    return d


def manifest_path(chapter_id: str) -> Path:
    p = chapter_dir(chapter_id) / "manifest.json"
    if not p.exists():
        raise ChapterNotFoundError(f"manifest.json não encontrado em {p}")
    return p


def load_manifest(chapter_id: str) -> Dict[str, Any]:
    """
    Lê e retorna o dict do manifest do capítulo.
    Mantém cache simples por processo (opcional futuramente).
    """
    p = manifest_path(chapter_id)
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ManifestError(f"JSON inválido em {p}: {e}") from e

    if not isinstance(data, dict):
        raise ManifestError("manifest.json deve ser um objeto JSON (dict).")

    # validações mínimas (v1)
    if "scenes" not in data or not isinstance(data["scenes"], dict):
        raise ManifestError("manifest.json deve conter 'scenes' como objeto (dict).")

    if "entry_scene" in data and not isinstance(data["entry_scene"], str):
        raise ManifestError("'entry_scene' deve ser string.")

    return data


def get_entry_scene_id(chapter_id: str) -> str:
    m = load_manifest(chapter_id)
    entry = m.get("entry_scene")
    if not entry:
        # fallback: pega a primeira key das cenas
        scenes = list(m["scenes"].keys())
        if not scenes:
            raise ManifestError("Nenhuma cena definida em 'scenes'.")
        return scenes[0]
    return entry


def get_scene(chapter_id: str, scene_id: str) -> SceneData:
    """
    Retorna SceneData já resolvido:
    - text carregado de text_file ou 'text'
    - image resolvido para caminho absoluto (string) ou ""
    - actions normalizadas com efeitos default + hint opcional
    """
    manifest = load_manifest(chapter_id)
    scenes = manifest["scenes"]

    if scene_id not in scenes:
        raise SceneNotFoundError(f"Cena '{scene_id}' não existe no capítulo '{chapter_id}'.")

    raw_scene = scenes[scene_id]
    if not isinstance(raw_scene, dict):
        raise ManifestError(f"Cena '{scene_id}' deve ser objeto (dict).")

    base_dir = chapter_dir(chapter_id)

    text = _resolve_text(base_dir, raw_scene, scene_id)
    image = _resolve_image(base_dir, raw_scene)
    actions = _resolve_actions(raw_scene)

    return SceneData(
        id=scene_id,
        text=text,
        image=image,
        actions=actions,
    )


# ---------- Internos (helpers) ----------

def _resolve_text(base_dir: Path, raw_scene: Dict[str, Any], scene_id: str) -> str:
    text_file = raw_scene.get("text_file")
    text_inline = raw_scene.get("text")

    if text_file and text_inline:
        raise ManifestError(f"Cena '{scene_id}' não pode ter 'text' e 'text_file' ao mesmo tempo.")

    if text_file:
        if not isinstance(text_file, str):
            raise ManifestError(f"'text_file' da cena '{scene_id}' deve ser string.")
        p = (base_dir / text_file).resolve()
        if not p.exists():
            raise ManifestError(f"text_file não encontrado: {p}")
        return p.read_text(encoding="utf-8")

    if text_inline is None:
        return ""  # permitido (cena sem texto)
    if not isinstance(text_inline, str):
        raise ManifestError(f"'text' da cena '{scene_id}' deve ser string.")
    return text_inline


def _resolve_image(base_dir: Path, raw_scene: Dict[str, Any]) -> str:
    image = raw_scene.get("image", "")
    if image is None:
        return ""
    if not isinstance(image, str):
        raise ManifestError("'image' deve ser string (ou vazio).")
    if image.strip() == "":
        return ""

    # resolve path relativo ao capítulo
    p = (base_dir / image).resolve()
    # Não obrigamos existir na Sprint 1 (pra não travar protótipo)
    return str(p)


def _resolve_actions(raw_scene: Dict[str, Any]) -> List[ActionData]:
    actions_raw = raw_scene.get("actions", [])
    if actions_raw is None:
        return []
    if not isinstance(actions_raw, list):
        raise ManifestError("'actions' deve ser uma lista.")

    out: List[ActionData] = []
    for i, a in enumerate(actions_raw):
        if not isinstance(a, dict):
            raise ManifestError(f"Ação index {i} deve ser objeto (dict).")

        key = a.get("key")
        label = a.get("label")
        goto = a.get("goto")

        if not isinstance(key, str) or not key:
            raise ManifestError(f"Ação index {i}: 'key' deve ser string não-vazia.")
        if not isinstance(label, str) or not label:
            raise ManifestError(f"Ação index {i}: 'label' deve ser string não-vazia.")
        if not isinstance(goto, str) or not goto:
            raise ManifestError(f"Ação index {i}: 'goto' deve ser string não-vazia.")

        effects = _parse_effects(a.get("effects"))

        hint = a.get("hint", "")
        if hint is None:
            hint = ""
        if not isinstance(hint, str):
            raise ManifestError(f"Ação index {i}: 'hint' deve ser string.")

        out.append(ActionData(key=key, label=label, goto=goto, effects=effects, hint=hint))

    return out


def _parse_effects(e: Any) -> EffectsData:
    if e is None:
        return EffectsData()
    if not isinstance(e, dict):
        raise ManifestError("'effects' deve ser objeto (dict).")

    def _get_int(name: str) -> int:
        v = e.get(name, 0)
        if v is None:
            return 0
        if not isinstance(v, int):
            raise ManifestError(f"effects.{name} deve ser int.")
        return v

    return EffectsData(
        sono=_get_int("sono"),
        energia=_get_int("energia"),
        foco=_get_int("foco"),
        estresse=_get_int("estresse"),
    )
