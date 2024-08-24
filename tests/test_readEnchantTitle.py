import pytest
import cv2

from src.readEnchantTitle import read_enchant_title

@pytest.mark.parametrize("img_path, expected", [
    # 表示なし
    ("./sample-data/20240823_121533.png", ("", 0)),
    ("./sample-data/20240823_185556.png", ("", 0)),
    ("./sample-data/20240823_185601.png", ("", 0)),
    ("./sample-data/20240823_185606.png", ("", 0)),
    ("./sample-data/20240823_185621.png", ("", 0)),
    ("./sample-data/20240823_185626.png", ("", 0)),
    ("./sample-data/20240823_185639.png", ("", 0)),
    # 位置が違う場所にある本
    ("./sample-data/20240823_185659.png", ("", 0)),

    # 幸運 II
    ("./sample-data/20240823_121543.png", ("幸運", 2)),
    # 射撃ダメージ増加 I
    ("./sample-data/20240823_185546.png", ("射撃ダメージ増加", 1)),
    # 射撃ダメージ増加 I
    ("./sample-data/20240823_185551.png", ("射撃ダメージ増加", 1)),
    # 水中採掘
    ("./sample-data/20240823_185616.png", ("水中採掘", 0)),
    # 射撃ダメージ増加 III
    ("./sample-data/20240823_185644.png", ("射撃ダメージ増加", 3)),
    # 高速装填 II
    ("./sample-data/20240823_185720.png", ("高速装填", 2)),
    # パンチ II
    ("./sample-data/20240823_185725.png", ("パンチ", 2)),
])
def test_classify_items(img_path, expected):
    img = cv2.imread(img_path)
    assert read_enchant_title(img) == expected

