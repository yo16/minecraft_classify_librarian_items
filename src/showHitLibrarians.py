import unicodedata

POSITION = (
    ["水生特効5",   None,           "防具貫通4",        "重撃5"],
    ["忠誠3",       "水中呼吸3",    "フレイム",         "ノックバック1"],
    ["入れ食い3",   "水中歩行3",    "無限",             "ノックバック2"],
    ["宝釣り3",     "水中採掘",     "射撃ダメージ増加5","アンデッド特効5"],
    [None,          None,           None,               "火属性2"],
    ["幸運3",       "棘の鎧3",      None,               "ドロップ増加3"],
    ["シルクタッチ","落下耐性4",    "耐久力3",          "範囲ダメージ増加3"],
    ["効率強化5",   "ダメージ軽減4","修繕",             "ダメージ増加5"]
)

def show_hit_librarians(
    enchant_title: str,
    enchant_level: int
):
    print(11);
    level_str = "" if enchant_level == 0 else f"{enchant_level}"
    enchant_str = f"{enchant_title}{level_str}"

    # 存在確認
    exist_enchant = False
    for line_ary in POSITION:
        for enchant_item in line_ary:
            if enchant_item == enchant_str:
                # 存在する
                exist_enchant = True
                break
        if exist_enchant:
            break
    
    if exist_enchant:
        # 表示する
        # １要素の幅は20
        element_width = 20
        print("="*(element_width*4))
        for line_ary in POSITION:
            line_str = ""
            for enchant_item in line_ary:
                if enchant_item is None:
                    empty_str = " ----"
                    line_str += f"{empty_str:<{element_width}}"
                else:
                    python_len = len(enchant_item)
                    multibite_len = count_multibyte_len(enchant_item)
                    # multibite_lenを2で割ったあまりが0でないときは、数字(半角)が１つついている
                    zenkaku_char_num = python_len - multibite_len%2
                    # (element_width-2)の幅にするためのスペースの数を数える
                    # 全角分は*2、最後についている半角１文字をあれば加える
                    space_num = (element_width-2) - (
                        (zenkaku_char_num * 2) + (multibite_len % 2)
                    )
                    # 修飾２文字＋エンチャント文字列の文字列長＋スペースの数が、format文字列で指定する文字列長
                    enchant_str_len = 2 + python_len + space_num

                    # 出力文字列を作成
                    if enchant_item == enchant_str:
                        # 一致するときは修飾
                        cur_str = f"[{enchant_item}]"
                    else:
                        cur_str = f" {enchant_item} "
                    line_str += f"{cur_str:<{enchant_str_len}}"

            print(line_str)
        print("="*(element_width*4))



def count_multibyte_len(s: str) -> int:
    count = 0
    for c in s:
        if unicodedata.east_asian_width(c) in ('F', 'W', 'A'):
            count += 2
        else:
            count += 1
    return count

