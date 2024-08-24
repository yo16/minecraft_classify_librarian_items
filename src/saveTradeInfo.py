# 取引内容をDBへ保存する

import sqlite3
from datetime import datetime

# DBファイル
DB_FILE = "./minecraft_data.db"

# 取引内容の型
class TradeInfo:
    def __init__(self, trade_type: int, name: str = None, level: int = None, price: int = None):
        self.trade_type = trade_type
        if trade_type == 0:
            self.name = "紙"
        elif trade_type == 1:
            self.name = "本棚"
        else:
            self.name = name
        self.level = level
        self.price = price

def save_trade_info(trade1: TradeInfo, trade2: TradeInfo):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # create table
    cur.execute(
        "create table if not exists lib_log " + \
        "( " + \
        "name text not null, " + \
        "level integer, " + \
        "price integer, " + \
        "created_at text not null" + \
        ");"
    )

    # insert
    insert_rec(cur, trade1)
    insert_rec(cur, trade2)

    # commit
    conn.commit()
    conn.close()


# insert
def insert_rec(cur: sqlite3.Cursor, trade_info: TradeInfo):
    now = datetime.now()
    created_at_str = now.strftime("%Y-%m-%d %H:%M:%S")

    cur.execute(
        "insert into lib_log (name, level, price, created_at) " + \
        "values (?, ?, ?, ?)",
        (
            trade_info.name,
            trade_info.level,
            trade_info.price,
            created_at_str
        )
    )


if __name__=="__main__":
    trade1 = TradeInfo(2, "忠誠", 2, 31)
    trade2 = TradeInfo(1)

    save_trade_info(trade1, trade2)
