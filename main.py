import requests
import json
import datetime as dt
import random
from tkinter import * #type: ignore
from tkinter import messagebox
import webbrowser

#----- SETUP -----

BLACK = "#222831"
WHITE= "#EEEEEE"
BLUE = "#83B4FF"

datetime = dt.datetime.now()
date = datetime.date()

day = date.strftime("%d")
month = date.strftime("%m")
year = date.year

#----- METHODS -----

def save_quote(quote):
    saved_quotes = []
    with open("saved_quotes.json", "r") as file:
        saved_quotes = json.load(file)

    if quote not in saved_quotes:
        saved_quotes.append(quote)
        with open("saved_quotes.json", "w") as file:
            json.dump(saved_quotes, file, indent=4)
            messagebox.showinfo("Info", "Quote saved successfully!")
    else:
        messagebox.showerror("Error", "This quote has already been saved.")
        pass
    
def see_author(author):
    author = author.split(" ")
    author = [tag.lower() for tag in author]
    author = "-".join(author)
    webbrowser.open_new_tab(f"https://zenquotes.io/authors/{author}")

def generate_new_quote():
    global quotes_list
    random_quote = random.choice(quotes_list)
    quote_text.config(text=f'" {random_quote["q"]} "')
    quote_author.config(text=f" - {random_quote["a"]}")
    quote_header.config(text="Another Inspirational Quote")
    author_button.config(command=lambda: see_author(random_quote["a"]))
    save_button.config(command=lambda: save_quote(random_quote))

    back_to_today_button.grid(row=1, column=2)

def back_to_todays_quote():
    quote_text.config(text=f'" {quote_of_the_day[0]["q"]} "')
    quote_author.config(text=f" - {quote_of_the_day[0]["a"]}")
    quote_header.config(text="Quote Of The Day")
    author_button.config(command=lambda: see_author(quote_of_the_day[0]["a"]))
    save_button.config(command=lambda: save_quote(quote_of_the_day[0]))

    back_to_today_button.grid_forget()

#----- API REQUEST -----

#quote_of_the_day
response = requests.get("https://zenquotes.io/api/today")
quote_of_the_day = []

if not response.ok:
    response.raise_for_status()
else:
    quote_of_the_day = response.json()

    #Saving quote to json file
    with open("quote_of_the_day.json", "w") as file:
        json.dump(quote_of_the_day, file, indent=4)

response = requests.get("https://zenquotes.io/api/quotes")
quotes_list = []

if not response.ok:
    response.raise_for_status()
else:
    quotes_list = response.json()

    #Saving all quotes to quotes_list.json
    with open("quotes_list.json", "w") as file:
        json.dump(quotes_list, file, indent=4)

#----- UI -----

window = Tk()
window.title("Quotes")
window.minsize(width=800, height=500)
window.config(padx=50, pady=60, bg=BLACK)

date_header = Label(text=f"{day}/{month}/{year}", font=("Poppins", 18), bg=BLACK, fg=WHITE)
date_header.grid(row=0, column=1)

quote_header = Label(text="Quote Of The Day", font=("Poppins", 22, "bold"), bg=BLACK, fg=WHITE)
quote_header.grid(row=1, column=1)

quote_text = Label(text=f'" {quote_of_the_day[0]["q"]} "', font=("Newsreader", 20), bg=BLACK, fg=WHITE)
quote_text.grid(row=2, column=0, columnspan=3, pady=(50, 5))

quote_author = Label(text=f"- {quote_of_the_day[0]["a"]} ", font=("Poppins", 16), bg=BLACK, fg=WHITE)
quote_author.grid(row=3, column=1, pady=(0, 50))

save_button = Button(text="Save Quote", padx=15, pady=5, width=22 , font=("Arial", 13, "bold"), bg=BLUE, fg=WHITE, command=lambda: save_quote(quote_of_the_day[0]))
save_button.grid(row=4, column=0)

author_button = Button(text="See More From Author", padx=15, pady=5, width=22 , font=("Arial", 13, "bold"), bg=BLUE, fg=WHITE, command=lambda: see_author(quote_of_the_day[0]["a"]) )
author_button.grid(row=4, column=1, pady=10)

generate_quote_button = Button(text="Generate Random Quote", padx=15, pady=5, width=22 , font=("Arial", 13, "bold"), bg=BLUE, fg=WHITE, command=generate_new_quote)
generate_quote_button.grid(row=4, column=2)

back_to_today_button = Button(text="Q.O.T.D.", padx=15, pady=5, width=15 , font=("Arial", 13, "bold"), bg=BLUE, fg=WHITE, command=back_to_todays_quote)



#separator = Label(text="-------------------------------------------------------------", font=("Poppins", 20), bg=BLACK, fg=WHITE)
#separator.grid(row=6, column=0, columnspan=3, pady=20)

window.mainloop()