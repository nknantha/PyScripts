"""
Quiz App using online Travia database.
Requires internet connection.

:URL: https://github.com/nknantha/PyScripts/tree/main/Quiz%20App
:Author: NanthaKumar<https://github.com/nknantha>
:Data: 2021/09/25
"""
import html
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import requests


class Question:
    __slots__ = '__text', '__ans'

    def __init__(self, text: str, ans: str) -> None:
        self.__text = html.unescape(text)
        self.__ans = html.unescape(ans)

    @property
    def text(self) -> str:
        return self.__text

    @property
    def ans(self) -> str:
        return self.__ans


class QuizBrain:
    QUESTION_COUNT = 10
    ENDPOINT = 'https://opentdb.com/api.php'

    PARAMETERS = {
        'amount': QUESTION_COUNT,
        'type': 'boolean'
    }

    def __init__(self) -> None:
        self._question_list = self._fetch_questions()
        self._question_number = 0
        self._current_question = None
        # self.score = 0

    def _fetch_questions(self) -> list:
        response = requests.get(url=self.ENDPOINT, params=self.PARAMETERS)
        response.raise_for_status()
        return [Question(q['question'], q['correct_answer']) for q in response.json()['results']]

    def still_has_questions(self) -> bool:
        return self._question_number < len(self._question_list)

    def next_question(self) -> str:
        self._current_question = self._question_list[self._question_number]
        self._question_number += 1
        return f"Q.{self._question_number}: {self._current_question.text}"

    def check_current_answer(self, user_answer: str) -> bool:
        return self._current_question.ans.lower() == user_answer.lower()

    def current_question_position(self) -> int:
        return self._question_number

    def total_question_count(self) -> int:
        return len(self._question_list)


class QuizApp:
    TITLE = 'nQuizz'
    BACKGROUND_COLOR = '#375362'

    X_PAD = 20
    Y_PAD = 20

    CANVAS_WIDTH = 300
    CANVAS_HEIGHT = 250
    CANVAS_X_PAD = 0
    CANVAS_Y_PAD = 50
    CANVAS_BACKGROUND = 'white'

    QUESTION_FONT = ('Arial', 20, 'italic')
    QUESTION_FONT_COLOR = 'black'

    SCORE_FONT = ('Arial', 20, 'normal')
    SCORE_FONT_COLOR = 'white'

    def __init__(self) -> None:
        self._quiz_brain = QuizBrain()

        # Window creation.
        self._root = tk.Tk()
        self._root.title(self.TITLE)
        self._root.resizable(0, 0)
        self._root.configure(padx=self.X_PAD, pady=self.Y_PAD, background=self.BACKGROUND_COLOR)

        # Score Label.
        self._score_value = 0
        self._score_label = ttk.Label(master=self._root, text='',
                                      background=self.BACKGROUND_COLOR,
                                      foreground=self.SCORE_FONT_COLOR,
                                      font=self.SCORE_FONT)
        self._score_label.grid(column=1, row=0, sticky=tk.E)
        self.__update_score()

        # Canvas & Question Display.
        self._canvas = tk.Canvas(master=self._root, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT,
                                 background=self.CANVAS_BACKGROUND, highlightthickness=0)
        self._canvas.grid(column=0, row=1, padx=self.CANVAS_X_PAD,
                          pady=self.CANVAS_Y_PAD, columnspan=2, sticky=tk.NSEW)
        self._question_text = self._canvas.create_text(self.CANVAS_WIDTH // 2,
                                                       self.CANVAS_HEIGHT // 2,
                                                       width=self.CANVAS_WIDTH - 10,
                                                       font=self.QUESTION_FONT,
                                                       fill=self.QUESTION_FONT_COLOR,
                                                       # anchor=tk.N,
                                                       text='')
        self.__checkout_next_question()

        # True & False Button.
        self._true_image = tk.PhotoImage(file='Images/true.png')
        self._false_image = tk.PhotoImage(file='Images/false.png')

        ttk.Style().configure('TButton', hightlightthickness=0, background=self.BACKGROUND_COLOR)

        ttk.Button(master=self._root, image=self._true_image,
                   command=lambda: self.__check_answer('true')).grid(column=0, row=2, sticky=tk.W)
        ttk.Button(master=self._root, image=self._false_image,
                   command=lambda: self.__check_answer('false')).grid(column=1, row=2, sticky=tk.E)

        # Mainloop.
        self._root.mainloop()

    def __update_score(self) -> None:
        self._score_label.configure(text=f"Score: {self._score_value}")

    def __checkout_next_question(self) -> None:
        if self._quiz_brain.still_has_questions():
            self._canvas.itemconfigure(self._question_text, text=self._quiz_brain.next_question())
        else:
            score_text = "You've successfully completed the quiz." \
                         f"\nYour Score {self._score_value}/" \
                         f"{self._quiz_brain.total_question_count()}."
            messagebox.showinfo(title='Quiz Finished', message=score_text)
            self._root.quit()

    def __check_answer(self, user_ans: str) -> None:
        if self._quiz_brain.check_current_answer(user_ans):
            self._score_value += 1
            self.__update_score()
            color = 'green'
        else:
            color = 'red'

        self._canvas.configure(background=color)
        self._root.update()
        time.sleep(0.5)
        self._canvas.configure(background=self.CANVAS_BACKGROUND)
        self.__checkout_next_question()


if __name__ == '__main__':
    QuizApp()
