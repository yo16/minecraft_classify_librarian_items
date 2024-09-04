import os
import json

ADMISSIBLE_LIB_JSON = "./src/resources/admissible_librarian.json"


class AdmissibleLibrarians:
    admit_info = {}

    def __init__(self):
        # 採用する司書定義のjsonファイルを開いて、採用情報を得る
        if os.path.exists(ADMISSIBLE_LIB_JSON):
            with open(ADMISSIBLE_LIB_JSON, mode="r", encoding="utf-8") as f:
                self.admit_info = json.load(f)
    
    # 採用するかどうかの判定
    def check_admissible(self, enchant_name, level, echo=True):
        if self.admit_info == {}:
            return False
        if "admissible_librarian" not in self.admit_info:
            return False
        
        for admissible_lib_type in self.admit_info["admissible_librarian"]:
            if admissible_lib_type["enchant"] == enchant_name and \
               admissible_lib_type["level"] == level:
                if echo:
                    print("***** ADMISSIBLE *****")
                return True
        
        return False

