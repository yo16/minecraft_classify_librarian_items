import pytest

from src.getWindowSize import get_window_size

@pytest.mark.parametrize("win_title, expected", [
    # テストが難しいので割愛
    ## Visual Studio Codeのタイトル（最大化）
    #("minecraft_classify_librarian_items", {"left": -8, "top": -8, "width": 1936, "height": 1048}),
    ("no window title", None),
])
def test_get_window_size(win_title, expected):
    assert get_window_size(win_title) == expected

