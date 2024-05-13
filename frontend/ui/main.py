import datetime
import tkinter
from tkinter import Tk, Canvas, PhotoImage, Label, Button, Entry, ttk, messagebox
from PIL import Image, ImageTk
from backend.core.date_validator import Validator
from backend.core.csv_date_io import IOHandler
from backend.core.date_and_time import DateHandler
from datetime import timedelta

window = Tk()
window.title("Working Hours Tracking")
window.geometry("800x600")
window.config(height=1000, width=800, bg="sky blue")

clock_image = Image.open("C:\\Users\\finke\\PycharmProjects\\WorkingHoursTracker\\frontend\\resources\\clock.png")
width, height = clock_image.size
window_width = 800  # Adjust these values as needed
window_height = 600
aspect_ratio = width / height
new_height = window_height
new_width = int(aspect_ratio * new_height)
image = clock_image.resize((new_width, new_height))

photo_image = ImageTk.PhotoImage(image)

rows = IOHandler.read_lines_from_csv(IOHandler.FULL_PATH)
total = datetime.timedelta()


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

start_time_label = Label(text="Start Time:")
start_time_label.grid(row=0, column=0, sticky="ewns")

end_time_label = Label(text="End Time:")
end_time_label.grid(row=1, column=0, sticky="ewns")

total_time_label = Label(text="Total Time:", highlightbackground="LightCyan2", font=("Helvetica", 14, "bold"),
                         highlightthickness=2)
total_time_label.grid(row=3, column=0, columnspan=1, sticky=tkinter.NSEW)


def calculate_total():
    global rows
    global total
    for item in rows:
        duration_parts = item[-1].split(":")
        total += datetime.timedelta(hours=int(duration_parts[0]),
                                    minutes=int(duration_parts[1]),
                                    seconds=int(duration_parts[2]))
    return total


total_time_result_label = Label(text=calculate_total(),
                                highlightbackground="LightCyan2",
                                font=("Helvetica", 14, "bold"),
                                highlightthickness=2)
total_time_result_label.grid(row=3, column=1, columnspan=2, sticky=tkinter.NSEW)

# ---------------------------- BUTTONS ------------------------------- #
log_btn = Button(text="Log work", command=log_dates)
log_btn.grid(row=0, column=2, sticky="ewns", rowspan=2)

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

for row in rows:
    table.insert('', tkinter.END, values=row)

table.grid(row=2, column=0, columnspan=3, sticky="ewns")
# ---------------------------- MESSAGE BOX --------------------------- #
confirmation_msg = messagebox.Message(window, message="Work Saved Successfully")

# -------------------------------------------------------------------- #
if __name__ == "__main__":
    window.mainloop()
