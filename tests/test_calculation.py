import pytest
from apps.calculation import add

@pytest.mark.parametrize("a, b, result", [
    (1, 1, 2),
    (2, 2, 4),
    (4, 4, 8)
])

# @pytest.fixture
# def zero_bank_account():
#     return bank_account(0)

def test_add(a, b, result):
    print("Testing...")

    assert add(a, b) == result

