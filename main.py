from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]

    shuffle(password_list)

    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_input.get().lower()
    email = username_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(message=f"These are the details entered: \n"
                                               f"Email: {email}\n Password: {password}\nIs it ok to save?")
        if is_ok:
            try:
                json_file = open("data.json", "r")
            except FileNotFoundError:
                json_file = open("data.json", "w")
                json.dump(new_data, json_file, indent=4)
            else:
                data = json.load(json_file)
                data.update(new_data)
                file = open("data.json", "w")
                json.dump(data, file, indent=4)
            finally:
                website_input.delete(0, END)
                password_input.delete(0, END)


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search_password():
    website = website_input.get().lower()
    if len(website) == 0:
        messagebox.showwarning(message="Please input the website.")
    else:
        try:
            json_file = open("data.json", "r")
        except FileNotFoundError:
            messagebox.showwarning(message="No Data File Found!")
        else:
            data = json.load(json_file)
            if website in data:
                email = data[website]["email"]
                password = data[website]["password"]
                messagebox.showinfo(title=website, message=f"Email: {email}\n Password: {password}")
            else:
                messagebox.showwarning(message="No details for the website exists!")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=60, pady=50)
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
username_label = Label(text="Email/Username:")
username_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries:
website_input = Entry(width=20)
website_input.focus()
website_input.grid(row=1, column=1)
username_input = Entry(width=35)
username_input.insert(0, "liguanna2017@outlook.com")
username_input.grid(row=2, column=1, columnspan=2)
password_input = Entry(width=20)
password_input.grid(row=3, column=1)

# Buttons:
search_button = Button(text="Search", width=11, command=search_password)
search_button.grid(row=1, column=2)
password_button = Button(text="Generate Password", width=11, command=generate_password)
password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=33, command=save)
add_button.grid(row=4, column=1, columnspan=2)
window.mainloop()
