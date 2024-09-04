from unittest import mock

from src.AdmissibleLibrarians import AdmissibleLibrarians

JSON_NOT_EXISTS = "./src/resources/not_found.json"


def test_normal_use():
    """ 普通の使い方 """
    al = AdmissibleLibrarians()
    
    assert al.check_admissible("入れ食い", 3, False) == True
    assert al.check_admissible("入れ食い", 2, False) == False


def test_file_not_found():
    """ JOSNファイルが存在しないとき """
    with mock.patch("src.AdmissibleLibrarians.ADMISSIBLE_LIB_JSON", JSON_NOT_EXISTS):
        al = AdmissibleLibrarians()

        # 普通に呼び出せるが、本来Trueであるものも、Falseと返す
        assert al.check_admissible("入れ食い", 3, False) == False
        assert al.check_admissible("入れ食い", 2, False) == False


def test_unknown():
    """ 未知のエンチャント名 """
    al = AdmissibleLibrarians()
    
    assert al.check_admissible("大食い", 3, False) == False


def test_stdout_normal(capsys):
    """ デフォルトは標準出力が出ること """
    al = AdmissibleLibrarians()
    al.check_admissible("入れ食い", 3)

    captured = capsys.readouterr()
    assert captured.out == "***** ADMISSIBLE *****\n"


def test_stdout_true(capsys):
    """ True指定で標準出力が出ること """
    al = AdmissibleLibrarians()
    al.check_admissible("入れ食い", 3, True)

    captured = capsys.readouterr()
    assert captured.out == "***** ADMISSIBLE *****\n"


def test_stdout_false(capsys):
    """ False指定で標準出力が出ないこと """
    al = AdmissibleLibrarians()
    al.check_admissible("入れ食い", 3, False)

    captured = capsys.readouterr()
    assert captured.out == ""


def test_stdout_true_but_not_admissible(capsys):
    """ True指定でも、受け入れ不可の場合は、標準出力が出ないこと """
    al = AdmissibleLibrarians()
    al.check_admissible("大食い", 3, True)

    captured = capsys.readouterr()
    assert captured.out == ""

