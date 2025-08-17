from tkinter import *
from random import randint, choice
import threading
from tkinter import ttk

# Main Window
root = Tk()
root.geometry("650x550")
root.title("Maths Quiz")

question = StringVar()
answer = StringVar()
givenAnswer = StringVar()
score = IntVar()
questionNo = IntVar()
timer = IntVar(value=10)
difficulty = StringVar(value="Easy")

questionLabel = None
resultLabel = None
timerLabel = None
timer_running = False


# ---------------- Difficulty Mapping ----------------
def get_operators():
    level = difficulty.get()
    if level == "Easy":
        return ['+']
    elif level == "Medium":
        return ['+', '-', '*']
    else:
        return ['+', '-', '*', '/']


# ---------------- Generate Question ----------------
def generateQuestion():
    global questionLabel, timer_running

    questionNo.set(questionNo.get() + 1)
    progress['value'] = questionNo.get()
    timer.set(10)

    number1 = randint(1, 20)
    number2 = randint(1, 20)
    operator = choice(get_operators())

    if operator == '/':
        number1 = number1 * number2
        question.set(f"{number1}/{number2}")
        answer.set(str(int(number1 / number2)))
    else:
        question.set(f"{number1}{operator}{number2}")
        answer.set(str(eval(question.get())))

    if questionLabel:
        questionLabel.config(text=f'Q{questionNo.get()} : {question.get()}')
    else:
        questionLabel = Label(root, text=f'Q{questionNo.get()} : {question.get()}', font=("arial", 20))
        questionLabel.grid(row=2, column=0, columnspan=2)

    givenAnswer.set("")
    updateTimer()
    timer_running = True
    countdown()


# ---------------- Timer Logic ----------------
def countdown():
    global timer_running
    if timer.get() > 0 and timer_running:
        timer.set(timer.get() - 1)
        timerLabel.config(text=f"Time Left: {timer.get()}s")
        root.after(1000, countdown)
    elif timer.get() == 0 and timer_running:
        timer_running = False
        checkAnswer(auto=True)


def updateTimer():
    global timerLabel
    if not timerLabel:
        timerLabel = Label(root, text=f"Time Left: {timer.get()}s", font=("arial", 16), fg="red")
        timerLabel.grid(row=4, column=0, columnspan=2)
    else:
        timerLabel.config(text=f"Time Left: {timer.get()}s")


# ---------------- Check Answer ----------------
def checkAnswer(auto=False):
    global resultLabel, timer_running
    timer_running = False

    if resultLabel:
        resultLabel.destroy()

    try:
        user_ans = float(givenAnswer.get()) if not auto else None
        correct_ans = float(answer.get())

        if not auto and round(user_ans, 2) == round(correct_ans, 2):
            score.set(score.get() + 1)
            resultLabel = Label(root, text="Correct", font=('arial', 20), fg='green')
        else:
            resultLabel = Label(root, text=f"Wrong! Answer: {correct_ans}", font=('arial', 20), fg='red')

    except:
        resultLabel = Label(root, text="Invalid Input", font=('arial', 20), fg='orange')

    resultLabel.grid(row=5, column=0, columnspan=2)
    scoreLabel.config(text=f'Score : {score.get()}')

    if questionNo.get() == 10:
        resultLabel.config(text=f'Final Score : {score.get()}/10', fg='blue')
    else:
        root.after(1000, generateQuestion)


# ---------------- Restart Quiz ----------------
def restart():
    score.set(0)
    questionNo.set(0)
    givenAnswer.set("")
    resultLabel.config(text="")
    scoreLabel.config(text=f'Score : {score.get()}')
    progress['value'] = 0
    generateQuestion()


# ---------------- UI Setup ----------------
headingLabel = Label(root, text="Maths Quiz", font=('arial', 25), fg="black")
headingLabel.grid(row=0, column=0, columnspan=2, pady=10)

# Difficulty Dropdown
difficultyLabel = Label(root, text="Select Difficulty:", font=("arial", 14))
difficultyLabel.grid(row=1, column=0, sticky=W, padx=10)
difficultyMenu = OptionMenu(root, difficulty, "Easy", "Medium", "Hard")
difficultyMenu.grid(row=1, column=1, sticky=W)

questionLabel = Label(root, text="", font=("arial", 20))
questionLabel.grid(row=2, column=0, columnspan=2)

answerEntry = Entry(root, textvariable=givenAnswer, font=("arial", 20))
answerEntry.grid(row=3, column=0, padx=10, pady=10)

submitButton = Button(root, text="Submit", font=("arial", 15), command=checkAnswer)
submitButton.grid(row=3, column=1, padx=10)

timerLabel = Label(root, text=f"Time Left: {timer.get()}s", font=("arial", 16), fg="red")
timerLabel.grid(row=4, column=0, columnspan=2)

resultLabel = Label(root, text="", font=('arial', 20), fg='blue')
resultLabel.grid(row=5, column=0, columnspan=2)

scoreLabel = Label(root, text=f'Score : {score.get()}', font=("arial", 20), fg='black')
scoreLabel.grid(row=6, column=0, columnspan=2)

restartButton = Button(root, text="Restart", font=("arial", 15), command=restart, width=30)
restartButton.grid(row=7, column=0, columnspan=2, pady=10)

progress = ttk.Progressbar(root, orient=HORIZONTAL, length=400, mode='determinate', maximum=10)
progress.grid(row=8, column=0, columnspan=2, pady=10)


generateQuestion()
root.mainloop()
