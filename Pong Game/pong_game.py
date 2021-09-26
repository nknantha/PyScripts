"""
Pong game using turtle module.

:URL: https://github.com/nknantha/PyScripts/tree/main/Pong%20Game/pong_game.py
:Author: NanthaKumar<https://github.com/nknantha>
:Date: 2021/09/26
"""
from turtle import Turtle, Screen
from time import sleep
from random import randrange


class Paddle(Turtle):

    # Paddle configurations.
    PADDLE_SIZE = 4.0
    PADDLE_COLOR = 'white'

    def __init__(self, step_size: int, x_range: int, y_range: int) -> None:
        super().__init__(shape='square')
        self.shapesize(0.3, self.PADDLE_SIZE, outline=2)
        self.up()
        self.setheading(90)
        self.color(self.PADDLE_COLOR)
        self.step_size = step_size
        self.x_range = x_range
        self.y_range = y_range

    def __is_movable(self, cor: float) -> bool:
        return -self.y_range < cor < self.y_range

    def go_up(self) -> None:
        if self.__is_movable(round(self.ycor(), 2) + self.PADDLE_SIZE * 10 + self.step_size):
            self.fd(self.step_size)

    def go_down(self) -> None:
        if self.__is_movable(round(self.ycor(), 2) - self.PADDLE_SIZE * 10 - self.step_size):
            self.bk(self.step_size)


class Ball(Turtle):

    # Ball configurations.
    BALL_SIZE = 1
    BALL_SHAPE = 'circle'
    BALL_COLOR = 'white'

    def __init__(self, step_size: int) -> None:
        super().__init__(shape=self.BALL_SHAPE)
        self.up()
        self.color(self.BALL_COLOR)
        self.shapesize(self.BALL_SIZE, self.BALL_SIZE)

        self.x_step = self.y_step = step_size

    def move(self) -> None:
        new_x = self.xcor() + self.x_step
        new_y = self.ycor() + self.y_step
        self.goto(new_x, new_y)

    def vertical_bounce(self) -> None:
        self.y_step *= -1

    def horizontal_bounce(self) -> None:
        self.x_step *= -1


class ScoreBoard:

    # Score Board Configurations.
    FONT = ('Arial', 28, 'bold')
    SPACING = 20
    COLOR = 'white'
    MAX_POINTS = 10

    def __init__(self, top_pos: int) -> None:
        self.l_score = 0
        self.r_score = 0

        self._l_tur = Turtle(visible=False)
        self._l_tur.up()
        self._l_tur.color(self.COLOR)
        self._l_tur.goto(-self.SPACING, top_pos)

        self._r_tur = Turtle(visible=False)
        self._r_tur.up()
        self._r_tur.color(self.COLOR)
        self._r_tur.goto(self.SPACING, top_pos)

    def update(self) -> None:
        self._r_tur.clear()
        self._l_tur.clear()

        self._r_tur.write(self.r_score, align='left', font=self.FONT)
        self._l_tur.write(self.l_score, align='right', font=self.FONT)

    def is_player_win(self):

        if self.l_score >= self.MAX_POINTS or self.r_score >= self.MAX_POINTS:
            if self.l_score >= self.MAX_POINTS:
                l_text, r_text = 'WIN', 'LOSS'
            elif self.r_score >= self.MAX_POINTS:
                l_text, r_text = 'LOSS', 'WIN'

            self._l_tur.bk(100)
            self._r_tur.fd(100)
            self._l_tur.write(l_text, align='right', font=self.FONT)
            self._r_tur.write(r_text, align='left', font=self.FONT)

            return True
        return False


class PongGame:

    # Game configurations.
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    SCREEN_BGCOLOR = 'black'
    SCREEN_TITLE = 'Pong Game'

    STEP_SIZE = 15
    PADDING = 20
    X_RANGE = int(SCREEN_WIDTH // 2)
    Y_RANGE = int(SCREEN_HEIGHT // 2)
    PAD_POS = int((X_RANGE // STEP_SIZE) * STEP_SIZE) - PADDING

    def __init__(self) -> None:
        # Screen setup.
        self.__setup_screen()

        # Paddles setup.
        self.__setup_paddles()

        # Ball setup.
        self.__setup_ball()

        # Score board setup.
        self.__setup_scoreboard()

    def __setup_scoreboard(self) -> None:
        self._scoreboard = ScoreBoard(self.Y_RANGE - self.PADDING * 3)

    def __setup_screen(self) -> None:
        self.screen = Screen()
        self.screen.setup(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        self.screen.cv._rootwindow.resizable(False, False)

        self.screen.tracer(0)
        self.screen.title(self.SCREEN_TITLE)
        self.screen.colormode(255)
        self.screen.bgcolor(self.SCREEN_BGCOLOR)

    def __setup_ball(self) -> None:
        self._ball = Ball(self.STEP_SIZE)

    def __setup_paddles(self) -> None:
        # Left paddle.
        self._l_paddle = Paddle(self.STEP_SIZE, self.PAD_POS, self.Y_RANGE)
        self._l_paddle.goto(-self.PAD_POS, 0)
        self.screen.onkeyrelease(self._l_paddle.go_up, 'w')
        self.screen.onkeyrelease(self._l_paddle.go_down, 's')

        # Right paddle.
        self._r_paddle = Paddle(self.STEP_SIZE, self.PAD_POS, self.Y_RANGE)
        self._r_paddle.goto(self.PAD_POS, 0)
        self.screen.onkeyrelease(self._r_paddle.go_up, 'Up')
        self.screen.onkeyrelease(self._r_paddle.go_down, 'Down')

    def __hold_game(self):
        turtle = Turtle(visible=False)
        turtle.up()
        turtle.goto(0, -self.Y_RANGE + self.PADDING + 10)
        turtle.color('white')
        turtle.write("Press 'SpaceBar' to start the game...", align='center', font=('Arial', 25, 'normal'))

        space_pressed = [0]

        def press_space():
            space_pressed.pop()

        self.screen.onkey(press_space, 'space')
        while space_pressed:
            self.screen.update()

        turtle.clear()
        self.screen.onkey(None, 'space')

    def run(self) -> None:

        wall_pos = self.Y_RANGE - self.PADDING
        paddle_x = self._r_paddle.xcor()
        speed = 0.2

        self.screen.listen()
        self._ball.goto(0, randrange(-(wall_pos - 10), (wall_pos - 10), self.STEP_SIZE))
        self._scoreboard.update()
        self.screen.update()

        self.__hold_game()

        while True:

            # Checking for win.
            if self._scoreboard.is_player_win():
                break

            # Wall Bounce.
            if abs(round(self._ball.ycor(), 2)) >= wall_pos:
                self._ball.vertical_bounce()

            # Ball out of space control.
            if abs(self._ball.xcor()) > paddle_x + 30:
                if self._ball.xcor() < 0:
                    self._scoreboard.r_score += 1
                else:
                    self._scoreboard.l_score += 1
                self._ball.goto(0, randrange(-(wall_pos - 10), (wall_pos - 10), self.STEP_SIZE))
                speed = 0.2

            ball_x_pos = round(self._ball.xcor(), 2) + 10
            ball_y_pos = round(self._ball.ycor(), 2) + 10
            r_paddle_y_pos = round(self._r_paddle.ycor(), 2)
            l_paddle_y_pos = round(self._l_paddle.ycor(), 2)

            # Right Paddle Bounce.
            if paddle_x - 10 <= ball_x_pos <= ball_x_pos \
                    and r_paddle_y_pos - 45 <= ball_y_pos <= r_paddle_y_pos + 45:
                self._ball.horizontal_bounce()
                speed *= 0.9

            # Left Paddle Bounce.
            if -(paddle_x - 10) <= ball_x_pos <= -(paddle_x - 20) \
                    and l_paddle_y_pos - 45 <= ball_y_pos <= l_paddle_y_pos + 45:
                self._ball.horizontal_bounce()
                speed *= 0.9

            self._ball.move()
            self._scoreboard.update()
            self.screen.update()
            sleep(speed)

        self._ball.ht()
        self.screen.update()
        self.screen.mainloop()


if __name__ == '__main__':
    PongGame().run()
