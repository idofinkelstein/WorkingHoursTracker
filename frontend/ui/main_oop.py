import os
import pathlib
import tkinter
from tkinter import Tk, Label, Button, Entry, ttk, messagebox, Toplevel
from PIL import Image, ImageTk
from backend.core.date_validator import Validator
from backend.core.csv_date_io import IOHandler
from backend.core.date_and_time import DateHandler
from datetime import datetime, timedelta
from tkcalendar import DateEntry
from tktimepicker import SpinTimePickerModern, constants


class App(Tk):
    csv_rows = IOHandler.read_lines_from_csv(IOHandler.FULL_PATH)
    total = timedelta()

    def __init__(self):
        super().__init__()
        self.title("Working Hours Tracking")
        self.geometry("700x500")
        self.config(bg="sky blue")
        self.minsize(600, 320)
        self.image_path = os.path.join(os.path.split(os.path.dirname(os.path.join(__file__)))[0],
                                       "resources", "clock.png")
        self.bg_image = self.adjust_image(self.image_path)
        self.photo_image = ImageTk.PhotoImage(self.bg_image)
        self.rows = IOHandler.read_lines_from_csv(IOHandler.FULL_PATH)
        self.confirmation_msg = messagebox.Message(self, message="Work Saved Successfully")

        # WIDGETS
        self.background_label = Label(image=self.photo_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.widgets = WidgetLayout(self)
        self.table = DateTable(self)

        self.mainloop()

    def get_time(self, time_entry: Entry):
        top = Toplevel(self)
        ttk.Label(top, text='Choose date and time').pack(padx=10, pady=10)

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

        ok_btn = Button(top,
                        text="ok",
                        command=lambda: App.updateTime(time_picker.time(), cal.get_date(), top, time_entry))
        ok_btn.pack()

    @staticmethod
    def calculate_total():
        for item in App.csv_rows:
            duration = DateHandler.construct_timedelta_from_string(item[-1])
            try:
                App.total += duration
            except ValueError as e:
                print("Error: Can't constructing timedelta object\n", e)
        return App.total

    def log_dates(self):
        start_date = self.widgets.start_time_entry.get()
        end_date = self.widgets.end_time_entry.get()

        if Validator.validate_input(start_date, end_date):
            start_date_obj = DateHandler.create_date(start_date)
            end_date_obj = DateHandler.create_date(end_date)
            hours_diff = DateHandler.subtract_time(start_date_obj, end_date_obj)
            zero_diff = timedelta()
            if hours_diff > zero_diff:
                IOHandler.save_to_csv(IOHandler.FULL_PATH, start_date, end_date, hours_diff)
                self.table.insert('', tkinter.END, values=[start_date, end_date, hours_diff])
                self.total += hours_diff
                self.widgets.total_time_result_label.config(text=self.total)
                self.confirmation_msg.show()

    def adjust_image(self, image_path: pathlib.Path):
        with Image.open(image_path) as image:
            width, height = image.size
            aspect_ratio = width / height
            new_height = 600
            new_width = int(aspect_ratio * new_height)
            image = image.resize((new_width, new_height))
        return image

    @staticmethod
    def updateTime(selected_time: tuple[int, int, str], selected_date: datetime, widget: Tk, time_entry: Entry):
        time_entry.delete(0, tkinter.END)
        time_entry.insert(0, f"{selected_date.day}/{selected_date.month}/{selected_date.year} "
                             f"{selected_time[0]}:{selected_time[1]}")
        widget.destroy()


class WidgetLayout:
    def __init__(self, main_app):
        self.total_time_label = None
        self.app = main_app
        self.end_time_entry = None
        self.start_time_entry = None
        self.end_time_button = None
        self.start_time_button = None
        self.log_button = None
        self.total_time_result_label = None
        self.create_widgets()
        self.place_widgets()

    def create_widgets(self):
        self.log_button = Button(text="Log work", command=self.app.log_dates)
        self.start_time_button = Button(text="Pick Start time",
                                        command=lambda: self.app.get_time(self.start_time_entry))
        self.end_time_button = Button(text="Pick End time", command=lambda: self.app.get_time(self.end_time_entry))
        self.start_time_entry = Entry(width=28)
        self.end_time_entry = Entry(width=28)
        self.total_time_label = Label(text="Total Time:", highlightbackground="LightCyan2",
                                      font=("Helvetica", 14, "bold"),
                                      highlightthickness=2)

        self.total_time_result_label = Label(text=str(App.calculate_total()),
                                             highlightbackground="LightCyan2",
                                             font=("Helvetica", 14, "bold"),
                                             highlightthickness=2)

    def place_widgets(self):
        self.log_button.grid(row=0, column=2, sticky=tkinter.NSEW, rowspan=2)
        self.start_time_button.grid(row=0, column=0, sticky=tkinter.NSEW)
        self.end_time_button.grid(row=1, column=0, sticky=tkinter.NSEW)
        self.start_time_entry.focus()
        self.start_time_entry.grid(row=0, column=1, sticky=tkinter.NSEW)
        self.end_time_entry.grid(row=1, column=1, columnspan=1, sticky=tkinter.NSEW)
        self.total_time_label.grid(row=3, column=0, columnspan=1, sticky=tkinter.NSEW)
        self.total_time_result_label.grid(row=3, column=1, columnspan=2, sticky=tkinter.NSEW)


class DateTable(ttk.Treeview):
    def __init__(self, parent):
        super().__init__(parent, columns=("start", "end", "duration"), show="headings")
        self.style = ttk.Style(parent)
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="snow",
                             fieldbackground="bisque2", foreground="blue4")

        self.heading("start", text="Start Time")
        self.heading("end", text="End Time")
        self.heading("duration", text="Duration")
        self.grid(row=2, column=0, columnspan=3, sticky="ewns")

        for row in App.csv_rows:
            self.insert('', tkinter.END, values=row)


if __name__ == "__main__":
    app = App()
