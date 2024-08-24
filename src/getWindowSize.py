# 指定されたウィンドウタイトルのウィンドウを取得し、サイズを返す
# 取得できないときは、Noneを返す

import pygetwindow as gw
from typing import Dict

def get_window_size(window_title: str) -> Dict[str, int] | None:
    # ウィンドウを取得
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        return None
    
    # ひとつという前提
    win = windows[0]

    return {
        "left": win.left,
        "top": win.top,
        "width": win.width,
        "height": win.height
    }


if __name__=="__main__":
    win_title = "Minecraft 1.21.1 - シングルプレイ"
    win_title = "minecraft_classify_librarian_items"
    ret = get_window_size(win_title)

    if ret:
        print(ret["left"])
        print(ret["top"])
        print(ret["width"])
        print(ret["height"])
    else:
        print("not found")
