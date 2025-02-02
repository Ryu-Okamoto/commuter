import numpy as np

from commuter.model import Predictor, next_mean, next_var


def test_next_mean():
    # case 1: [1,2,3,4,5] + [6]
    new_value = 6
    n = 5
    mean = np.array([1, 2, 3, 4, 5]).mean()
    actual = next_mean(new_value, n, mean)

    expected = np.array([1, 2, 3, 4, 5, 6]).mean()
    acceptable_error = 1.0e-5
    assert abs(actual - expected) < acceptable_error

    # case 2: [1,3] + [6]
    new_value = 6
    n = 2
    mean = np.array([1, 3]).mean()
    actual = next_mean(new_value, n, mean)

    expected = np.array([1, 3, 6]).mean()
    acceptable_error = 1.0e-5
    assert abs(actual - expected) < acceptable_error


def test_next_var():
    # case 1: [1,2,3,4,5] + [6]
    new_value = 6
    n = 5
    mean = np.array([1, 2, 3, 4, 5]).mean()
    var = np.array([1, 2, 3, 4, 5]).var()
    actual = next_var(new_value, n, mean, var)

    expected = np.array([1, 2, 3, 4, 5, 6]).var()
    acceptable_error = 1.0e-5
    assert abs(actual - expected) < acceptable_error

    # case 2: [1,3] + [6]
    new_value = 6
    n = 2
    mean = np.array([1, 3]).mean()
    var = np.array([1, 3]).var()
    actual = next_var(new_value, n, mean, var)

    expected = np.array([1, 3, 6]).var()
    acceptable_error = 1.0e-5
    assert abs(actual - expected) < acceptable_error


def test_in_model():
    # case: [1, 2, 3, 4, 5] + [6]
    data = np.array([1, 2, 3, 4, 5])
    model = Predictor([.0, .0])
    model.fit_local(data, data)

    # precondition
    actual_x_mean = model.x_mean
    actual_x_var = model.x_var
    actual_y_mean = model.y_mean
    actual_y_var = model.y_var

    expected_mean = data.mean()
    expected_var = data.var()
    acceptable_error = 1.0e-5
    assert abs(actual_x_mean - expected_mean) < acceptable_error
    assert abs(actual_x_var - expected_var) < acceptable_error
    assert abs(actual_y_mean - expected_mean) < acceptable_error
    assert abs(actual_y_var - expected_var) < acceptable_error

    # online learning
    model.fit_online(6.0, 6.0)
    actual_x_mean = model.x_mean
    actual_x_var = model.x_var
    actual_y_mean = model.y_mean
    actual_y_var = model.y_var

    data = np.array([1, 2, 3, 4, 5, 6])
    expected_mean = data.mean()
    expected_var = data.var()
    acceptable_error = 1.0e-5
    assert abs(actual_x_mean - expected_mean) < acceptable_error
    assert abs(actual_x_var - expected_var) < acceptable_error
    assert abs(actual_y_mean - expected_mean) < acceptable_error
    assert abs(actual_y_var - expected_var) < acceptable_error
