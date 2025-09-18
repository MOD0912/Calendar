import Rainbowborder
import customtkinter as ctk
import calendar
import json 
class Kalendar(ctk.CTkFrame):
    def __init__(self, master, corner_radius=10, fg_color="#1f1f1f"):
        super().__init__(master, corner_radius=corner_radius, fg_color=fg_color)
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)
        self.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.todos = {}  # Dictionary to store to-dos with (month, date) as keys
        self.current_month = 12  # December is month 12, not 11
        self.date_labels = []  # Store references to date labels for text updates only
        self.date_buttons_created = False  # Track if buttons have been created
        self.to_do_frame = None  # Track the current to-do frame
        try:
            with open("todo.json", "r") as f:
                self.todos = json.load(f)
        except FileNotFoundError:
            self.todos = {}

        print(self.todos)
        self.create_widgets()
    
    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Todo Calendar", font=ctk.CTkFont(size=50, weight="bold"))
        self.label.grid(row=0, column=5)
        
        self.Month_frame = ctk.CTkFrame(self, height=80, fg_color="#2b2b2b", corner_radius=20)
        self.Month_frame.grid(row=1, column=4, columnspan=3, sticky="ew")
        self.Month_frame.rowconfigure(0, weight=1)
        self.Month_frame.columnconfigure((0, 1, 2), weight=1)
        self.Month_Label = ctk.CTkLabel(self.Month_frame, text="December", font=ctk.CTkFont(size=30, weight="bold"))
        self.Month_Label.grid(row=0, column=1, pady=10, padx=10)
        self.Month_right = ctk.CTkButton(self.Month_frame, text=">", fg_color="#2b2b2b", width=30, height=30, corner_radius=15, font=ctk.CTkFont(size=40, weight="bold"), command=lambda: self.change_month(1))
        self.Month_right.grid(row=0, column=2, sticky="e", padx=5, pady=5)
        self.Month_left = ctk.CTkButton(self.Month_frame, text="<", fg_color="#2b2b2b", width=30, height=30, corner_radius=15, font=ctk.CTkFont(size=40, weight="bold"), command=lambda: self.change_month(-1))
        self.Month_left.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.calendar_frame = ctk.CTkFrame(self, fg_color="#2b2b2b", corner_radius=20)
        self.calendar_frame.grid(row=2, column=0, columnspan=11, rowspan=8, sticky="nsew", padx=20, pady=10)
        self.calendar_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.calendar_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        
        self.frame = ctk.CTkFrame(self.calendar_frame, fg_color="#3b3b3b", corner_radius=20, height=20)
        self.frame.grid(row=0, column=0, columnspan=7, sticky="nsew")
        self.frame.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.populate_dates()
        
        

    def populate_dates(self):
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        month_calendar = calendar.monthcalendar(2025, self.current_month)
        print(month_calendar)
        
        # Create day headers only once
        if not self.date_buttons_created:
            for i, day in enumerate(days):
                day_label = ctk.CTkLabel(self.frame, text=day, font=ctk.CTkFont(size=20, weight="bold"), fg_color="#3b3b3b", corner_radius=0)
                day_label.grid(row=0, column=i, sticky="nsew")
            
            # Create all date buttons once (6 rows x 7 columns = 42 buttons total)
            for week_num in range(6):  # Maximum 6 weeks in a month view
                week_buttons = []
                for day_num in range(7):  # 7 days per week
                    date_textbox = ctk.CTkTextbox(
                        self.calendar_frame, 
                        font=ctk.CTkFont(size=15),
                        width=50,  # Fixed width
                        height=30,  # Fixed height
                        fg_color="#2b2b2b",
                    )
                    date_textbox.grid(row=week_num + 1, column=day_num, padx=5, pady=5, sticky="nsew")
                    date_textbox.bind("<Button-1>", lambda e, r=week_num, c=day_num: self.button_clicked(r, c))
                    week_buttons.append(date_textbox)
                self.date_labels.append(week_buttons)
            
            self.date_buttons_created = True
        
        # Update button texts and states for current month
        for week_num, week in enumerate(month_calendar):
            for day_num, date in enumerate(week):
                button = self.date_labels[week_num][day_num]
                button.configure(state="normal")  # Enable button to update text
                button.delete("0.0", "end")  # Clear existing text
                if date == 0:
                    button.configure(fg_color="#2b2b2b")
                else:
                    button.insert("0.0", f'''
                            {date}
__________________________________
{self.todos.get(f"{self.current_month} {date}", "")}
                                  ''')
                    
                button.configure(state="disabled")
        
        # Hide buttons for weeks not needed this month
        for week_num in range(len(month_calendar), 6):
            for day_num in range(7):
                button = self.date_labels[week_num][day_num]
                button.configure(fg_color="#2b2b2b")
        
        self.to_do_frame = ctk.CTkFrame(self, height=200, fg_color="#2b2b2b", corner_radius=20)
        
        
        
    def button_clicked(self, row, col):
        """Handle button clicks and get the actual date from the current month calendar"""
        month_calendar = calendar.monthcalendar(2025, self.current_month)
        if row < len(month_calendar) and col < len(month_calendar[row]):
            date = month_calendar[row][col]
            if date != 0:  # Only process valid dates
                self.open_to_do(date, self.current_month)
        
    def destroy_old_labels(self, old_labels):
        for label in old_labels:
            label.destroy()
        old_labels.clear()
        
    def change_month(self, delta):
        self.current_month += delta
        # Handle year wraparound properly
        if self.current_month > 12:
            self.current_month = 1
        elif self.current_month < 1:
            self.current_month = 12
        
        self.Month_Label.configure(text=self.months[self.current_month - 1])  # months list is 0-indexed
        self.populate_dates()
        
    def open_to_do(self, date, month):
        if date == 0:
            return  # Ignore clicks on empty dates
        print(month, date) 
        
        try:
            text = self.todos[f"{month} {date}"]
        except KeyError:
            text = ""
        print("To-Do for", date, month, ":", text)
        self.to_do_frame = ctk.CTkFrame(self, height=200, fg_color="#2b2b2b", corner_radius=20)
        self.to_do_frame.grid(row=0, column=0, columnspan=11, rowspan=11, sticky="nsew", padx=20, pady=10)
        self.to_do_frame.rowconfigure(0, weight=1)
        self.to_do_frame.rowconfigure(1, weight=10)
        self.to_do_frame.columnconfigure((0, 1, 2, 3), weight=1)
        self.to_do_frame.lift()  # Bring the to-do frame to the front
        # Set focus to textbox to enable key bindings
        
        self.label = ctk.CTkLabel(self.to_do_frame, text=f"To-Do for {self.months[month - 1]} {date}:", font=ctk.CTkFont(size=40, weight="bold"))
        self.label.grid(row=0, column=2, sticky="w", padx=10, pady=5)
        self.line = ctk.CTkLabel(self.to_do_frame, text="-"*1000, font=ctk.CTkFont(size=20))
        self.line.grid(row=0, column=0, columnspan=4, sticky="ews", padx=10, pady=5)
        self.textbox = ctk.CTkTextbox(self.to_do_frame, font=ctk.CTkFont(size=20), wrap="word", fg_color="#2b2b2b", border_color="#2b2b2b", corner_radius=10, border_spacing=100)
        self.textbox.lift()
        self.textbox.grid(row=1, column=0, columnspan=9, rowspan=8, sticky="nsew", padx=10, pady=5)
        self.textbox.insert("0.0", text if text != "<empty>" else "")
        root.after(50, self.textbox.focus_set)  # Set focus to textbox to enable key bindings
        # Bind escape key to close the to-do frame
        self.textbox.bind("<Escape>", lambda e: self.close_todo_frame())
    
    def close_todo_frame(self):
        """Close the to-do frame by saving and destroying it, then refresh calendar UI"""
        if self.to_do_frame is not None:
            self.save_todo()
            self.to_do_frame.destroy()
            self.to_do_frame = None
            self.populate_dates()  # Refresh calendar UI after saving
            
    
    def on_exit(self):
        self.save_todo()
        self.to_do_frame.destroy()
        
        

    def save_todo(self):    
        if self.to_do_frame is None:
            return  # Nothing to save if frame doesn't exist
        try:
            self.textbox_content = self.textbox.get("0.0", "end-1c").strip()
                # Extract date and month from the label text
            label_text = self.label.cget("text")
            parts = label_text.split()
            if len(parts) >= 4:
                month_name = parts[2]
                date_str = parts[3].rstrip(":")
                try:
                    month = self.months.index(month_name) + 1  # Convert month name to month number
                    date = int(date_str)
                    if self.textbox_content == "":
                        if f"{month} {date}" in self.todos:
                            del self.todos[f"{month} {date}"]  # Remove empty to-dos
                            print(f"Removed To-Do for {month_name} {date}")
                    self.todos[f"{month} {date}"] = self.textbox_content
                    print(f"Saved To-Do for {month_name} {date}: {self.textbox_content}")
                except ValueError:
                    print("Error parsing date or month.")

        except Exception as e:
            print("Error saving To-Do:", e)

def on_exit():
    if kalendar.to_do_frame is not None:
        kalendar.save_todo()
    with open("todo.json", "w") as f:
        json.dump(kalendar.todos, f)
    exit()


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.title("Rainbow Border Example")


    root.resizable(False, False)
    root.geometry("2000x1200+280+200")
    #remove highlight border
    rainbow_border = Rainbowborder.RainbowBorder(root, border_width=5)
    kalendar = Kalendar(rainbow_border)
    kalendar.pack(fill="both", expand=True, padx=10, pady=10)
    root.protocol("WM_DELETE_WINDOW", on_exit)
    root.mainloop()
