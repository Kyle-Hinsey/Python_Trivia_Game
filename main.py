# Kyle Hinsey, CIS 345, TTh 12:00, Project Beta
import json
from tkinter import *
from tkinter import messagebox
from random import sample
from difflib import get_close_matches


class Question:
    def __init__(self, question, class_points, choices, class_answer, correct_feedback, incorrect_feedback):
        """the choices being passed in will be an array"""
        self.question_asked = question
        self.point_value = class_points
        self.answer_options = choices
        self.right_answer = class_answer
        self.correct_feedback = correct_feedback
        self.incorrect_feedback = incorrect_feedback

    @property
    def question_asked(self):
        """Getter for the question being asked"""
        return self.__question_asked

    @question_asked.setter
    def question_asked(self, new_question):
        """Setter for the question being asked"""
        self.__question_asked = new_question

    @property
    def point_value(self):
        """Getter for the point value of the question"""
        return self.__point_value

    @point_value.setter
    def point_value(self, new_value):
        """Setter for the point value of the question"""
        self.__point_value = new_value

    @property
    def answer_options(self):
        """Getter for the choices the user can choose as the answer"""
        return self.__answer_options

    @answer_options.setter
    def answer_options(self, new_options):
        """Setter for the choices the user can choose as the answer"""
        self.__answer_options = new_options

    @property
    def right_answer(self):
        """Getter for the right answer to the question"""
        return self.__right_answer

    @right_answer.setter
    def right_answer(self, new_answer):
        """Setter for the right answer to the question"""
        self.__right_answer = new_answer

    @property
    def correct_feedback(self):
        """Getter for the feedback if the user gets the answer correct"""
        return self.__correct_feedback

    @correct_feedback.setter
    def correct_feedback(self, new_correct_feedback):
        """Setter for the feedback if the user gets the answer correct"""
        self.__correct_feedback = new_correct_feedback

    @property
    def incorrect_feedback(self):
        """Getter for the feedback if the user answered incorrectly"""
        return self.__incorrect_feedback

    @incorrect_feedback.setter
    def incorrect_feedback(self, new_incorrect_feedback):
        """Setter for the feedback if the user answered incorrectly"""
        self.__incorrect_feedback = new_incorrect_feedback


def load_questions():
    """this function will load the data from the json and have it be accessible in the program"""
    global questions_class_list
    try:
        with open('questions.json', 'r') as fp:
            tmp_question = None
            tmp_questions_dict = json.load(fp)
            # create the question classes
            for key, value in tmp_questions_dict.items():
                tmp_question = Question(key, value['point_value'], value['answer_options'], value['right_answer'],
                                        value['correct_feedback'], value['incorrect_feedback'])
                questions_class_list.append(tmp_question)
    except IOError:
        # set values to nothing
        questions_class_list = list()


def dump_questions():
    """save to the file"""
    global questions_class_list
    tmp_questions_dict = dict()
    for q in questions_class_list:
        tmp_questions_dict[q.question_asked] = {'point_value': q.point_value, 'answer_options': q.answer_options,
                                                'right_answer': q.right_answer, 'correct_feedback': q.correct_feedback,
                                                'incorrect_feedback': q.incorrect_feedback}
    with open('questions.json', 'w') as fp:
        json.dump(tmp_questions_dict, fp)
    # clear list
    questions_class_list = list()


def take_quiz():
    """will allow users to the take quiz"""
    global questions_class_list, screen_frame, window

    def display_question():
        """will display the quiz question and everything else associated with taking the quiz"""
        # clear screen
        clear_screen()

        # list of all the options for the quiz
        quiz_answer_options = asked_questions[question_count].answer_options

        # Label display the question the user is on
        on_question_number_lbl = Label(screen_frame, text=f'Question {question_count + 1}/3', bg=bg_color)
        on_question_number_lbl.grid(row=0, column=0, sticky=W)

        # Label displaying how many points the user has earned
        points_lbl = Label(screen_frame, text=f'Earned Points: {earned_points_var}/{total_points_var}', bg=bg_color)
        points_lbl.grid(row=0, column=1, sticky=E)

        # Displaying the question itself
        question_quiz_lbl = Label(screen_frame, text=asked_questions[question_count].question_asked, bg=bg_color)
        question_quiz_lbl.grid(row=1, column=0, pady=(5, 5))

        # display how many points the question is worth
        quiz_points_lbl = Label(screen_frame, text=f'Point Value: {asked_questions[question_count].point_value}'
                                , bg=bg_color)
        quiz_points_lbl.grid(row=1, column=1, padx=(40, 0), pady=(5, 5), sticky=E)

        # Choices for the user to select
        """The trisatevalue is set to 'x'. This is to prevent all of the radio button from being select when the 
        screen_frame loads. Excluding the tristatevalue in all of the radio buttons will result in all of the radio 
        buttons being selected when the question loads. This parameter (tristatevalue) was added to add aesthetics to 
        the program and prevent user error resulting in the crash of the program."""
        option1_radiobtn = Radiobutton(screen_frame, text=quiz_answer_options[0], bg=bg_color,
                                       variable=quiz_answer_selected, value=quiz_answer_options[0], tristatevalue='x')
        option1_radiobtn.grid(row=2, column=0, sticky=W)
        option2_radiobtn = Radiobutton(screen_frame, text=quiz_answer_options[1], bg=bg_color,
                                       variable=quiz_answer_selected, value=quiz_answer_options[1], tristatevalue='x')
        option2_radiobtn.grid(row=2, column=1, sticky=W)
        option3_radiobtn = Radiobutton(screen_frame, text=quiz_answer_options[2], bg=bg_color,
                                       variable=quiz_answer_selected, value=quiz_answer_options[2], tristatevalue='x')
        option3_radiobtn.grid(row=3, column=0, sticky=W)
        option4_radiobtn = Radiobutton(screen_frame, text=quiz_answer_options[3], bg=bg_color,
                                       variable=quiz_answer_selected, value=quiz_answer_options[3], tristatevalue='x')
        option4_radiobtn.grid(row=3, column=1, sticky=W)

        # button that will handle the the events of the quiz
        quiz_btn = Button(screen_frame, text=quiz_btn_txt, command=quiz_btn_command)
        quiz_btn.grid(row=4, column=1, sticky=E, pady=(15, 0))

        # label to provide feedback to the user
        quiz_feedback_lbl = Label(screen_frame, text=quiz_feedback_var.get(), bg=bg_color)
        quiz_feedback_lbl.grid(row=5, column=0, columnspan=2, pady=(15, 0))

    def submit_btn_func():
        """gives user feedback and will process their score"""
        nonlocal quiz_btn_txt, quiz_btn_command, earned_points_var, total_points_var, num_of_corr_questions_answered
        # provide feedback based on answer
        if quiz_answer_selected.get() == asked_questions[question_count].right_answer:
            quiz_feedback_var.set(asked_questions[question_count].correct_feedback)
            # add to user point score
            earned_points_var += asked_questions[question_count].point_value
            total_points_var += asked_questions[question_count].point_value
            # add to user question score
            num_of_corr_questions_answered += 1
        else:
            quiz_feedback_var.set(asked_questions[question_count].incorrect_feedback)
            # add to user point score
            total_points_var += asked_questions[question_count].point_value
        # change the text and command in the quiz_btn
        if question_count == 2:
            quiz_btn_txt = 'Finish'
        else:
            quiz_btn_txt = 'Next Question'
        quiz_btn_command = next_btn_func
        # call the display function to update page
        display_question()

    def next_btn_func():
        """change the appearance and functionality of the button in the corner"""
        nonlocal question_count, quiz_btn_txt, quiz_btn_command
        # increase question count
        question_count += 1
        # set the quiz_feedback_var back to blank
        quiz_feedback_var.set("")
        if question_count == 3:
            finish_btn_func()
        else:
            # change the text and command in the quiz_btn
            quiz_btn_txt = 'Submit Answer'
            quiz_btn_command = submit_btn_func
            # call function to reload the window
            display_question()

    def finish_btn_func():
        """will take the user to a finish screen and display their results"""
        # clear screen
        clear_screen()
        # labels congratulating the user and showing their score
        congrats_lbl = Label(screen_frame, text="Congratulations you finished the Mental Anguish Trivia Quiz!"
                             , bg=bg_color)
        congrats_lbl.pack()
        questions_corr_lbl = Label(screen_frame, text=f'You answered {num_of_corr_questions_answered} out of 3 '
                                                      f'questions correctly.', bg=bg_color)
        questions_corr_lbl.pack()
        points_earned_lbl = Label(screen_frame, text=f'You got {earned_points_var} out of {total_points_var} points.',
                                  bg=bg_color)
        points_earned_lbl.pack()

    # variables
    asked_questions = sample(questions_class_list, 3)
    quiz_answer_selected = StringVar()
    question_count = 0
    quiz_feedback_var = StringVar()
    quiz_btn_txt = "Submit Answer"
    quiz_btn_command = submit_btn_func
    total_points_var = 0
    earned_points_var = 0
    num_of_corr_questions_answered = 0

    # change window size
    window.geometry("600x250")

    # call function to display on load
    display_question()


def manage_questions():
    """function call to manage the questions"""
    global question_txt, option1, option2, option3, option4, answer, points, cor_feedback, incor_feedback, window

    def delete_onclick(event):
        """once user double clicks question, will ask if they want to proceed and then delete question if yes"""
        global questions_class_list
        # get the index of the question to be deleted
        delete_question_index = question_listbox.curselection()[0]

        # message displayed to the user
        message = f'Are you sure you want to delete the question:\n' \
                  f'{questions_class_list[delete_question_index].question_asked}'

        # message box asking the user if they are sure
        msgbox_delete_question = messagebox.askquestion('Delete Question', message)

        # if they don't want to delete then pass and do nothing
        if msgbox_delete_question == 'no':
            pass
        elif msgbox_delete_question == 'yes':
            # delete question from question_class_list
            del questions_class_list[delete_question_index]
            # clear responses
            clear_responses()
            # recursion, recall to reload proper list
            manage_questions()

    def edit_question(event):
        """will allow users to edit certain questions"""
        # get the index of the question to be edited
        edit_question_index = question_listbox.curselection()[0]

        # set values in the entry box to that of the question selected
        question_txt.set(questions_class_list[edit_question_index].question_asked)
        option1.set(questions_class_list[edit_question_index].answer_options[0])
        option2.set(questions_class_list[edit_question_index].answer_options[1])
        option3.set(questions_class_list[edit_question_index].answer_options[2])
        option4.set(questions_class_list[edit_question_index].answer_options[3])
        answer.set(questions_class_list[edit_question_index].right_answer)
        points.set(questions_class_list[edit_question_index].point_value)
        cor_feedback.set(questions_class_list[edit_question_index].correct_feedback)
        incor_feedback.set(questions_class_list[edit_question_index].incorrect_feedback)

    def ok_func():
        """will process the form"""
        # handle possible error
        if (question_txt.get() == "" or option1.get() == "" or option2.get() == "" or option3.get() == "" or
                option4.get() == "" or answer.get() == "" or points.get() == "" or cor_feedback.get() == ""
                or incor_feedback.get() == ""):
            messagebox.showerror("Error", "Please fill out all of the fields")
        elif points.get() not in ["1", "2", "3"]:
            messagebox.showerror("Error", "Please enter a valid point value")
        elif answer.get() != option1.get() and answer.get() != option2.get() and answer.get() != option3.get() \
                and answer.get() != option4.get():
            messagebox.showerror("Error", "Please ensure that the question answer is an option to select")
        # no errors
        else:
            """In case the user was editing the question, the program will loop through all the questions and see if it 
            is already in the list. If that was the case and the user was editing the question, the program will delete
            that question and then add it to the end of the list. If it is a new question, the program will just add the
            question to the list. Editing a question does not involve changing the the question text. That would be 
            creating a new question."""
            for question in questions_class_list:
                if question_txt.get() == question.question_asked:
                    del questions_class_list[questions_class_list.index(question)]

            # save/append question to the list
            questions_class_list.append(Question(question_txt.get(), int(points.get()), [option1.get(), option2.get(),
                                                                                         option3.get(), option4.get()],
                                                 answer.get(), cor_feedback.get(), incor_feedback.get()))
            messagebox.showinfo("Question Added", "Your question has been added to the question list")
            # clear all fields
            clear_responses()
        # recursion to show changes in listbox
        manage_questions()

    def clear_responses():
        """will clear the responses from the respective boxes"""
        global question_txt, option1, option2, option3, option4, answer, points, cor_feedback, incor_feedback
        # rest all variables
        question_txt.set("")
        option1.set("")
        option2.set("")
        option3.set("")
        option4.set("")
        answer.set("")
        points.set("")
        cor_feedback.set("")
        incor_feedback.set("")

    # clear the screen
    clear_screen()

    # change the window geometry
    window.geometry("1000x500")

    # divide the main frame (screen_frame) into two sections
    right_side_screen_frame = Frame(screen_frame, bg=bg_color)
    right_side_screen_frame.grid(row=0, column=1, sticky=W, padx=(25, 0))
    left_side_screen_frame = Frame(screen_frame, bg=bg_color)
    left_side_screen_frame.grid(row=0, column=0, sticky=E)

    # ==================================================================================================================
    # Edit/Delete Question Section - Left Hand Side
    # ==================================================================================================================

    # information telling the user what to do
    lstbox_info_lbl1 = Label(left_side_screen_frame, text='TRIPLE CLICK to DELETE a question from the options below.'
                             , bg=bg_color)
    lstbox_info_lbl1.grid(row=0, column=0, sticky=W, pady=(10, 0))
    lstbox_info_lbl2 = Label(left_side_screen_frame, text='DOUBLE CLICK to EDIT it.', bg=bg_color)
    lstbox_info_lbl2.grid(row=1, column=0, sticky=W, pady=(0, 0))
    lstbox_info_lbl3 = Label(left_side_screen_frame, text='(Editing the question text is creating a new question '
                                                          'NOT EDITING it.)', bg=bg_color)
    lstbox_info_lbl3.grid(row=2, column=0, sticky=W, pady=(0, 0))
    lstbox_info_lbl4 = Label(left_side_screen_frame, text='(Editing refers to changing the dependencies in the '
                                                          'question text.)', bg=bg_color)
    lstbox_info_lbl4.grid(row=3, column=0, sticky=W, pady=(0, 10))

    # create list box
    question_listbox = Listbox(left_side_screen_frame, width=65)
    question_listbox.grid(row=4, column=0)

    # load list box
    for q in questions_class_list:
        question_listbox.insert(END, q.question_asked)

    # bind the double click to the list box
    question_listbox.bind('<Triple-Button-1>', delete_onclick)
    question_listbox.bind('<Double-Button-1>', edit_question)

    # ==================================================================================================================
    # Add Question Section - Right Hand Side
    # ==================================================================================================================

    # instructions
    header = Label(right_side_screen_frame, text="Fill out the form below to add a question", bg=bg_color)
    header.grid(row=0, column=0, columnspan=2, pady=(20, 0))

    # question to ask
    question_txt_lbl = Label(right_side_screen_frame, text='Enter the question:', bg=bg_color)
    question_txt_lbl.grid(row=1, column=0, pady=(20, 0), sticky=W)
    question_txt_ent = Entry(right_side_screen_frame, textvariable=question_txt, width=50)
    question_txt_ent.grid(row=1, column=1, pady=(20, 0), sticky=W)

    # option 1
    option1_lbl = Label(right_side_screen_frame, text='Enter the first option:', bg=bg_color)
    option1_lbl.grid(row=2, column=0, pady=(10, 0), sticky=W)
    option1_ent = Entry(right_side_screen_frame, textvariable=option1, width=25)
    option1_ent.grid(row=2, column=1, pady=(10, 0), sticky=W)

    # option 2
    option2_lbl = Label(right_side_screen_frame, text='Enter the second option:', bg=bg_color)
    option2_lbl.grid(row=3, column=0, pady=(10, 0), sticky=W)
    option2_ent = Entry(right_side_screen_frame, textvariable=option2, width=25)
    option2_ent.grid(row=3, column=1, pady=(10, 0), sticky=W)

    # option 3
    option3_lbl = Label(right_side_screen_frame, text='Enter the third option:', bg=bg_color)
    option3_lbl.grid(row=4, column=0, pady=(10, 0), sticky=W)
    option3_ent = Entry(right_side_screen_frame, textvariable=option3, width=25)
    option3_ent.grid(row=4, column=1, pady=(10, 0), sticky=W)

    # option 4
    option4_lbl = Label(right_side_screen_frame, text='Enter the fourth option:', bg=bg_color)
    option4_lbl.grid(row=5, column=0, pady=(10, 0), sticky=W)
    option4_ent = Entry(right_side_screen_frame, textvariable=option4, width=25)
    option4_ent.grid(row=5, column=1, pady=(10, 0), sticky=W)

    # correct answer
    answer_lbl = Label(right_side_screen_frame, text='Enter the correct answer:', bg=bg_color)
    answer_lbl.grid(row=6, column=0, pady=(10, 0), sticky=W)
    answer_ent = Entry(right_side_screen_frame, textvariable=answer, width=25)
    answer_ent.grid(row=6, column=1, pady=(10, 0), sticky=W)

    # point value
    points_lbl = Label(right_side_screen_frame, text="Enter a point value (1-3):", bg=bg_color)
    points_lbl.grid(row=7, column=0, pady=(10, 0), sticky=W)
    points_ent = Entry(right_side_screen_frame, textvariable=points, width=5)
    points_ent.grid(row=7, column=1, pady=(10, 0), sticky=W)

    # correct feedback
    cor_feedback_lbl = Label(right_side_screen_frame, text="Enter feedback when answered correctly:", bg=bg_color)
    cor_feedback_lbl.grid(row=8, column=0, pady=(10, 0), sticky=W)
    cor_feedback_ent = Entry(right_side_screen_frame, textvariable=cor_feedback, width=50)
    cor_feedback_ent.grid(row=8, column=1, pady=(10, 0), sticky=W)

    # incorrect feedback
    incor_feedback_lbl = Label(right_side_screen_frame, text="Enter feedback when answered incorrectly:", bg=bg_color)
    incor_feedback_lbl.grid(row=9, column=0, pady=(10, 0), sticky=W)
    incor_feedback_ent = Entry(right_side_screen_frame, textvariable=incor_feedback, width=50)
    incor_feedback_ent.grid(row=9, column=1, pady=(10, 0), sticky=W)

    # clear all the fields - cancel
    cancel_btn = Button(right_side_screen_frame, command=clear_responses, text="Cancel", width=15)
    cancel_btn.grid(row=10, column=0, pady=(20, 0))
    # submit the form
    ok_btn = Button(right_side_screen_frame, command=ok_func, text='Ok', width=15)
    ok_btn.grid(row=10, column=1, pady=(20, 0))


def view_questions():
    """view all available questions"""
    global questions_class_list, screen_frame
    clear_screen()

    # list box for questions
    question_list_lbl = Label(screen_frame, text='List of all the questions', bg=bg_color)
    question_list_lbl.pack()
    view_question_listbox = Listbox(screen_frame, width=60)
    view_question_listbox.pack()

    # fill listbox with all questions
    for q in questions_class_list:
        view_question_listbox.insert(END, q.question_asked)


def search_question():
    """search for a specific question"""
    global questions_class_list, screen_frame

    def main_search_area():
        """tkinter objects placed in frame"""

        def search_func():
            """function called once search button is pressed"""
            nonlocal questions_to_search_lst
            # show all questions if search blank
            if question_search_var.get() == "":
                questions_to_search_lst = [q.question_asked for q in questions_class_list]
            else:
                view_question_listbox.delete('0', 'end')
                search_results = get_close_matches(question_search_var.get(),
                                                   [k.question_asked for k in questions_class_list],
                                                   n=5, cutoff=.2)
                questions_to_search_lst = search_results
            main_search_area()

        # clear screen
        clear_screen()

        # user info
        info_lbl1 = Label(screen_frame, text='Enter a question below and press search to find it.', bg=bg_color)
        info_lbl1.pack()
        info_lbl2 = Label(screen_frame, text='To show all the questions, leave the text box blank and the press search',
                          bg=bg_color)
        info_lbl2.pack()

        # listbox
        view_question_listbox = Listbox(screen_frame, width=60)
        view_question_listbox.pack()

        # fill listbox with all questions
        for q in questions_to_search_lst:
            view_question_listbox.insert(END, q)

        # search entry box
        search_ent = Entry(screen_frame, textvariable=question_search_var, width=60)
        search_ent.pack(pady=(15, 0))

        # search button
        search_btn = Button(screen_frame, text='Search', command=search_func, width=25)
        search_btn.pack(pady=(5, 0))

    # variables
    question_search_var = StringVar()
    questions_to_search_lst = [q.question_asked for q in questions_class_list]

    # change window size
    window.geometry("500x350")

    # call the main_search_area to populate screen
    main_search_area()


def clear_screen():
    """will clear all the widgets from the previous screen and allow new ones to appear"""
    for widget in screen_frame.winfo_children():
        widget.destroy()


def window_closing():
    """will save the data to the json file before the window closes"""
    global window, questions_class_list
    # if the list is not blank (no errors loading the data, etc.), then save data
    if len(questions_class_list) != 0:
        # save question classes to json file
        dump_questions()
    # exit application
    window.quit()


# window of the application
window = Tk()
window.title('Mental Anguish')
bg_color = 'cornsilk'
window.config(bg=bg_color)

# global variables
questions_class_list = list()
question_txt = StringVar()
option1 = StringVar()
option2 = StringVar()
option3 = StringVar()
option4 = StringVar()
answer = StringVar()
points = StringVar()
cor_feedback = StringVar()
incor_feedback = StringVar()

# load the file into the program
load_questions()

# Menu Bar
menu_bar = Menu(window)
window.config(menu=menu_bar)
menu_bar.add_command(label='Take Quiz', command=take_quiz)
menu_bar.add_command(label='Manage Questions', command=manage_questions)
menu_bar.add_command(label='Search for a Question', command=search_question)
menu_bar.add_command(label='Exit', command=window_closing)

# created a screen that allows for dynamic content
screen_frame = Frame(window, bg=bg_color)
screen_frame.pack(padx=25, pady=25)

# call the home page so that is the first thing that will appear when the program is loaded
view_questions()

# close program logic
window.protocol("WM_DELETE_WINDOW", window_closing)

window.mainloop()
# end application
