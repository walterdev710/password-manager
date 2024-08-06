from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

FONT_NAME = "Calibri"
FONT_SIZE= 12
BG_COLOR = "white"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

#Password Generator Project
def pass_generate():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]  

    password_nums = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_nums

    random.shuffle(password_list)

    password = "".join(password_list)

    pyperclip.copy(password)
    pass_entry.insert(0, password)

# ---------------------------- Hide and show password ---------------------------- 
def toggle_password():
    if pass_entry.cget("show") == "":
        pass_entry.config(show="*")
        toggle_btn.config(text="Show")
    else:
        pass_entry.config(show="")
        toggle_btn.config(text="Hide")
        
# ---------------------------- Writing in json  ---------------------------- #
def writing_in(data):
    with open("data.json", "w") as data_file:
        json.dump(data, data_file, indent=4)



# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_data():
    website = web_entry.get()
    email = email_entry.get()
    password = pass_entry.get()
    new_data = {
        website:{
            "email":email,
            "password": password             
            
        }
    }   
    
    
    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showerror(title="OOPS", message="Don't leave any inputs empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                # == Read the existing File == # 
                data = json.load(data_file)
        except FileNotFoundError:
            writing_in(new_data)
        else:
            # Update the file with new data
            data.update(new_data)
            writing_in(data)
        finally:
            web_entry.delete(0, END)
            pass_entry.delete(0, END)


def find_pass():
    website = web_entry.get()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            
    except FileNotFoundError:
        messagebox.showerror(title="Oops",message="No data file found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="No website", message=f"No details for the {website} exist")
           
            
            
           


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=60, pady=60, bg="white")

canvas = Canvas(width=200, height=200, bg=BG_COLOR, highlightthickness=0)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

# -------------------------- Labels --------------------------
web_label = Label(text="Website:", font=(FONT_NAME, FONT_SIZE), bg=BG_COLOR,)
web_label.grid(row=1, column=0,)

email_label = Label(text="Email/Username: ", font=(FONT_NAME, FONT_SIZE), bg=BG_COLOR,)
email_label.grid(row=2, column=0)

pass_label = Label(text="Password: ", font=(FONT_NAME, FONT_SIZE), bg=BG_COLOR,)
pass_label.grid(row=3, column=0)

# -------------------------- Entries -------------------------- #

web_entry = Entry(width=21, highlightthickness=0)
web_entry.focus()
web_entry.grid(row=1, column=1, pady=5)


email_entry = Entry(width=35, highlightthickness=0)
email_entry.insert(0, "fake@gmail.com")
email_entry.grid(row=2, column=1, pady=5, columnspan=2)

pass_entry = Entry(width=21, highlightthickness=0, show="*")
pass_entry.grid(row=3, pady=5, column=1)

# Toggle btn for showing and hiding password
toggle_btn = Button(text="Show", width=10, bg=BG_COLOR, highlightthickness=0, command=toggle_password)
toggle_btn.grid(row=3, column=2)

# -------------------------- Buttons -------------------------- #
search_btn = Button(text="Search", bg=BG_COLOR, width=10, command=find_pass)
search_btn.grid(row=1, column=2 )


generate_pass_btn = Button(text="Generate Password ", width=29, bg=BG_COLOR, highlightthickness=0, font=(FONT_NAME), command=pass_generate)
generate_pass_btn.grid(row=4, column=1, columnspan=2, pady=5)

add_btn = Button(text="Add", width=29, bg=BG_COLOR, highlightthickness=0, font=(FONT_NAME), command=save_data)
add_btn.grid(row=5, column=1, columnspan=2)

window.mainloop()