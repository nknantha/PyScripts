"""
Pomodoro Clock in Python with GUI.

:URL: https://github.com/nknantha/PyScripts/tree/main/Pomodoro/pomodoro.py
:Author: NanthaKumar<https://github.com/nknantha>
:Date: 2021/09/25
"""

from math import floor
from tkinter import *
from tkinter import ttk


class Pomodoro:
    TITLE = 'Pomodoro'
    PINK = "#e2979c"
    RED = "#e7305b"
    GREEN = "#9bdeac"
    YELLOW = "#f7f5dd"
    FONT_NAME = "Courier"
    WORK_MIN = 25
    SHORT_BREAK_MIN = 5
    LONG_BREAK_MIN = 20

    def __init__(self):
        self._reps = 1
        self._is_timer_running = False

        # Window Setup.
        self.__setup_window()

        # Info Label.
        self.__setup_info_label()

        # Canvas.
        self.__setup_canvas()

        # Check Mark Label.
        self.__setup_check_mark_label()

        # Buttons.
        self.__setup_buttons()

        # Start Running.
        self._run()

    def __setup_window(self):
        self._root = Tk()
        self._root.title(self.TITLE)
        self._root.configure(padx=20, pady=20, background=self.YELLOW)
        self._root.resizable(0, 0)

    def __setup_info_label(self):
        self._info_label = ttk.Label(master=self._root, text='Timer', foreground=self.GREEN,
                                     background=self.YELLOW, font=(self.FONT_NAME, 35, 'bold'))
        self._info_label.grid(column=1, row=0, padx=10, pady=10)

    def __setup_canvas(self):
        self._image_file = PhotoImage(file='Images/tomato.png')

        canvas_width = self._image_file.width()
        canvas_height = self._image_file.height()

        self._canvas = Canvas(master=self._root, width=canvas_width, height=canvas_height,
                              background=self.YELLOW, highlightthickness=0)

        self._canvas.create_image(canvas_width // 2, canvas_height // 2, image=self._image_file)

        self._timer_text = self._canvas.create_text(canvas_width // 2, (canvas_height // 2) + 10,
                                                    text='00:00', fill='white',
                                                    font=(self.FONT_NAME, 25, 'bold'))
        self._canvas.grid(column=1, row=1, padx=10, pady=10)

    def __setup_check_mark_label(self):
        self._check_mark_label = ttk.Label(master=self._root, text='', background=self.YELLOW,
                                           foreground=self.GREEN, font=(self.FONT_NAME, 20, 'bold'))
        self._check_mark_label.grid(column=1, row=3, padx=10, pady=10)

    def __setup_buttons(self):
        self._start_button = ttk.Button(master=self._root, text='Start',
                                        default='active', command=self.__start_timer)
        self._start_button.focus()
        self._start_button.grid(column=0, row=2, padx=10, pady=10, sticky=E)

        self._reset_button = ttk.Button(master=self._root, text='Reset', command=self.__reset_timer)
        self._reset_button.grid(column=2, row=2, padx=10, pady=10, sticky=W)

    def __start_timer(self):

        if not self._is_timer_running:
            self._is_timer_running = True

            if self._reps % 8 == 0:
                self._check_mark_label.configure(text='✓' * 4)
                self._info_label.configure(text='Break', foreground=self.RED)

                # self._root.lift()
                self._root.attributes('-topmost', True)
                self._root.focus_force()

                self.__countdown(60 * self.LONG_BREAK_MIN)
            elif self._reps % 2 == 0:
                self._info_label.configure(text='Break', foreground=self.PINK)

                # self._root.lift()
                self._root.attributes('-topmost', True)
                self._root.focus_force()

                self.__countdown(60 * self.SHORT_BREAK_MIN)
            else:
                self._info_label.configure(text='Work', foreground=self.GREEN)
                self.__countdown(60 * self.WORK_MIN)

    def __countdown(self, count):
        if count > -1 and self._is_timer_running:
            mins = floor(count / 60)
            secs = count % 60
            self._canvas.itemconfigure(self._timer_text, text=f'{mins:02d}:{secs:02d}')
            self._root.after(1000, self.__countdown, count - 1)
        elif self._is_timer_running:
            self._reps += 1
            self._is_timer_running = False
            self._check_mark_label.configure(text='✓' * (floor(self._reps / 2) % 4))
            self.__start_timer()

    def __reset_timer(self):
        self._is_timer_running = False
        self._reps = 1
        self._info_label['text'] = 'Timer'
        self._check_mark_label['text'] = ''
        self._canvas.itemconfigure(self._timer_text, text='00:00')

    def _run(self):
        self._root.mainloop()


if __name__ == '__main__':
    Pomodoro()
