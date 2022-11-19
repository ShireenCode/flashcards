from tkinter import *
import pandas as pd
import random

# CONSTANTS
BACKGROUND_COLOR = "#B1DDC6"
chosen_card = {}
to_learn = {}
# ------------------------------
#UI
window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# ------------------------------
# Generate French words

try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pd.read_csv("data/french_words.csv")
    df = data.to_dict(orient="records")
else:
    df = pd.read_csv(data)
    df = df.to_dict(orient="records")


def generate_word():
    global chosen_card, timer
    window.after_cancel(timer)
    chosen_card = random.choice(df)
    flashcard.itemconfig(language, text="French", fill="black")
    flashcard.itemconfig(french_word, text=chosen_card["French"], fill="black")
    flashcard.itemconfig(flashcard_bg, image=flashcard_front_img)
    timer = window.after(3000, func=reveal_answer)


def reveal_answer():
    flashcard.itemconfig(language, text="English", fill="white")
    flashcard.itemconfig(french_word, text=chosen_card["English"], fill="white")
    flashcard.itemconfig(flashcard_bg, image=flashcard_back_img)

def known_word():
    df.remove(chosen_card)
    generate_word()
    data2 = pd.DataFrame(df)
    data2.to_csv("data/words_to_learn.csv", index=False)

# ------------------------------

#Flashcard
flashcard = Canvas(width=800, height=526)
flashcard.config(bg=BACKGROUND_COLOR, highlightthickness=0)
flashcard.grid(row=0, column=0, columnspan=2)
flashcard_front_img = PhotoImage(file="images/card_front.png")
flashcard_back_img = PhotoImage(file="images/card_back.png")
flashcard_bg = flashcard.create_image(400, 263, image=flashcard_front_img)
language = flashcard.create_text(400, 150, text="French", font=("Ariel", 40, "italic"), fill="black")
french_word = flashcard.create_text(400, 263, text="Start", font=("Ariel", 60, "bold"))

#Wrong button
wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=generate_word)
wrong_button.grid(row=1, column=0)

#Right button
right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=known_word)
right_button.grid(row=1, column=1)


timer = window.after(3000, func=generate_word)
generate_word()

window.mainloop()
