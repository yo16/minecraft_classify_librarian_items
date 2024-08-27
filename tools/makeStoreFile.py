# title_store.pklを作る
# readEnchantTitle.pyを改造して作ったので、関数名がアレだが、まぁ一時的なものだから。


# 表示されているエンチャント本のタイトルを取得する
# 取引画面が表示されている前提
# もしエンチャントの本のタイトルが表示されていない場合は、何も返さない

import os
import sys
import cv2
import numpy as np
from typing import Tuple
import pickle



# Lv画像を読んでおく
LV_IMAGES = [
    cv2.imread("./src/resources/lv1.png", cv2.IMREAD_GRAYSCALE),
    cv2.imread("./src/resources/lv2.png", cv2.IMREAD_GRAYSCALE),
    cv2.imread("./src/resources/lv3.png", cv2.IMREAD_GRAYSCALE),
    cv2.imread("./src/resources/lv4.png", cv2.IMREAD_GRAYSCALE),
    cv2.imread("./src/resources/lv5.png", cv2.IMREAD_GRAYSCALE),
]



# 全体のキャプチャ画像から、エンチャント本の文字だけのグレイスケールの画像に変換する
def img_preprocess(img: np.ndarray, debug_mode=False, invert=True, text_padding=0) -> np.ndarray | None:
    # エンチャントの本のタイトルが出る矩形領域を取り出す
    # (x,y) = 290,100 ～ 570,270
    target_area = img[100:270, 290:570]
    cv2.imwrite("./tmp/target_area.png", target_area) if debug_mode else None
    
    # BGRからHSVに変換
    hsv = cv2.cvtColor(target_area, cv2.COLOR_BGR2HSV)
    
    # 紫の矩形のマスクを定義
    # photoshop:0-360, 100%, 100% → cv2:0-180, 0-255, 0-255
    lower_purple = np.array([250/2, 0.75*255, 0.2*255])
    upper_purple = np.array([280/2, 255, 0.4*255])
    mask = cv2.inRange(hsv, lower_purple, upper_purple)

    # マスクに輪郭を適用
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 輪郭を確認
    found_image = None
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        if (w>150 and h>50):
            #print("found!")
            #cv2.imwrite(f"./tmp/contour_{i}.png", target_area[y:y+h, x:x+w])
            found_image = target_area[y:y+h, x:x+w]     # GBRの画像から取り出す
    if found_image is None:
        #print("no contours found.")
        return None
    cv2.imwrite("./tmp/found_image.png", found_image) if debug_mode else None

    # エンチャント文字の部分だけ取り出す
    img_line_size = found_image[(30-text_padding):(45+text_padding), (7-text_padding):]
    cv2.imwrite("./tmp/img_line_size.png", img_line_size) if debug_mode else None
    found_image2 = img_line_size

    # 横幅のサイズを整形する（横幅を200pxにする）
    height, width, color = found_image2.shape
    img_resized = np.zeros((height, 200, color), dtype=int)
    img_resized[:height, :width, :] = found_image2

    # エンチャントの文字（特定の色の部分）だけ取り出す
    lower_bound = np.array([165, 165, 165])
    upper_bound = np.array([170, 170, 170])
    mask_enchant_char = cv2.inRange(img_resized, lower_bound, upper_bound)
    cv2.imwrite("./tmp/mask_enchant_char1.png", mask_enchant_char) if debug_mode else None
    if np.all(mask_enchant_char == 0):
        # エンチャントの文字色がない → 呪い系の文字色で探す
        lower_bound = np.array([79, 79, 247])
        upper_bound = np.array([89, 89, 255])
        mask_enchant_char = cv2.inRange(img_resized, lower_bound, upper_bound)
        cv2.imwrite("./tmp/mask_enchant_char2.png", mask_enchant_char) if debug_mode else None
    cv2.imwrite("./tmp/img_enchant_char.png", img_resized) if debug_mode else None

    # 白黒反転（白地に黒の文字にする）
    if invert:
        img_enchant_char = np.ones_like(img_resized, dtype=np.uint8) * 255
        img_enchant_char[mask_enchant_char == 255] = [0, 0, 0]

        # グレースケール化
        img_enchant_char_gray = cv2.cvtColor(img_enchant_char, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("./tmp/img_enchant_char_gray.png", img_enchant_char_gray)
    else:
        img_enchant_char_gray = mask_enchant_char

    ## ２倍にしてみる
    #img_line_size_x2 = cv2.resize(img_enchant_char_gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    ##cv2.imwrite("./tmp/img_line_size_x2.png", img_line_size_x2) if debug_mode else None

    #return img_line_size_x2
    return img_enchant_char_gray



# タイトルとレベルを読む
def read_enchant_title(img: np.ndarray, debug_mode=False, tmp_title="") -> Tuple[str, int]:
    # 画像前処理
    img_text = img_preprocess(img, debug_mode, text_padding=0, invert=False)
    if img_text is None:
        return ("", 0)
    
    # 一番右端のindexを取得
    max_rightmost_index = np.max(np.where(img_text == 255)[1])
    #print(max_rightmost_index)

    # 画像の終了位置は含めないため、+1しておく
    max_rightmost_index += 1

    # LV_IMAGESと比較
    lv = 0
    rtrim_width = 0     # Lvの分を除去する幅
    for i, lv_img in enumerate(LV_IMAGES):
        # 右端から比較
        _, lv_img_width = lv_img.shape
        if debug_mode:
            cv2.imwrite(f"./tmp/lv_{(i+1)}_target.png", img_text[:, max_rightmost_index-lv_img_width:max_rightmost_index])
            cv2.imwrite(f"./tmp/lv_{(i+1)}_comp.png", lv_img)
        if np.array_equal(
            img_text[:, max_rightmost_index-lv_img_width:max_rightmost_index],
            lv_img
        ):
           # 見つけた
           lv = i + 1
           rtrim_width = lv_img_width
           break
    print(f"Lv:{lv}")

    # Lvを除いた文字を取り出す
    img_pure_title = img_text[:, :max_rightmost_index-rtrim_width]
    cv2.imwrite("./tmp/img_pure_title.png", img_pure_title) if debug_mode else None

    # もう一度15x200pxに整形して、1次元配列化
    img_title = np.zeros((15, 200), dtype=np.uint8)
    img_title[:, :max_rightmost_index-rtrim_width] = img_pure_title
    #cv2.imwrite("./tmp/img_title.png", img_title) if debug_mode else None
    img_title_line = img_title.flatten()
    #print(img_title_line.shape)


    pickle_file_path = "./tmp/title_store.pkl"
    if os.path.exists(pickle_file_path):
        with open(pickle_file_path, "rb") as f:
            title_store = pickle.load(f)
    else:
        title_store = {
            "data": [
                {
                    "name": tmp_title,
                    "line": img_title_line,
                },
            ],
        }
        with open(pickle_file_path, "wb") as f:
            pickle.dump(title_store, f)
    # titleが登録済みか、未登録かを判断し、未登録だったら追加
    is_registered = False
    found_line = []
    for title_obj in title_store["data"]:
        if tmp_title == title_obj["name"]:
            # 発見！
            is_registered = True
            found_line = title_obj["line"]
            break
    # 未登録だったら登録
    if not is_registered:
        print(f"登録：{tmp_title}")
        title_store["data"].append({
            "name": tmp_title,
            "line": img_title_line
        })
        with open(pickle_file_path, "wb") as f:
            pickle.dump(title_store, f)
    else:
        print(f"登録済みでした: {tmp_title}")
        # 念のため、完全一致を確認
        if np.array_equal(
            np.array(found_line),
            img_title_line
        ):
            print("一致OK！")
        else:
            print("lineが一致してません！")
            return (tmp_title, 99)


    return (tmp_title, lv)





if __name__=="__main__":
    # 表示なし
    image_path = "./sample-data/20240823_121533.png"
    image_path = "./sample-data/20240823_185556.png"
    image_path = "./sample-data/20240823_185601.png"
    image_path = "./sample-data/20240823_185606.png"
    image_path = "./sample-data/20240823_185621.png"
    image_path = "./sample-data/20240823_185626.png"
    image_path = "./sample-data/20240823_185639.png"
    # 位置が違う場所にある本
    image_path = "./sample-data/20240823_185659.png"
    

    # 幸運 II
    image_path = "./sample-data/20240823_121543.png"
    # 射撃ダメージ増加 I
    image_path = "./sample-data/20240823_185546.png"
    # 射撃ダメージ増加 I
    image_path = "./sample-data/20240823_185551.png"
    # 水中採掘
    #image_path = "./sample-data/20240823_185616.png"
    # 射撃ダメージ増加 III
    #image_path = "./sample-data/20240823_185644.png"
    # 高速装填 II
    #image_path = "./sample-data/20240823_185720.png"
    ## パンチ II
    #image_path = "./sample-data/20240823_185725.png"
    ## 束縛の呪い
    #image_path = "./sample-data/sokubaku.png"
    ## ノックバック I
    image_path = "./sample-data/knockback1.png"
    ## 氷渡り II
    #image_path = "./sample-data/koori2.png"
    ## 効率強化 IV
    #image_path = "./sample-data/koritsu4.png"
    ## フレイム
    #image_path = "./sample-data/flame.png"
    ## 棘の鎧 III
    #image_path = "./sample-data/toge3.png"
    ## ダメージ増加 V
    #image_path = "./sample-data/damage5.png"
    ## 範囲ダメージ増加 II
    #image_path = "./sample-data/hanni2.png"
    ## ノックバック II
    #image_path = "./sample-data/knockback2.png"
    ## 棘の鎧 II
    #image_path = "./sample-data/toge2.png"
    ## 虫特効 II
    #image_path = "./sample-data/mushi2.png"
    ## 忠誠 II
    #image_path = "./sample-data/chuusei2.png"
    ## 防具貫通 II
    #image_path = "./sample-data/bougu_kantsu2.png"
    ## 防具貫通 IV
    #image_path = "./sample-data/bougu_kantsu4.png"
    ## 無限
    #image_path = "./sample-data/mugen.png"
    ## アンデッド特効 V
    #image_path = "./sample-data/undead5.png"
    ## 入れ食い III
    #image_path = "./sample-data/iregui3.png"
    ## 火炎耐性 IV
    #image_path = "./sample-data/kaen_taisei4.png"
    ## 幸運 III
    #image_path = "./sample-data/kouun3.png"
    ## 修繕
    #image_path = "./sample-data/shuuzen.png"
    ## 消滅の呪い
    #image_path = "./sample-data/shometsu.png"
    ## シルクタッチ
    #image_path = "./sample-data/silk_touch.png"
    ## 水生特効 V
    #image_path = "./sample-data/suisei_tokkou5.png"
    ## 水中呼吸 III
    #image_path = "./sample-data/suichuu_kokyuu3.png"
    ## 水中歩行 III
    #image_path = "./sample-data/suichuu_hokou3.png"
    ## 耐久力 III
    #image_path = "./sample-data/taikyuuryoku3.png"
    ## 宝釣り III
    #image_path = "./sample-data/takara3.png"
    ## ダメージ軽減 IV
    #image_path = "./sample-data/damage_keigen4.png"
    ## ドロップ増加 III
    #image_path = "./sample-data/drop_zouka3.png"
    ## 火属性 II
    image_path = "./sample-data/hizokusei2.png"
    # 落下耐性 IV
    #image_path = "./sample-data/rakka_taisei4.png"
    # 幸運 I
    image_path = "./sample-data/kouun1.png"

    #img = cv2.imread(image_path)
    #ret = read_enchant_title(img, debug_mode=True, tmp_title="幸運")
    #print(ret)

    #img2 = img_preprocess(img, debug_mode=False, invert=False, text_padding=0)
    #cv2.imwrite("./tmp/img_preprocess_out.png", img2)
    #print(img2.shape)
    ## 一番右端のindexを取得
    #max_rightmost_index = np.max(np.where(img2 == 255)[1])
    #print(max_rightmost_index)

    if True:
        import json
        # JSONファイルを読み込む
        json_file_path = "./sample-data/data_map.json"
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data_map = json.load(file)
        
        for i, img_info in enumerate(data_map["data"]):
            if len(img_info["file_name"]) == 0:
                continue

            image_path = f"./sample-data/{img_info["file_name"]}"
            if not os.path.exists(image_path):
                print(f"ファイルがないっ！{i}")
                print(image_path)
                sys.exit(90)
            img = cv2.imread(image_path)

            ret = read_enchant_title(img, debug_mode=True, tmp_title=img_info["enchant"])

            if ret[1] != img_info["level"]:
                print(f"レベルが違う！{i}")
                print(ret[1])
                sys.exit(91)

