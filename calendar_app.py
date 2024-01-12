import tkinter as tk
from tkcalendar import Calendar

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Календар")

        # Календар
        self.calendar = Calendar(self.root, selectmode="day")
        self.calendar.pack(fill="both", expand=True)

    def get_selected_date(self):
        return self.calendar.get_date()

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = CalendarApp(root)
#     root.mainloop()
