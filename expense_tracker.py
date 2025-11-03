import tkinter as tk
from tkinter import messagebox, ttk, Toplevel
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv, os
from datetime import datetime

# ------------------ File Setup ------------------
filename = "expenses.csv"
income_file = "income.txt"

if not os.path.exists(filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Category", "Amount"])

def load_income():
    if os.path.exists(income_file):
        with open(income_file, "r") as f:
            try:
                return float(f.read().strip())
            except:
                return 0.0
    return 0.0

def save_income(amount):
    with open(income_file, "w") as f:
        f.write(str(amount))

# ------------------ Modern Theme Colors ------------------
BG_COLOR = "#f8fafc"
CARD_COLOR = "#ffffff"
ACCENT_COLOR = "#3b82f6"
SECONDARY_COLOR = "#6366f1"
SUCCESS_COLOR = "#10b981"
WARNING_COLOR = "#f59e0b"
DANGER_COLOR = "#ef4444"
TEXT_COLOR = "#1e293b"
TEXT_SECONDARY = "#64748b"
BORDER_COLOR = "#e2e8f0"
# ------------------ Functions ------------------
def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        try:
            date_obj = datetime.strptime(date_str, "%Y/%m/%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter date in YYYY-MM-DD format.")
            return None
    return date_obj.strftime("%d-%m-%Y")

def add_expense():
    date = date_entry.get().strip()
    category = category_combobox.get().strip()
    amount = amount_entry.get().strip()

    if not date or not category or not amount:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    formatted_date = format_date(date)
    if formatted_date is None:
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number")
        return

    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([formatted_date, category, amount])

    messagebox.showinfo("Success", f"✅ Expense Added!\nDate: {formatted_date}\nAmount: ₹{amount:.2f}")
    date_entry.delete(0, tk.END)
    category_combobox.set('')
    amount_entry.delete(0, tk.END)
    show_expenses()
    update_dashboard()
def show_expenses():
    for row in tree.get_children():
        tree.delete(row)
    total = 0.0
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            tree.insert("", tk.END, values=row)
            try:
                total += float(row[2])
            except ValueError:
                pass
    total_expenses_label.config(text=f"₹{total:,.2f}")

def delete_selected_record():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a record to delete!")
        return

    record = tree.item(selected[0])['values']
    date, category, amount = record

    confirm = messagebox.askyesno("Confirm Delete", f"Delete record:\n{date}, {category}, ₹{amount}?")
    if confirm:
        with open(filename, 'r') as f:
            rows = list(csv.reader(f))
        header, data = rows[0], rows[1:]
        data = [r for r in data if not (r[0] == str(date) and r[1] == str(category) and r[2] == str(amount))]

        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)

        show_expenses()
        update_dashboard()
        messagebox.showinfo("Deleted", "Record deleted successfully!")

def clear_all_records():
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete all records?")
    if confirm:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Category", "Amount"])
        show_expenses()
        update_dashboard()
        messagebox.showinfo("Cleared", "All records cleared successfully!")

def set_income_window():
    win = Toplevel(root)
    win.title("Set Monthly Income")
    win.geometry("400x300")
    win.configure(bg=BG_COLOR)
    win.resizable(False, False)
    # Center the window
    win.transient(root)
    win.grab_set()
    
    # Header
    header_frame = tk.Frame(win, bg=ACCENT_COLOR, height=80)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text="Set Monthly Income", font=("Segoe UI", 18, "bold"), 
             bg=ACCENT_COLOR, fg="white").pack(expand=True)
    
    # Content
    content_frame = tk.Frame(win, bg=BG_COLOR)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
    
    tk.Label(content_frame, text="Enter your monthly income:", bg=BG_COLOR, fg=TEXT_COLOR,
             font=("Segoe UI", 12)).pack(pady=(0, 10))
    
    income_var = tk.StringVar(value=f"{load_income():.2f}")
    
    amount_frame = tk.Frame(content_frame, bg=BG_COLOR)
    amount_frame.pack(pady=20)
    
    tk.Label(amount_frame, text="₹", font=("Segoe UI", 16, "bold"), 
             bg=BG_COLOR, fg=TEXT_COLOR).pack(side=tk.LEFT, padx=(0, 5))
    
    income_entry = tk.Entry(amount_frame, textvariable=income_var, font=("Segoe UI", 16), 
                           justify='center', relief="solid", bd=1, bg="white",
                           width=15)
    income_entry.pack(side=tk.LEFT)
    income_entry.select_range(0, tk.END)
    income_entry.focus()
    
    def save_income_and_close():
        try:
            amt = float(income_entry.get())
            save_income(amt)
            messagebox.showinfo("Success", f"Income set to ₹{amt:,.2f}")
            update_dashboard()
            win.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
    btn_frame = tk.Frame(content_frame, bg=BG_COLOR)
    btn_frame.pack(pady=30)
    
    tk.Button(btn_frame, text="💾 Save Income", command=save_income_and_close,
              bg=SUCCESS_COLOR, fg="white", font=("Segoe UI", 12, "bold"),
              relief="flat", width=15, pady=12, cursor="hand2").pack(side=tk.LEFT, padx=10)
    
    tk.Button(btn_frame, text="❌ Cancel", command=win.destroy,
              bg=TEXT_SECONDARY, fg="white", font=("Segoe UI", 12),
              relief="flat", width=12, pady=12, cursor="hand2").pack(side=tk.LEFT, padx=10)

    # Enter key binding
    win.bind('<Return>', lambda e: save_income_and_close())

def show_spent_percentage():
    total_exp = 0.0
    with open(filename, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            try:
                total_exp += float(row[2])
            except:
                pass

    income = load_income()
    if income <= 0:
        messagebox.showwarning("No Income", "Please set your income first!")
        return

    percent = (total_exp / income) * 100
    messagebox.showinfo("Budget Analysis", 
                       f"💰 Total Expenses: ₹{total_exp:,.2f}\n"
                       f"💵 Monthly Income: ₹{income:,.2f}\n"
                       f"📊 Budget Used: {percent:.1f}%")

def show_graph():
    data = np.genfromtxt(filename, delimiter=",", dtype=str, skip_header=1)
    if data.size == 0:
        messagebox.showwarning("No Data", "No expenses to visualize!")
        return

    categories = data[:, 1]
    amounts = data[:, 2].astype(float)
    unique_cats = np.unique(categories)
    sums = [np.sum(amounts[categories == cat]) for cat in unique_cats]

    graph_win = Toplevel(root)
    graph_win.title("📊 Expense Analytics Dashboard")
    graph_win.geometry("1000x700")
    graph_win.configure(bg=BG_COLOR)

    # Header
    header_frame = tk.Frame(graph_win, bg=ACCENT_COLOR, height=60)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text="Expense Analytics", font=("Segoe UI", 20, "bold"), 
             bg=ACCENT_COLOR, fg="white").pack(expand=True)

    # Create modern matplotlib style
    plt.style.use('default')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor(BG_COLOR)
    
    # Color palette
    colors = [ACCENT_COLOR, SECONDARY_COLOR, SUCCESS_COLOR, WARNING_COLOR, DANGER_COLOR, '#8b5cf6', '#06b6d4']
    
    # Bar Chart
    bars = ax1.bar(unique_cats, sums, color=colors[:len(unique_cats)], alpha=0.8, edgecolor='white', linewidth=1)
    ax1.set_title("Expenses by Category", fontsize=14, fontweight='bold', pad=20, color=TEXT_COLOR)
    ax1.set_xlabel("Category", fontweight='bold', color=TEXT_SECONDARY)
    ax1.set_ylabel("Amount (₹)", fontweight='bold', color=TEXT_SECONDARY)
    ax1.tick_params(axis='x', rotation=45, colors=TEXT_SECONDARY)
    ax1.tick_params(axis='y', colors=TEXT_SECONDARY)
    ax1.grid(True, alpha=0.3)
    ax1.set_facecolor('#f8fafc')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + max(sums)*0.01,
                f'₹{height:,.0f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Pie Chart
    wedges, texts, autotexts = ax2.pie(sums, labels=unique_cats, autopct='%1.1f%%', 
                                      startangle=90, colors=colors[:len(unique_cats)],
                                      textprops={'fontsize': 10, 'color': TEXT_COLOR})
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax2.set_title("Expense Distribution", fontsize=14, fontweight='bold', pad=20, color=TEXT_COLOR)

    plt.tight_layout(pad=3.0)

    canvas = FigureCanvasTkAgg(fig, master=graph_win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Close button
    tk.Button(graph_win, text="⬅ Back to Dashboard", command=graph_win.destroy,
              bg=ACCENT_COLOR, fg="white", font=("Segoe UI", 12, "bold"),
              relief="flat", width=20, pady=10, cursor="hand2").pack(pady=20)

def update_dashboard():
    # Calculate total expenses
    total_exp = 0.0
    category_count = {}
    
    with open(filename, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            try:
                amount = float(row[2])
                total_exp += amount
                category = row[1]
                category_count[category] = category_count.get(category, 0) + 1
            except:
                pass
    
    # Update total expenses
    total_expenses_label.config(text=f"₹{total_exp:,.2f}")
    
    # Update income
    income = load_income()
    income_label.config(text=f"₹{income:,.2f}")
    
    # Update transaction count
    transaction_count = len(tree.get_children())
    transactions_label.config(text=str(transaction_count))
    
    # Update budget percentage
    if income > 0:
        percentage = (total_exp / income) * 100
        percentage_label.config(text=f"{percentage:.1f}%")
        
        # Update progress bar
        progress_value = min(percentage, 100)
        progress_bar['value'] = progress_value
        
        # Change color based on percentage
        if percentage <= 60:
            progress_bar.configure(style="Green.Horizontal.TProgressbar")
        elif percentage <= 85:
            progress_bar.configure(style="Yellow.Horizontal.TProgressbar")
        else:
            progress_bar.configure(style="Red.Horizontal.TProgressbar")
    else:
        percentage_label.config(text="Set Income")
        progress_bar['value'] = 0

def on_income_label_click(event):
    """Allow clicking on income label to set income"""
    set_income_window()

# ------------------ Professional GUI ------------------
root = tk.Tk()
root.title("ExpenseTracker Pro • Personal Finance Manager")
root.geometry("1300x850")
root.configure(bg=BG_COLOR)
root.resizable(True, True)

# Configure ttk styles
style = ttk.Style()
style.theme_use('clam')
style.configure("Green.Horizontal.TProgressbar", troughcolor=BORDER_COLOR, background=SUCCESS_COLOR)
style.configure("Yellow.Horizontal.TProgressbar", troughcolor=BORDER_COLOR, background=WARNING_COLOR)
style.configure("Red.Horizontal.TProgressbar", troughcolor=BORDER_COLOR, background=DANGER_COLOR)

# ---- Header ----
header_frame = tk.Frame(root, bg=ACCENT_COLOR, height=80)
header_frame.pack(fill=tk.X)
header_frame.pack_propagate(False)

# Logo and title
title_frame = tk.Frame(header_frame, bg=ACCENT_COLOR)
title_frame.pack(expand=True)

tk.Label(title_frame, text="💰", font=("Segoe UI", 24), bg=ACCENT_COLOR, fg="white").pack(side=tk.LEFT, padx=(0, 10))
tk.Label(title_frame, text="Personal Expense Tracker", font=("Segoe UI", 24, "bold"), 
         bg=ACCENT_COLOR, fg="white").pack(side=tk.LEFT)

# ---- Dashboard Stats ----
stats_frame = tk.Frame(root, bg=BG_COLOR)
stats_frame.pack(fill=tk.X, padx=20, pady=20)

def create_stat_card(parent, title, value, icon, color, clickable=False):
    card = tk.Frame(parent, bg=CARD_COLOR, relief="flat", bd=1, highlightbackground=BORDER_COLOR, 
                   highlightthickness=1, width=220, height=100)
    card.pack_propagate(False)
    
    # Icon and title
    icon_frame = tk.Frame(card, bg=CARD_COLOR)
    icon_frame.pack(fill=tk.X, padx=15, pady=(15, 5))
    
    tk.Label(icon_frame, text=icon, font=("Segoe UI", 14), bg=CARD_COLOR, fg=color).pack(side=tk.LEFT)
    tk.Label(icon_frame, text=title, font=("Segoe UI", 10), bg=CARD_COLOR, fg=TEXT_SECONDARY).pack(side=tk.LEFT, padx=(5, 0))
    
    # Value
    value_label = tk.Label(card, text=value, font=("Segoe UI", 18, "bold"), 
                          bg=CARD_COLOR, fg=TEXT_COLOR, cursor="hand2" if clickable else "arrow")
    value_label.pack(anchor="w", padx=15, pady=(0, 15))
    
    return card, value_label

# Create stat cards with proper spacing
total_card, total_expenses_label = create_stat_card(stats_frame, "TOTAL EXPENSES", "₹0.00", "💸", DANGER_COLOR)
total_card.pack(side=tk.LEFT, padx=(0, 15))

income_card, income_label = create_stat_card(stats_frame, "MONTHLY INCOME", "₹0.00", "💰", SUCCESS_COLOR, clickable=True)
income_card.pack(side=tk.LEFT, padx=(0, 15))

transactions_card, transactions_label = create_stat_card(stats_frame, "TRANSACTIONS", "0", "📊", ACCENT_COLOR)
transactions_card.pack(side=tk.LEFT, padx=(0, 15))

percentage_card, percentage_label = create_stat_card(stats_frame, "BUDGET USED", "0%", "📈", WARNING_COLOR)
percentage_card.pack(side=tk.LEFT, padx=(0, 15))

# Make income label clickable
income_label.bind("<Button-1>", on_income_label_click)

# Progress bar frame
progress_frame = tk.Frame(stats_frame, bg=BG_COLOR)
progress_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0))

tk.Label(progress_frame, text="BUDGET PROGRESS", font=("Segoe UI", 10), 
         bg=BG_COLOR, fg=TEXT_SECONDARY).pack(anchor="w")

progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=400, 
                              mode="determinate", style="Green.Horizontal.TProgressbar")
progress_bar.pack(fill=tk.X, pady=(5, 0))

# ---- Main Content ----
main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

# Left side - Input form and quick actions
left_frame = tk.Frame(main_frame, bg=BG_COLOR, width=400)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
left_frame.pack_propagate(False)

# Input card
input_card = tk.Frame(left_frame, bg=CARD_COLOR, relief="flat", bd=1, 
                     highlightbackground=BORDER_COLOR, highlightthickness=1)
input_card.pack(fill=tk.X, pady=(0, 15))

# Card header
card_header = tk.Frame(input_card, bg=ACCENT_COLOR, height=40)
card_header.pack(fill=tk.X)
card_header.pack_propagate(False)

tk.Label(card_header, text="➕ ADD NEW EXPENSE", font=("Segoe UI", 12, "bold"), 
         bg=ACCENT_COLOR, fg="white").pack(expand=True)

# Form content
form_frame = tk.Frame(input_card, bg=CARD_COLOR)
form_frame.pack(fill=tk.BOTH, padx=20, pady=15)

common_categories = ["Food & Dining", "Transportation", "Shopping", "Entertainment", 
                    "Bills & Utilities", "Healthcare", "Education", "Travel", "Other"]

# Date field
tk.Label(form_frame, text="Date (YYYY-MM-DD)", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 5))
date_entry = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, 
                     bg="white", width=30)
date_entry.grid(row=1, column=0, sticky="ew", pady=(0, 10))

# Category field
tk.Label(form_frame, text="Category", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky="w", pady=(0, 5))
category_combobox = ttk.Combobox(form_frame, values=common_categories, 
                                font=("Segoe UI", 11), state="normal", width=28)
category_combobox.grid(row=3, column=0, sticky="ew", pady=(0, 10))

# Amount field
tk.Label(form_frame, text="Amount (₹)", bg=CARD_COLOR, fg=TEXT_COLOR,
         font=("Segoe UI", 10, "bold")).grid(row=4, column=0, sticky="w", pady=(0, 5))
amount_entry = tk.Entry(form_frame, font=("Segoe UI", 11), relief="solid", bd=1, 
                       bg="white", width=30)
amount_entry.grid(row=5, column=0, sticky="ew", pady=(0, 15))

# Add expense button
add_btn = tk.Button(form_frame, text="➕ ADD EXPENSE", command=add_expense,
                    bg=ACCENT_COLOR, fg="white", font=("Segoe UI", 11, "bold"),
                    relief="flat", pady=8, cursor="hand2")
add_btn.grid(row=6, column=0, sticky="ew")

# Quick actions card - WITH SET INCOME BUTTON
actions_card = tk.Frame(left_frame, bg=CARD_COLOR, relief="flat", bd=1, 
                       highlightbackground=BORDER_COLOR, highlightthickness=1)
actions_card.pack(fill=tk.BOTH, expand=True)

actions_header = tk.Frame(actions_card, bg=SECONDARY_COLOR, height=35)
actions_header.pack(fill=tk.X)
actions_header.pack_propagate(False)

tk.Label(actions_header, text="⚡ QUICK ACTIONS", font=("Segoe UI", 11, "bold"),
         bg=SECONDARY_COLOR, fg="white").pack(expand=True)

# UPDATED: Added Set Income button back
actions_container = tk.Frame(actions_card, bg=CARD_COLOR)
actions_container.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)

action_buttons = [
    ("📊 Analytics", show_graph, ACCENT_COLOR),
    ("💰 Set Income", set_income_window, SUCCESS_COLOR),
    ("🗑 Delete", delete_selected_record, DANGER_COLOR),
    ("🧹 Clear All", clear_all_records, WARNING_COLOR)
]

# Compact buttons
for i, (text, cmd, color) in enumerate(action_buttons):
    btn = tk.Button(actions_container, text=text, command=cmd, bg=color,
                   fg="white", font=("Segoe UI", 9),
                   relief="flat", width=15, pady=6, cursor="hand2")
    btn.pack(fill=tk.X, pady=3)

# Right side - Expense list
right_frame = tk.Frame(main_frame, bg=BG_COLOR)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# List header
list_header = tk.Frame(right_frame, bg=CARD_COLOR, relief="flat", bd=1,
                      highlightbackground=BORDER_COLOR, highlightthickness=1)
list_header.pack(fill=tk.X)

tk.Label(list_header, text="📋 EXPENSE HISTORY", font=("Segoe UI", 12, "bold"), 
         bg=CARD_COLOR, fg=TEXT_COLOR, pady=12).pack()

# Treeview with modern styling
tree_container = tk.Frame(right_frame, bg=BG_COLOR)
tree_container.pack(fill=tk.BOTH, expand=True, pady=(8, 0))

# Configure treeview style
style.configure("Custom.Treeview", 
                background=CARD_COLOR,
                foreground=TEXT_COLOR,
                fieldbackground=CARD_COLOR,
                borderwidth=0,
                font=("Segoe UI", 10))
style.configure("Custom.Treeview.Heading",
                background=ACCENT_COLOR,
                foreground="white",
                relief="flat",
                font=("Segoe UI", 11, "bold"))
style.map("Custom.Treeview", 
          background=[('selected', '#dbeafe')])

tree = ttk.Treeview(tree_container, columns=("Date", "Category", "Amount"), 
                   show="headings", height=20, style="Custom.Treeview")

tree.heading("Date", text="📅 DATE")
tree.heading("Category", text="🏷 CATEGORY")
tree.heading("Amount", text="💸 AMOUNT")

tree.column("Date", width=120, anchor="center")
tree.column("Category", width=150, anchor="center")
tree.column("Amount", width=120, anchor="center")

# Add scrollbar
scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Initialize the application
show_expenses()
update_dashboard()

# Center the window on screen
root.update_idletasks()
x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
root.geometry(f"+{x}+{y}")

root.mainloop()