import pytest
from src.classifyItems import classify_items

@pytest.mark.parametrize("img_path, expected", [
    # 取引画面
    ("./sample-data/20240823_121533.png", (2,1)),
    ("./sample-data/20240823_121543.png", (2,1)),
    ("./sample-data/20240823_121548.png", (2,1)),
    ("./sample-data/20240823_121613.png", (2,0)),
    ("./sample-data/20240823_121734.png", (2,0)),
    ("./sample-data/20240823_121739.png", (0,1)),
    ("./sample-data/20240823_121744.png", (2,1)),
    ("./sample-data/20240823_121750.png", (2,1)),
    ("./sample-data/20240823_121755.png", (1,2)),
    ("./sample-data/20240823_121800.png", (0,2)),
    ("./sample-data/20240823_121805.png", (1,2)),
    ("./sample-data/20240823_121810.png", (0,2)),
    ("./sample-data/20240823_121815.png", (0,2)),
])
def test_classify_items(img_path, expected):
    assert classify_items(img_path) == expected

