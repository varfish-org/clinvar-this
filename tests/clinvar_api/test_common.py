from clinvar_api import common


def test_clean_for_json_bool():
    assert common.clean_for_json(True) is True


def test_clean_for_json_int():
    assert common.clean_for_json(1) == 1


def test_clean_for_json_float():
    assert common.clean_for_json(1.0) == 1.0


def test_clean_for_json_str():
    assert common.clean_for_json("x") == "x"


def test_clean_for_json_list():
    assert common.clean_for_json([1, 2, 3, 4]) == [1, 2, 3, 4]
    assert common.clean_for_json([[1], [2]]) == [[1], [2]]


def test_clean_for_json_dict():
    assert common.clean_for_json({"key": "value"}) == {"key": "value"}
    assert common.clean_for_json({"key": "value", "none": None}) == {"key": "value"}
    assert common.clean_for_json([{"key": "value", "none": None}]) == [{"key": "value"}]
    assert common.clean_for_json({"d": {"key": "value", "none": None}}) == {"d": {"key": "value"}}
