import pytest


@pytest.mark.parametrize(
    "t,X,times,expected,raises",
    [
        (10, 5, [[1, 3], [7, 9], [12, 15]], 0, None),
        (8, 5, [[1, 3], [7, 9], [12, 15]], 5, None),
        (13, 5, [[1, 3], [7, 9], [12, 15]], 5, None),
        (17, 5, [[1, 3], [7, 9], [12, 15]], 0, None),
        (17, 5, [1], None, TypeError),
        (17, 5, [[1, 3, 6], [7, 9, 11], [12, 15, 17]], None, TypeError),
    ],
)
def test_dose_steady(t, X, times, expected, raises):
    """Test that dose_steady administers dose at correct times."""
    from pkmodel.functions import dose_steady

    if raises:
        with pytest.raises(raises):
            assert dose_steady(t, None, X, times) == expected
    else:
        assert dose_steady(t, None, X, times) == expected
