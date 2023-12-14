# make it interactive
    # connect the bottom frame to the words in the middle Frame
    # highlight current word
    # indicate correct and incorrect characters pushed
    # upon space move to next word in list
    # if close to the end then bring in and append a new list of words
# calc score

from tkinter import *  # noqa: F403
from random_word import RandomWords, Wordnik

window = Tk()  # noqa: F405
window.title("Typing Speed Test")
window.geometry("600x525")  # adjust the size here

canvas = Canvas(width=600, height=200, background="#800808")  # noqa: F405\
canvas.pack()

title = canvas.create_text(
    300,
    50,
    text="Typing Speed Test",
    width=350,
    font=("Arial", 30, "bold"),
    fill="white",
)

question = canvas.create_text(
    300,
    125,
    text="How fast are your fingers?",
    width=550,
    font=("Arial", 16, "bold"),
    fill="white",
)

directions = canvas.create_text(
    300,
    155,
    text="Do the one-minute typing test to find out! Press the space bar after each word. At the end, you'll get your typing speed in CPM and WPM. Good luck!",
    width=550,
    font=("Arial", 14),
    fill="white",
)

def top_frame(container):
    frame = Frame(container)  # noqa: F405

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=3)
    frame.columnconfigure(3, weight=1)
    frame.columnconfigure(4, weight=3)
    frame.columnconfigure(5, weight=1)
    frame.columnconfigure(6, weight=3)
    frame.columnconfigure(7, weight=1)

    # CPM
    Label(frame, text="Corrected CPM: ").grid(column=0, row=0)  # noqa: F405
    corrected_cpm = Entry(frame, width=10)  # noqa: F405
    corrected_cpm.grid(column=1, row=0)

    # WPM
    Label(frame, text="WPM: ").grid(column=3, row=0)  # noqa: F405
    words_per_min = Entry(frame, width=10)  # noqa: F405
    words_per_min.grid(column=4, row=0)

    # Time left
    Label(frame, text="Time Left: ").grid(column=5, row=0)  # noqa: F405
    time_left = Entry(frame, width=10)  # need timer here  # noqa: F405
    time_left.grid(column=6, row=0)

    # Restart
    Label(
        frame,
        text="Restart",
        foreground="white",
        font=("Arial", 12, "underline"),
        cursor="man",
    ).grid(column=7, row=0)  # noqa: F405

    return frame


wordnik_service = Wordnik()

random_words = wordnik_service.get_random_words()


def middle_frame(container):
    frame = Frame(container)  # noqa: F405
    frame.columnconfigure(0, weight=1)

    words_text = " ".join(random_words)

    text_box = Text(
        frame, width=60, height=10, wrap=WORD, font=("Arial", 15), padx=20, pady=20
    )  # noqa: F405
    text_box.insert(END, words_text)  # noqa: F405
    text_box.config(state=DISABLED)  # noqa: F405
    text_box.pack(fill=X)  # noqa: F405

    bottom_frame = Text(frame, width=60, height=1, wrap=WORD, font=('Arial', 15), padx=20, pady=20)

    def on_entry(event):
        if bottom_frame.get("1.0", "end-1c") == "type the words here...":
            bottom_frame.delete("1.0", "end")
    
    def on_exit(event):
        if bottom_frame.get("1.0", "end-1c") == "":
            bottom_frame.insert("1.0", "type the words here...")

    def on_key(event):
        global random_words
        # pop off first word in random word
        # as letter is typed pop off first letter
        # when space is hit, restart with next word?
        print(event.char)
        print(random_words[0][0])
        if event.char != ' ':
            if len(random_words) > 0:
                current_word = random_words.pop(0)
                print(f'removed word: {current_word}')
                print(f'removed word type: {type(current_word)}')
                current_word_list = list(current_word)
                print(f'removed word list: {current_word_list}')
                print(f'removed word type list: {type(current_word_list)}')
                print(f'removed char: {current_word[0]}')
                print(f'remaining words: {random_words}')
                # compare event.char to the current_word_list[0], if same then pop off into another list and color letter yellow, if diff then pop off into another list and color letter red
        else:
            print('space hit')
        # current_word = random_words[1:]
        # print(current_word)
        # if event.char == random_words[0][0]:
        #     print('bingo')

        # else:
        #     print('bongo')


    bottom_frame.insert("1.0", "type the words here...")
    bottom_frame.pack(fill=X)

    bottom_frame.bind("<FocusIn>", on_entry)
    bottom_frame.bind("<FocusOut>", on_exit)
    bottom_frame.bind("<Key>", on_key)

    

    return frame

# def bottom_frame(container):
#     frame = Frame(container)
#     frame.columnconfigure(0, weight=1)

#     text_box = Text(
#         frame, width=60, height=1, wrap=WORD, font=("Arial", 15), padx=20, pady=20,
#     )  # noqa: F405

#     def on_entry(event):
#         if text_box.get("1.0", "end-1c") == "type the words here...":
#             text_box.delete("1.0", "end")

#     def on_exit(event):
#         if text_box.get("1.0", "end-1c") == "":
#             text_box.insert("1.0", "type the words here...")

#     text_box.insert("1.0", "type the words here...")
#     text_box.pack(fill=X)  # noqa: F405

#     text_box.bind("<FocusIn>", on_entry)
#     text_box.bind("<FocusOut>", on_exit)

#     return frame


def main_frame(parent):
    main_frame = Frame(parent)  # noqa: F405
    # main_frame.pack()
    main_frame.grid(row=3, column=0)

    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(0, weight=4)
    main_frame.rowconfigure(1, weight=3)
    # main_frame.rowconfigure(2, weight=2)

    top = top_frame(main_frame)
    top.grid(row=0, column=0, sticky="ew")
    middle = middle_frame(main_frame)
    middle.grid(row=1, column=0)
    # bottom = bottom_frame(main_frame)
    # bottom.grid(row=2, column=0)


container_frame = Frame(window)  # noqa: F405
container_frame.pack()

main_frame(container_frame)
window.mainloop()
