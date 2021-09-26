"""
Snake game using turtle module.

:URL:
:Author: NanthaKumar<https://github.com/nknantha>
:Date: 2021/09/26
"""

from random import randrange
from time import sleep
from turtle import Turtle, Screen
from typing import Union, Tuple

COLORTUPLE = Union[str, Tuple[int, int, int]]

# GAME Configurations.
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
SCREEN_BGCOLOR = 'black'
SCREEN_TITLE = 'Snake Game'
STEP_SIZE = 20


class Food(Turtle):

    # Food Configuration.
    FOOD_SHAPE = 'circle'
    FOOD_COLOR = 'blue'
    FOOD_SIZE = 0.5
    FOOD_W_RANGE = ((int(SCREEN_WIDTH // 2) // STEP_SIZE) - 2) * STEP_SIZE
    FOOD_H_RANGE = ((int(SCREEN_HEIGHT // 2) // STEP_SIZE) - 2) * STEP_SIZE
    STEP_SIZE = STEP_SIZE

    def __init__(self) -> None:
        super().__init__()
        self.shape(self.FOOD_SHAPE)
        self.shapesize(self.FOOD_SIZE, self.FOOD_SIZE)
        self.color(self.FOOD_COLOR)
        self.up()
        self.speed(0)
        self.refresh()

    def refresh(self) -> None:
        new_x = randrange(-self.FOOD_W_RANGE, self.FOOD_W_RANGE, self.STEP_SIZE)
        new_y = randrange(-self.FOOD_H_RANGE, self.FOOD_H_RANGE, self.STEP_SIZE)
        # print(new_x, new_y)
        self.goto(new_x, new_y)


class InfoBoard:
    __slots__ = '_score', '_score_board'

    # Info Board Configuration.
    SCORE_POSITION = int(SCREEN_HEIGHT // 2) - 20
    FONT = ('Arial', 12, 'bold')
    FONT_COLOR = 'white'

    def __init__(self) -> None:
        self._score = 0
        self._score_board = Turtle(visible=False)
        self._score_board.color(self.FONT_COLOR)
        self._score_board.up()
        self._score_board.goto(0, self.SCORE_POSITION)
        self._update_score()

    def _update_score(self) -> None:
        self._score_board.clear()
        self._score_board.write(f'Score: {self._score}', align='center', font=self.FONT)

    def add_score(self) -> None:
        self._score += 1
        self._update_score()

    def game_over(self) -> None:
        self._score_board.goto(0, 0)
        self._score_board.write('GAME OVER', align='center', font=self.FONT)


class Snake:
    __slots__ = '_segments', 'head'

    # Snake Configurations.
    STEP_SIZE = STEP_SIZE
    HEAD_SIZE = 0.9
    BODY_SIZE = 0.8

    HEAD_COLOR = 'green'
    BODY_COLOR = 'white'
    COLLISION_COLOR = 'red'

    HEAD_SHAPE = 'circle'
    BODY_SHAPE = 'circle'

    def __init__(self) -> None:
        self._segments = []
        self._create_segments()
        self.head = self._segments[0]

    @staticmethod
    def __create_turtle(shape: str, size: Union[int, float], color: COLORTUPLE) -> Turtle:
        new_turtle = Turtle(shape=shape)
        new_turtle.up()
        new_turtle.shapesize(size, size)
        new_turtle.color(color)
        new_turtle.speed(0)
        return new_turtle

    def _create_segments(self) -> None:
        # Head creation.
        self._segments.append(self.__create_turtle(self.HEAD_SHAPE, self.HEAD_SIZE, self.HEAD_COLOR))

        # Body creation.
        for i in range(1, 3):
            new_turtle = self.__create_turtle(self.BODY_SHAPE, self.BODY_SIZE, self.BODY_COLOR)
            new_turtle.bk(self.STEP_SIZE * i)
            self._segments.append(new_turtle)

    def _change_direction(self, deg: int) -> None:
        if int((self.head.heading() + 180) % 360) != (deg % 360):
            self.head.setheading(deg)

    def _forward_segments(self) -> None:
        for j in range(len(self._segments) - 1, 0, -1):
            new_x = self._segments[j - 1].xcor()
            new_y = self._segments[j - 1].ycor()
            self._segments[j].goto(new_x, new_y)
        self.head.fd(self.STEP_SIZE)

    def add_segment(self) -> None:
        new_turtle = self.__create_turtle(self.BODY_SHAPE, self.BODY_SIZE, self.BODY_COLOR)
        new_turtle.goto(self._segments[-1].pos())
        self._segments.append(new_turtle)

    def down(self) -> None:
        self._change_direction(270)

    def head_collision(self) -> None:
        self.head.color(self.COLLISION_COLOR)

    def left(self) -> None:
        self._change_direction(180)

    def move(self) -> None:
        self._forward_segments()

    def right(self) -> None:
        self._change_direction(0)

    def segment_collision(self) -> bool:
        for i in range(1, len(self._segments)):
            if round(self.head.xcor(), 2) == round(self._segments[i].xcor(), 2) \
                    and round(self.head.ycor(), 2) == round(self._segments[i].ycor(), 2):
                self._segments[i].color(self.COLLISION_COLOR)
                return True
        return False

    def up(self) -> None:
        self._change_direction(90)


class SnakeGame:
    __slots__ = 'screen', 'x_range', 'y_range', 'food', 'snake', 'infoboard'

    def __init__(self) -> None:

        # Screen setup.
        self.screen = Screen()
        self.screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.screen.cv._rootwindow.resizable(False, False)

        self.x_range = int(SCREEN_WIDTH // 2) - STEP_SIZE
        self.y_range = int(SCREEN_HEIGHT // 2) - STEP_SIZE

        self.screen.tracer(0)
        self.screen.bgcolor(SCREEN_BGCOLOR)
        self.screen.title(SCREEN_TITLE)
        self.screen.colormode(255)

        # Game objects setup.
        self.food = Food()
        self.snake = Snake()
        self.infoboard = InfoBoard()

    def __hold_game(self):
        turtle = Turtle(visible=False)
        turtle.up()
        turtle.goto(0, -(SCREEN_HEIGHT // 2) + STEP_SIZE)
        turtle.color(InfoBoard.FONT_COLOR)
        turtle.write("Press 'SpaceBar' to start the game...", align='center', font=InfoBoard.FONT)

        key_press = [0]

        def press_key():
            key_press.pop()

        self.screen.onkey(press_key, 'space')
        while key_press:
            self.screen.update()

        self.screen.onkey(None, 'space')
        turtle.clear()

    def _food_collision(self) -> bool:
        return round(self.food.xcor(), 2) == round(self.snake.head.xcor(), 2) \
               and round(self.food.ycor(), 2) == round(self.snake.head.ycor(), 2)

    def _wall_collision(self) -> bool:
        return abs(self.snake.head.xcor()) >= self.x_range \
               or abs(self.snake.head.ycor()) >= self.y_range

    def _enable_keys(self) -> None:
        self.screen.onkey(self.snake.up, 'Up')
        self.screen.onkey(self.snake.down, 'Down')
        self.screen.onkey(self.snake.right, 'Right')
        self.screen.onkey(self.snake.left, 'Left')

    def _disable_keys(self) -> None:
        self.screen.onkey(None, 'Up')
        self.screen.onkey(None, 'Down')
        self.screen.onkey(None, 'Right')
        self.screen.onkey(None, 'Left')

    def run(self) -> None:
        # Game Loop.
        self._enable_keys()
        self.screen.listen()

        speed = 0.3
        game_on = True

        self.__hold_game()

        while game_on:
            self.screen.update()

            # Food collision.
            if self._food_collision():
                self.food.refresh()
                self.snake.add_segment()
                self.infoboard.add_score()
                speed *= 0.99

            # Wall collision.
            if self._wall_collision() or self.snake.segment_collision():
                self.snake.head_collision()
                game_on = False
                self.infoboard.game_over()
                self.screen.update()
            else:
                self.snake.move()

            sleep(speed)

        self.screen.exitonclick()


if __name__ == '__main__':
    SnakeGame().run()
