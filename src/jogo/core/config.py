from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    # base
    fps: int = 30

    # visual ASCII (desktop-first)
    ascii_font_size: int = 18

    # conteúdo
    default_chapter: str = "chapter_01"
