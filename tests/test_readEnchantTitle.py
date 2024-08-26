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

    ("./sample-data/20240823_121543.png", ("幸運", 2)),
    ("./sample-data/20240823_185546.png", ("射撃ダメージ増加", 1)),
    ("./sample-data/20240823_185551.png", ("射撃ダメージ増加", 1)),
    ("./sample-data/20240823_185616.png", ("水中採掘", 0)),
    ("./sample-data/20240823_185644.png", ("射撃ダメージ増加", 3)),
    ("./sample-data/20240823_185720.png", ("高速装填", 2)),
    ("./sample-data/20240823_185725.png", ("パンチ", 2)),
    ("./sample-data/punch1.png", ("パンチ", 1)),
    ("./sample-data/sokubaku.png", ("束縛の呪い", 0)),
    ("./sample-data/knockback1.png", ("ノックバック", 1)),
    ("./sample-data/knockback2.png", ("ノックバック", 2)),
    ("./sample-data/koori2.png", ("氷渡り", 2)),
    ("./sample-data/koritsu4.png", ("効率強化", 4)),
    ("./sample-data/flame.png", ("フレイム", 0)),
    ("./sample-data/toge2.png", ("棘の鎧", 2)),
    ("./sample-data/toge3.png", ("棘の鎧", 3)),
    ("./sample-data/damage_zouka5.png", ("ダメージ増加", 5)),
    ("./sample-data/hanni2.png", ("範囲ダメージ増加", 2)),
    ("./sample-data/mushi2.png", ("虫特効", 2)),
    ("./sample-data/chuusei2.png", ("忠誠", 2)),
    ("./sample-data/shometsu.png", ("消滅の呪い", 0)),
    ("./sample-data/bougu_kantsu2.png", ("防具貫通", 2)),
    ("./sample-data/bougu_kantsu4.png", ("防具貫通", 4)),
    ("./sample-data/damage_keigen4.png", ("ダメージ軽減", 4)),
    ("./sample-data/mugen.png", ("無限", 0)),
    ("./sample-data/undead5.png", ("アンデッド特効", 5)),
    ("./sample-data/iregui3.png", ("入れ食い", 3)),
    ("./sample-data/kaen_taisei4.png", ("火炎耐性", 4)),
    ("./sample-data/kouun3.png", ("幸運", 3)),
    ("./sample-data/shuuzen.png", ("修繕", 0)),
    ("./sample-data/silk_touch.png", ("シルクタッチ", 0)),
    ("./sample-data/suisei_tokkou5.png", ("水生特効", 5)),
    ("./sample-data/suichuu_kokyuu3.png", ("水中呼吸", 3)),
    ("./sample-data/suichuu_hokou3.png", ("水中歩行", 3)),
    ("./sample-data/taikyuuryoku3.png", ("耐久力", 3)),
    ("./sample-data/takara3.png", ("宝釣り", 3)),
    ("./sample-data/drop_zouka3.png", ("ドロップ増加", 3)),
    ("./sample-data/hizokusei2.png", ("火属性", 2)),
])
def test_classify_items(img_path, expected):
    img = cv2.imread(img_path)
    assert read_enchant_title(img) == expected

