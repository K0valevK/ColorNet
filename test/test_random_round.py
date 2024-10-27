from pytest import mark, param
from gameplay.random_round import RoundGenerator
from graphics.figure import Graphic, Rectangle


@mark.parametrize(
    "expected",
    [
        param(
            "lmao",
            id="basic test"
        )
    ]
)
def test_create_round(expected):
    result = RoundGenerator.create_round(Rectangle, 3, 12, True, False, True)
    print(result)
