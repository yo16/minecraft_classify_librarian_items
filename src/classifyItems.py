# 取引ウィンドウに表示されている２つのアイテムを判定する
# 取引画面が表示されている前提

import numpy as np
import cv2

ITEM_RECT = (
    {'x1': 170, 'y1': 143, 'x2': 342, 'y2': 179},
    {'x1': 170, 'y1': 183, 'x2': 342, 'y2': 219},
)
# １アイテムの紙の部分（１アイテム画像中の、x:10, y:0, w:32, h: 36）
IMG_IS_PAPER: np.ndarray = cv2.imread("./src/resources/trade_paper.png")
# １アイテムの本の部分（１アイテム画像中の、x:67, y:0, w:32, h: 36）
IMG_IS_BOOK: np.ndarray = cv2.imread("./src/resources/trade_book.png")

def classify_items(img: np.ndarray) -> tuple:
    # 固定で２つの領域を取り出す
    # 1. x1:170, y1:143, x2: 342, y2: 179
    # 2. x1:170, y1:183, x2: 342, y2: 219

    ## 検査対象画像
    #img = cv2.imread(image_path)
    ##cv2.imwrite("./tmp/tmp0.png", img)

    # 検査部分の取り出し
    roi_img = img[
        ITEM_RECT[0]['y1']:ITEM_RECT[0]['y2'],
        ITEM_RECT[0]['x1']:ITEM_RECT[0]['x2'],
    ]
    #cv2.imwrite("./tmp/tmp1.png", roi_img)
    ret1 = classify_item_oneline(roi_img)

    roi_img = img[
        ITEM_RECT[1]['y1']:ITEM_RECT[1]['y2'],
        ITEM_RECT[1]['x1']:ITEM_RECT[1]['x2'],
    ]
    #cv2.imwrite("./tmp/tmp2.png", roi_img)
    ret2 = classify_item_oneline(roi_img)

    return (ret1, ret2)


# １つのアイテムの部分（w:172, h:36）から、内容を返す
# 0: 紙, 1: 本棚, 2: 本
def classify_item_oneline(img: np.ndarray) -> int:
    # 画像と非マスク領域が一致しているか確認
    def is_same_img(img_target: np.ndarray, roi_coords: tuple, img_mask: np.ndarray) -> bool:
        # img_targetから、比較する矩形領域を抽出
        x1, y1, x2, y2 = roi_coords
        img_target_area = img_target[y1:y2, x1:x2]

        # マスク画像を、(真っ黒)=0 と そうでない=1 部分に分離
        img_clear_mask = cv2.inRange(img_mask, (1,1,1), (255, 255, 255))

        # 対象画像から、非マスク領域を抽出
        img_target_masked = cv2.bitwise_and(img_target_area, img_target_area, mask=img_clear_mask)

        # マスクがかけれた対象画像と、マスク画像を比較
        diff = cv2.absdiff(img_target_masked, img_mask)
        # 違いがゼロだったら一致
        return (np.count_nonzero(diff)==0)

    # 交換アイテムの１つ目と、紙の画像の比較
    if (is_same_img(img, (10,0, 42,36), IMG_IS_PAPER)):
        return 0
    
    # 交換アイテムの２つ目と、本の画像の比較
    if (is_same_img(img, (68,0, 100,36), IMG_IS_BOOK)):
        return 2
    
    # 本棚
    return 1




if __name__=="__main__":
    # 本(2), 本棚(1)
    image_path = "./sample-data/20240823_121533.png"
    # 紙(0), 本(2)
    #image_path = "./sample-data/20240823_121810.png"

    img = cv2.imread(image_path)

    #ret = classify_items(img)
    #print(ret)

    ret1, ret2 = classify_items(img)
    print(ret1)
    print(ret2)
