import pickle
import numpy as np
from typing import List

def determine_enchant_title_method(title_store_file: str):
    with open(title_store_file, "rb") as f:
        store = pickle.load(f)
        # 下記の型
        # "data": [
        #     {
        #         "name": str,
        #         "line": array,
        #     },
        # ]
    
    # 読んだデータを入れ替える
    lines = np.empty((0, 3000), dtype=np.uint8)
    titles: List[str] = []
    for title_info in store["data"]:
        titles.append(title_info["name"])
        lines = np.vstack([lines, np.array(title_info["line"])])
    
    # 計算しやすいように、255を1に変換
    lines[lines == 255] = 1
    
    #print(lines.shape)
    #print(lines[0, :100])

    # 分岐点をprintする
    print_split_point(lines, np.array(titles), np.arange(len(lines)))

    return


# 分岐点をprintする
# もう、if文を書いちゃう
def print_split_point(ary: np.array, titles: np.array, indices: np.array, depth: int=0):
    jisage = depth * 4

    # 現在の選択肢
    print(" "*jisage + f"# {indices}")

    y, x = ary.shape
    if y <= 1:
        print(" "*jisage + f"return \"{titles[0]}\"")
        return

    # 1次元目の方向に足し算して、今の配列要素の半分くらいのindexを得る
    target_i = get_half_value_index(ary)

    # 得た点で、値が0と1の配列を分ける
    ary0_indices = np.where(ary[:, target_i] == 0)
    ary1_indices = np.where(ary[:, target_i] == 1)
    ary0 = ary[ary0_indices]
    ary1 = ary[ary1_indices]
    ttl0 = titles[ary0_indices]
    ttl1 = titles[ary1_indices]
    ind0 = indices[ary0_indices]
    ind1 = indices[ary1_indices]

    # それぞれ分割される配列の数を得る
    print(" "*jisage + f"# {target_i} ({len(ary0)}:{len(ary1)})")

    # if文の都合で、"1"である方を先に
    print(" "*jisage + f"if img[{target_i}]:")
    #print(ary1)
    #if len(ind1)==1:
    #    print(f"{' '*jisage}[{ind1[0]}] {ttl1[0]}")
    #else:
    #    print(f"{' '*jisage}{ind1}")
    # 再帰的に、1で呼び出す
    print_split_point(ary1, ttl1, ind1, depth+1)

    # elseで、"0"である方
    print(" "*jisage + f"else:")
    #print(ary0)
    #if len(ind0)==1:
    #    print(f"{' '*jisage}[{ind0[0]}] {ttl0[0]}")
    #else:
    #    print(f"{' '*jisage}{ind0}")
    # 再帰的に、0で呼び出す
    print_split_point(ary0, ttl0, ind0, depth+1)



# 1次元目の方向に足し算して、今の配列要素の半分くらいのindexを得る
def get_half_value_index(ary: np.ndarray) -> int:
    y, x = ary.shape
    sum_array = np.sum(ary, axis=0)
    #print(sum_array[:100])
    #print(np.max(sum_array))

    # 半分の値の配列
    half_val = int(y / 2)
    ary_half_val = np.ones((3000,), dtype=np.int64) * half_val
    #print(ary_half_val)
    
    # 半分の値との差の配列
    half_val_distance = np.abs(sum_array - ary_half_val)

    # 一番小さな値のindexを１つ返す
    min_index = np.argmin(half_val_distance)
    
    return min_index



if __name__=="__main__":
    determine_enchant_title_method("./sample-data/title_store.pkl")
# 結果
"""
# [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38]
# 1007 (20:19)
if img[1007]:
    # [ 2  3  5  6  7 10 16 17 18 19 20 22 25 26 29 31 32 35 38]
    # 220 (10:9)
    if img[220]:
        # [ 3  6 10 20 22 25 29 32 38]
        # 221 (5:4)
        if img[221]:
            # [25 29 32 38]
            # 7 (2:2)
            if img[7]:
                # [25 32]
                # 29 (1:1)
                if img[29]:
                    # [25]
                    return "忠誠"
                else:
                    # [32]
                    return "火属性"
            else:
                # [29 38]
                # 2 (1:1)
                if img[2]:
                    # [29]
                    return "爆発耐性"
                else:
                    # [38]
                    return "重撃"
        else:
            # [ 3  6 10 20 22]
            # 19 (3:2)
            if img[19]:
                # [ 6 10]
                # 0 (1:1)
                if img[0]:
                    # [6]
                    return "激流"
                else:
                    # [10]
                    return "氷渡り"
            else:
                # [ 3 20 22]
                # 20 (2:1)
                if img[20]:
                    # [3]
                    return "火炎耐性"
                else:
                    # [20 22]
                    # 27 (1:1)
                    if img[27]:
                        # [22]
                        return "宝釣り"
                    else:
                        # [20]
                        return "束縛の呪い"
    else:
        # [ 2  5  7 16 17 18 19 26 31 35]
        # 264 (5:5)
        if img[264]:
            # [16 17 18 19 26]
            # 46 (3:2)
            if img[46]:
                # [16 17]
                # 39 (1:1)
                if img[39]:
                    # [16]
                    return "水生特効"
                else:
                    # [17]
                    return "水中呼吸"
            else:
                # [18 19 26]
                # 38 (2:1)
                if img[38]:
                    # [18]
                    return "水中採掘"
                else:
                    # [19 26]
                    # 7 (1:1)
                    if img[7]:
                        # [19]
                        return "水中歩行"
                    else:
                        # [26]
                        return "飛び道具耐性"
        else:
            # [ 2  5  7 31 35]
            # 7 (3:2)
            if img[7]:
                # [ 7 35]
                # 21 (1:1)
                if img[21]:
                    # [35]
                    return "虫特効"
                else:
                    # [7]
                    return "幸運"
            else:
                # [ 2  5 31]
                # 42 (2:1)
                if img[42]:
                    # [2]
                    return "入れ食い"
                else:
                    # [ 5 31]
                    # 203 (1:1)
                    if img[203]:
                        # [5]
                        return "貫通"
                    else:
                        # [31]
                        return "パンチ"
else:
    # [ 0  1  4  8  9 11 12 13 14 15 21 23 24 27 28 30 33 34 36 37]
    # 404 (10:10)
    if img[404]:
        # [ 1  8  9 11 23 24 30 34 36 37]
        # 218 (5:5)
        if img[218]:
            # [ 8 11 30 34 36]
            # 4 (3:2)
            if img[4]:
                # [11 36]
                # 10 (1:1)
                if img[10]:
                    # [36]
                    return "落下耐性"
                else:
                    # [11]
                    return "射撃ダメージ増加"
            else:
                # [ 8 30 34]
                # 2 (2:1)
                if img[2]:
                    # [30]
                    return "範囲ダメージ増加"
                else:
                    # [ 8 34]
                    # 3 (1:1)
                    if img[3]:
                        # [34]
                        return "無限"
                    else:
                        # [8]
                        return "高速装填"
        else:
            # [ 1  9 23 24 37]
            # 10 (3:2)
            if img[10]:
                # [1 9]
                # 3 (1:1)
                if img[3]:
                    # [1]
                    return "棘の鎧"
                else:
                    # [9]
                    return "効率強化"
            else:
                # [23 24 37]
                # 9 (2:1)
                if img[9]:
                    # [37]
                    return "防具貫通"
                else:
                    # [23 24]
                    # 74 (1:1)
                    if img[74]:
                        # [24]
                        return "ダメージ増加"
                    else:
                        # [23]
                        return "ダメージ軽減"
    else:
        # [ 0  4 12 13 14 15 21 27 28 33]
        # 412 (5:5)
        if img[412]:
            # [ 4 12 13 14 21]
            # 204 (3:2)
            if img[204]:
                # [14 21]
                # 12 (1:1)
                if img[12]:
                    # [21]
                    return "耐久力"
                else:
                    # [14]
                    return "召雷"
            else:
                # [ 4 12 13]
                # 1 (2:1)
                if img[1]:
                    # [13]
                    return "消滅の呪い"
                else:
                    # [ 4 12]
                    # 2 (1:1)
                    if img[2]:
                        # [4]
                        return "拡散"
                    else:
                        # [12]
                        return "修繕"
        else:
            # [ 0 15 27 28 33]
            # 93 (3:2)
            if img[93]:
                # [ 0 27]
                # 74 (1:1)
                if img[74]:
                    # [27]
                    return "ドロップ増加"
                else:
                    # [0]
                    return "アンデッド特効"
            else:
                # [15 28 33]
                # 408 (2:1)
                if img[408]:
                    # [28]
                    return "ノックバック"
                else:
                    # [15 33]
                    # 420 (1:1)
                    if img[420]:
                        # [33]
                        return "フレイム"
                    else:
                        # [15]
                        return "シルクタッチ"
"""
