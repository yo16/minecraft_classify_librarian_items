import pytest
from src.isLibrarianTradeWindowOpen import is_librarian_trade_window_open

@pytest.mark.parametrize("img_path, expected", [
    # 取引画面
    ("./sample-data/20240823_121533.png", True),
    ("./sample-data/20240823_121543.png", True),
    ("./sample-data/20240823_121548.png", True),
    ("./sample-data/20240823_121613.png", True),
    ("./sample-data/20240823_121734.png", True),
    ("./sample-data/20240823_121739.png", True),
    ("./sample-data/20240823_121744.png", True),
    ("./sample-data/20240823_121750.png", True),
    ("./sample-data/20240823_121755.png", True),
    ("./sample-data/20240823_121800.png", True),
    ("./sample-data/20240823_121805.png", True),
    ("./sample-data/20240823_121810.png", True),
    ("./sample-data/20240823_121815.png", True),

    # 非取引画面
    ("./sample-data/20240823_121528.png", False),
    ("./sample-data/20240823_121538.png", False),
    ("./sample-data/20240823_121553.png", False),
    ("./sample-data/20240823_121558.png", False),
    ("./sample-data/20240823_121603.png", False),
    ("./sample-data/20240823_121608.png", False),
    ("./sample-data/20240823_121729.png", False),
])
def test_is_librarian_trade_window_open(img_path, expected):
    assert is_librarian_trade_window_open(img_path) == expected

