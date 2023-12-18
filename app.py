# make it interactive
    # indicate correct and incorrect characters pushed
    # if close to the end then bring in and append a new list of words
# calc score

import random
from tkinter import *
from xml.etree.ElementTree import TreeBuilder  # noqa: F403
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

# random_words = wordnik_service.get_random_words()
random_words = ['john', 'jingle', 'jheimer']
end_index = ''
start_index = ''
current_letters = []
count = 0
word_count = 0
old_start_index = 0
original_start_index = 0

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
    
    def on_key(event):
        global random_words
        global start_index
        global current_letters
        global count
        global word_count
        global old_start_index
        global original_start_index
        
        if event.char != ' ':
            if len(current_word_list) > 0:
                count += 1
                if event.char == current_word_list[0]: 
                    char_index = start_index.split('.')
                    char_whole = char_index[0]
                    char_index = int(char_index[1])
                    char_index = char_index + 1
                    char_index = count - char_index
                    char_index = char_whole + '.' + str(char_index)
                    # print(f'char index at start: {char_index}')
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
                        print(f'start convert is: {start_index_convert[1]}')
                        if old_start_index == 0:
                        # if start something is less than a number then subtract the start index conver by 1, else do otherwise
                            print(f'old start index is {old_start_index}')
                            start_index_convert_dec = int(start_index_convert[1]) - 1
                            original_start_index = start_index_convert_dec
                            old_start_index += 1
                        else:
                            print('here')
                            # add start index or start_index_convert to old_start_index
                            print(f'the start index is {start_index} and the convert is {start_index_convert[1]}')
                            print(f'old start index is {old_start_index}')
                            # start_index_convert_dec = int(start_index_convert[1])
                            # start_index_convert_dec = int(old_start_index) + int(start_index_convert[1])
                            start_index_convert_dec = int(old_start_index) + original_start_index
                            print(start_index_convert_dec)
                            old_start_index += 1
                       
                        start_index_convert_dec_string = str(start_index_convert_dec)
                        start_index = start_index_convert[0] + '.' + start_index_convert_dec_string
                        text_content = text_box.get(start_index, end_index)
                        
                        char_convert = char_index.split('.')[1]
                        char_convert = int(char_convert)
                        
                        # found_char = text_content.find(current_word_list[0], start_index_convert_dec)
                        found_char = text_content.find(current_word_list[0], 0)
                        found_character = text_content[found_char]
  
                        if found_char != -1:
                            print(f'start index convet dec is {start_index_convert_dec}')
                            print(f'char convert is {char_convert}')
                            print(f'start index is {start_index}')
                            # found_char_position = char_whole + '.' + str(found_char)
                            found_char_position = char_whole + '.' + start_index_convert_dec_string
                            # here !!!
                            print(f'found_char_position is {found_char_position}')
                            next_char_position = found_char_position + '+1c'
                            print(f'next char pos is {next_char_position}')
                            # text_box.tag_add('font', found_char_position, next_char_position)
                            text_box.tag_add('font', start_index, next_char_position)
                            text_box.tag_config('font', foreground='yellow' )
                            current_letters.append(current_word_list.pop(0))
                        else:
                            print('char not found')
                            print(f'the actual cahr is {found_character}')
                            print(f'found char is {found_char} and should be 0 or true')
                            print(text_content)
                            print(current_word_list[0])
                else:
                    # color the char character red
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

    bottom_frame.insert("1.0", "type the words here...")
    bottom_frame.pack(fill=X)

    bottom_frame.bind("<FocusIn>", on_entry)
    bottom_frame.bind("<FocusOut>", on_exit)
    bottom_frame.bind("<Key>", on_key)

    

    return frame

def main_frame(parent):
    main_frame = Frame(parent)  # noqa: F405
    main_frame.grid(row=3, column=0)

    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(0, weight=4)
    main_frame.rowconfigure(1, weight=3)

    top = top_frame(main_frame)
    top.grid(row=0, column=0, sticky="ew")
    middle = middle_frame(main_frame)
    middle.grid(row=1, column=0)

container_frame = Frame(window)  # noqa: F405
container_frame.pack()

main_frame(container_frame)
window.mainloop()
