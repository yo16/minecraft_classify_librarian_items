# マイクラを見て、司書との取引画面が出たらDBへ登録

import time
from isLibrarianTradeWindowOpen import is_librarian_trade_window_open

def monitor_minecraft(
    window_title: str,
    sleep_time: float,
    max_count: int,
):
    # 取引中フラグ(True: 司書との取引ウィンドウが開いている)
    is_trading = False

    for _ in range(max_count):
        time.sleep(sleep_time)

        

        # 司書の取引ウィンドウが開かれているかどうか判定する
        if (is_librarian_trade_window_open())




if __name__=="__main__":
    window_title = "Minecraft 1.21.1 - シングルプレイ"
    sleep_time = 0.5
    max_count = 10

    monitor_minecraft(
        window_title,
        sleep_time,
        max_count
    )

