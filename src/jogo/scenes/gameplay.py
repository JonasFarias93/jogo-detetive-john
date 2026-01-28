from __future__ import annotations

from dataclasses import dataclass

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen

from jogo.chapters.registry import (
    ChapterNotFoundError,
    ManifestError,
    SceneNotFoundError,
    get_entry_scene_id,
    get_scene,
)
from jogo.ui.widgets.actions_panel import ActionsPanel
from jogo.ui.widgets.scene_panel import ScenePanel
from jogo.ui.widgets.status_panel import StatusPanel


@dataclass
class PlayerStats:
    sono: int = 65
    energia: int = 55
    foco: int = 70
    estresse: int = 20


class GameplayScreen(MDScreen):
    """
    Orquestrador: mantém estado, chama chapters/registry, atualiza UI.
    UI estável: nunca crasha por erro no manifest/arquivos.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Estado do jogo (Sprint 1)
        self.stats = PlayerStats()
        self.current_chapter_id = "chapter_01"
        self.current_scene_id: str | None = None

        # Refs de UI
        self.status_panel: StatusPanel | None = None
        self.scene_panel: ScenePanel | None = None
        self.actions_panel: ActionsPanel | None = None

        # Guard para não recriar UI
        self._ui_built = False

    def on_enter(self, *args):
        # Monta UI UMA vez (estável)
        if not self._ui_built:
            self._build_ui()
            self._ui_built = True

        # Sempre que entrar, tenta renderizar a cena atual (ou entry)
        self.load_and_render_scene()

    # ---------------------------
    # UI build (uma vez)
    # ---------------------------
    def _build_ui(self):
        self.clear_widgets()

        root = MDBoxLayout(orientation="vertical", padding="16dp", spacing="14dp")

        # STATUS
        self.status_panel = StatusPanel()
        root.add_widget(self.status_panel)

        # CENA
        self.scene_panel = ScenePanel()
        root.add_widget(self.scene_panel)

        # AÇÕES
        self.actions_panel = ActionsPanel()
        root.add_widget(self.actions_panel)

        self.add_widget(root)

        # primeira renderização do status
        self._refresh_status_panel()

    # ---------------------------
    # Render / Orquestração
    # ---------------------------
    def load_and_render_scene(self):
        """
        Carrega SceneData do registry e aplica na UI.
        Se falhar, exibe erro dentro do ScenePanel (sem crash).
        """
        if not self.scene_panel:
            return

        # Determina a cena inicial caso ainda não exista
        if not self.current_scene_id:
            try:
                self.current_scene_id = get_entry_scene_id(self.current_chapter_id)
            except Exception as e:
                self._render_error(
                    title="Erro ao obter entry_scene",
                    detail=str(e),
                )
                # mesmo em erro, mantém ações limpas pra UI não confundir
                if self.actions_panel:
                    self.actions_panel.set_actions([])
                return

        try:
            scene = get_scene(self.current_chapter_id, self.current_scene_id)
        except (ChapterNotFoundError, ManifestError, SceneNotFoundError) as e:
            self._render_error(
                title="Erro ao carregar cena",
                detail=f"chapter={self.current_chapter_id} scene={self.current_scene_id}\n{e}",
            )
            if self.actions_panel:
                self.actions_panel.set_actions([])
            return
        except Exception as e:
            self._render_error(
                title="Erro inesperado",
                detail=repr(e),
            )
            if self.actions_panel:
                self.actions_panel.set_actions([])
            return

        # Aplicar na UI (sem rebuild)
        self.scene_panel.set_text(scene.text)
        self.scene_panel.set_image(scene.image)

        # AÇÕES: conectar SceneData.actions -> ActionsPanel
        if self.actions_panel:
            ui_actions = []
            for act in scene.actions:
                ui_actions.append(
                    {
                        "label": act.label,
                        "hint": act.hint,
                        "callback": (lambda a=act: self._on_action_selected(a)),
                    }
                )
            self.actions_panel.set_actions(ui_actions)

        # Status pode mudar via ações; aqui só garantimos que está consistente
        self._refresh_status_panel()

    def _on_action_selected(self, action):
        """
        Recebe um ActionData do registry (scene.actions) e:
        - aplica effects (deltas) nos stats
        - atualiza status
        - muda current_scene_id para action.goto
        - re-renderiza a cena
        """
        # aplica efeitos (deltas) com clamp 0..100
        self.stats.sono = max(0, min(100, self.stats.sono + action.effects.sono))
        self.stats.energia = max(0, min(100, self.stats.energia + action.effects.energia))
        self.stats.foco = max(0, min(100, self.stats.foco + action.effects.foco))
        self.stats.estresse = max(0, min(100, self.stats.estresse + action.effects.estresse))

        self._refresh_status_panel()

        # muda cena e re-renderiza
        self.current_scene_id = action.goto
        self.load_and_render_scene()

    def _refresh_status_panel(self):
        if not self.status_panel:
            return

        self.status_panel.set_stats(
            sono=self.stats.sono,
            energia=self.stats.energia,
            foco=self.stats.foco,
            estresse=self.stats.estresse,
        )

    # ---------------------------
    # Error UX (UI estável)
    # ---------------------------
    def _render_error(self, *, title: str, detail: str):
        if not self.scene_panel:
            return

        msg = (
            f"{title}\n\n"
            f"{detail}\n\n"
            "Dica: confira o manifest.json do capítulo (schema, scenes, entry_scene) "
            "e se text_file aponta para um caminho válido."
        )
        self.scene_panel.set_text(msg)
        self.scene_panel.set_image("")
