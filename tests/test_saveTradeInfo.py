import os
from unittest import mock
import pytest
import sqlite3
from datetime import datetime
from collections import Counter

from src.saveTradeInfo import save_trade_info, TradeInfo

# テストで使うDB
# DBファイルが存在しないときのDB
DB_FILE_NOT_EXISTS = "./test_no_db.db"
# DBはあるが、テーブルが存在しないときのDB
DB_FILE_TABLE_NOT_EXISTS = "./test_no_table.db"
# insertのテスト用（別に分けなくてもいいけど）
DB_FILE_TEST = "./test.db"


# テスト前の準備
def setup_module(module):
    """ セットアップ """
    # テスト用のDBを削除
    if os.path.exists(DB_FILE_NOT_EXISTS):
        os.remove(DB_FILE_NOT_EXISTS)
    if os.path.exists(DB_FILE_TABLE_NOT_EXISTS):
        os.remove(DB_FILE_TABLE_NOT_EXISTS)
    if os.path.exists(DB_FILE_TEST):
        os.remove(DB_FILE_TEST)

# 終了時の後片付け
def teardown_module(module):
    """ テストモジュールのクリーンアップ """
    if os.path.exists(DB_FILE_NOT_EXISTS):
        os.remove(DB_FILE_NOT_EXISTS)
    if os.path.exists(DB_FILE_TABLE_NOT_EXISTS):
        os.remove(DB_FILE_TABLE_NOT_EXISTS)
    if os.path.exists(DB_FILE_TEST):
        os.remove(DB_FILE_TEST)



def test_insert_with_no_db_file():
    """ DBファイルが存在しないとき """
    with mock.patch("src.saveTradeInfo.DB_FILE", DB_FILE_NOT_EXISTS):
        # 実行
        trade1 = TradeInfo(0)
        trade2 = TradeInfo(1)
        save_trade_info(trade1, trade2)
        assert os.path.exists(DB_FILE_NOT_EXISTS)

        # 確認
        conn = sqlite3.connect(DB_FILE_NOT_EXISTS)
        c = conn.cursor()
        c.execute("select count(*) from lib_log")
        list = c.fetchone()
        assert list == (2,)
        conn.close()


def test_insert_with_no_table():
    """ ファイルはあるがテーブルが存在しないとき """
    with mock.patch("src.saveTradeInfo.DB_FILE", DB_FILE_TABLE_NOT_EXISTS):
        # 準備（最初はファイルも存在しない）
        conn_prep = sqlite3.connect(DB_FILE_TABLE_NOT_EXISTS)
        c = conn_prep.cursor()
        # create table
        c.execute(
            "create table if not exists lib_log " + \
            "( " + \
            "name text not null, " + \
            "level integer, " + \
            "price integer, " + \
            "created_at text not null" + \
            ");"
        )
        conn_prep.commit()
        conn_prep.close()

        # 実行
        trade1 = TradeInfo(0)
        trade2 = TradeInfo(1)
        save_trade_info(trade1, trade2)
        assert os.path.exists(DB_FILE_TABLE_NOT_EXISTS)

        # 確認
        conn = sqlite3.connect(DB_FILE_TABLE_NOT_EXISTS)
        c = conn.cursor()
        c.execute("select count(*) from lib_log")
        list = c.fetchone()
        assert list == (2,)
        conn.close()


@pytest.mark.parametrize("test_seq, trade1, trade2, expected", [
    (1, (0,), (1,), [("紙", None, None), ("本棚", None, None)]),
    (2, (1,), (0,), [("紙", None, None), ("本棚", None, None)]),
    (3, (0,), (2,"忠誠",2,31), [("紙", None, None), ("忠誠", 2, 31)]),
    (4, (2,"修繕"), (0,), [("紙", None, None), ("修繕", None, None)]),
])
def test_insert_trades(test_seq, trade1, trade2, expected):
    """ insertするテスト """
    timestamp_s = test_seq
    with mock.patch("src.saveTradeInfo.DB_FILE", DB_FILE_TEST):
        # 準備
        mock_now = datetime(2024,8,24, 12,34, timestamp_s)
        mock_created_at_str = mock_now.strftime("%Y-%m-%d %H:%M:%S")    # 抽出用
        with mock.patch("src.saveTradeInfo.datetime") as mock_datetime:
            mock_datetime.now.return_value = mock_now
            mock_datetime.strftime = datetime.strftime  # そのまま使う

            # 実行
            ty1 = trade1[0]
            nm1 = trade1[1] if len(trade1)>1 else None
            lv1 = trade1[2] if len(trade1)>2 else None
            pr1 = trade1[3] if len(trade1)>3 else None
            tr1 = TradeInfo(ty1, nm1, lv1, pr1)
            ty2 = trade2[0]
            nm2 = trade2[1] if len(trade2)>1 else None
            lv2 = trade2[2] if len(trade2)>2 else None
            pr2 = trade2[3] if len(trade2)>3 else None
            tr2 = TradeInfo(ty2, nm2, lv2, pr2)
            save_trade_info(tr1, tr2)

        # 確認
        conn = sqlite3.connect(DB_FILE_TEST)
        cur = conn.cursor()
        cur.execute(
            "select name, level, price from lib_log where created_at=?",
            (mock_created_at_str,)
        )
        rows = cur.fetchall()
        assert Counter(rows) == Counter([expected[0], expected[1]])
        
        conn.close()
