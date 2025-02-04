from commuter.hhmmss import serialize, deserialize, subtract_hhmmss


def test_serialize():
    assert serialize('000000') == 0
    assert serialize('000001') == 1
    assert serialize('000100') == 60
    assert serialize('010000') == 60 * 60
    assert serialize('235959') == 60 * 60 * 23 + 60 * 59 + 59

    # abnormal cases
    assert serialize('240000') == None
    assert serialize('999999') == None


def test_deserialize():
    assert deserialize(0) == '000000'
    assert deserialize(1) == '000001'
    assert deserialize(60) == '000100'
    assert deserialize(60 * 60) == '010000'
    assert deserialize(60 * 60 * 23 + 60 * 59 + 59) == '235959'

    # abnormal cases
    assert deserialize(99999) == None
    assert deserialize(-1) == None
    assert deserialize(60 * 60 * 23 + 60 * 59 + 59 + 1) == None


def test_invertibility(): 
    assert deserialize(serialize('012345')) == '012345'
    assert deserialize(serialize('101010')) == '101010'
    assert serialize(deserialize(7777)) == 7777
    assert serialize(deserialize(24)) == 24


def test_subtract_hhmmss():
    assert subtract_hhmmss('000034', '000023') == '000011'
    assert subtract_hhmmss('005600', '003400') == '002200'
    assert subtract_hhmmss('120000', '040000') == '080000'

    assert subtract_hhmmss('000100', '000025') == '000035'
    assert subtract_hhmmss('010000', '002500') == '003500'
    assert subtract_hhmmss('020050', '000060') == '015950'

    # abnormal cases
    assert subtract_hhmmss('999999', '000000') == None
    assert subtract_hhmmss('111111', '999999') == None
    assert subtract_hhmmss('000010', '000030') == None