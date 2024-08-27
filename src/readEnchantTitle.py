# 表示されているエンチャント本のタイトルを取得する
# 取引画面が表示されている前提
# もしエンチャントの本のタイトルが表示されていない場合は、何も返さない

import os
import sys
import cv2
import numpy as np
#import pytesseract
#import re
from typing import Tuple

#TESSERACT_EXE_PATH = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
#TESSERACT_DATA_PATH = "C:\\Program Files\\Tesseract-OCR\\tessdata"
#
#pytesseract.pytesseract.tesseract_cmd = TESSERACT_EXE_PATH
#os.environ["PATH"] += os.pathsep + TESSERACT_EXE_PATH
#os.environ["TESSDATA_PREFIX"] = TESSERACT_DATA_PATH

from .judgeTitle import judge_title


# Lv画像を読んでおく
LV_IMAGES = [
    cv2.imread("./src/resources/lv1.png", cv2.IMREAD_GRAYSCALE),
    cv2.imread("./src/resources/lv2.png", cv2.IMREAD_GRAYSCALE),
    cv2.imread("./src/resources/lv3.png", cv2.IMREAD_GRAYSCALE),
    cv2.imread("./src/resources/lv4.png", cv2.IMREAD_GRAYSCALE),
    cv2.imread("./src/resources/lv5.png", cv2.IMREAD_GRAYSCALE),
]



# 全体のキャプチャ画像から、エンチャント本の文字だけのグレイスケールの画像に変換する
def img_preprocess(img: np.ndarray, debug_mode=False, invert=False, text_padding=0) -> np.ndarray | None:
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



## エンチャント本のタイトル部分の文字とレベルを取り出す
#def read_enchant_title_ocr(img: np.ndarray, debug_mode=False) -> Tuple[str, int]:
#    # 画像前処理
#    img2 = img_preprocess(img, debug_mode, text_padding=7)
#    if img2 is None:
#        return ("", 0)
#
#    # OCR
#    config = "--psm 7 "
#    #detected_text = pytesseract.image_to_string(img_line_size, lang='jpn', config=config)
#    #detected_text = pytesseract.image_to_string(img_line_size, lang='jpn', config=config)
#    detected_text = pytesseract.image_to_string(img2, lang='jpn', config=config)
#    print(f"0[{detected_text}]") if debug_mode else None
#
#    # 末尾の改行を取る
#    replaced_text = detected_text.rstrip("\n")
#
#    print(f"1[{replaced_text}]") if debug_mode else None
#
#    # 防具[叶結]通 1 → 防具貫通 IV
#    replaced_text = re.sub(r"防具[叶結]通 1", "防具貫通 IV", replaced_text)
#    replaced_text = re.sub(r"防具[叶結]通", "防具貫通", replaced_text)
#    # "[IT]" → "I"
#    replaced_text = re.sub(r"[1T]", "I", replaced_text)
#    # "IHI" → "II"
#    replaced_text = replaced_text.replace("IHI", "II")
#    #replaced_text = re.sub(r"[1Tエ]", "I", replaced_text)
#    print(f"2[{replaced_text}]") if debug_mode else None
#    # "M" → "IV"
#    replaced_text = re.sub(r"IM", "IV", replaced_text)
#    # "U" → "V"
#    replaced_text = re.sub(r"U", "V", replaced_text)
#    # "ノックバック"が、"フックタバッタ"とか"フックタバパック"とかに間違われるので、強制置換
#    # （"ノックバック"は、そのあとのIもひどい。「フックタバック Tエ」になる。明朝体が苦手か）
#    replaced_text = re.sub(r"[ノメフブ][ッツ][クタ]{1,2}[バパ]{1,2}ッ[クタ]{1,2}", "ノックバック", replaced_text)
#    # "ノックバック"の後ろに"エ"があったら捨てる
#    replaced_text = re.sub(r"(ノックバック.*)[エｴ]", r"\1", replaced_text)
#    # "ノックバック"の後ろに"エ"があったら捨てる
#    replaced_text = re.sub(r"(ノックバック.*)[エｴ]", r"\1", replaced_text)
#    # "パッチ" → "パンチ"
#    replaced_text = re.sub(r"パッ[ン]?チ", r"パンチ", replaced_text)
#    # "パンチ"の後ろに"エ"があったらIにする
#    replaced_text = re.sub(r"パンチ\s*エ", "パンチ I", replaced_text)
#    # "東縛" → "束縛"
#    replaced_text = re.sub("[束東][縛績]", "束縛", replaced_text)
#    # "来渡" → "氷渡"
#    replaced_text = re.sub("[来求]渡", "氷渡", replaced_text)
#    # フレイょふ → フレイム
#    replaced_text = re.sub(r"フレイ[ょよ]?[ふム]", "フレイム", replaced_text)
#    # 還の鏡 → 棘の鎧
#    replaced_text = re.sub(r"[還練壇棘]の[鏡鐘鎧]", "棘の鎧", replaced_text)
#    # 箇囲 → 範囲
#    replaced_text = re.sub(r"箇囲", "範囲", replaced_text)
#    # 申 → 虫
#    replaced_text = re.sub(r"申", "虫", replaced_text)
#    # ダ[ュユ]メージ → ダメージ
#    replaced_text = re.sub(r"ダメ?[ユュ]?メージ", "ダメージ", replaced_text)
#    # ダメージ増加 V
#    replaced_text = re.sub(r"ダメージ増加見", "ダメージ増加 V", replaced_text)
#    # ダメージ増加の後に、何もない場合はV
#    replaced_text = re.sub(r"ダメージ増加$", "ダメージ増加 V", replaced_text)
#    # 恵語 → 忠誠
#    replaced_text = re.sub(r"[忠恵員][誠語]", "忠誠", replaced_text)
#    # 消漠 → 消滅
#    replaced_text = replaced_text.replace("消漠", "消滅")
#    
#
#    ## "I"があった場合は、その前にスペースを１つ入れる
#    replaced_text = re.sub(r"([^\sI]+)(I+)", r"\1 \2", replaced_text)
#
#    # スペースを除去して、(I+)を数値化する
#    ret_tuple = None
#    match_IV = re.search(r"(.*?)IV$", replaced_text)
#    match_V = re.search(r"(.*?)V$", replaced_text)
#    match_I = re.search(r"(.*?)(I+)$", replaced_text)
#    if match_IV:
#        prefix = match_IV.group(1).replace(" ", "")
#        ret_tuple = (prefix, 4)
#    elif match_V:
#        prefix = match_V.group(1).replace(" ", "")
#        ret_tuple = (prefix, 5)
#    elif match_I:
#        prefix = match_I.group(1).replace(" ", "")
#        count_I = len(match_I.group(2))
#        ret_tuple = (prefix, count_I)
#    else:
#        print("Lv is not found!")
#        ret_tuple = (replaced_text, 0)
#
#    return ret_tuple


# 前処理後のテキストの部分の画像から、Lvを取得するとともに、Lvを消した画像(200x15 pixcel)を返す
def get_and_erase_level(img_text: np.ndarray, debug_mode: bool=False) -> Tuple[int, np.ndarray]:
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

    # Lvを除いた文字を取り出す
    img_pure_title = img_text[:, :max_rightmost_index-rtrim_width]
    cv2.imwrite("./tmp/img_pure_title.png", img_pure_title) if debug_mode else None

    # もう一度200x15pxに整形
    img_title = np.zeros((15, 200), dtype=np.uint8)
    img_title[:, :max_rightmost_index-rtrim_width] = img_pure_title
    cv2.imwrite("./tmp/img_title.png", img_title) if debug_mode else None

    return (lv, img_title)


# タイトルとレベルを読む
def read_enchant_title(img: np.ndarray, debug_mode=False) -> Tuple[str, int]:
    # 画像前処理
    img_text = img_preprocess(img, debug_mode, text_padding=0, invert=False)
    if img_text is None:
        return ("", 0)
    
#    # 一番右端のindexを取得
#    max_rightmost_index = np.max(np.where(img_text == 255)[1])
#    #print(max_rightmost_index)
#
#    # 画像の終了位置は含めないため、+1しておく
#    max_rightmost_index += 1
#
#    # LV_IMAGESと比較
#    lv = 0
#    rtrim_width = 0     # Lvの分を除去する幅
#    for i, lv_img in enumerate(LV_IMAGES):
#        # 右端から比較
#        _, lv_img_width = lv_img.shape
#        if debug_mode:
#            cv2.imwrite(f"./tmp/lv_{(i+1)}_target.png", img_text[:, max_rightmost_index-lv_img_width:max_rightmost_index])
#            cv2.imwrite(f"./tmp/lv_{(i+1)}_comp.png", lv_img)
#        if np.array_equal(
#            img_text[:, max_rightmost_index-lv_img_width:max_rightmost_index],
#            lv_img
#        ):
#           # 見つけた
#           lv = i + 1
#           rtrim_width = lv_img_width
#           break
#
#    # Lvを除いた文字を取り出す
#    img_pure_title = img_text[:, :max_rightmost_index-rtrim_width]
#    cv2.imwrite("./tmp/img_pure_title.png", img_pure_title) if debug_mode else None
#
#    # もう一度200x15pxに整形して、1次元配列化
#    img_title = np.zeros((15, 200), dtype=np.uint8)
#    img_title[:, :max_rightmost_index-rtrim_width] = img_pure_title
#    cv2.imwrite("./tmp/img_title.png", img_title) if debug_mode else None
#    img_title_line = img_title.flatten()
#    cv2.imwrite("./tmp/img_title_line.png", img_title_line) if debug_mode else None
    
    # 前処理後のテキストの部分の画像から、Lvを取得するとともに、Lvを消した画像(200x15 pixcel)を返す
    lv, img_title = get_and_erase_level(img_text, debug_mode)

    # １次元化
    img_title_line = img_title.flatten()
    #cv2.imwrite("./tmp/img_title_line.png", img_title_line) if debug_mode else None
    
    # 判断
    title_text = judge_title(img_title_line)
    
    return (title_text, lv)




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
    image_path = "./sample-data/flame.png"
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
    image_path = "./sample-data/mushi2.png"
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
    #image_path = "./sample-data/hizokusei2.png"
    # 落下耐性 IV
    #image_path = "./sample-data/rakka_taisei4.png"
    # 幸運 I
    #image_path = "./sample-data/kouun1.png"

    img = cv2.imread(image_path)
    ret = read_enchant_title(img, debug_mode=True)
    print(ret)

    #img2 = img_preprocess(img, debug_mode=False, invert=False, text_padding=0)
    #cv2.imwrite("./tmp/img_preprocess_out.png", img2)
    #print(img2.shape)
    ## 一番右端のindexを取得
    #max_rightmost_index = np.max(np.where(img2 == 255)[1])
    #print(max_rightmost_index)

    

