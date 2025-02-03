from commuter.model_helper import serialize, deserialize


def test_serialize():
    assert serialize('000000') == 0
    assert serialize('000001') == 1
    assert serialize('000100') == 60
    assert serialize('010000') == 60 * 60
    assert serialize('235959') == 60 * 60 * 23 + 60 * 59 + 59


def test_deserialize():
    assert deserialize(0) == '000000'
    assert deserialize(1) == '000001'
    assert deserialize(60) == '000100'
    assert deserialize(60 * 60) == '010000'
    assert deserialize(60 * 60 * 23 + 60 * 59 + 59) == '235959'


def test_invertibility(): 
    assert deserialize(serialize('012345')) == '012345'
    assert deserialize(serialize('101010')) == '101010'
    assert serialize(deserialize(7777)) == 7777
    assert serialize(deserialize(24)) == 24