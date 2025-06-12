from time import sleep
from tkinter import *
from tkinter import ttk
import time
from pygame import mixer
from tkinter import font


def on_tab_change(event):
    current_tab = notebook.select()
    current_frame = notebook.nametowidget(current_tab)
    for child in current_frame.winfo_children():
        if isinstance(child, ttk.Frame):
            for inner_child in child.winfo_children():
                if isinstance(inner_child, Text):
                    inner_child.focus_set()
                    return


root = Tk()
root.geometry("610x500+600+200")
root.title("Морзянка")
root.config(cursor="heart")

notebook_style = ttk.Style()
notebook_style.theme_use('winnative')
notebook_style.configure("My.TNotebook", padding=5, background="#00483E")
notebook_style.configure(
    "My.TNotebook.Tab",
    font=("Book Antiqua", 12),
    background="#A7DDD6",
    foreground="#001915",
    padding=[8, 2],
)
notebook_style.map(
    "My.TNotebook.Tab",
    background=[("selected", "#CCEBE6")],  # Цвет фона активной вкладки
    foreground=[("selected", "#15534A")],  # Цвет текста активной вкладки
)

frame_style = ttk.Style()
frame_style.configure('My.TFrame', background="#CCEBE6")
button_style = ttk.Style()
button_style.configure('My.TButton', background="#195E55", foreground='#001915', font=("Book Antiqua", 12))
check_style = ttk.Style()
check_style.configure('My.TCheckbutton', background="#E4F7F4", foreground='#001915', font=("Book Antiqua", 12))
radio_style = ttk.Style()
radio_style.configure('My.TRadiobutton', background="#E4F7F4", foreground='#001915', font=("Book Antiqua", 12))
label_style = ttk.Style()
label_style.configure('My.TLabel', background="#E4F7F4", foreground='#001915', font=("Book Antiqua", 20, 'bold'))
text_background, text_foreground, text_font = '#F9FFFE', '#00221D', ("Book Antiqua", 18, 'bold')

notebook = ttk.Notebook(root, style='My.TNotebook')
notebook.pack(expand=True, fill=BOTH)
note1 = ttk.Frame(notebook, style='My.TFrame')
note1.pack(fill=BOTH, expand=True)
note2 = ttk.Frame(notebook, style='My.TFrame')
note2.pack(fill=BOTH, expand=True)
note3 = ttk.Frame(notebook, style='My.TFrame')
note3.pack(fill=BOTH, expand=True)
note4 = ttk.Frame(notebook, style='My.TFrame')
note4.pack(fill=BOTH, expand=True)
notebook.add(note1, text='Morse Code в текст')
notebook.add(note2, text='MC в текст Light Ver')
notebook.add(note3, text='Текст в Morse Code')
notebook.add(note4, text='Обучение')
notebook.bind("<<NotebookTabChanged>>", on_tab_change)

mixer.init()
key_press_time = None
new_word = False
key_is_held = False
is_playing = False
# for family in font.families():
#     print(family)
cfont = font.Font(family='Leelawadee', size=10, weight='normal', slant='roman')
dot_sound =  mixer.Sound('morse_code1.mp3')
dash_sound =  mixer.Sound('morse_code2.mp3')
morse_code = {
    '.-': 'А', '-...': 'Б', '.--': 'В', '--.': 'Г', '-..': 'Д',
    '.': 'Е', '...-':'Ж', '--..':'З', '..':'И',
    '.---':'Й', '-.-':'К', '.-..':'Л', '--':'М', '-.':'Н',
    '---':'О', '.--.':'П', '.-.':'Р', '...':'С', '-':'Т',
    '..-':'У', '..-.':'Ф', '....':'Х', '-.-.':'Ц', '---.':'Ч',
    '----':'Ш', '--.-':'Щ', '.--.-.':'Ъ' ,'-.--':'Ы',
    '-..-':'Ь', '...-...':'Э', '..--':'Ю', '.-.-':'Я', '......': '.',
    '.-.-.-': ',', '-..-.': '/', '..--..': '?', '--..--': '!'
}
reverse_morse_code = {value: key for key, value in morse_code.items()}
keys_alpha = list(morse_code.values())
values_code = list(morse_code.keys())


#------------------------Первая вкладка---------------------------

def get_translate():
    txt = enter_morse.get(1.0, END).rstrip().split()
    output_text.delete(1.0, END)
    output_text.insert(END, "".join([morse_code[letter] if letter in morse_code.keys() else " " for letter in txt ]))
    enter_morse.focus_set()


def on_key_press(event):
    global key_press_time, key_is_held, new_word
    if event.keysym == 'space' and not key_is_held:
        key_is_held = True
        key_press_time = time.time()
        d = time.time() - new_word
        if len(enter_morse.get(1.0, END)) > 1:
            if 0.4 < d <= 1:
                enter_morse.insert(END, " ")
            elif d > 1:
                enter_morse.insert(END, " | ")
        new_word = None
    if event.keysym == 'BackSpace':
        return "continue"
    return "break"


def on_key_release(event):
    global key_press_time, key_is_held, new_word
    if event.keysym == 'space' and key_is_held:
        duration = time.time() - key_press_time
        # enter_morse.insert(END, f'!{duration:.2f}!')
        if duration < 0.20:
            dot_sound.play()
            enter_morse.insert(END, '.')
        else:
            dash_sound.play()
            enter_morse.insert(END, '-')
        key_press_time = None
        key_is_held = False
        new_word = time.time()
        return "break"


input_frame = ttk.Frame(note1, border=4, relief=SUNKEN, padding=[3, 3])
input_frame.place(relheight=0.40, relwidth=0.98, relx=0.01, rely=0.01)
enter_morse = Text(input_frame, wrap="word", background=text_background, foreground=text_foreground, font=text_font)
enter_morse.pack(expand=True, fill=BOTH)
enter_morse.bind("<KeyPress>", on_key_press)
enter_morse.bind("<KeyRelease>", on_key_release)
enter_morse.focus_set()

act_frame = ttk.Frame(note1, border=4, relief=RAISED, padding=[3, 3])
act_frame.place(relheight=0.15, relwidth=0.98, relx=0.01, rely=0.42)
act_button = ttk.Button(act_frame, text="Перевести", command=get_translate, style='My.TButton')
act_button.pack(expand=True, fill=BOTH)

output_frame = ttk.Frame(note1, border=4, relief=SUNKEN, padding=[3, 3])
output_frame.place(relheight=0.40, relwidth=0.98, relx=0.01, rely=0.58)
output_text = Text(output_frame, wrap="word", background=text_background, foreground=text_foreground, font=text_font)
output_text.pack(expand=True, fill=BOTH)


#------------------------Вторая вкладка---------------------------
def light_get_translate():
    txt = light_enter_morse.get(1.0, END).rstrip().split(" ")
    light_output_text.delete(1.0, END)
    light_output_text.insert(END, "".join([morse_code[letter] if letter in morse_code.keys() else " " for letter in txt ]))
    light_enter_morse.focus_set()


def on_key_press(event):
    global key_press_time, key_is_held
    if event.keysym == 'space' and not key_is_held:
        key_is_held = True
        key_press_time = time.time()
    if event.keysym == 'BackSpace':
        return "continue"
    if event.keysym == 'n':
        light_enter_morse.insert(END, " ")
    if event.keysym == 'w':
        light_enter_morse.insert(END, " | ")
    return "break"


def on_key_release(event):
    global key_press_time, key_is_held
    if event.keysym == 'space' and key_is_held:
        duration = time.time() - key_press_time
        if duration < 0.20:
            dot_sound.play()
            light_enter_morse.insert(END, '.')
        else:
            dash_sound.play()
            light_enter_morse.insert(END, '-')
        key_press_time = None
        key_is_held = False
        return "break"


light_input_frame = ttk.Frame(note2, border=4, relief=SUNKEN, padding=[3, 3])
light_input_frame.place(relheight=0.40, relwidth=0.98, relx=0.01, rely=0.01)
light_enter_morse = Text(light_input_frame, wrap="word", background=text_background, foreground=text_foreground,
                         font=text_font)
light_enter_morse.pack(expand=True, fill=BOTH)
light_enter_morse.bind("<KeyPress>", on_key_press)
light_enter_morse.bind("<KeyRelease>", on_key_release)

light_act_frame = ttk.Frame(note2, border=4, relief=RAISED, padding=[3, 3])
light_act_frame.place(relheight=0.15, relwidth=0.98, relx=0.01, rely=0.42)
light_act_button = ttk.Button(light_act_frame, text="Перевести", command=light_get_translate, style='My.TButton')
light_act_button.pack(expand=True, fill=BOTH)

light_output_frame = ttk.Frame(note2, border=4, relief=SUNKEN, padding=[3, 3])
light_output_frame.place(relheight=0.40, relwidth=0.98, relx=0.01, rely=0.58)
light_output_text = Text(light_output_frame, wrap="word", background=text_background, foreground=text_foreground,
                         font=text_font)
light_output_text.pack(expand=True, fill=BOTH)


#------------------------Третья вкладка---------------------------

def get_translate_text():
    output_morse.delete('1.0', END)
    correct_text = ' '.join(enter_text.get(1.0, END).split())
    for word in correct_text:
        correct_word = word.upper()
        if correct_word not in keys_alpha:
            if word == " ":
                output_morse.insert(END, " | ")
            else:
                output_morse.insert(END, word)
        else:
            m = reverse_morse_code[correct_word]
            output_morse.insert(END, m + " ")
            for elm in m:
                if elm == ".":
                    dot_sound.play()
                    output_morse.update()
                    sleep(0.3)
                else:
                    dash_sound.play()
                    output_morse.update()
                    sleep(0.6)
    enter_text.focus_set()


text_input_frame = ttk.Frame(note3, border=4, relief=SUNKEN, padding=[3, 3])
text_input_frame.place(relheight=0.40, relwidth=0.98, relx=0.01, rely=0.01)
enter_text = Text(text_input_frame, wrap="word", background=text_background, foreground=text_foreground, font=text_font)
enter_text.pack(expand=True, fill=BOTH)

text_act_frame = ttk.Frame(note3, border=4, relief=RAISED, padding=[3, 3])
text_act_frame.place(relheight=0.15, relwidth=0.98, relx=0.01, rely=0.42)
text_act_button = ttk.Button(text_act_frame, text="Перевести", command=get_translate_text, style='My.TButton')
text_act_button.pack(expand=True, fill=BOTH)

get_morse_frame = ttk.Frame(note3, border=4, relief=SUNKEN, padding=[3, 3])
get_morse_frame.place(relheight=0.40, relwidth=0.98, relx=0.01, rely=0.58)
output_morse = Text(get_morse_frame, wrap="word", background=text_background, foreground=text_foreground, font=text_font)
output_morse.pack(expand=True, fill=BOTH)


#------------------------Четвертая вкладка---------------------------

def learn_key_press(event):
    global key_press_time, key_is_held
    if event.keysym == 'space' and not key_is_held:
        key_is_held = True
        key_press_time = time.time()
    if event.keysym == 'BackSpace':
        return "continue"
    if event.keysym == "Return":
        check_mistake()
    return "break"


def learn_key_release(event):
    global key_press_time, key_is_held
    if event.keysym == 'space' and key_is_held:
        duration = time.time() - key_press_time
        if duration < 0.20:
            dot_sound.play()
            enter_letter.insert(END, '.')
        else:
            dash_sound.play()
            enter_letter.insert(END, '-')
        key_press_time = None
        key_is_held = False
        return "break"


def check_mistake():
    global i
    enabled.set(1) if enter_letter.get() == for_check.get() else enabled.set(0)
    if enabled.get() == 1:
        if i < 32:
            i += 1
        else:
            i = 0
        letter.set(keys_alpha[i])
        for_check.set(values_code[i])
    enter_letter.delete(0, END)
    enter_letter.focus()


def select():
    global check_close

    def on_window_close():
        global check_close
        check_close = True
        window.destroy()
        radio_check.set(0)

    if check_close:
        check_close = False
        window = Toplevel(root)
        window.title("Справочник")
        window.geometry("420x400")
        window.configure(bg='#E4F7F4')
        window.resizable(False, False)

        count_row = 6
        len_keys_alpha = len(keys_alpha)
        count_column = len_keys_alpha // count_row + 1
        for c in range(count_column):
            window.columnconfigure(index=c, weight=1)
        for r in range(count_row):
            window.rowconfigure(index=r, weight=1)
        count_alpha = 0
        for i in range(count_row):
            for j in range(count_column):
                if count_alpha < len_keys_alpha:
                    ttk.Label(window, text=f'  {keys_alpha[count_alpha]}: {values_code[count_alpha]}  ', background="#E4F7F4", foreground='#001915',
                              font=("Book Antiqua", 12, 'bold')).grid(row=i, column=j, sticky='nsew')
                    count_alpha += 1
                else:
                    break
        window.protocol("WM_DELETE_WINDOW", on_window_close)

    enter_letter.focus()

check_close = True

learn_frame = ttk.Frame(note4, border=2, relief=SOLID, padding=[3, 3])
learn_frame.pack(expand=True, fill=BOTH)
for r in range(4):
    learn_frame.rowconfigure(index=r, weight=1)
for c in range(2):
   learn_frame.columnconfigure(index=c, weight=1)

enabled = IntVar(value=0)
letter = StringVar(value=keys_alpha[0])
for_check = StringVar(value=values_code[0])
i = 0

alphabet = ttk.Label(learn_frame, border=2, textvariable=letter, anchor='center', style='My.TLabel')
alphabet.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

enter_letter = ttk.Entry(learn_frame, background='#EBFFFC', foreground='#00221D', font=("Book Antiqua", 18, 'bold'))
enter_letter.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
enter_letter.bind("<KeyPress>", learn_key_press)
enter_letter.bind("<KeyRelease>", learn_key_release)

enabled_ckeckbutton = ttk.Checkbutton(learn_frame, text='ВЕРНО', variable=enabled, style='My.TCheckbutton')
enabled_ckeckbutton.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)

check_button = ttk.Button(learn_frame, text='Проверить', command=check_mistake, style='My.TButton')
check_button.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

radio_check = IntVar(value=0)
radiobutton_check = ttk.Radiobutton(learn_frame, text='Подсказка', variable=radio_check, command=select,
                                    style='My.TRadiobutton')
radiobutton_check.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)


root.mainloop()