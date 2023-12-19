# see if can reduce the words to words between 5 and 10 characters 
# make text bigger

import glob
import random
from tkinter import *
from xml.etree.ElementTree import TreeBuilder  # noqa: F403
from random_word import RandomWords, Wordnik
import time

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

CPM = 0

wordnik_service = Wordnik()

random_words = wordnik_service.get_random_words()
# random_words = ['john', 'jingle', 'jheimer']
end_index = ''
start_index = ''
current_letters = []
count = 0
word_count = 0
old_start_index = 0
original_start_index = 0
errors = 0
start = True

def middle_frame(container):
    global CPM
    global start
    #top frame start here 
    top_frame = Frame(container)  # noqa: F405

    top_frame.columnconfigure(0, weight=1)
    top_frame.columnconfigure(1, weight=3)
    top_frame.columnconfigure(3, weight=1)
    top_frame.columnconfigure(4, weight=3)
    top_frame.columnconfigure(5, weight=1)
    top_frame.columnconfigure(6, weight=3)
    top_frame.columnconfigure(7, weight=1)

    # CPM
    corrected_cpm = Label(top_frame, text=f"Accuracy: {CPM}%")  # noqa: F405
    corrected_cpm.grid(column=0, row=0)

    # WPM
    words_per_min = Label(top_frame, text='WPM: ')  # noqa: F405
    words_per_min.grid(column=3, row=0)

    # countdown timer
    def countdown(seconds):
       if seconds > 0:
            time_left.config(text=f'Time Left: {seconds}')
            window.after(1000, countdown, seconds - 1)
       else:
           time_left.config(text=f'Time\'s up!')

    time_left = Label(top_frame, text="Time Left: 60")  # noqa: F405
    time_left.grid(column=5, row=0)

    # Restart
    Label(  # noqa: F405
        top_frame,
        text="Restart",
        foreground="white",
        font=("Arial", 12, "underline"),
        cursor="man",
    ).grid(column=7, row=0)  # noqa: F405

    # countdown(60)

    # middle frame start here 
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
    
    current_word_list = []

    def remove_word():
        global end_index
        global start_index
        current_word = random_words.pop(0)
        for letter in current_word:
            current_word_list.append(letter)
        highlight_word = ''.join(current_word_list).lower()

        if end_index != '':
            split_end = end_index.split('.')
            split_whole = split_end[0]
            split_end = int(split_end[1])
            split_end = split_end + 2
            split_end = str(split_end)
            split_end = split_whole + '.' + split_end
            start_index = split_end
        else:
            start_index = "1.0"

        if start_index == "1.0": 
            text_content = text_box.get(start_index, "end").lower()
            convert_start_index = 0
            found_word = text_content.find(highlight_word, convert_start_index)
            if found_word != -1:
                length = str(len(highlight_word))
                end_index = "1" + "." + length
                text_box.tag_add('highlight', start_index, end_index)
                text_box.tag_config('highlight', background='green')
        else:
            split_start = start_index.split('.')
            split_whole = split_start[0]
            split_start = int(split_start[1])
            split_start = split_start - 1
            
            convert_start_index = int(start_index.split('.')[1])
            convert_start_index = convert_start_index - 1
            convert_start_index = str(convert_start_index)
            convert_start_index = split_whole + '.' + convert_start_index

            text_content = text_box.get(convert_start_index, "end").lower()
            highlight_word = ''.join(current_word_list)
            
            found_word = text_content.find(highlight_word, 0)
            if found_word != -1:
                length = len(highlight_word)
                end_index = convert_start_index.split('.')
                end_whole = end_index[0]
                end_dec = int(end_index[1])
                end_dec = end_dec + length
                end_dec = str(end_dec)
                end_index = end_whole + "." + end_dec
                convert_start_index = str(convert_start_index)
                text_box.tag_add('highlight', convert_start_index, end_index)
                text_box.tag_config('highlight', background='green' )
            else:
                print('word not found')
    
    remove_word()

    def clear_highlight():
        text_box.tag_remove('highlight', '1.0', 'end')
    
    def disable_backspace(event):
        return 'break'
    
    def on_key(event):
        global random_words
        global start_index
        global current_letters
        global count
        global word_count
        global old_start_index
        global original_start_index
        global CPM
        global errors
        global start

        if start:
                countdown(60)
                start = False

        if event.char != ' ':
            CPM += 1

            if len(current_word_list) > 0:
                count += 1
                if event.char == current_word_list[0]: 
                    char_index = start_index.split('.')
                    char_whole = char_index[0]
                    char_index = int(char_index[1])
                    char_index = char_index + 1
                    char_index = count - char_index
                    char_index = char_whole + '.' + str(char_index)

                    if word_count == 0:
                        text_content = text_box.get(start_index, end_index)
                        char_convert = char_index.split('.')[1]
                        char_convert = int(char_convert)
                        found_char = text_content.find(current_word_list[0], char_convert)

                        if found_char != -1:
                            found_char_position = char_whole + '.' + str(found_char)
                            next_char_position = found_char_position + '+1c'
                            text_box.tag_add('font', found_char_position, next_char_position)
                            text_box.tag_config('font', foreground='yellow' )
                            current_letters.append(current_word_list.pop(0))
                        else:
                            print('char not found')
                    else:
                        start_index_convert = start_index.split('.')
                        if old_start_index == 0:
                            start_index_convert_dec = int(start_index_convert[1]) - 1
                            original_start_index = start_index_convert_dec
                            old_start_index += 1
                        else:
                            start_index_convert_dec = int(old_start_index) + original_start_index
                            old_start_index += 1
                       
                        start_index_convert_dec_string = str(start_index_convert_dec)
                        start_index = start_index_convert[0] + '.' + start_index_convert_dec_string
                        text_content = text_box.get(start_index, end_index)
                        char_convert = char_index.split('.')[1]
                        char_convert = int(char_convert)
                        found_char = text_content.find(current_word_list[0], 0)
  
                        if found_char != -1:
                            found_char_position = char_whole + '.' + start_index_convert_dec_string
                            next_char_position = found_char_position + '+1c'
                            text_box.tag_add('font', start_index, next_char_position)
                            text_box.tag_config('font', foreground='yellow' )
                            current_letters.append(current_word_list.pop(0))
                        else:
                            print('char not found')
                else:
                    errors += 1
                    # color the char character red
                    if word_count == 0:
                        char_index = 1
                        char_index = count - char_index
                        full_char_index = "1." + str(char_index)
                        text_content = text_box.get(start_index, end_index)
                        found_char = text_content.find(text_content[char_index], char_index)
                        if found_char != -1:
                            next_char_position = full_char_index + '+1c'
                            text_box.tag_add('wrong_font', full_char_index, next_char_position)
                            text_box.tag_config('wrong_font', foreground='red')
                            current_letters.append(current_word_list.pop(0))
                        else:
                            print('char not found')
                    else:
                        # the word count is greater than 0
                        start_index_convert = start_index.split('.')
                        if old_start_index == 0:
                            start_index_convert_dec = int(start_index_convert[1]) - 1
                            original_start_index = start_index_convert_dec
                            old_start_index += 1
                        else:
                            start_index_convert_dec = int(old_start_index) + original_start_index
                            old_start_index += 1

                        start_index_convert_dec_string = str(start_index_convert_dec)
                        start_index = start_index_convert[0] + '.' + start_index_convert_dec_string
                        text_content = text_box.get(start_index, end_index)
                        found_char = text_content.find(current_word_list[0], 0)

                        if found_char != -1:
                            found_char_position = start_index_convert[0] + '.' + start_index_convert_dec_string
                            next_char_position = found_char_position + '+1c'
                            text_box.tag_add('wrong_font', start_index, next_char_position)
                            text_box.tag_config('wrong_font', foreground='red' )
                            current_letters.append(current_word_list.pop(0))
                        else:
                            print('char not found')

            if errors > 0 and CPM >= 1:
                accuracy = CPM - errors
                accuracy = accuracy/CPM
                cpm_score = accuracy * 100.0
                corrected_cpm.config(text=f"Accuracy: {round(cpm_score)}%")
            else:
                corrected_cpm.config(text="Accuracy: 100%")

            WPM = (CPM/5)/1
            words_per_min.config(text=f'WPM: {WPM}')

        else:            
            if len(current_word_list) != 0:
                print('not end of word')
                return 'break'
            else:
                count += 1
                current_letters = []
                count = 0
                old_start_index = 0
                word_count += 1
                clear_highlight()
                remove_word()

    top_frame.grid(row=0, column=0, sticky="ew")
    bottom_frame.insert("1.0", "type the words here...")
    bottom_frame.pack(fill=X)

    bottom_frame.bind("<FocusIn>", on_entry)
    bottom_frame.bind("<FocusOut>", on_exit)
    bottom_frame.bind("<BackSpace>", disable_backspace)
    bottom_frame.bind("<Key>", on_key)

    return frame

def main_frame(parent):
    main_frame = Frame(parent)  # noqa: F405
    main_frame.grid(row=3, column=0)

    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(0, weight=4)
    main_frame.rowconfigure(1, weight=3)

    middle = middle_frame(main_frame)
    middle.grid(row=1, column=0, sticky="ew")

container_frame = Frame(window)  # noqa: F405
container_frame.pack()

main_frame(container_frame)
window.mainloop()
