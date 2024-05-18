import tkinter
from tkinter import Tk, Label, Button, Entry, ttk, messagebox, Toplevel
from PIL import Image, ImageTk
from backend.core.date_validator import Validator
from backend.core.csv_date_io import IOHandler
from backend.core.date_and_time import DateHandler
from datetime import datetime, timedelta
from tkcalendar import DateEntry
from tktimepicker import SpinTimePickerModern, constants

window = Tk()
window.title("Working Hours Tracking")
window.geometry("800x600")
window.config(bg="sky blue")

clock_image = Image.open("C:\\Users\\finke\\PycharmProjects\\WorkingHoursTracker\\frontend\\resources\\clock.png")
width, height = clock_image.size
window_width = 800  # Adjust these values as needed
window_height = 600
aspect_ratio = width / height
new_height = window_height
new_width = int(aspect_ratio * new_height)
image = clock_image.resize((new_width, new_height))

photo_image = ImageTk.PhotoImage(image)

csv_rows = IOHandler.read_lines_from_csv(IOHandler.FULL_PATH)
total = timedelta()


# ---------------------------- METHODS ------------------------------- #
def log_dates():
    global total
    start_date = start_time_entry.get()
    end_date = end_time_entry.get()

    if Validator.validate_input(start_date, end_date):
        start_date_obj = DateHandler.create_date(start_date)
        end_date_obj = DateHandler.create_date(end_date)
        hours_diff = DateHandler.subtract_time(start_date_obj, end_date_obj)
        zero_diff = timedelta()
        if hours_diff > zero_diff:
            IOHandler.save_to_csv(IOHandler.FULL_PATH, start_date, end_date, hours_diff)
            table.insert('', tkinter.END, values=[start_date, end_date, hours_diff])
            total += hours_diff
            total_time_result_label.config(text=total)
            confirmation_msg.show()


# ---------------------------- LABELS ------------------------------- #
background_label = Label(image=photo_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

total_time_label = Label(text="Total Time:", highlightbackground="LightCyan2", font=("Helvetica", 14, "bold"),
                         highlightthickness=2)
total_time_label.grid(row=3, column=0, columnspan=1, sticky=tkinter.NSEW)


def calculate_total():
    global csv_rows
    global total
    for item in csv_rows:
        duration = DateHandler.construct_timedelta_from_string(item[-1])
        try:
            total += duration
        except ValueError as e:
            print("Error: Can't constructing timedelta object\n", e)
    return total


def updateTime(selected_time, selected_date: datetime, widget, time_entry):
    time_entry.delete(0, tkinter.END)
    time_entry.insert(0, f"{selected_date.day}/{selected_date.month}/{selected_date.year} "
                         f"{selected_time[0]}:{selected_time[1]}")
    widget.destroy()


def get_time(time_entry):
    top = Toplevel(window)
    ttk.Label(top, text='Choose date').pack(padx=10, pady=10)

    cal = DateEntry(top, width=12, background='darkblue',
                    foreground='white', borderwidth=2, selectmode='day', date_pattern='DD/MM/YYYY')
    cal.pack(padx=10, pady=10)

    time_picker = SpinTimePickerModern(top)
    time_picker.addAll(constants.HOURS24)  # adds hours clock, minutes and period
    time_picker.configureAll(bg="#404040", height=1, fg="#ffffff", font=("Times", 16), hoverbg="#404040",
                             hovercolor="#d73333", clickedbg="#2e2d2d", clickedcolor="#d73333")
    time_picker.configure_separator(bg="#404040", fg="#ffffff")
    time_picker.addHours24()

    time_picker.pack(expand=True, fill="both")

    # chosen_date = cal.selection_get()
    ok_btn = Button(top, text="ok", command=lambda: updateTime(time_picker.time(), cal.get_date(), top, time_entry))
    ok_btn.pack()


total_time_result_label = Label(text=str(calculate_total()),
                                highlightbackground="LightCyan2",
                                font=("Helvetica", 14, "bold"),
                                highlightthickness=2)
total_time_result_label.grid(row=3, column=1, columnspan=2, sticky=tkinter.NSEW)

# ---------------------------- BUTTONS ------------------------------- #
log_btn = Button(text="Log work", command=log_dates)
log_btn.grid(row=0, column=2, sticky="ewns", rowspan=2)

start_time_button = Button(text="Pick Start time", command=lambda: get_time(start_time_entry))
start_time_button.grid(row=0, column=0, sticky="ew")

end_time_button = Button(text="Pick End time", command=lambda: get_time(end_time_entry))
end_time_button.grid(row=1, column=0, sticky="ew")

# ---------------------------- ENTRIES ------------------------------- #
start_time_entry = Entry(width=28)
start_time_entry.focus()
start_time_entry.grid(row=0, column=1, sticky="ew")

end_time_entry = Entry(width=28)
end_time_entry.grid(row=1, column=1, columnspan=1, sticky="ew")

# ---------------------------- TABLE ------------------------------- #
style = ttk.Style(window)
style.theme_use("clam")
style.configure("Treeview", background="snow",
                fieldbackground="bisque2", foreground="blue4")

table = ttk.Treeview(window, columns=("start", "end", "duration"), show="headings")
table.heading("start", text="Start Time")
table.heading("end", text="End Time")
table.heading("duration", text="Duration")
table.grid(row=2, column=0, columnspan=3, sticky="ewns")

for row in csv_rows:
    table.insert('', tkinter.END, values=row)

# ---------------------------- MESSAGE BOX --------------------------- #
confirmation_msg = messagebox.Message(window, message="Work Saved Successfully")

# -------------------------------------------------------------------- #
if __name__ == "__main__":
    window.mainloop()
