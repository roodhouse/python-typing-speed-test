# make it interactive
    # indicate correct and incorrect characters pushed
    # if close to the end then bring in and append a new list of words
# calc score

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
        # start_index = ''

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
        
        if event.char != ' ':
            if len(current_word_list) > 0:
                count += 1
                if event.char == current_word_list[0]: 
                    # color the character yellow
                    char_index = start_index.split('.')
                    char_whole = char_index[0]
                    char_index = int(char_index[1])
                    char_index = char_index + 1
                    char_index = count - char_index
                    char_index = char_whole + '.' + str(char_index)
                    text_content = text_box.get(start_index, end_index)
                    print(f'text_content is {text_content}')
                    text_content_single = text_box.get(char_index)
                    print(f'text_content_single is {text_content_single}')
                    
                    char_convert = char_index.split('.')[1]
                    char_convert = int(char_convert)
                    found_char = text_content.find(current_word_list[0], char_convert)
                    print(found_char)
  
                    if found_char != -1:
                        found_char_position = char_whole + '.' + str(found_char)
                        print(f'found char postion is: {found_char_position}')
                        next_char_position = found_char_position + '+1c'
                        print(f'end pos is {next_char_position}')
                        text_box.tag_add('font', found_char_position, next_char_position)
                        text_box.tag_config('font', foreground='yellow' )
                        current_letters.append(current_word_list.pop(0))
                else:
                    current_letters.append(current_word_list.pop(0))
                    # color the character red
                    
        else:
            if len(current_word_list) != 0:
                print('not end of word')
                return 'break'
            else:
                current_letters = []
                count = 0
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
