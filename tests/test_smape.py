import numpy as np
from hypothesis import given
from hypothesis.extra import numpy
from hypothesis.strategies import integers


def smape_old(true: list, pred: list) -> float:
    """
    Calculate SMAPE.

    Parameters
    ----------
    true : list
        True labels
    pred : list
        Prediction values

    Returns
    -------
    float
        SMAPE metric
    """
    numerator = 0
    denominator = 0

    for i in range(len(true)):
        numerator += abs(true[i] - pred[i])
        denominator += abs(true[i]) + abs(pred[i])

    return 2 * numerator / denominator * 100


def smape(true: list, pred: list) -> float:
    """
    Calculate SMAPE.

    Parameters
    ----------
    true : list
        True labels
    pred : list
        Prediction values

    Returns
    -------
    float
        SMAPE metric
    """

    numerator = 0
    denominator = 0
    count = 0

    for t, p in zip(true, pred, strict=False):
        if t is not None and p is not None:
            numerator += abs(t - p)
            denominator += abs(t) + abs(p)
            count += 1

    if denominator == 0:
        return 0.0

    return 2 * numerator / denominator * 100


size = integers(min_value=0, max_value=0)


@given(
    true=numpy.arrays(dtype=np.float32, shape=size),
    predict=numpy.arrays(dtype=np.float32, shape=size),
)
def test_smape(true, predict):
    smape_metric_old = smape_old(true, predict)
    smape_metric = smape(true, predict)
    assert np.isclose(smape_metric_old, smape_metric)
