from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry

root = Tk()

# Make root to span full width and always fill up extra space
root.geometry("800x900")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Window title
root.title("Personal Finance Tracker")
canvas = Canvas(root)
canvas.grid(row=0, column=0, sticky="nsew")
scrollbar = Scrollbar(root)
scrollbar.grid(row=0, column=1, sticky="ns")
canvas.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=canvas.yview)

transactions = []
category_options = ["Bills", "Salary", "Feeding", "Miscellaneous"]
category_filter_options = ["All", "Bills", "Salary", "Feeding", "Miscellaneous"]
selected_index = None
err_msg = ""
total_income = 0
total_expense = 0
remaining_balance = 0
color = "red"
##Error message
err_msg_display = None
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "TCombobox",
    foreground="black",  # Text color
    background="white",  # Background color
    fieldbackground="lightgrey",  # Input field color
    font=("Arial", 12),  # Font type and size
    padding=5,
)

def get_total_vals(type, amount):
    global total_income, total_expense, remaining_balance, transactions
    if len(transactions) != 0:
        #for transaction in transactions:
        if type == "Income":
            total_income += int(amount)
        elif type == "Expense":
            total_expense += int(amount)
        remaining_balance = total_income - total_expense
# Function to get all input values
def get_value():
    global selected_index, err_msg, err_msg_display, color
    category = selected_option.get()
    amount = amount_entry.get()
    date = date_entry.get()
    trans_type = "Income" if v.get() == 1 else "Expense"

    if err_msg_display:
        err_msg_display.destroy()
    if amount == "":
        err_msg = "No field should be left empty"
    elif not amount.isdigit():
        err_msg = "Please input a valid amount, non-digit values are not allowed."
    else:
        err_msg = ""
    if err_msg:
        err_msg_display = Label(form_container, text=err_msg)
        err_msg_display.grid(row=2, column=0, columnspan=2)
        return
    if selected_index is not None:
            # Update the current selected transaction when user edits transaction
            transactions[selected_index] = {
                "category": category,
                "amount": amount,
                "date": date,
                "type": trans_type,
            }
            selected_index = None
            filter_dropdown.current(0)
    else:
            # Create a new transaction and it to the existing transactions when user is creating a new transaction and not editing.
        transaction = {
                "category": category,
                "amount": amount,
                "date": date,
                "type": trans_type,
            }
        transactions.append(transaction)
    create_element(transactions)
    get_total_vals(trans_type, amount)
    income.configure(text="Total Income:" + str(total_income))
    expense.configure(text="Total Expense:" + str(total_expense))
    total.configure(text="Remaining Balance:" + str(remaining_balance))
    if total_income > total_expense:
        color = "green"
    else:
        color = "red"
    total.configure(fg=color)
    # Reset entry fields
    selected_option.set(category_options[0])
    amount_entry.delete(0, END)
    date_entry.delete(0, END)


# Function to create transactions
def create_element(trans):
    for widget in inner_container.winfo_children():
        widget.destroy()
    for index, transaction in enumerate(trans):
        frame = Frame(inner_container, width=700, height=40, pady=5)
        frame.grid_propagate(False)
        frame.grid(row=index + 1, column=0, pady=10)
        for i in range(6):
            frame.columnconfigure(i, weight=1)
        label = Label(frame, text=transaction["category"], width=20)
        label.grid(row=0, column=0)
        label.grid_propagate(False)
        label = Label(frame, text=transaction["amount"], width=20)
        label.grid(row=0, column=1)
        label.grid_propagate(False)
        label = Label(frame, text=transaction["date"], width=20)
        label.grid(row=0, column=2)
        label.grid_propagate(False)
        label = Label(frame, text=transaction["type"], width=20)
        label.grid(row=0, column=3)
        label.grid_propagate(False)
        btn = Button(
            frame,
            text="Edit",
            command=lambda i=index: edit_transaction(i),
            border=0,
            pady=5,
            padx=5,
            bg="#3498DB",
            fg="#FFFFFF",
            font=(..., 10, "bold"),
            cursor="hand2",
        )
        btn.grid(row=0, column=4)
        btn = Button(
            frame,
            text="Delete",
            command=lambda i=index: delete_element(i),
            border=0,
            pady=5,
            padx=5,
            bg="#3498DB",
            fg="#FFFFFF",
            font=(..., 10, "bold"),
            cursor="hand2",
        )
        btn.grid(row=0, column=5)

# Function to delete transactions
def delete_element(index):
    global transactions, total_expense, total_income, remaining_balance
    if transactions[index]["type"] == "Income":
        total_income -= int(transactions[index]["amount"])
    else:
        total_expense -= int(transactions[index]["amount"])
    remaining_balance = total_income - total_expense
    transactions.pop(index)
    create_element(transactions)
    income.configure(text="Total Income:" + str(total_income))
    expense.configure(text="Total Expense:" + str(total_expense))
    total.configure(text="Remaining Balance:" + str(remaining_balance))

# Function to edit transactions
def edit_transaction(index):
    global selected_index, total_expense, total_income
    global transactions
    selected_index = index
    amount_entry.delete(0, END)
    category_entry.set(transactions[index]["category"])
    amount_entry.insert(0, transactions[index]["amount"])
    date_entry.set_date(transactions[index]["date"])
    if transactions[index]["type"] == "Income":
        total_income -= int(transactions[index]["amount"])
    else:
        total_expense -= int(transactions[index]["amount"])
    income.configure(text="Total Income:" + str(total_income))
    expense.configure(text="Total Expense:" + str(total_expense))
    total.configure(text="Remaining Balance:" + str(remaining_balance))
    


# Function to filter transactions based on category
def filter_transactions(category):
    global transactions
    filtered_transactions = [
        transaction
        for transaction in transactions
        if transaction["category"] == category
    ]
    return filtered_transactions


def filter_handler(*args):
    global transactions
    if selected_filter_option.get() == "All":
        create_element(transactions)
    else:
        filtered_transactions = filter_transactions(selected_filter_option.get())
        create_element(filtered_transactions)


# Create another container inside the root container to contain all of my content
body_container = Frame(canvas, bg="#f7f7f7")
canvas.create_window((0,0), window=body_container, anchor="nw")
transactions_container = Frame(body_container, width=700)
transactions_container.grid(row=2, column=0, columnspan=2, sticky="ns")
balance_container =Frame(body_container, width=600, bg="lightgrey", pady=20, padx=20)
balance_container.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=20, padx=20)
selected_filter_option = StringVar()
frame = Frame(transactions_container, width=700, height=40, bg="lightgrey", pady=5)
frame.grid_propagate(False)
frame.grid(row=1, column=0, pady=10)
for i in range(6):
    frame.columnconfigure(i, weight=1)
Label(frame, text="Category", bg="#2ECC71", width=20).grid(row=0, column=0)
Label(frame, text="Amount", bg="#2ECC71", width=20).grid(row=0, column=1)
Label(frame, text="Date", bg="#2ECC71", width=20).grid(row=0, column=2)
Label(frame, text="Type", bg="#2ECC71", width=20).grid(row=0, column=3)
filter_dropdown = ttk.Combobox(
    frame,
    textvariable=selected_filter_option,
    values=category_filter_options,
    state="readonly",
    width=8,
)
filter_dropdown.grid(row=0, column=4)
filter_dropdown.current(0)
filter_dropdown.bind("<<ComboboxSelected>>", filter_handler)
inner_container = Frame(transactions_container, bg="lightgrey")
inner_container.grid(row=2, column=0, columnspan=2)

# Add header text using the label widget
header = Label(
    body_container,
    text="Personal Finance Tracker",
    bg="#f7f7f7",
    fg="#3498DB",
    font=(
        "Times",
        16,
        "bold",
        "italic",
    ),
)
header.grid(row=0, column=0, sticky="nsew")

# Add a new container for my form
form_container = Frame(body_container, bg="#2ECC71", width=450, padx=20, pady=10)

# Set width of my form container and make it centered
form_container.grid(row=1, column=0, sticky="", padx=50, pady=20)
body_container.grid_columnconfigure(0, weight=1)


# Add labels and entry widgets to recieve user input
# category input
Label(form_container, text="Category").grid(row=0, pady=10, sticky="w")
# Category input
# Set user selected option
selected_option = StringVar()
# create the actual dropdown menu
category_entry = ttk.Combobox(
    form_container,
    textvariable=selected_option,
    values=category_options,
    style="TCombobox",
    state="readonly",
    width=41,
)
category_entry.current(0)
category_entry.grid(row=0, column=1, ipady=3, padx=10)

# Amount input
Label(form_container, text="Amount").grid(row=1, pady=10, sticky="w")
amount_entry = Entry(form_container, width=45)
amount_entry.grid(row=1, column=1, ipady=7, padx=10)


# date input
Label(form_container, text="Date").grid(row=3, pady=10, sticky="w")
date_entry = DateEntry(
    form_container,
    width=41,
    background="darkblue",
    foreground="white",
    borderwidth=2,
    date_pattern="dd-mm-yyyy",
    state="readonly",
)
date_entry.grid(row=3, column=1, ipady=3, padx=10)

# income type radio button
container = Frame(form_container, bg="#2ECC71")
container.grid(row=4, column=0, columnspan=2, pady=10, sticky="nsew")
Label(container, text="Type").grid(row=0, column=0, pady=10)
v = IntVar()
radiobtn = Radiobutton(container, text="Income", variable=v, value=1, width=15, bg="#2ECC71")
radiobtn.grid(row=0, column=1, padx=20, sticky="e")
radiobtn = Radiobutton(container, text="Expense", variable=v, value=2, width=15, bg="#2ECC71")
radiobtn.grid(row=0, column=2, padx=20)
Button(
    form_container,
    text="Add Transaction",
    command=get_value,
    border=0,
    pady=5,
    padx=5,
    bg="#3498DB",
    fg="#FFFFFF",
    font=(..., 10, "bold"),
    cursor="hand2",
).grid(row=5, column=1, sticky="e")
#Display balances
income = Label(balance_container, text= "Total Income: "  + str(total_income), pady=10, font=(...,10, "bold"), fg="green")
income.grid(row=0,column=0, sticky="we", pady=10,padx=10)
expense = Label(balance_container, text= "Total Expense: " + str(total_expense), pady=10, font=(...,10, "bold"), fg="red")
expense.grid(row=0,column=1, sticky="we", pady=10,padx=10)
total = Label(balance_container, text= "Total Balance: " + str(remaining_balance), pady=10, font=(...,10, "bold"), fg= "red")
total.grid(row=0,column=2, sticky="we", pady=10, padx=10)
canvas.config(scrollregion=canvas.bbox("all"))
root.mainloop()
