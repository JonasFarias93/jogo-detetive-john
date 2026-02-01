from jogo.content import registry


def test_load_manifest_chapter_01():
    m = registry.load_manifest("chapter_01")
    assert isinstance(m, dict)
    assert "scenes" in m


def test_entry_scene_exists():
    entry = registry.get_entry_scene_id("chapter_01")
    assert isinstance(entry, str)
    assert entry != ""


def test_get_scene_returns_scene_data():
    entry = registry.get_entry_scene_id("chapter_01")
    scn = registry.get_scene("chapter_01", entry)

    assert scn.id == entry
    assert isinstance(scn.text, str)
    assert isinstance(scn.actions, list)
