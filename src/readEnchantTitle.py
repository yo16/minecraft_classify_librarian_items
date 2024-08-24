# 取引ウィンドウに表示されている２つのアイテムを判定する
# 取引画面が表示されている前提
# もしエンチャントの本のタイトルが表示されていない場合は、何も返さない

import os
import cv2
import numpy as np
import pytesseract
import re

TESSERACT_EXE_PATH = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
TESSERACT_DATA_PATH = "C:\\Program Files\\Tesseract-OCR\\tessdata"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_EXE_PATH
os.environ["PATH"] += os.pathsep + TESSERACT_EXE_PATH
os.environ["TESSDATA_PREFIX"] = TESSERACT_DATA_PATH


def read_enchant_title(img: np.ndarray) -> str:
    ## 検査対象画像
    #img = cv2.imread(img_path)

    # 矩形領域を取り出す
    # (x,y) = 303,107 ～ 562,246
    target_area = img[107:246, 303:562]
    #cv2.imwrite("./tmp/target_area.png", target_area)
    
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
        print("no contours found.")
        return ("", 0)
    #cv2.imwrite("./tmp/found_image.png", found_image)

    # エンチャントの文字（特定の色の部分）だけ取り出す
    lower_bound = np.array([165, 165, 165])
    upper_bound = np.array([170, 170, 170])
    mask_enchant_char = cv2.inRange(found_image, lower_bound, upper_bound)
    # それ以外は全部白、文字は全部黒に変換
    img_enchant_char = np.ones_like(found_image) * 255
    img_enchant_char[mask_enchant_char == 255] = [0, 0, 0]
    #cv2.imwrite("./tmp/img_enchant_char.png", img_enchant_char)

    # グレースケール化
    img_enchant_char_gray = cv2.cvtColor(img_enchant_char, cv2.COLOR_BGR2GRAY)
    #cv2.imwrite("./tmp/img_enchant_char_gray.png", img_enchant_char_gray)

    # 文字の高さに合わせたサイズにする
    img_line_size = img_enchant_char_gray[24:49, :]
    #cv2.imwrite("./tmp/img_line_size.png", img_line_size)

    # OCR
    config = "--psm 7 "
    detected_text = pytesseract.image_to_string(img_line_size, lang='jpn', config=config)
    #print(f"[{detected_text}]")

    # 末尾の改行を取る
    detected_text = detected_text.rstrip("\n")

    # "I"が、"1"と"T"に間違われることがあるので、強制置換（1もTも出てこないはず）
    replaced_text = re.sub(r"[1T]", "I", detected_text)

    ## "I"があった場合は、その前にスペースを１つ入れる
    #replaced_text = re.sub(r"([^\sI]+)(I+)", r"\1 \2", replaced_text)

    # スペースを除去して、(I+)を数値化する
    ret_tuple = None
    match_I = re.search(r"(.*?)(I+)$", replaced_text)
    if match_I:
        prefix = match_I.group(1).replace(" ", "")
        count_I = len(match_I.group(2))
        ret_tuple = (prefix, count_I)
    else:
        ret_tuple = (replaced_text, 0)

    return ret_tuple



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
    # 射撃ダメージ増加 I（幅がちょっと広い）
    image_path = "./sample-data/20240823_185546.png"
    # 射撃ダメージ増加 I（幅がちょっと広い、位置違い）
    image_path = "./sample-data/20240823_185551.png"
    # 水中採掘
    image_path = "./sample-data/20240823_185616.png"
    # 射撃ダメージ増加 III（幅がちょっと広い）
    image_path = "./sample-data/20240823_185644.png"
    # 高速装填 II
    image_path = "./sample-data/20240823_185720.png"
    # パンチ II
    image_path = "./sample-data/20240823_185725.png"
    

    img = cv2.imread(image_path)
    ret = read_enchant_title(img)
    print(ret)

