# エンチャント本の価格を取得する
# エンチャント本はあり、その位置（１行目か２行目か）はわかっている前提
# tesseractが数字を読めないので、力技で読む

import os
import cv2
import numpy as np
import re



# 高価に訂正されているかどうかを判定するピクセルの、全体の座標(x, y)
CHECK_COORDINATE = (192, 167)
# このピクセルの色が赤のときは、高価に訂正されている
IS_HIGHPRICE_COLOR_RGB = (186, 55, 15)

# １段目の座標、２段目の場合はy+=40
LINE_OFFSET = 40
# 高価に訂正されている場合は、x+=28
HIGH_OFFSET = 28

# 全体のx1, y1, x2, y2 = 186, 159, 239, 176
# 有効な価格の開始位置 通常x1, y1, 訂正x2, y2 = 186, 159, 214, 159
# 幅, 高さ：26, 18
# 金額の矩形領域(x1, y1, x2, y2)（上の段の正常価格の場合）
PRICE_RECT = (186, 159, 186+26, 159+18)

# 価格の文字色()
PRICE_RGB = (252, 252, 252)

def read_enchant_price(img: np.ndarray, enchant_line: int) -> int:

    # ２段目の場合に加算するオフセット値、１段目の場合はゼロ
    line_offset = (enchant_line-1) * LINE_OFFSET
    #print(f"offset:{line_offset}")

    # 通常版か訂正版(rgb=186,55,15)かを判定
    b, g, r = img[CHECK_COORDINATE[1]+line_offset, CHECK_COORDINATE[0]]
    #print(f"{r}, {g}, {b}")
    is_normal_price = False \
        if r == IS_HIGHPRICE_COLOR_RGB[0] and \
           g == IS_HIGHPRICE_COLOR_RGB[1] and \
           b == IS_HIGHPRICE_COLOR_RGB[2] \
        else True
    high_offset = 0 if is_normal_price else HIGH_OFFSET
    #print(f"is_normal_price: {is_normal_price}")

    # 数値の領域を取得
    img_price = img[
        PRICE_RECT[1] + line_offset : PRICE_RECT[3] + line_offset,
        PRICE_RECT[0] + high_offset : PRICE_RECT[2] + high_offset
    ]

    # それ以外は全部白、文字は全部黒に変換
    col_price = np.array([PRICE_RGB[2], PRICE_RGB[1], PRICE_RGB[0]])
    mask_enchant_price = cv2.inRange(img_price, col_price, col_price)
    #cv2.imwrite("./tmp/mask_enchant_price.png", mask_enchant_price)
    img_enchant_price = np.ones_like(img_price) * 255
    img_enchant_price[mask_enchant_price == 255] = [0, 0, 0]
    #cv2.imwrite("./tmp/img_enchant_price.png", img_enchant_price)

    # 数字を読む
    price_int = to_int(img_enchant_price)

    return price_int


def to_int(img: np.ndarray) -> int:
    # １桁目
    n1 = parse_one(img[2:15, 2:11])
    # ２桁目
    n2 = parse_one(img[2:15, 14:23])

    return n1*10 + n2


# １文字の数字を読む
# 2x2ドットで、1ドットのような描き方をしているので
# 実質は5x7ピクセルだが、単純に2倍した座標値を見ている
def parse_one(img: np.ndarray) -> int:
    if img[10, 6, 0] == 0:
        return 9
    elif img[8, 6, 0] == 0:
        return 4
    elif img[2, 4, 0] == 0:
        return 1
    elif img[12, 0, 0] == 0:
        return 2
    elif img[4, 2, 0] == 0:
        return 5
    elif img[2, 2, 0] == 0:
        return 6
    elif img[0, 0, 0] == 0:
        return 7
    elif img[6, 0, 0] == 0:
        return 0
    elif img[6, 2, 0] == 0:
        return 8
    elif img[2, 0, 0] == 0:
        return 3
    
    # １桁目がない場合（１の位のみの数字）
    return 0



if __name__=="__main__":
    # 通常
    image_path, line, expected = ("./sample-data/20240823_121543.png", 1, 8)
    image_path, line, expected = ("./sample-data/20240823_121548.png", 1, 18)
    image_path, line, expected = ("./sample-data/20240823_121613.png", 1, 39)
    image_path, line, expected = ("./sample-data/20240823_121734.png", 1, 9)
    image_path, line, expected = ("./sample-data/20240823_121744.png", 1, 31)
    image_path, line, expected = ("./sample-data/20240823_121750.png", 1, 31)
    image_path, line, expected = ("./sample-data/20240823_121755.png", 2, 32)
    image_path, line, expected = ("./sample-data/20240823_121800.png", 2, 11)
    image_path, line, expected = ("./sample-data/20240823_121805.png", 2, 41)
    image_path, line, expected = ("./sample-data/20240823_121810.png", 2, 20)
    image_path, line, expected = ("./sample-data/20240823_121815.png", 2, 20)

    # 訂正
    image_path, line, expected = ("./sample-data/20240823_185546.png", 1, 18)
    image_path, line, expected = ("./sample-data/20240823_185551.png", 1, 18)
    image_path, line, expected = ("./sample-data/20240823_185556.png", 1, 18)
    image_path, line, expected = ("./sample-data/20240823_185601.png", 1, 18)
    image_path, line, expected = ("./sample-data/20240823_185616.png", 2, 11)
    image_path, line, expected = ("./sample-data/20240823_185621.png", 2, 11)
    image_path, line, expected = ("./sample-data/20240823_185639.png", 1, 46)
    image_path, line, expected = ("./sample-data/20240823_185644.png", 1, 46)
    image_path, line, expected = ("./sample-data/20240823_185649.png", 1, 46)
    image_path, line, expected = ("./sample-data/20240823_185709.png", 1, 46)
    image_path, line, expected = ("./sample-data/20240823_185720.png", 2, 27)
    image_path, line, expected = ("./sample-data/20240823_185725.png", 1, 33)
    

    img = cv2.imread(image_path)
    ret = read_enchant_price(img, line)
    print(f"{expected} - {ret}")

