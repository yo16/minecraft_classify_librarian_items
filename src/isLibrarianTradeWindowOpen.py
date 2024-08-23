# 画像ファイルから、司書の取引画面が開かれているかどうか判定する
# 画像ファイルは、take_screenshot_continuousで取得した、
# 870 x 519 のキャプチャ画像に限定する

import numpy as np
import cv2

TRADE_MASKED_IMAGE_PATH = "./src/resources/librarian_trade_mask.png"

def is_librarian_trade_window_open(image_path: str) -> bool:
    # 対象画像の読み込み
    img_cur = cv2.imread(image_path)

    # 司書の取引画面以外をマスクしたマスク画像の読み込み
    img_trade_masked = cv2.imread(TRADE_MASKED_IMAGE_PATH)
    # 非マスク領域を抽出（真っ黒以外）
    range_mask = cv2.inRange(img_trade_masked, (1,1,1), (255, 255, 255))

    # 対象画像に非マスク領域を適用して抽出
    img_cur_masked = cv2.bitwise_and(img_cur, img_cur, mask=range_mask)
    #cv2.imwrite("./tmp/tmp2.png", img_cur_masked)

    # 比較
    diff = cv2.absdiff(img_cur_masked, img_trade_masked)
    # ゼロでない部分（一致しない部分）のカウント
    non_zero_count = np.count_nonzero(diff)
    
    # ゼロなら一致
    return (non_zero_count == 0)


if __name__=="__main__":
    # 取引画面
    image_path = "./sample-data/20240823_121533.png"

    # 非取引画面
    image_path = "./sample-data/20240823_121528.png"

    ret = is_librarian_trade_window_open(image_path)
    print(ret)
