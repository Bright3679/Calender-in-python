# import tkinter as tk
# from tkinter import ttk
# import calendar
# from datetime import datetime
# import ctypes

# try:
#     ctypes.windll.shcore.SetProcessDpiAwareness(1)
# except:
#     ctypes.windll.user32.SetProcessDPIAware()

# def update_calendar(year, month):
#     cal = calendar.monthcalendar(year, month)
    
#     for widget in cal_frame.winfo_children():
#         widget.destroy()

#     days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

#     for col, day_name in enumerate(days_of_week):
#         ttk.Label(cal_frame, text=day_name, padding=5, background='lightgrey').grid(row=0, column=col, sticky='nsew')

#     today = datetime.now()
#     current_month = today.month
#     current_year = today.year

#     for row, week in enumerate(cal, start=1):
#         for col, day in enumerate(week):
#             if day == 0:
#                 display_day = ''
#                 day_button = None 
#             else:
#                 display_day = str(day)
#                 if year == current_year and month == current_month and day == today.day:
#                     day_button = ttk.Button(
#                         cal_frame,
#                         text=display_day,
#                         padding=5,
#                         style='Today.TButton',
#                         command=lambda y=year, m=month, d=day: on_day_click(y, m, d)
#                     )
#                 else:
#                     day_button = ttk.Button(
#                         cal_frame,
#                         text=display_day,
#                         padding=5,
#                         command=lambda y=year, m=month, d=day: on_day_click(y, m, d)
#                     )

#             if day_button is not None:
#                 day_button.grid(row=row, column=col, sticky='nsew')

# def on_day_click(year, month, day):
#     print(f"You clicked on {day}/{month}/{year}")

# def month_changed(event):
#     selected_month = month_combo.get()
#     month_number = list(calendar.month_name).index(selected_month)
#     update_calendar(int(year_combo.get()), month_number)

# def close_window():
#     root.destroy()

# root = tk.Tk()
# root.geometry("900x500")
# root.resizable(True, True)
# root.title("Calendar GUI")

# style = ttk.Style()
# style.theme_use('clam')
# style.configure('Today.TButton', background='orange')

# cal_frame = ttk.Frame(root, padding="10")
# cal_frame.grid(row=1, column=0, columnspan=2, sticky='nsew')

# root.grid_columnconfigure(0, weight=1)
# root.grid_rowconfigure(1, weight=1)

# current_year = datetime.now().year
# current_month = datetime.now().month

# month_combo = ttk.Combobox(root, values=list(calendar.month_name)[1:], state='readonly')
# month_combo.set(calendar.month_name[current_month])
# month_combo.grid(row=0, column=0, padx=10, pady=10, sticky='w')
# month_combo.bind("<<ComboboxSelected>>", month_changed)

# year_combo = ttk.Combobox(root, values=[str(year) for year in range(current_year - 10, current_year + 11)], state='readonly')
# year_combo.set(str(current_year))
# year_combo.grid(row=0, column=1, padx=10, pady=10, sticky='e')
# year_combo.bind("<<ComboboxSelected>>", month_changed)

# update_calendar(current_year, current_month)

# close_button = ttk.Button(root, text="Close", command=close_window)
# close_button.grid(row=2, column=1, padx=10, pady=10, sticky='se')

# root.mainloop()
#############################################
#with features 

import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime
import csv

import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    ctypes.windll.user32.SetProcessDPIAware()

current_year = datetime.now().year
current_month = datetime.now().month
events = {} 


def load_events():
    global events
    try:
        with open('events.csv', 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                year, month, day = map(int, row[0].split('-'))
                events[(year, month, day)] = row[1]
    except FileNotFoundError:
        events = {}


def save_events():
    with open('events.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for key, value in events.items():
            writer.writerow([f"{key[0]}-{key[1]}-{key[2]}", value])


def update_calendar(year, month):
    cal = calendar.monthcalendar(year, month)

    for widget in cal_frame.winfo_children():
        widget.destroy()

    days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    for col, day_name in enumerate(days_of_week):
        ttk.Label(cal_frame, text=day_name, padding=5, background='lightgrey').grid(row=0, column=col, sticky='nsew')

    for row, week in enumerate(cal, start=1):
        for col, day in enumerate(week):
            if day != 0:
                date_tuple = (year, month, day)
                display_day = str(day)
                if date_tuple in events:
                    day_button = ttk.Button(
                        cal_frame,
                        text=display_day,
                        padding=5,
                        style='Event.TButton',
                        command=lambda y=year, m=month, d=day: on_day_click(y, m, d)
                    )
                else:
                    day_button = ttk.Button(
                        cal_frame,
                        text=display_day,
                        padding=5,
                        command=lambda y=year, m=month, d=day: on_day_click(y, m, d)
                    )
                day_button.grid(row=row, column=col, sticky='nsew')


def on_day_click(year, month, day):
    date_tuple = (year, month, day)
    if date_tuple in events:
        event_text = events[date_tuple]
    else:
        event_text = ""
    result = EventDialog(root, event_text)
    if result is not None:
        events[date_tuple] = result
        save_events()
        update_calendar(year, month)


def month_changed(event):
    selected_month = month_combo.get()
    month_number = list(calendar.month_name).index(selected_month)
    update_calendar(int(year_combo.get()), month_number)


def navigate(delta):
    global current_year, current_month
    new_month = current_month + delta
    if new_month < 1:
        current_year -= 1
        current_month = 12
    elif new_month > 12:
        current_year += 1
        current_month = 1
    else:
        current_month = new_month
    month_combo.set(calendar.month_name[current_month])
    year_combo.set(str(current_year))
    update_calendar(current_year, current_month)


def close_window():
    save_events()  
    root.destroy()


class EventDialog(tk.Toplevel):
    def __init__(self, parent, event_text=""):
        super().__init__(parent)
        self.title("Event")
        self.geometry("300x150")   

        self.event_text = tk.StringVar()
        self.event_text.set(event_text)

        ttk.Label(self, text="Event Description:").pack(pady=10)
        self.event_entry = ttk.Entry(self, textvariable=self.event_text, width=30)
        self.event_entry.pack(pady=10)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Save", command=self.save_event).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).grid(row=0, column=1, padx=10)

        self.transient(parent)
        self.grab_set()
        self.wait_window(self)

    def save_event(self):
        self.event_text = self.event_entry.get()
        self.destroy()


root = tk.Tk()
root.geometry("900x500")
root.resizable(True, True)
root.title("Calendar GUI")


style = ttk.Style()
style.configure('Event.TButton', background='yellow')

cal_frame = ttk.Frame(root, padding="10")
cal_frame.grid(row=1, column=0, columnspan=3, sticky='nsew')

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

load_events()
update_calendar(current_year, current_month)

nav_frame = ttk.Frame(root)
nav_frame.grid(row=0, column=1, pady=10)
ttk.Button(nav_frame, text="< Prev Month", command=lambda: navigate(-1)).pack(side=tk.LEFT, padx=10)
ttk.Button(nav_frame, text="Next Month >", command=lambda: navigate(1)).pack(side=tk.LEFT, padx=10)

month_combo = ttk.Combobox(root, values=list(calendar.month_name)[1:], state='readonly')
month_combo.set(calendar.month_name[current_month])
month_combo.grid(row=0, column=0, padx=10, pady=10, sticky='w')
month_combo.bind("<<ComboboxSelected>>", month_changed)

year_combo = ttk.Combobox(root, values=[str(year) for year in range(current_year - 10, current_year + 11)], state='readonly')
year_combo.set(str(current_year))
year_combo.grid(row=0, column=2, padx=10, pady=10, sticky='e')
year_combo.bind("<<ComboboxSelected>>", month_changed)

close_button = ttk.Button(root, text="Close", command=close_window)
close_button.grid(row=2, column=2, padx=10, pady=10, sticky='se')

root.mainloop()
