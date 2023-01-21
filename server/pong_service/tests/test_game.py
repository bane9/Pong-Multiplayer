import os
import sys

path = os.path.join(os.getcwd(), "pong_service")

if path not in sys.path:
    sys.path.append(path)

from pong_service.game import AABB, Ball, Paddle


def test_aabb():
    obj1 = AABB(10, 10, 100, 100)
    obj2 = AABB(10, 10, 100, 100)

    assert obj1.is_coliding(obj2)


def test_ball():
    ball = Ball(10, 10, 10, 10)

    pos = ball.get_position()

    ball.update()

    assert pos != ball.get_position()


def test_paddle():
    paddle = Paddle(10, 10, 10, 10)

    paddle.update_position(800)

    assert paddle.rect.y == 400

    paddle.update_position(-100)

    assert paddle.rect.y == 0

    assert paddle.rect.x == 10
