import json
import os
import cv2
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from src.readEnchantTitle import img_preprocess, get_and_erase_level


# data_map.jsonを使って、judgeTitleで使う、文字だけの200x15の画像を作る
def make_test_data_judgeTitle():
    # jsonを読む
    json_path = "./sample-data/data_map.json"
    with open(json_path, mode="r", encoding="utf-8") as f:
        data_map = json.load(f)
    
    # サンプルデータから、Lv抜きの画像だけを抽出する
    for file_info in data_map["data"]:
        # 画像名を決定
        fname = file_info["file_name"]
        if len(fname)==0:
            continue

        base_name, ext = os.path.splitext(fname)
        text_file_name = f"{base_name}_text{ext}"
        text_file_path = f"./sample-data/{text_file_name}"

        # キャプチャ画像から、テキストだけにする
        img_file_path = f"./sample-data/{file_info["file_name"]}"
        img = cv2.imread(img_file_path)
        img2 = img_preprocess(img, invert=False, text_padding=0)
        _, img3 = get_and_erase_level(img2)

        # 画像として保存
        cv2.imwrite(text_file_path, img3)
        print(text_file_path)



if __name__=="__main__":
    print(123)
    make_test_data_judgeTitle()
