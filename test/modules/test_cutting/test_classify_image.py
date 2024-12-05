import numpy as np

from modules.cutting.classify_shape import classify_shape


def test_classify_triangle():
    approx = np.array([[0, 0], [1, 0], [0, 1]])
    result = classify_shape(approx)
    assert result == "triangle"


def test_classify_rectangle():
    approx = np.array([[0, 0], [4, 0], [4, 2], [0, 2]])
    result = classify_shape(approx)
    assert result == "rectangle"


def test_classify_pentagon():
    approx = np.array([[0, 0], [1, 0], [1, 1], [0.5, 1.5], [0, 1]])
    result = classify_shape(approx)
    assert result == "pentagon"


def test_classify_hexagon():
    approx = np.array([[0, 0], [1, 0], [1.5, 0.5], [1, 1], [0, 1], [-0.5, 0.5]])
    result = classify_shape(approx)
    assert result == "hexagonal"


def test_classify_polygon():
    approx = np.array(
        [[0, 0], [1, 0], [1, 1], [0.5, 1.5], [0, 1], [-0.5, 0.5], [-1, 0]]
    )
    result = classify_shape(approx)
    assert result == "Polygon with 7 vertices"
