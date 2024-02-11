from tkinter import *
from tkinter import messagebox
import numpy as np
import window_setter as ws
from statics import static
import threading
from time import sleep
import customtkinter
from PIL import Image, ImageTk
import cv2
from deepface import DeepFace
import show_score
from utils import exam_page_model

# for mixing the cards
is_first = True
on_post = False
is_destroy = False
question_counter = 0
cur_answer = 5
q_and_a_holder = []
nlps = []
answers = []
emotions = []
answers_holder = []
times = []
score = 0
statics = static.Statics()
questions = statics.get_questions()
cap = cv2.VideoCapture(0)
seconds = 3600
starting_time = seconds
get_emotion = False
database = exam_page_model.ExamPageModel()
final_name = ""

# Load DEEPFACE model
model = DeepFace.build_model('Emotion')
# Define emotion labels
emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
key = ['A', 'B', 'C', 'D']

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def show_image(frame):
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    camera_frame.imgtk = imgtk
    camera_frame.configure(image=imgtk, width=200, height=300)
    sleep(.01)
    if is_destroy:
        return
    show_frame()


def show_frame():
    global get_emotion
    while not is_destroy:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)

        # Convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=10, minSize=(30, 30))

        for (x, y, w, h) in faces:
            # Extract the face ROI (Region of Interest)
            face_roi = gray_frame[y:y + h, x:x + w]

            # Resize the face ROI to match the input shape of the model
            resized_face = cv2.resize(face_roi, (48, 48), interpolation=cv2.INTER_AREA)

            # Preprocess the image for DEEPFACE
            normalized_face = resized_face / 255.0
            reshaped_face = normalized_face.reshape(1, 48, 48, 1)

            # Predict emotions using the pre-trained model
            preds = model.predict(reshaped_face)
            emotion_idx = np.argmax(preds)
            emotion = emotion_labels[emotion_idx]

            # Draw rectangle around face and label with predicted emotion
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            if emotion == "sad":
                emotion = "Bored"
            elif emotion == "angry":
                emotion = "Frustration"
            elif emotion == "happy":
                emotion = "Excited"
            elif emotion == "disgust":
                emotion = "Confusion"
            elif emotion == "neutral":
                emotion = "Neutral"
            elif emotion == "fear":
                emotion = "Nervous"
            elif emotion == "surprise":
                emotion = "Surprise"

            cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            if get_emotion:
                if question_counter + 1 > len(emotions):
                    temp_emotion = [emotion]
                    emotions.append(temp_emotion)
                else:
                    temp_emotion = emotions[question_counter]
                    temp_emotion.append(emotion)

        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)

        if not is_destroy:
            imgtk = ImageTk.PhotoImage(image=img)
            camera_frame.imgtk = imgtk
            camera_frame.configure(image=imgtk, width=200, height=300)

        img.close()
        sleep(.01)

    # show_image_thread = threading.Thread(target=show_image, args=(frame, ))
    # show_image_thread.start()
    # show_image_thread.join()


def open_get_emotion():
    global get_emotion
    while not is_destroy:
        get_emotion = False
        if on_post:
            for i in range(2):
                if is_destroy:
                    return
                sleep(1)
            get_emotion = True
        sleep(.15)


# class Stopper:
#     def __init__(self):
#         self.thread = threading.Thread(target=set_enabled, args=())
#
#     def start_thread(self):
#         next_button["state"] = "disabled"
#         self.thread.start()


class ShowAnsStopper:
    def __init__(self):
        self.thread = threading.Thread(target=show_post_survey, args=())

    def start_thread(self):
        next_button["state"] = "disabled"
        self.thread.start()


class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer App")

        # Initialize timer variables
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
        global seconds
        if self.timer_running:
            seconds -= 1
            minutes = seconds // 60
            temp_seconds = seconds % 60
            time_str = f"{minutes:02}:{temp_seconds:02}"
            timer.config(text=time_str)
            self.root.after(1000, self.update_timer)


def on_click(pos):
    global cur_answer
    answer = answers_holder[question_counter]
    if not cur_answer == 5:
        answer[cur_answer - 1].configure(fg_color="#EDF2F4")

    cur_answer = pos
    answer[pos - 1].configure(fg_color="#c4c4c4")


def get_questions():
    global q_and_a_holder
    for item in questions:
        question_holder = customtkinter.CTkFrame(center_frame, fg_color="#8D99AE", corner_radius=10)

        question_label = customtkinter.CTkLabel(question_holder,
                                                text=item.get("question"),
                                                font=("Helvetica", 25),
                                                justify='center',
                                                wraplength=600,
                                                fg_color="#EDF2F4",
                                                corner_radius=10,
                                                )

        answer_1 = customtkinter.CTkButton(master=question_holder,
                                           corner_radius=10,
                                           text=item.get(1),
                                           fg_color="#EDF2F4",
                                           command=lambda: on_click(1),
                                           font=("Arial", 20),
                                           text_color="black",
                                           hover_color='#c4c4c4',
                                           )

        answer_2 = customtkinter.CTkButton(master=question_holder,
                                           corner_radius=10,
                                           text=item.get(2),
                                           fg_color="#EDF2F4",
                                           command=lambda: on_click(2),
                                           font=("Arial", 20),
                                           text_color="black",
                                           hover_color='#c4c4c4',
                                           )

        answer_3 = customtkinter.CTkButton(master=question_holder,
                                           corner_radius=10,
                                           text=item.get(3),
                                           fg_color="#EDF2F4",
                                           command=lambda: on_click(3),
                                           font=("Arial", 20),
                                           text_color="black",
                                           hover_color='#c4c4c4',
                                           )

        answer_4 = customtkinter.CTkButton(master=question_holder,
                                           corner_radius=10,
                                           text=item.get(4),
                                           fg_color="#EDF2F4",
                                           command=lambda: on_click(4),
                                           font=("Arial", 20),
                                           text_color="black",
                                           hover_color='#c4c4c4',
                                           )

        question_label.grid(column=0, row=0, columnspan=2, sticky="nsew", padx=10, pady=20, ipady=60)
        answer_1.grid(column=0, row=1, sticky="nsew", padx=10, pady=(0, 10), ipady=60)
        answer_2.grid(column=1, row=1, sticky="nsew", padx=(0, 10), pady=(0, 10), ipady=60)
        answer_3.grid(column=0, row=2, sticky="nsew", padx=10, pady=(0, 20), ipady=60)
        answer_4.grid(column=1, row=2, sticky="nsew", padx=(0, 10), pady=(0, 20), ipady=60)

        answer_1._text_label.configure(wraplength=350, justify=CENTER)
        answer_2._text_label.configure(wraplength=350, justify=CENTER)
        answer_3._text_label.configure(wraplength=350, justify=CENTER)
        answer_4._text_label.configure(wraplength=350, justify=CENTER)

        question_holder.grid_columnconfigure(0, weight=1)
        question_holder.grid_columnconfigure(1, weight=1)
        question_holder.grid_rowconfigure(0, weight=2)
        question_holder.grid_rowconfigure(1, weight=1)
        question_holder.grid_rowconfigure(2, weight=1)

        answers_holder.append([answer_1, answer_2, answer_3, answer_4])
        q_and_a_holder.append(question_holder)


def show_answer():
    global score
    correct_ans = questions[question_counter].get("correct") - 1
    if correct_ans == cur_answer - 1:
        score += 1

    answer = answers_holder[question_counter]
    answer[cur_answer - 1].configure(fg_color="#701313")
    answer[questions[question_counter].get("correct") - 1].configure(fg_color="#32a852")


def show_post_survey():
    global post_survey
    global on_post
    global what_do_you_feel

    sleep(1)

    next_button["state"] = "normal"
    post_survey = customtkinter.CTkFrame(master=center_frame, corner_radius=10, fg_color="#8D99AE")
    prompt_label = customtkinter.CTkLabel(master=post_survey,
                                          text=f"What do you feel answering question number {question_counter + 1}?",
                                          font=("Arial", 25),
                                          corner_radius=10,
                                          fg_color="#EDF2F4",
                                          height=80,
                                          justify=LEFT)

    what_do_you_feel = customtkinter.CTkTextbox(master=post_survey, font=("Arial", 20), corner_radius=10, height=300)
    prompt_label.grid(column=0, row=0, sticky="nsew", padx=40, pady=(60, 20))
    what_do_you_feel.grid(column=0, row=1, sticky="nsew", padx=40, pady=(0, 60))
    what_do_you_feel.focus_set()

    post_survey.columnconfigure(0, weight=1)
    post_survey.rowconfigure(0, weight=1)
    post_survey.rowconfigure(1, weight=2)

    timer_class.stop_timer()
    q_and_a_holder[question_counter].destroy()
    post_survey.pack(fill="both", expand=True)


def goto_next():
    show_answer_stopper = ShowAnsStopper()
    global timer_class
    global is_first
    global on_post
    global question_counter
    global post_survey
    global what_do_you_feel
    global cur_answer
    global get_emotion
    global times
    global starting_time
    global final_name

    if is_first:
        if name.get() == "":
            messagebox.showinfo("showinfo", "Sorry but pre-survey is a required field!")
            return
        final_name = name.get()
        pre_survey.destroy()
        q_and_a_holder[question_counter].pack(fill="both", expand=True, pady=10)
        next_button.config(text="Next")
        is_first = False
        timer_class.start_timer()
        on_post = True
        threading.Thread(target=open_get_emotion, args=()).start()

    elif question_counter < len(q_and_a_holder) - 1 and not on_post:
        post_survey_answer = what_do_you_feel.get("0.0", 'end-1c')

        if len(post_survey_answer) == 0:
            messagebox.showinfo("showinfo", "Sorry but Post-Survey Feedback is a required field!")
            return

        cur_answer = 5
        nlps.append(post_survey_answer)
        post_survey.destroy()
        timer_class.start_timer()
        q_and_a_holder[question_counter].destroy()
        question_counter = question_counter + 1
        q_and_a_holder[question_counter].pack(fill="both", expand=True, pady=10)
        counter.config(text=update_item_number())
        on_post = True
        print("hi")
        starting_time = seconds

    elif question_counter < len(q_and_a_holder) and on_post:
        # post survey
        if cur_answer == 5:
            messagebox.showinfo("showinfo", "Sorry but you haven't choose an answer yet!")
            return

        on_post = False
        show_answer()
        answers.append(key[cur_answer - 1])
        show_answer_stopper.start_thread()
        times.append(starting_time - seconds)

    else:
        post_survey_answer = what_do_you_feel.get("0.0", 'end-1c')
        if len(post_survey_answer) == 0:
            messagebox.showinfo("showinfo", "Sorry but Post-Survey Feedback is a required field!")
            return
        nlps.append(post_survey_answer)

        print(f"answers: {answers}")
        print(f"nlps:{nlps}")
        print(f"emotion:{emotions}")
        print(f"times:{times}")
        data = {
            'Bored': 0,
            'Frustration': 0,
            'Excited': 0,
            'Neutral': 0,
            'Confusion': 0,
            'Nervous': 0,
            'Surprise': 0
        }

        for item in emotions:
            for emotion in item:
                data[emotion] = data[emotion] + 1

        # get the average emotion for every number
        final_emotion = []
        for emotion in emotions:
            final_emotion.append(max(emotion, key=emotion.count))

        total_time = 3600 - seconds
        data_model = {
            'name': final_name,
            'answers': answers,
            'cnns': final_emotion,
            'nlps': nlps,
            'score': score,
            'time': total_time,
            'times': times
        }

        database.add_data(data_model)

        main_frame.destroy()
        show_score_page = show_score.ShowScore(score, total_time, data)
        show_score_page.create_frame()


def radiobutton_event():
    print("radiobutton toggled, current value:", radio_var.get())


main_frame = Tk()
# main_frame.resizable(False, False)
main_frame.config(bg='black')
main_frame.title(statics.get_title())
ws.FullScreenApp(main_frame)
main_frame.state('zoomed')

timer_class = TimerApp(main_frame)

# center frame
scrollable_frame = customtkinter.CTkScrollableFrame(main_frame, fg_color="#2B2D42")
scrollable_frame.grid(row=0, column=0, sticky="nsew")

center_frame = Frame(scrollable_frame)
center_frame.pack(side='top', expand=True, padx=40, fill=BOTH)

# for the pre-survey

instructions = Label(master=center_frame,
                     font=("Arial", 15),
                     justify='left',
                     anchor='w',
                     bg="#2B2D42",
                     fg="white",
                     wraplength=800,
                     text="Instructions:\n\nSimilarly, the emotions section can be rated on the same "
                          "scale, with 1 representing 'Not Expressive,' 2 representing 'Slightly "
                          "Expressive,' 3 representing 'Moderately Expressive,' 4 representing 'Very "
                          "Expressive,' and 5 representing 'Extremely Expressive.'"
                     )
instructions.pack(side='top', fill=X, pady=20)

pre_survey = customtkinter.CTkFrame(master=center_frame, fg_color="#8D99AE")

name_label = customtkinter.CTkLabel(pre_survey, text="Name", font=("Arial", 25))
name_label.pack(side='top', anchor='w', padx=40, pady=(60, 20))

name = customtkinter.CTkEntry(pre_survey,
                              placeholder_text="Name",
                              font=("Arial", 25),
                              height=50,
                              corner_radius=30)

name.pack(side='top', padx=40, pady=(0, 10), fill=X)

prompt_label_pre = customtkinter.CTkLabel(master=pre_survey,
                                          text=f"What do you feel answering question number {question_counter + 1}?",
                                          font=("Arial", 25),
                                          corner_radius=10,
                                          fg_color="#EDF2F4",
                                          justify=LEFT)

prompt_label_pre.pack(side='top', anchor='w', padx=40, pady=20)

radio_var = IntVar(value=0)
radiobutton_1 = customtkinter.CTkRadioButton(pre_survey, text="CTkRadioButton 1",
                                             font=("Arial", 20),
                                             command=radiobutton_event, variable=radio_var, value=1, fg_color="#EDF2F4")
radiobutton_2 = customtkinter.CTkRadioButton(pre_survey, text="CTkRadioButton 2",
                                             font=("Arial", 20),
                                             command=radiobutton_event, variable=radio_var, value=2, fg_color="#EDF2F4")
radiobutton_3 = customtkinter.CTkRadioButton(pre_survey, text="CTkRadioButton 3",
                                             font=("Arial", 20),
                                             command=radiobutton_event, variable=radio_var, value=1, fg_color="#EDF2F4")
radiobutton_4 = customtkinter.CTkRadioButton(pre_survey, text="CTkRadioButton 4",
                                             font=("Arial", 20),
                                             command=radiobutton_event, variable=radio_var, value=2, fg_color="#EDF2F4")

radiobutton_1.pack(side='top', anchor='w', padx=40)
radiobutton_2.pack(side='top', anchor='w', padx=40)
radiobutton_3.pack(side='top', anchor='w', padx=40)
radiobutton_4.pack(side='top', anchor='w', padx=40, pady=(0, 40))

# pre_survey.grid_rowconfigure(0, weight=0)
# pre_survey.grid_rowconfigure(1, weight=2)
# pre_survey.grid_rowconfigure(2, weight=1)
# pre_survey.grid_rowconfigure(3, weight=1)
# pre_survey.grid_rowconfigure(4, weight=1)
# pre_survey.grid_rowconfigure(5, weight=1)
# pre_survey.grid_columnconfigure(0, weight=1)

pre_survey.pack(fill="both", expand=True, side='top')

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

next_holder.pack(side="bottom", anchor="e", pady=20)
divider.pack(side="right")
next_button.pack(side="right")
divider1.pack(side="right")

post_survey = Frame(center_frame)
what_do_you_feel = customtkinter.CTkTextbox(post_survey, height=5, font=("Arial", 10), padx=10, pady=10)
# generate questions
get_questions()

# right frame
right_frame = Frame(main_frame)
right_frame.grid(row=0, column=1, sticky="nsew")

# holder
holder = Frame(right_frame, bg="#2B2D42")
holder.grid(row=0, column=0, pady=(50, 10), padx=(0, 10), sticky='we')

# timer and count
timer = Label(holder, text="00:00", font=("Arial", 15), bg="#EDF2F4", fg="black", width=10)
divider3 = customtkinter.CTkLabel(master=holder, text="", corner_radius=1, fg_color="#FE3F56", width=10, height=30)
divider4 = customtkinter.CTkLabel(master=holder, text="", corner_radius=1, fg_color="#FE3F56", width=10, height=30)


def update_item_number():
    return f"{question_counter + 1}/{len(q_and_a_holder)}"


def on_close():
    global is_destroy
    is_destroy = True
    main_frame.destroy()


counter = Label(holder, text=update_item_number(), font=("Arial", 15), bg="#EDF2F4", fg="black", width=10)
divider4.pack(side="right", padx=(0, 10))
timer.pack(side="right")
divider3.pack(side="right", padx=(0, 10))
counter.pack(side="right")

camera_frame = Label(right_frame, bg="black", height=20)
camera_frame.grid(row=1, column=0, padx=(0, 20), sticky='we')

right_frame.columnconfigure(0, weight=1)

main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=0)
# scrollable_frame.grid_columnconfigure(0, weight=1)
# scrollable_frame.grid_columnconfigure(1, weight=0)
main_frame.grid_rowconfigure(0, weight=1)

main_frame.protocol("WM_DELETE_WINDOW", on_close)
main_frame.config(bg='#2B2D42')
right_frame.config(bg='#2B2D42')
center_frame.config(bg='#2B2D42')
center_frame.grid_rowconfigure(0, weight=0)
center_frame.grid_rowconfigure(1, weight=1)

# starting the opencv
camera_thread = threading.Thread(target=show_frame, args=())
camera_thread.start()

main_frame.mainloop()
