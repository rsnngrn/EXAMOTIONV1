from tkinter import *
from tkinter import messagebox
import window_setter as ws
from statics import static, rounder
import threading
from time import sleep
import customtkinter

# for mixing the cards
is_first = True
on_post = False
is_destroy = False
question_counter = 0
q_and_a_holder = []
nlps = []
answers = []


def set_enabled():
    for i in range(15):
        if is_destroy:
            return
        sleep(1)

    next_button["state"] = "normal"


class Stopper:
    def __init__(self):
        self.thread = threading.Thread(target=set_enabled, args=())

    def start_thread(self):
        next_button["state"] = "disabled"
        self.thread.start()


class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer App")

        # Initialize timer variables
        self.seconds = 3600
        self.timer_running = False

        # Update the timer display
        self.update_timer()

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def stop_timer(self):
        self.timer_running = False

    def update_timer(self):
        if self.timer_running:
            self.seconds -= 1
            minutes = self.seconds // 60
            seconds = self.seconds % 60
            time_str = f"{minutes:02}:{seconds:02}"
            timer.config(text=time_str)
            self.root.after(1000, self.update_timer)


answers_holder = []


def on_click(pos):
    answer = answers_holder[question_counter]
    answer[pos].configure(border_color="#2B2D42", border_width=5)


def get_questions():
    global q_and_a_holder
    for i in range(10):
        question_holder = customtkinter.CTkFrame(center_frame, fg_color="#8D99AE", corner_radius=10)

        question_label = customtkinter.CTkLabel(question_holder,
                                                text=f"{i + 1}:Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris molestie leo vitae augue lacinia, a dignissim neque ultricies. Donec ut ex risus. Nunc at quam ultricies, congue nibh tempor, imperdiet metus. Vestibulum mi enim, finibus eget lacus quis, fringilla gravida erat. Etiam erat dolor, venenatis cursus est ut, hendrerit ullamcorper nunc.",
                                                font=("Helvetica", 25),
                                                justify='center',
                                                wraplength=700,
                                                fg_color="#EDF2F4",
                                                corner_radius=10,
                                                )

        answer_1 = customtkinter.CTkButton(master=question_holder,
                                           corner_radius=10,
                                           text="answer1",
                                           fg_color="#EDF2F4",
                                           command=lambda: on_click(0),
                                           font=("Arial", 20),
                                           text_color="black",
                                           border_width=5,
                                           border_color="#EDF2F4"
                                           )

        answer_2 = customtkinter.CTkButton(master=question_holder,
                                           corner_radius=10,
                                           text="answer2",
                                           fg_color="#EDF2F4",
                                           command=lambda: on_click(1),
                                           font=("Arial", 20),
                                           text_color="black"
                                           )

        answer_3 = customtkinter.CTkButton(master=question_holder,
                                           corner_radius=10,
                                           text="answer3",
                                           fg_color="#EDF2F4",
                                           command=lambda: on_click(2),
                                           font=("Arial", 20),
                                           text_color="black"
                                           )

        answer_4 = customtkinter.CTkButton(master=question_holder,
                                           corner_radius=10,
                                           text="answer4",
                                           fg_color="#EDF2F4",
                                           command=lambda: on_click(3),
                                           font=("Arial", 20),
                                           text_color="black"
                                           )

        question_label.grid(column=0, row=0, columnspan=2, sticky="nsew", padx=20, pady=20)
        answer_1.grid(column=0, row=1, sticky="nsew", padx=20, pady=20)
        answer_2.grid(column=1, row=1, sticky="nsew", padx=20, pady=20)
        answer_3.grid(column=0, row=2, sticky="nsew", padx=20, pady=20)
        answer_4.grid(column=1, row=2, sticky="nsew", padx=20, pady=20)

        question_holder.grid_columnconfigure(0, weight=1)
        question_holder.grid_columnconfigure(1, weight=1)
        question_holder.grid_rowconfigure(0, weight=2)
        question_holder.grid_rowconfigure(1, weight=1)
        question_holder.grid_rowconfigure(2, weight=1)

        answers_holder.append([answer_1, answer_2, answer_3, answer_4])
        q_and_a_holder.append(question_holder)


def goto_next():
    stopper = Stopper()
    global timer_class
    global is_first
    global on_post
    global question_counter
    global post_survey
    global what_do_you_feel

    if is_first:
        pre_survey.destroy()
        q_and_a_holder[question_counter].pack(fill="both", expand=True, padx=20, pady=10)
        next_button.config(text="Next")
        is_first = False
        timer_class.start_timer()
        stopper.start_thread()
        on_post = True

    elif question_counter < len(q_and_a_holder) - 1 and not on_post:
        post_survey_answer = what_do_you_feel.get("1.0", 'end-1c')
        if len(post_survey_answer) == 0:
            messagebox.showinfo("showinfo", "Sorry but Post-Survey Feedback is a required field!")
            return
        answers.append(post_survey_answer)
        post_survey.destroy()
        timer_class.start_timer()
        q_and_a_holder[question_counter].destroy()
        question_counter = question_counter + 1
        q_and_a_holder[question_counter].pack(fill="both", expand=True, padx=20, pady=10)
        next_button["state"] = "disabled"
        stopper.start_thread()
        counter.config(text=update_item_number())
        on_post = True

    elif question_counter < len(q_and_a_holder) and on_post:
        # post survey
        post_survey = Frame(center_frame)
        post_survey.config(bg='black')
        prompt_label = Label(post_survey,
                             text=f"What do you feel answering question number {question_counter + 1}?",
                             font=("Arial", 15),
                             justify=LEFT)
        what_do_you_feel = Text(post_survey, height=5, font=("Arial", 10), padx=10, pady=10)

        prompt_label.grid(column=0, row=0, sticky="nsew")
        what_do_you_feel.grid(column=0, row=1, sticky="nsew", padx=30, pady=10)
        post_survey.columnconfigure(0, weight=1)

        on_post = False
        timer_class.stop_timer()
        q_and_a_holder[question_counter].destroy()
        post_survey.pack(fill="both", expand=True, padx=20, pady=50)

    else:
        answers.append(what_do_you_feel.get("1.0", 'end-1c'))
        print(answers)
        main_frame.destroy()


statics = static.Statics()
main_frame = Tk()
main_frame.resizable(False, False)
main_frame.config(bg='black')
main_frame.title(statics.get_title())
ws.FullScreenApp(main_frame)
main_frame.state('zoomed')

timer_class = TimerApp(main_frame)

# center frame
center_frame = Frame(main_frame)
center_frame.grid(row=0, column=0, sticky="nsew")

# for the pre-survey

instructions = customtkinter.CTkLabel(master=center_frame,
                                      font=("Arial", 20),
                                      text_color="white",
                                      wraplength=1100,
                                      height=100,
                                      justify='left',
                                      text="Instructions:\n\nSimilarly, the emotions section can be rated on the same scale, with 1 representing 'Not Expressive,' 2 representing 'Slightly Expressive,' 3 representing 'Moderately Expressive,' 4 representing 'Very Expressive,' and 5 representing 'Extremely Expressive.'"
                                      )
instructions.pack(fill='x', padx=40, pady=20)


pre_survey = customtkinter.CTkFrame(master=center_frame, fg_color="#8D99AE")
pre_survey.pack(fill="both", expand=True, padx=40, pady=20)

next_holder = Frame(center_frame)

next_button = Button(next_holder, text="Start Exam",
                     cursor='hand2',
                     bg="#EDF2F4",
                     fg="black",
                     borderwidth=0,
                     highlightthickness=0,
                     width=20,
                     height=2,
                     font=("Times", 12),
                     command=goto_next
                     )

divider = customtkinter.CTkLabel(master=next_holder, text="", corner_radius=1, fg_color="#FE3F56", height=48, width=10)
divider1 = customtkinter.CTkLabel(master=next_holder, text="", corner_radius=1, fg_color="#FE3F56", height=48, width=10)

next_holder.pack(side="bottom", anchor="e", padx=(0, 40), pady=20)
divider.pack(side="right")
next_button.pack(side="right")
divider1.pack(side="right")

post_survey = Frame(center_frame)
what_do_you_feel = Text(post_survey, height=5, font=("Arial", 10), padx=10, pady=10)

# generate questions
get_questions()

# right frame
right_frame = Frame(main_frame)
right_frame.grid(row=0, column=1, sticky="nsew")

# holder
holder = Frame(right_frame)
holder.grid(row=0, column=0, pady=(50, 10), padx=(0, 10), sticky='we')

# timer and count
timer = Label(holder, text="00:00", font=("Arial", 15), bg="black", fg="white", width=10)


def update_item_number():
    return f"{question_counter + 1}/{len(q_and_a_holder)}"


def on_close():
    global is_destroy
    is_destroy = True
    main_frame.destroy()


counter = Label(holder, text=update_item_number(), font=("Arial", 15), bg="black", fg="white", width=10)
timer.pack(side="right", padx=10)
counter.pack(side="right")

camera_frame = Label(right_frame, bg="black", height=20)
camera_frame.grid(row=1, column=0, padx=(0, 20), sticky='we')

right_frame.columnconfigure(0, weight=1)

main_frame.grid_columnconfigure(0, weight=3)
main_frame.grid_columnconfigure(1, weight=2)
main_frame.rowconfigure(0, weight=1)
main_frame.protocol("WM_DELETE_WINDOW", on_close)
main_frame.config(bg='#2B2D42')
right_frame.config(bg='#2B2D42')
center_frame.config(bg='#2B2D42')
main_frame.mainloop()
