# マイクラを見て、司書との取引画面が出たらDBへ登録

import time
import mss
import numpy as np
import cv2

from getWindowSize import get_window_size
from isLibrarianTradeWindowOpen import is_librarian_trade_window_open
from classifyItems import classify_items
from readEnchantTitle import read_enchant_title
from readEnchantPrice import read_enchant_price
from saveTradeInfo import save_trade_info, TradeInfo

def monitor_minecraft(
    window_title: str,
    sleep_time: float,
    max_count: int,
    debug_mode: bool = False
):
    # ウィンドウサイズを取得する
    # "left", "top", "width", "height"のdictが返る
    # （ウィンドウの位置は、ずらしちゃダメ）
    win_size = get_window_size(window_title)
    if not win_size:
        print(f"window not found: {window_title}")
        return

    # 取引中フラグ(True: 司書との取引ウィンドウが開いている)
    is_trading = False

    for i in range(max_count):
        time.sleep(sleep_time)
        print("0: monitor!") if debug_mode else None

        # キャプチャして、numpyの配列化
        img_rgb = None
        with mss.mss() as sct:
            screenshot = sct.grab(win_size)
            img_rgb = np.array(screenshot)
        # RGBからBGRに変換 (cv2のデフォルトがBGRのため)
        #img = img_rgb[..., :3][:, :, ::-1]
            # BGRAからBGRに変換（Alphaチャンネルを除外）
        #img_bgr = np.array(screenshot)[..., :3]
        img = np.array(img_rgb)[..., :3]


        # 司書の取引ウィンドウが開かれているかどうか判定する
        cv2.imwrite(f"./tmp/win_{i}.png", img)
        if not is_librarian_trade_window_open(img):
            # 開かれていない場合は、取引フラグをFalseにして、ループのトップへ戻る
            is_trading = False
            print("1: is_librarian_trade_window_open: FALSE") if debug_mode else None
            continue
        # 以降は、取引ウィンドウが開かれている

        # 取引フラグが立っているとき、前回のウィンドウが開いたままになっている
        # すでにキャプチャして解析した後のはずなので、何もせずループのトップへ戻る
        if is_trading:
            print("2: IS TRADING") if debug_mode else None
            continue
        # 以降は、取引ウィンドウが開かれていて、取引フラグがFalse

        # 取引フラグを立てる
        is_trading = True

        # 取引ウィンドウに表示されている２つのアイテムを判定する
        # 0:紙, 1:本棚, 2:エンチャント本
        items = classify_items(img)
        print(f"3-1: {items[0]}") if debug_mode else None
        print(f"3-2: {items[1]}") if debug_mode else None

        # 紙と本棚だけの場合は、その内容をDBに登録
        if items[0] != 2 and items[1] != 2:
            ti1 = TradeInfo(items[0])
            ti2 = TradeInfo(items[1])
            print(ti1.to_string())
            print(ti2.to_string())
            save_trade_info(ti1, ti2)
            continue

        # エンチャントの本の場合は、その内容を判定する
        # タイトル
        enchant_title, enchant_level = read_enchant_title(img)
        if len(enchant_title) == 0:
            # エンチャント本の内容が取れていない場合はなにもしない
            print(f"5: NO TITLE!") if debug_mode else None
            cv2.imwrite("./tmp/no_title.png", img) if debug_mode else None
            # 取引フラグを倒す
            is_trading = False
            continue
        # 価格
        enchant_line = 1 if items[0] == 2 else 2
        enchant_price = read_enchant_price(img, enchant_line)

        # DBへ登録
        enchant_trade_info = TradeInfo(
            2,                  # 2: エンチャント本
            enchant_title,
            enchant_level,
            enchant_price
        )
        ti1 = TradeInfo(items[0]) if items[0]!=2 else enchant_trade_info
        ti2 = TradeInfo(items[1]) if items[1]!=2 else enchant_trade_info
        print(ti1.to_string())
        print(ti2.to_string())
        save_trade_info(ti1, ti2)




if __name__=="__main__":
    window_title = "Minecraft 1.21.1 - シングルプレイ"
    sleep_time = 0.2
    max_count = int(60 / sleep_time)     # 合計秒数/slee_time

    monitor_minecraft(
        window_title,
        sleep_time,
        max_count,
        debug_mode=False
    )

