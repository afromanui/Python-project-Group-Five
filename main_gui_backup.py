import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from services.auth_service import AuthService
from services.patient_service import PatientService
from services.doctor_service import DoctorService
from services.appointment_service import AppointmentService
from services.medical_record_service import MedicalRecordService
from services.billing_service import BillingService
from services.administrator_service import AdministratorService


# ============================================================
# HOSPITAL MANAGEMENT SYSTEM
# PROFESSIONAL CRUD GUI
# PYTHON + MYSQL
# ============================================================

APP_TITLE = "Hospital Management System"

WINDOW_WIDTH = 1350
WINDOW_HEIGHT = 800

CURRENCY = "K"
FONT = "Segoe UI"


# ============================================================
# COLOURS
# ============================================================

NAVY = "#17365D"
DARK_NAVY = "#102A43"
BLUE = "#1F4E78"
LIGHT_BLUE = "#EAF3F8"

BACKGROUND = "#F4F7FA"
WHITE = "#FFFFFF"

TEXT = "#1F2937"
MUTED = "#64748B"
BORDER = "#D5DDE5"

GREEN = "#2E7D32"
LIGHT_GREEN = "#E8F5E9"

ORANGE = "#B7791F"
LIGHT_ORANGE = "#FFF8E1"

RED = "#B91C1C"
LIGHT_RED = "#FEE2E2"

PURPLE = "#6B4FA1"
LIGHT_PURPLE = "#F3EFFB"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_value(row, *names, default=""):
    """Safely retrieve a value from a dictionary or object."""

    if row is None:
        return default

    if isinstance(row, dict):
        for name in names:
            if name in row:
                value = row[name]
                return default if value is None else value

    else:
        for name in names:
            if hasattr(row, name):
                value = getattr(row, name)
                return default if value is None else value

    return default


def safe_text(value):
    if value is None:
        return ""
    return str(value)


def money(value):
    try:
        return f"{CURRENCY} {float(value):,.2f}"
    except (ValueError, TypeError):
        return f"{CURRENCY} 0.00"


def parse_id(value, field_name):
    value = str(value).strip()

    if not value:
        raise ValueError(f"{field_name} is required.")

    try:
        return int(value)
    except ValueError:
        raise ValueError(f"{field_name} must be a valid number.")


def selected_tree_id(tree):
    selection = tree.selection()

    if not selection:
        return None

    values = tree.item(selection[0], "values")

    if not values:
        return None

    return values[0]


# ============================================================
# LOGIN PAGE
# ============================================================

class LoginPage(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg=BACKGROUND)

        self.app = app
        self.auth_service = AuthService()

        self.show_login_form()

    def clear_page(self):
        for widget in self.winfo_children():
            widget.destroy()

    def create_center_container(self):

        outer = tk.Frame(self, bg=BACKGROUND)
        outer.pack(fill="both", expand=True)

        card = tk.Frame(
            outer,
            bg=WHITE,
            bd=1,
            relief="solid"
        )

        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=500
        )

        return card

    # ========================================================
    # LOGIN
    # ========================================================

    def show_login_form(self):

        self.clear_page()

        card = self.create_center_container()

        header = tk.Frame(
            card,
            bg=NAVY,
            height=125
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="✚",
            font=(FONT, 30, "bold"),
            bg=NAVY,
            fg=WHITE
        ).pack(pady=(15, 0))

        tk.Label(
            header,
            text="HOSPITAL MANAGEMENT SYSTEM",
            font=(FONT, 15, "bold"),
            bg=NAVY,
            fg=WHITE
        ).pack()

        tk.Label(
            header,
            text="Secure Staff Sign In",
            font=(FONT, 9),
            bg=NAVY,
            fg="#D9E7F2"
        ).pack()

        form = tk.Frame(card, bg=WHITE)
        form.pack(fill="x", padx=45, pady=30)

        tk.Label(
            form,
            text="Sign In",
            font=(FONT, 20, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(anchor="w")

        tk.Label(
            form,
            text="Enter your account details to continue.",
            font=(FONT, 9),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w", pady=(3, 20))

        tk.Label(
            form,
            text="Username",
            font=(FONT, 10, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(anchor="w")

        self.login_username = ttk.Entry(
            form,
            font=(FONT, 10)
        )
        self.login_username.pack(
            fill="x",
            pady=(6, 15)
        )

        tk.Label(
            form,
            text="Password",
            font=(FONT, 10, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(anchor="w")

        self.login_password = ttk.Entry(
            form,
            show="*",
            font=(FONT, 10)
        )
        self.login_password.pack(
            fill="x",
            pady=(6, 20)
        )

        tk.Button(
            form,
            text="SIGN IN",
            font=(FONT, 10, "bold"),
            bg=NAVY,
            fg=WHITE,
            activebackground=BLUE,
            activeforeground=WHITE,
            relief="flat",
            cursor="hand2",
            pady=11,
            command=self.sign_in
        ).pack(fill="x")

        tk.Label(
            form,
            text="Don't have an account?",
            font=(FONT, 9),
            bg=WHITE,
            fg=MUTED
        ).pack(pady=(20, 3))

        tk.Button(
            form,
            text="Create New Account",
            font=(FONT, 9, "bold"),
            bg=WHITE,
            fg=BLUE,
            activebackground=LIGHT_BLUE,
            activeforeground=NAVY,
            relief="flat",
            cursor="hand2",
            command=self.show_signup_form
        ).pack()

        tk.Label(
            card,
            text=(
                "Created by: Kimberly Saelon • Barbara • Rowen\n"
                "Group 5 – Bachelor in Information Technology\n"
                "Powered by Python & MySQL"
            ),
            font=(FONT, 8),
            bg=WHITE,
            fg=MUTED
        ).pack(pady=(0, 25))

        self.login_username.focus_set()

        self.login_username.bind(
            "<Return>",
            lambda event: self.sign_in()
        )

        self.login_password.bind(
            "<Return>",
            lambda event: self.sign_in()
        )

    def sign_in(self):

        username = self.login_username.get().strip()
        password = self.login_password.get()

        if not username:
            messagebox.showwarning(
                "Sign In",
                "Please enter your username."
            )
            self.login_username.focus_set()
            return

        if not password:
            messagebox.showwarning(
                "Sign In",
                "Please enter your password."
            )
            self.login_password.focus_set()
            return

        try:

            self.app.configure(cursor="watch")
            self.update_idletasks()

            user = self.auth_service.login(
                username,
                password
            )

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                "Unable to sign in.\n\n"
                f"{type(error).__name__}: {error}"
            )

            return

        finally:
            self.app.configure(cursor="")

        if user:

            self.app.login_successful(user)

        else:

            messagebox.showerror(
                "Sign In Failed",
                "Invalid username or password."
            )

            self.login_password.delete(0, tk.END)
            self.login_password.focus_set()

    # ========================================================
    # SIGN UP
    # ========================================================

    def show_signup_form(self):

        self.clear_page()

        card = self.create_center_container()

        header = tk.Frame(
            card,
            bg=NAVY,
            height=115
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="CREATE ACCOUNT",
            font=(FONT, 17, "bold"),
            bg=NAVY,
            fg=WHITE
        ).pack(pady=(23, 4))

        tk.Label(
            header,
            text="Hospital Management System",
            font=(FONT, 9),
            bg=NAVY,
            fg="#D9E7F2"
        ).pack()

        form = tk.Frame(card, bg=WHITE)
        form.pack(fill="x", padx=45, pady=25)

        tk.Label(
            form,
            text="Sign Up",
            font=(FONT, 20, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(anchor="w")

        tk.Label(
            form,
            text="Create a new hospital system user account.",
            font=(FONT, 9),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w", pady=(3, 18))

        tk.Label(
            form,
            text="Username",
            font=(FONT, 10, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(anchor="w")

        self.signup_username = ttk.Entry(
            form,
            font=(FONT, 10)
        )
        self.signup_username.pack(
            fill="x",
            pady=(5, 12)
        )

        tk.Label(
            form,
            text="Password",
            font=(FONT, 10, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(anchor="w")

        self.signup_password = ttk.Entry(
            form,
            show="*",
            font=(FONT, 10)
        )
        self.signup_password.pack(
            fill="x",
            pady=(5, 12)
        )

        tk.Label(
            form,
            text="Confirm Password",
            font=(FONT, 10, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(anchor="w")

        self.signup_confirm = ttk.Entry(
            form,
            show="*",
            font=(FONT, 10)
        )
        self.signup_confirm.pack(
            fill="x",
            pady=(5, 12)
        )

        tk.Label(
            form,
            text="Role",
            font=(FONT, 10, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(anchor="w")

        self.signup_role = ttk.Combobox(
            form,
            state="readonly",
            values=(
                "Staff",
                "Doctor",
                "Administrator"
            ),
            font=(FONT, 10)
        )

        self.signup_role.pack(
            fill="x",
            pady=(5, 20)
        )

        self.signup_role.set("Staff")

        tk.Button(
            form,
            text="CREATE ACCOUNT",
            font=(FONT, 10, "bold"),
            bg=NAVY,
            fg=WHITE,
            activebackground=BLUE,
            activeforeground=WHITE,
            relief="flat",
            cursor="hand2",
            pady=10,
            command=self.sign_up
        ).pack(fill="x")

        tk.Button(
            form,
            text="← Back to Sign In",
            font=(FONT, 9, "bold"),
            bg=WHITE,
            fg=BLUE,
            activebackground=LIGHT_BLUE,
            activeforeground=NAVY,
            relief="flat",
            cursor="hand2",
            command=self.show_login_form
        ).pack(pady=(15, 0))

        tk.Label(
            card,
            text=(
                "Created by: Kimberly Saelon • Barbara • Rowen\n"
                "Group 5 – Bachelor in Information Technology"
            ),
            font=(FONT, 8),
            bg=WHITE,
            fg=MUTED
        ).pack(pady=(0, 20))

        self.signup_username.focus_set()

    def sign_up(self):

        username = self.signup_username.get().strip()
        password = self.signup_password.get()
        confirm = self.signup_confirm.get()
        role = self.signup_role.get().strip() or "Staff"

        if not username:
            messagebox.showwarning(
                "Sign Up",
                "Please enter a username."
            )
            self.signup_username.focus_set()
            return

        if not password:
            messagebox.showwarning(
                "Sign Up",
                "Please enter a password."
            )
            self.signup_password.focus_set()
            return

        if not confirm:
            messagebox.showwarning(
                "Sign Up",
                "Please confirm your password."
            )
            self.signup_confirm.focus_set()
            return

        if password != confirm:
            messagebox.showerror(
                "Sign Up",
                "The passwords do not match."
            )
            self.signup_confirm.focus_set()
            return

        try:

            self.app.configure(cursor="watch")
            self.update_idletasks()

            success, message = self.auth_service.register_user(
                username,
                password,
                confirm,
                role
            )

        except Exception as error:

            success = False
            message = (
                "Unable to create the account.\n\n"
                f"{type(error).__name__}: {error}"
            )

        finally:
            self.app.configure(cursor="")

        if success:

            messagebox.showinfo(
                "Account Created",
                message + "\n\nYou can now sign in."
            )

            self.show_login_form()

            self.login_username.insert(
                0,
                username
            )

            self.login_password.focus_set()

        else:

            messagebox.showerror(
                "Account Creation Failed",
                message
            )


# ============================================================
# BASE PAGE
# ============================================================

class BasePage(tk.Frame):

    def __init__(
        self,
        parent,
        app,
        title,
        subtitle
    ):

        super().__init__(
            parent,
            bg=BACKGROUND
        )

        self.app = app
        self.title_text = title
        self.subtitle_text = subtitle

        self.build_header()

    def build_header(self):

        header = tk.Frame(
            self,
            bg=WHITE,
            height=75
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        title_frame = tk.Frame(
            header,
            bg=WHITE
        )

        title_frame.pack(
            side="left",
            padx=25
        )

        tk.Label(
            title_frame,
            text=self.title_text,
            font=(FONT, 21, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(
            anchor="w",
            pady=(12, 0)
        )

        tk.Label(
            title_frame,
            text=self.subtitle_text,
            font=(FONT, 9),
            bg=WHITE,
            fg=MUTED
        ).pack(anchor="w")

        self.refresh_button = tk.Button(
            header,
            text="↻  Refresh",
            font=(FONT, 10, "bold"),
            bg=LIGHT_BLUE,
            fg=BLUE,
            activebackground="#D6E8F2",
            activeforeground=NAVY,
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=8,
            command=self.refresh
        )

        self.refresh_button.pack(
            side="right",
            padx=25,
            pady=18
        )

        tk.Frame(
            self,
            bg=BORDER,
            height=1
        ).pack(fill="x")

    def refresh(self):
        pass


# ============================================================
# DATA PAGE
# ============================================================

class DataPage(BasePage):

    def __init__(
        self,
        parent,
        app,
        title,
        subtitle,
        columns
    ):

        self.columns = columns

        super().__init__(
            parent,
            app,
            title,
            subtitle
        )

        self.build_page()

    # ========================================================
    # BUILD PAGE
    # ========================================================

    def build_page(self):

        # ----------------------------------------------------
        # ACTION BAR
        # ----------------------------------------------------

        action_bar = tk.Frame(
            self,
            bg=BACKGROUND
        )

        action_bar.pack(
            fill="x",
            padx=25,
            pady=(18, 5)
        )

        tk.Button(
            action_bar,
            text="＋ Add New",
            font=(FONT, 9, "bold"),
            bg=NAVY,
            fg=WHITE,
            activebackground=BLUE,
            activeforeground=WHITE,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7,
            command=self.add_record
        ).pack(
            side="left",
            padx=(0, 7)
        )

        tk.Button(
            action_bar,
            text="✎ Edit Selected",
            font=(FONT, 9, "bold"),
            bg=BLUE,
            fg=WHITE,
            activebackground=NAVY,
            activeforeground=WHITE,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7,
            command=self.edit_selected
        ).pack(
            side="left",
            padx=7
        )

        tk.Button(
            action_bar,
            text="✕ Delete Selected",
            font=(FONT, 9, "bold"),
            bg=RED,
            fg=WHITE,
            activebackground="#8B0000",
            activeforeground=WHITE,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7,
            command=self.delete_selected
        ).pack(
            side="left",
            padx=7
        )

        tk.Button(
            action_bar,
            text="↻ Refresh",
            font=(FONT, 9, "bold"),
            bg=LIGHT_GREEN,
            fg=GREEN,
            activebackground="#D8ECD9",
            activeforeground=GREEN,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=7,
            command=self.refresh
        ).pack(
            side="left",
            padx=7
        )

        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        search_frame = tk.Frame(
            self,
            bg=BACKGROUND
        )

        search_frame.pack(
            fill="x",
            padx=25,
            pady=(8, 15)
        )

        tk.Label(
            search_frame,
            text="Search:",
            font=(FONT, 10, "bold"),
            bg=BACKGROUND,
            fg=TEXT
        ).pack(side="left")

        self.search_var = tk.StringVar()

        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=35,
            font=(FONT, 10)
        )

        search_entry.pack(
            side="left",
            padx=8
        )

        search_entry.bind(
            "<KeyRelease>",
            lambda event: self.refresh()
        )

        tk.Button(
            search_frame,
            text="Clear Search",
            font=(FONT, 9),
            bg=WHITE,
            fg=TEXT,
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=6,
            command=self.clear_search
        ).pack(side="left")

        self.count_label = tk.Label(
            search_frame,
            text="0 record(s)",
            font=(FONT, 9),
            bg=BACKGROUND,
            fg=MUTED
        )

        self.count_label.pack(
            side="right"
        )

        # ----------------------------------------------------
        # TABLE
        # ----------------------------------------------------

        table_container = tk.Frame(
            self,
            bg=WHITE,
            bd=1,
            relief="solid"
        )

        table_container.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 25)
        )

        tree_frame = tk.Frame(
            table_container,
            bg=WHITE
        )

        tree_frame.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=12
        )

        keys = [
            column[0]
            for column in self.columns
        ]

        self.tree = ttk.Treeview(
            tree_frame,
            columns=keys,
            show="headings",
            selectmode="browse"
        )

        for key, heading, width in self.columns:

            self.tree.heading(
                key,
                text=heading
            )

            self.tree.column(
                key,
                width=width,
                anchor="w",
                minwidth=50
            )

        vertical = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=self.tree.yview
        )

        horizontal = ttk.Scrollbar(
            tree_frame,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=vertical.set,
            xscrollcommand=horizontal.set
        )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        vertical.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        horizontal.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        tree_frame.rowconfigure(
            0,
            weight=1
        )

        tree_frame.columnconfigure(
            0,
            weight=1
        )

        self.tree.bind(
            "<Double-1>",
            lambda event: self.edit_selected()
        )

        self.tree.bind(
            "<Delete>",
            lambda event: self.delete_selected()
        )

    # ========================================================
    # TABLE
    # ========================================================

    def load_table(self, rows):

        for item in self.tree.get_children():
            self.tree.delete(item)

        search = self.search_var.get().strip().lower()

        visible = 0

        for row in rows:

            values = self.row_values(row)

            searchable = " ".join(
                safe_text(value)
                for value in values
            ).lower()

            if search and search not in searchable:
                continue

            self.tree.insert(
                "",
                "end",
                values=values
            )

            visible += 1

        if search:

            self.count_label.config(
                text=f"{visible} matching record(s)"
            )

        else:

            self.count_label.config(
                text=f"{len(rows)} record(s)"
            )

    def row_values(self, row):
        raise NotImplementedError

    def get_rows(self):
        raise NotImplementedError

    # ========================================================
    # CRUD METHODS
    # ========================================================

    def add_record(self):
        messagebox.showinfo(
            "Add Record",
            f"Add form for {self.title_text} is not configured."
        )

    def edit_selected(self):

        row_id = selected_tree_id(self.tree)

        if row_id is None:

            messagebox.showwarning(
                "Edit Record",
                f"Please select a {self.title_text.lower()} record first."
            )

            return

        self.edit_record(row_id)

    def edit_record(self, row_id):

        messagebox.showinfo(
            "Edit Record",
            f"Edit form for {self.title_text} is not configured."
        )

    def delete_selected(self):

        row_id = selected_tree_id(self.tree)

        if row_id is None:

            messagebox.showwarning(
                "Delete Record",
                f"Please select a {self.title_text.lower()} record first."
            )

            return

        answer = messagebox.askyesno(
            "Confirm Delete",
            (
                f"Are you sure you want to delete this "
                f"{self.title_text.lower()} record?\n\n"
                f"Record ID: {row_id}"
            )
        )

        if not answer:
            return

        try:

            self.delete_record(row_id)

            self.refresh()

            self.app.set_status(
                f"{self.title_text}: record deleted successfully",
                GREEN
            )

        except Exception as error:

            self.app.set_status(
                f"{self.title_text}: delete failed",
                RED
            )

            messagebox.showerror(
                "Delete Error",
                (
                    f"Unable to delete the record.\n\n"
                    f"{type(error).__name__}: {error}\n\n"
                    "If this record is linked to another hospital "
                    "record, delete or update the related record first."
                )
            )

    def delete_record(self, row_id):
        raise NotImplementedError

    # ========================================================
    # REFRESH
    # ========================================================

    def refresh(self):

        try:

            rows = list(
                self.get_rows()
            )

            self.load_table(rows)

            self.app.set_status(
                f"{self.title_text}: {len(rows)} record(s) loaded from MySQL",
                GREEN
            )

        except Exception as error:

            self.app.set_status(
                f"{self.title_text}: Refresh failed",
                RED
            )

            messagebox.showerror(
                "Refresh Error",
                (
                    f"Unable to refresh {self.title_text}.\n\n"
                    f"{type(error).__name__}: {error}"
                )
            )

    def clear_search(self):

        self.search_var.set("")
        self.refresh()


# ============================================================
# FORM WINDOW HELPER
# ============================================================

class FormWindow(tk.Toplevel):

    def __init__(
        self,
        parent,
        title,
        width=520,
        height=600
    ):

        super().__init__(parent)

        self.title(title)
        self.geometry(f"{width}x{height}")
        self.minsize(width, height)

        self.configure(bg=BACKGROUND)

        self.transient(parent)
        self.grab_set()

        self.protocol(
            "WM_DELETE_WINDOW",
            self.destroy
        )

    def header(self, title, subtitle):

        frame = tk.Frame(
            self,
            bg=NAVY,
            height=85
        )

        frame.pack(fill="x")
        frame.pack_propagate(False)

        tk.Label(
            frame,
            text=title,
            font=(FONT, 17, "bold"),
            bg=NAVY,
            fg=WHITE
        ).pack(
            anchor="w",
            padx=22,
            pady=(16, 2)
        )

        tk.Label(
            frame,
            text=subtitle,
            font=(FONT, 9),
            bg=NAVY,
            fg="#D9E7F2"
        ).pack(
            anchor="w",
            padx=22
        )

    def body(self):

        frame = tk.Frame(
            self,
            bg=WHITE
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        return frame

    def field(
        self,
        parent,
        label,
        variable=None,
        show=None
    ):

        tk.Label(
            parent,
            text=label,
            font=(FONT, 9, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(
            anchor="w",
            pady=(7, 3)
        )

        entry = ttk.Entry(
            parent,
            textvariable=variable,
            show=show,
            font=(FONT, 10)
        )

        entry.pack(
            fill="x",
            pady=(0, 5)
        )

        return entry

    def combo(
        self,
        parent,
        label,
        variable,
        values,
        readonly=True
    ):

        tk.Label(
            parent,
            text=label,
            font=(FONT, 9, "bold"),
            bg=WHITE,
            fg=TEXT
        ).pack(
            anchor="w",
            pady=(7, 3)
        )

        combo = ttk.Combobox(
            parent,
            textvariable=variable,
            values=values,
            state="readonly" if readonly else "normal",
            font=(FONT, 10)
        )

        combo.pack(
            fill="x",
            pady=(0, 5)
        )

        return combo

    def buttons(self, parent, save_command):

        frame = tk.Frame(
            parent,
            bg=WHITE
        )

        frame.pack(
            fill="x",
            pady=(20, 5)
        )

        tk.Button(
            frame,
            text="Save",
            font=(FONT, 10, "bold"),
            bg=NAVY,
            fg=WHITE,
            activebackground=BLUE,
            activeforeground=WHITE,
            relief="flat",
            cursor="hand2",
            padx=22,
            pady=9,
            command=save_command
        ).pack(
            side="left",
            padx=(0, 8)
        )

        tk.Button(
            frame,
            text="Cancel",
            font=(FONT, 10),
            bg=LIGHT_RED,
            fg=RED,
            relief="flat",
            cursor="hand2",
            padx=22,
            pady=9,
            command=self.destroy
        ).pack(side="left")


# ============================================================
# PATIENTS
# ============================================================

class PatientsPage(DataPage):

    def __init__(self, parent, app):

        self.service = PatientService()

        columns = (
            ("id", "ID", 60),
            ("first_name", "First Name", 130),
            ("last_name", "Last Name", 130),
            ("dob", "Date of Birth", 110),
            ("gender", "Gender", 90),
            ("phone", "Phone", 120),
            ("address", "Address", 180),
            ("emergency", "Emergency Contact", 160),
        )

        super().__init__(
            parent,
            app,
            "Patients",
            "Patient registration and information",
            columns
        )

    def get_rows(self):
        return self.service.get_all_patients()

    def row_values(self, patient):

        return (
            get_value(patient, "patient_id", "id"),
            get_value(patient, "first_name"),
            get_value(patient, "last_name"),
            get_value(patient, "date_of_birth", "dob"),
            get_value(patient, "gender"),
            get_value(patient, "phone"),
            get_value(patient, "address"),
            get_value(patient, "emergency_contact")
        )

    def add_record(self):

        window = FormWindow(
            self,
            "Add Patient",
            560,
            610
        )

        window.header(
            "Add New Patient",
            "Enter patient information"
        )

        body = window.body()

        first = tk.StringVar()
        last = tk.StringVar()
        dob = tk.StringVar()
        gender = tk.StringVar()
        phone = tk.StringVar()
        address = tk.StringVar()
        emergency = tk.StringVar()

        window.field(body, "First Name *", first)
        window.field(body, "Last Name *", last)
        window.field(body, "Date of Birth", dob)

        window.combo(
            body,
            "Gender",
            gender,
            ["", "Male", "Female", "Other"]
        )

        window.field(body, "Phone", phone)
        window.field(body, "Address", address)
        window.field(body, "Emergency Contact", emergency)

        def save():

            try:

                if not first.get().strip():
                    raise ValueError("First name is required.")

                if not last.get().strip():
                    raise ValueError("Last name is required.")

                self.service.add_patient(
                    first.get().strip(),
                    last.get().strip(),
                    dob.get().strip(),
                    gender.get().strip(),
                    phone.get().strip(),
                    address.get().strip(),
                    emergency.get().strip()
                )

                window.destroy()
                self.refresh()

                self.app.set_status(
                    "Patient added successfully",
                    GREEN
                )

                messagebox.showinfo(
                    "Patient Added",
                    "Patient record added successfully."
                )

            except Exception as error:

                messagebox.showerror(
                    "Add Patient Error",
                    f"Unable to add patient.\n\n"
                    f"{type(error).__name__}: {error}"
                )

        window.buttons(body, save)

    def edit_record(self, row_id):

        try:
            patient = self.service.get_patient(
                int(row_id)
            )

            if not patient:
                raise ValueError(
                    "Patient record could not be found."
                )

        except Exception as error:

            messagebox.showerror(
                "Edit Patient",
                f"Unable to load patient.\n\n"
                f"{type(error).__name__}: {error}"
            )

            return

        window = FormWindow(
            self,
            "Edit Patient",
            560,
            610
        )

        window.header(
            "Edit Patient",
            f"Patient ID: {row_id}"
        )

        body = window.body()

        first = tk.StringVar(
            value=safe_text(
                get_value(patient, "first_name")
            )
        )

        last = tk.StringVar(
            value=safe_text(
                get_value(patient, "last_name")
            )
        )

        dob = tk.StringVar(
            value=safe_text(
                get_value(patient, "date_of_birth", "dob")
            )
        )

        gender = tk.StringVar(
            value=safe_text(
                get_value(patient, "gender")
            )
        )

        phone = tk.StringVar(
            value=safe_text(
                get_value(patient, "phone")
            )
        )

        address = tk.StringVar(
            value=safe_text(
                get_value(patient, "address")
            )
        )

        emergency = tk.StringVar(
            value=safe_text(
                get_value(patient, "emergency_contact")
            )
        )

        window.field(body, "First Name *", first)
        window.field(body, "Last Name *", last)
        window.field(body, "Date of Birth", dob)

        window.combo(
            body,
            "Gender",
            gender,
            ["", "Male", "Female", "Other"]
        )

        window.field(body, "Phone", phone)
        window.field(body, "Address", address)
        window.field(body, "Emergency Contact", emergency)

        def save():

            try:

                if not first.get().strip():
                    raise ValueError("First name is required.")

                if not last.get().strip():
                    raise ValueError("Last name is required.")

                self.service.update_patient(
                    int(row_id),
                    first.get().strip(),
                    last.get().strip(),
                    dob.get().strip(),
                    gender.get().strip(),
                    phone.get().strip(),
                    address.get().strip(),
                    emergency.get().strip()
                )

                window.destroy()
                self.refresh()

                self.app.set_status(
                    "Patient updated successfully",
                    GREEN
                )

                messagebox.showinfo(
                    "Patient Updated",
                    "Patient record updated successfully."
                )

            except Exception as error:

                messagebox.showerror(
                    "Edit Patient Error",
                    f"Unable to update patient.\n\n"
                    f"{type(error).__name__}: {error}"
                )

        window.buttons(body, save)

    def delete_record(self, row_id):

        self.service.delete_patient(
            int(row_id)
        )


# ============================================================
# DOCTORS
# ============================================================

class DoctorsPage(DataPage):

    def __init__(self, parent, app):

        self.service = DoctorService()

        columns = (
            ("id", "ID", 60),
            ("first_name", "First Name", 130),
            ("last_name", "Last Name", 130),
            ("specialization", "Specialization", 180),
            ("phone", "Phone", 120),
            ("email", "Email", 200),
        )

        super().__init__(
            parent,
            app,
            "Doctors",
            "Doctor registration and professional information",
            columns
        )

    def get_rows(self):
        return self.service.get_all_doctors()

    def row_values(self, doctor):

        return (
            get_value(doctor, "doctor_id", "id"),
            get_value(doctor, "first_name"),
            get_value(doctor, "last_name"),
            get_value(doctor, "specialization"),
            get_value(doctor, "phone"),
            get_value(doctor, "email")
        )

    def add_record(self):

        window = FormWindow(
            self,
            "Add Doctor",
            560,
            520
        )

        window.header(
            "Add New Doctor",
            "Enter doctor information"
        )

        body = window.body()

        first = tk.StringVar()
        last = tk.StringVar()
        specialization = tk.StringVar()
        phone = tk.StringVar()
        email = tk.StringVar()

        window.field(body, "First Name *", first)
        window.field(body, "Last Name *", last)
        window.field(body, "Specialization", specialization)
        window.field(body, "Phone", phone)
        window.field(body, "Email", email)

        def save():

            try:

                if not first.get().strip():
                    raise ValueError("First name is required.")

                if not last.get().strip():
                    raise ValueError("Last name is required.")

                self.service.add_doctor(
                    first.get().strip(),
                    last.get().strip(),
                    specialization.get().strip(),
                    phone.get().strip(),
                    email.get().strip()
                )

                window.destroy()
                self.refresh()

                self.app.set_status(
                    "Doctor added successfully",
                    GREEN
                )

                messagebox.showinfo(
                    "Doctor Added",
                    "Doctor record added successfully."
                )

            except Exception as error:

                messagebox.showerror(
                    "Add Doctor Error",
                    f"Unable to add doctor.\n\n"
                    f"{type(error).__name__}: {error}"
                )

        window.buttons(body, save)

    def edit_record(self, row_id):

        try:

            doctor = self.service.get_doctor(
                int(row_id)
            )

            if not doctor:
                raise ValueError(
                    "Doctor record could not be found."
                )

        except Exception as error:

            messagebox.showerror(
                "Edit Doctor",
                f"Unable to load doctor.\n\n"
                f"{type(error).__name__}: {error}"
            )

            return

        window = FormWindow(
            self,
            "Edit Doctor",
            560,
            520
        )

        window.header(
            "Edit Doctor",
            f"Doctor ID: {row_id}"
        )

        body = window.body()

        first = tk.StringVar(
            value=safe_text(
                get_value(doctor, "first_name")
            )
        )

        last = tk.StringVar(
            value=safe_text(
                get_value(doctor, "last_name")
            )
        )

        specialization = tk.StringVar(
            value=safe_text(
                get_value(doctor, "specialization")
            )
        )

        phone = tk.StringVar(
            value=safe_text(
                get_value(doctor, "phone")
            )
        )

        email = tk.StringVar(
            value=safe_text(
                get_value(doctor, "email")
            )
        )

        window.field(body, "First Name *", first)
        window.field(body, "Last Name *", last)
        window.field(body, "Specialization", specialization)
        window.field(body, "Phone", phone)
        window.field(body, "Email", email)

        def save():

            try:

                if not first.get().strip():
                    raise ValueError("First name is required.")

                if not last.get().strip():
                    raise ValueError("Last name is required.")

                self.service.update_doctor(
                    int(row_id),
                    first.get().strip(),
                    last.get().strip(),
                    specialization.get().strip(),
                    phone.get().strip(),
                    email.get().strip()
                )

                window.destroy()
                self.refresh()

                self.app.set_status(
                    "Doctor updated successfully",
                    GREEN
                )

                messagebox.showinfo(
                    "Doctor Updated",
                    "Doctor record updated successfully."
                )

            except Exception as error:

                messagebox.showerror(
                    "Edit Doctor Error",
                    f"Unable to update doctor.\n\n"
                    f"{type(error).__name__}: {error}"
                )

        window.buttons(body, save)

    def delete_record(self, row_id):

        self.service.delete_doctor(
            int(row_id)
        )


# ============================================================
# APPOINTMENTS
# ============================================================

class AppointmentsPage(DataPage):

    def __init__(self, parent, app):

        self.service = AppointmentService()
        self.patient_service = PatientService()
        self.doctor_service = DoctorService()

        columns = (
            ("id", "ID", 60),
            ("patient", "Patient", 180),
            ("doctor", "Doctor", 180),
            ("date", "Date", 110),
            ("time", "Time", 90),
            ("reason", "Reason", 200),
            ("status", "Status", 110),
        )

        super().__init__(
            parent,
            app,
            "Appointments",
            "Schedule and manage hospital appointments",
            columns
        )

    def get_rows(self):
        return self.service.get_all_appointments()

    def row_values(self, row):

        patient_name = get_value(
            row,
            "patient_name"
        )

        if not patient_name:

            first = get_value(
                row,
                "patient_first_name"
            )

            last = get_value(
                row,
                "patient_last_name"
            )

            patient_name = f"{first} {last}".strip()

        if not patient_name:

            patient_name = (
                f"Patient #{get_value(row, 'patient_id')}"
            )

        doctor_name = get_value(
            row,
            "doctor_name"
        )

        if not doctor_name:

            first = get_value(
                row,
                "doctor_first_name"
            )

            last = get_value(
                row,
                "doctor_last_name"
            )

            doctor_name = f"Dr. {first} {last}".strip()

        if doctor_name == "Dr.":

            doctor_name = (
                f"Doctor #{get_value(row, 'doctor_id')}"
            )

        return (
            get_value(row, "appointment_id", "id"),
            patient_name,
            doctor_name,
            get_value(row, "appointment_date", "date"),
            get_value(row, "appointment_time", "time"),
            get_value(row, "reason"),
            get_value(row, "status", default="Scheduled")
        )

    def get_patient_choices(self):

        patients = list(
            self.patient_service.get_all_patients()
        )

        choices = []

        for patient in patients:

            patient_id = get_value(
                patient,
                "patient_id",
                "id"
            )

            first = get_value(
                patient,
                "first_name"
            )

            last = get_value(
                patient,
                "last_name"
            )

            name = f"{first} {last}".strip()

            choices.append(
                f"{patient_id} - {name}"
            )

        return choices

    def get_doctor_choices(self):

        doctors = list(
            self.doctor_service.get_all_doctors()
        )

        choices = []

        for doctor in doctors:

            doctor_id = get_value(
                doctor,
                "doctor_id",
                "id"
            )

            first = get_value(
                doctor,
                "first_name"
            )

            last = get_value(
                doctor,
                "last_name"
            )

            name = f"Dr. {first} {last}".strip()

            choices.append(
                f"{doctor_id} - {name}"
            )

        return choices

    @staticmethod
    def extract_choice_id(value):

        try:
            return int(
                str(value).split("-", 1)[0].strip()
            )
        except (ValueError, IndexError):
            raise ValueError(
                "Please select a valid patient or doctor."
            )

    def add_record(self):

        try:

            patient_choices = self.get_patient_choices()
            doctor_choices = self.get_doctor_choices()

        except Exception as error:

            messagebox.showerror(
                "Appointment",
                f"Unable to load patients/doctors.\n\n"
                f"{type(error).__name__}: {error}"
            )

            return

        if not patient_choices:

            messagebox.showwarning(
                "Appointment",
                "You must add at least one patient before creating an appointment."
            )

            return

        if not doctor_choices:

            messagebox.showwarning(
                "Appointment",
                "You must add at least one doctor before creating an appointment."
            )

            return

        window = FormWindow(
            self,
            "Add Appointment",
            570,
            620
        )

        window.header(
            "Add New Appointment",
            "Schedule a patient with a doctor"
        )

        body = window.body()

        patient = tk.StringVar()
        doctor = tk.StringVar()
        date = tk.StringVar(
            value=datetime.now().strftime("%Y-%m-%d")
        )
        time = tk.StringVar()
        reason = tk.StringVar()
        status = tk.StringVar(
            value="Scheduled"
        )

        window.combo(
            body,
            "Patient *",
            patient,
            patient_choices
        )

        window.combo(
            body,
            "Doctor *",
            doctor,
            doctor_choices
        )

        window.field(
            body,
            "Appointment Date (YYYY-MM-DD) *",
            date
        )

        window.field(
            body,
            "Appointment Time (HH:MM)",
            time
        )

        window.field(
            body,
            "Reason",
            reason
        )

        window.combo(
            body,
            "Status",
            status,
            ["Scheduled", "Completed", "Cancelled"]
        )

        def save():

            try:

                patient_id = self.extract_choice_id(
                    patient.get()
                )

                doctor_id = self.extract_choice_id(
                    doctor.get()
                )

                if not date.get().strip():
                    raise ValueError(
                        "Appointment date is required."
                    )

                self.service.add_appointment(
                    patient_id,
                    doctor_id,
                    date.get().strip(),
                    time.get().strip(),
                    reason.get().strip(),
                    status.get().strip()
                )

                window.destroy()
                self.refresh()

                self.app.set_status(
                    "Appointment added successfully",
                    GREEN
                )

                messagebox.showinfo(
                    "Appointment Added",
                    "Appointment added successfully."
                )

            except Exception as error:

                messagebox.showerror(
                    "Add Appointment Error",
                    f"Unable to add appointment.\n\n"
                    f"{type(error).__name__}: {error}"
                )

        window.buttons(body, save)

    def edit_record(self, row_id):

        try:

            appointment = self.service.get_appointment(
                int(row_id)
            )

            if not appointment:
                raise ValueError(
                    "Appointment record could not be found."
                )

            patient_choices = self.get_patient_choices()
            doctor_choices = self.get_doctor_choices()

        except Exception as error:

            messagebox.showerror(
                "Edit Appointment",
                f"Unable to load appointment.\n\n"
                f"{type(error).__name__}: {error}"
            )

            return

        window = FormWindow(
            self,
            "Edit Appointment",
            570,
            620
        )

        window.header(
            "Edit Appointment",
            f"Appointment ID: {row_id}"
        )

        body = window.body()

        patient_id = get_value(
            appointment,
            "patient_id"
        )

        doctor_id = get_value(
            appointment,
            "doctor_id"
        )

        patient_value = ""

        for choice in patient_choices:

            if str(choice).split("-", 1)[0].strip() == str(patient_id):
                patient_value = choice
                break

        doctor_value = ""

        for choice in doctor_choices:

            if str(choice).split("-", 1)[0].strip() == str(doctor_id):
                doctor_value = choice
                break

        patient = tk.StringVar(
            value=patient_value
        )

        doctor = tk.StringVar(
            value=doctor_value
        )

        date = tk.StringVar(
            value=safe_text(
                get_value(
                    appointment,
                    "appointment_date"
                )
            )[:10]
        )

        time = tk.StringVar(
            value=safe_text(
                get_value(
                    appointment,
                    "appointment_time"
                )
            )
        )

        reason = tk.StringVar(
            value=safe_text(
                get_value(
                    appointment,
                    "reason"
                )
            )
        )

        status = tk.StringVar(
            value=safe_text(
                get_value(
                    appointment,
                    "status",
                    default="Scheduled"
                )
            )
        )

        window.combo(
            body,
            "Patient *",
            patient,
            patient_choices
        )

        window.combo(
            body,
            "Doctor *",
            doctor,
            doctor_choices
        )

        window.field(
            body,
            "Appointment Date (YYYY-MM-DD) *",
            date
        )

        window.field(
            body,
            "Appointment Time (HH:MM)",
            time
        )

        window.field(
            body,
            "Reason",
            reason
        )

        window.combo(
            body,
            "Status",
            status,
            ["Scheduled", "Completed", "Cancelled"]
        )

        def save():

            try:

                new_patient_id = self.extract_choice_id(
                    patient.get()
                )

                new_doctor_id = self.extract_choice_id(
                    doctor.get()
                )

                self.service.update_appointment(
                    int(row_id),
                    new_patient_id,
                    new_doctor_id,
                    date.get().strip(),
                    time.get().strip(),
                    reason.get().strip(),
                    status.get().strip()
                )

                window.destroy()
                self.refresh()

                self.app.set_status(
                    "Appointment updated successfully",
                    GREEN
                )

                messagebox.showinfo(
                    "Appointment Updated",
                    "Appointment updated successfully."
                )

            except Exception as error:

                messagebox.showerror(
                    "Edit Appointment Error",
                    f"Unable to update appointment.\n\n"
                    f"{type(error).__name__}: {error}"
                )

        window.buttons(body, save)

    def delete_record(self, row_id):

        self.service.delete_appointment(
            int(row_id)
        )


# ============================================================
# MEDICAL RECORDS
# ============================================================

class MedicalRecordsPage(DataPage):

    def __init__(self, parent, app):

        self.service = MedicalRecordService()
        self.patient_service = PatientService()
        self.doctor_service = DoctorService()
        self.appointment_service = AppointmentService()

        columns = (
            ("id", "ID", 60),
            ("patient", "Patient", 180),
            ("doctor", "Doctor", 180),
            ("diagnosis", "Diagnosis", 180),
            ("treatment", "Treatment", 180),
            ("notes", "Notes", 220),
            ("created", "Created At", 150),
        )

        super().__init__(
            parent,
            app,
            "Medical Records",
            "Patient diagnoses, treatments and clinical records",
            columns
        )

    def get_rows(self):
        return self.service.get_all_medical_records()

    def row_values(self, row):

        patient_name = get_value(
            row,
            "patient_name"
        )

        if not patient_name:

            patient_name = (
                f"{get_value(row, 'patient_first_name')} "
                f"{get_value(row, 'patient_last_name')}"
            ).strip()

        if not patient_name:

            patient_name = (
                f"Patient #{get_value(row, 'patient_id')}"
            )

        doctor_name = get_value(
            row,
            "doctor_name"
        )

        if not doctor_name:

            doctor_name = (
                f"Dr. {get_value(row, 'doctor_first_name')} "
                f"{get_value(row, 'doctor_last_name')}"
            ).strip()

        if doctor_name == "Dr.":

            doctor_name = (
                f"Doctor #{get_value(row, 'doctor_id')}"
            )

        return (
            get_value(row, "record_id", "id"),
            patient_name,
            doctor_name,
            get_value(row, "diagnosis"),
            get_value(row, "treatment"),
            get_value(row, "notes"),
            get_value(row, "created_at")
        )

    def patient_choices(self):

        patients = list(
            self.patient_service.get_all_patients()
        )

        choices = []

        for patient in patients:

            patient_id = get_value(
                patient,
                "patient_id",
                "id"
            )

            name = (
                f"{get_value(patient, 'first_name')} "
                f"{get_value(patient, 'last_name')}"
            ).strip()

            choices.append(
                f"{patient_id} - {name}"
            )

        return choices

    def doctor_choices(self):

        doctors = list(
            self.doctor_service.get_all_doctors()
        )

        choices = []

        for doctor in doctors:

            doctor_id = get_value(
                doctor,
                "doctor_id",
                "id"
            )

            name = (
                f"Dr. {get_value(doctor, 'first_name')} "
                f"{get_value(doctor, 'last_name')}"
            ).strip()

            choices.append(
                f"{doctor_id} - {name}"
            )

        return choices

    def appointment_choices(self):

        appointments = list(
            self.appointment_service.get_all_appointments()
        )

        choices = [
            "None"
        ]

        for appointment in appointments:

            appointment_id = get_value(
                appointment,
                "appointment_id",
                "id"
            )

            date = safe_text(
                get_value(
                    appointment,
                    "appointment_date"
                )
            )[:10]

            choices.append(
                f"{appointment_id} - {date}"
            )

        return choices

    @staticmethod
    def extract_id(value, allow_none=False):

        if allow_none and (
            not value or value == "None"
        ):
            return None

        try:
            return int(
                str(value).split("-", 1)[0].strip()
            )

        except (ValueError, IndexError):

            raise ValueError(
                "Please select a valid record."
            )

    def add_record(self):

        try:

            patients = self.patient_choices()
            doctors = self.doctor_choices()
            appointments = self.appointment_choices()

        except Exception as error:

            messagebox.showerror(
                "Medical Record",
                f"Unable to load related records.\n\n"
                f"{type(error).__name__}: {error}"
            )

            return

        if not patients:

            messagebox.showwarning(
                "Medical Record",
                "Please add a patient first."
            )

            return

        if not doctors:

            messagebox.showwarning(
                "Medical Record",
                "Please add a doctor first."
            )

            return

        window = FormWindow(
            self,
            "Add Medical Record",
            600,
            650
        )

        window.header(
            "Add Medical Record",
            "Enter patient clinical information"
        )

        body = window.body()

        patient = tk.StringVar()
        doctor = tk.StringVar()
        appointment = tk.StringVar(
            value="None"
        )
        diagnosis = tk.StringVar()
        treatment = tk.StringVar()
        notes = tk.StringVar()

        window.combo(
            body,
            "Patient *",
            patient,
            patients
        )

        window.combo(
            body,
            "Doctor *",
            doctor,
            doctors
        )

        window.combo(
            body,
            "Appointment",
            appointment,
            appointments
        )

        window.field(
            body,
            "Diagnosis",
            diagnosis
        )

        window.field(
            body,
            "Treatment",
            treatment
        )

        window.field(
            body,
            "Notes / Prescription",
            notes
        )

        def save():

            try:

                patient_id = self.extract_id(
                    patient.get()
                )

                doctor_id = self.extract_id(
                    doctor.get()
                )

                appointment_id = self.extract_id(
                    appointment.get(),
                    allow_none=True
                )

                self.service.add_medical_record(
                    patient_id,
                    doctor_id,
                    appointment_id,
                    diagnosis.get().strip(),
                    treatment.get().strip(),
                    notes.get().strip()
                )

                window.destroy()
                self.refresh()

                self.app.set_status(
                    "Medical record added successfully",
                    GREEN
                )

                messagebox.showinfo(
                    "Medical Record Added",
                    "Medical record added successfully."
                )

            except Exception as error:

                messagebox.showerror(
                    "Add Medical Record Error",
                    f"Unable to add medical record.\n\n"
                    f"{type(error).__name__}: {error}"
                )

        window.buttons(body, save)

    def edit_record(self, row_id):

        try:

            record = self.service.get_medical_record(
                int(row_id)
            )

            if not record:
                raise ValueError(
                    "Medical record could not be found."
                )

            patients = self.patient_choices()
            doctors = self.doctor_choices()
            appointments = self.appointment_choices()

        except Exception as error:

            messagebox.showerror(
                "Edit Medical Record",
                f"Unable to load medical record.\n\n"
                f"{type(error).__name__}: {error}"
            )

            return

        patient_id = get_value(
            record,
            "patient_id"
        )

        doctor_id = get_value(
            record,
            "doctor_id"
        )

        appointment_id = get_value(
            record,
            "appointment_id"
        )

        patient_value = ""

        for choice in patients:

            if str(choice).split("-", 1)[0].strip() == str(patient_id):
                patient_value = choice
                break

        doctor_value = ""

        for choice in doctors:

            if str(choice).split("-", 1)[0].strip() == str(doctor_id):
                doctor_value = choice
                break

        appointment_value = "None"

        if appointment_id:

            for choice in appointments:

                if str(choice).split("-", 1)[0].strip() == str(appointment_id):
                    appointment_value = choice
                    break

        window = FormWindow(
            self,
            "Edit Medical Record",
            600,
            650
        )

        window.header(
            "Edit Medical Record",
            f"Record ID: {row_id}"
        )

        body = window.body()

        patient = tk.StringVar(
            value=patient_value
        )

        doctor = tk.StringVar(
            value=doctor_value
        )

        appointment = tk.StringVar(
            value=appointment_value
        )

        diagnosis = tk.StringVar(
            value=safe_text(
                get_value(record, "diagnosis")
            )
        )

        treatment = tk.StringVar(
            value=safe_text(
                get_value(record, "treatment")
            )
        )

        notes = tk.StringVar(
            value=safe_text(
                get_value(record, "notes", "prescription")
            )
        )

        window.combo(
            body,
            "Patient *",
            patient,
            patients
        )

        window.combo(
            body,
            "Doctor *",
            doctor,
            doctors
        )

        window.combo(
            body,
            "Appointment",
            appointment,
            appointments
        )

        window.field(
            body,
            "Diagnosis",
            diagnosis
        )

        window.field(
            body,
            "Treatment",
            treatment
        )

        window.field(
            body,
            "Notes / Prescription",
            notes
        )

        def save():

            try:

                new_patient_id = self.extract_id(
                    patient.get()
                )

                new_doctor_id = self.extract_id(
                    doctor.get()
                )

                new_appointment_id = self.extract_id(
                    appointment.get(),
                    allow_none=True
                )

                self.service.update_medical_record(
                    int(row_id),
                    new_patient_id,
                    new_doctor_id,
                    new_appointment_id,
                    diagnosis.get().strip(),
                    treatment.get().strip(),
                    notes.get().strip()
                )

                window.destroy()
                self.refresh()

                self.app.set_status(
                    "Medical record updated successfully",
                    GREEN
                )

                messagebox.showinfo(
                    "Medical Record Updated",
                    "Medical record updated successfully."
                )

            except Exception as error:

                messagebox.showerror(
                    "Edit Medical Record Error",
                    f"Unable to update medical record.\n\n"
                    f"{type(error).__name__}: {error}"
                )

        window.buttons(body, save)

    def delete_record(self, row_id):

        self.service.delete_medical_record(
            int(row_id)
        )


# ============================================================
# BILLING
# ============================================================

class BillingPage(DataPage):

    def __init__(self, parent, app):

        self.service = BillingService()
        self.patient_service = PatientService()
        self.appointment_service = AppointmentService()

        columns = (
            ("id", "Bill ID", 70),
            ("patient", "Patient", 180),
            ("appointment", "Appointment", 100),
            ("amount", "Amount", 120),
            ("description", "Description", 220),
            ("status", "Status", 100),
            ("payment_date", "Payment Date", 130),
        )

        super().__init__(
            parent,
            app,
            "Billing",
            "Hospital billing and payments • PNG Kina",
            columns
        )

    def get_rows(self):
        return self.service.get_all_bills()

    def row_values(self, row):

        patient_name = get_value(
            row,
            "patient_name"
        )

        if not patient_name:

            patient_name = (
                f"{get_value(row, 'patient_first_name')} "
                f"{get_value(row, 'patient_last_name')}"
            ).strip()

        if not patient_name:

            patient_name = (
                f"Patient #{get_value(row, 'patient_id')}"
            )

        amount = get_value(
            row,
            "amount",
            "total",
            "total_amount",
            "bill_amount",
            default=0
        )

        return (
            get_value(row, "bill_id", "id"),
            patient_name,
            get_value(row, "appointment_id"),
            money(amount),
            get_value(row, "description"),
            get_value(row, "status"),
            get_value(row, "payment_date", default="Not paid")
        )

    def patient_choices(self):

        patients = list(
            self.patient_service.get_all_patients()
        )

        choices = []

        for patient in patients:

            patient_id = get_value(
                patient,
                "patient_id",
                "id"
            )

            name = (
                f"{get_value(patient, 'first_name')} "
                f"{get_value(patient, 'last_name')}"
            ).strip()

            choices.append(
                f"{patient_id} - {name}"
            )

        return choices

    def appointment_choices(self):

        appointments = list(
            self.appointment_service.get_all_appointments()
        )

        choices = [
            "None"
        ]

        for appointment in appointments:

            appointment_id = get_value(
                appointment,
                "appointment_id",
                "id"
            )

            date = safe_text(
                get_value(
                    appointment,
                    "appointment_date"
                )
            )[:10]

            choices.append(
                f"{appointment_id} - {date}"
            )

        return choices

    @staticmethod
    def extract_id(value, allow_none=False):

        if allow_none and (
            not value or value == "None"
        ):
            return None

        try:
            return int(
                str(value).split("-", 1)[0].strip()
            )

        except (ValueError, IndexError):

            raise ValueError(
                "Please select a valid record."
            )

    def add_record(self):

        try:

            patients = self.patient_choices()
            appointments = self.appointment_choices()

        except Exception as error:

            messagebox.showerror(
                "Billing",
                f"Unable to load related records.\n\n"
                f"{type(error).__name__}: {error}"
            )

            return

        if not patients:

            messagebox.showwarning(
                "Billing",
                "Please add a patient before creating a bill."
            )

            return

        window = FormWindow(
            self,
            "Add Bill",
            570,
            570
        )

        window.header(
            "Add New Bill",
            "Create a hospital billing record"
        )

        body = window.body()

        patient = tk.StringVar()
        appointment = tk.StringVar(
            value="None"
        )
        amount = tk.StringVar()
        description = tk.StringVar()
        status = tk.StringVar(
            value="Unpaid"
        )

        window.combo(
            body,
            "Patient *",
            patient,
            patients
        )

        window.combo(
            body,
            "Appointment",
            appointment,
            appointments
        )

        window.field(
            body,
            "Amount (PNG Kina) *",
            amount
        )

        window.field(
            body,
            "Description",
            description
        )

        window.combo(
            body,
            "Payment Status",
            status,
            ["Unpaid", "Paid", "Cancelled"]
        )

        def save():

            try:

                patient_id = self.extract_id(
                    patient.get()
                )

                appointment_id = self.extract_id(
                    appointment.get(),
                    allow_none=True
                )

                if not amount.get().strip():
                    raise ValueError(
                        "Amount is required."
                    )

                amount_value = float(
                    amount.get().strip()
                )

                if amount_value < 0:
                    raise ValueError(
                        "Amount cannot be negative."
                    )

                self.service.add_bill(
                    patient_id,
                    appointment_id,
                    amount_value,
                    description.get().strip(),
                    status.get().strip()
                )

                window.destroy()
                self.refresh()

                self.app.set_status(
                    "Bill added successfully",
                    GREEN
                )

                messagebox.showinfo(
                    "Bill Added",
                    "Billing record added successfully."
                )

            except Exception as error:

                messagebox.showerror(
                    "Add Bill Error",
                    f"Unable to add bill.\n\n"
                    f"{type(error).__name__}: {error}"
                )

        window.buttons(body, save)

    def edit_record(self, row_id):

        try:

            bill = self.service.get_bill(
                int(row_id)
            )

            if not bill:
                raise ValueError(
                    "Bill could not be found."
                )

            patients = self.patient_choices()
            appointments = self.appointment_choices()

        except Exception as error:

            messagebox.showerror(
                "Edit Bill",
                f"Unable to load bill.\n\n"
                f"{type(error).__name__}: {error}"
            )

            return

        patient_id = get_value(
            bill,
            "patient_id"
        )

        appointment_id = get_value(
            bill,
            "appointment_id"
        )

        patient_value = ""

        for choice in patients:

            if str(choice).split("-", 1)[0].strip() == str(patient_id):
                patient_value = choice
                break

        appointment_value = "None"

        if appointment_id:

            for choice in appointments:

                if str(choice).split("-", 1)[0].strip() == str(appointment_id):
                    appointment_value = choice
                    break

        window = FormWindow(
            self,
            "Edit Bill",
            570,
            570
        )

        window.header(
            "Edit Bill",
            f"Bill ID: {row_id}"
        )

        body = window.body()

        patient = tk.StringVar(
            value=patient_value
        )

        appointment = tk.StringVar(
            value=appointment_value
        )

        amount = tk.StringVar(
            value=safe_text(
                get_value(bill, "amount")
            )
        )

        description = tk.StringVar(
            value=safe_text(
                get_value(bill, "description")
            )
        )

        status = tk.StringVar(
            value=safe_text(
                get_value(
                    bill,
                    "status",
                    default="Unpaid"
                )
            )
        )

        window.combo(
            body,
            "Patient *",
            patient,
            patients
        )

        window.combo(
            body,
            "Appointment",
            appointment,
            appointments
        )

        window.field(
            body,
            "Amount (PNG Kina) *",
            amount
        )

        window.field(
            body,
            "Description",
            description
        )

        window.combo(
            body,
            "Payment Status",
            status,
            ["Unpaid", "Paid", "Cancelled"]
        )

        def save():

            try:

                new_patient_id = self.extract_id(
                    patient.get()
                )

                new_appointment_id = self.extract_id(
                    appointment.get(),
                    allow_none=True
                )

                amount_value = float(
                    amount.get().strip()
                )

                if amount_value < 0:
                    raise ValueError(
                        "Amount cannot be negative."
                    )

                self.service.update_bill(
                    int(row_id),
                    new_patient_id,
                    new_appointment_id,
                    amount_value,
                    description.get().strip(),
                    status.get().strip()
                )

                window.destroy()
                self.refresh()

                self.app.set_status(
                    "Bill updated successfully",
                    GREEN
                )

                messagebox.showinfo(
                    "Bill Updated",
                    "Billing record updated successfully."
                )

            except Exception as error:

                messagebox.showerror(
                    "Edit Bill Error",
                    f"Unable to update bill.\n\n"
                    f"{type(error).__name__}: {error}"
                )

        window.buttons(body, save)

    def delete_record(self, row_id):

        self.service.delete_bill(
            int(row_id)
        )


# ============================================================
# ADMINISTRATORS
# ============================================================

class AdministratorsPage(DataPage):

    def __init__(self, parent, app):

        self.service = AdministratorService()

        columns = (
            ("id", "Admin ID", 80),
            ("full_name", "Full Name", 220),
            ("email", "Email", 250),
            ("phone", "Phone", 150),
        )

        super().__init__(
            parent,
            app,
            "Administrators",
            "Hospital system administrator information",
            columns
        )

    def get_rows(self):
        return self.service.get_all_administrators()

    def row_values(self, row):

        return (
            get_value(row, "admin_id", "id"),
            get_value(row, "full_name"),
            get_value(row, "email"),
            get_value(row, "phone")
        )

    def add_record(self):

        window = FormWindow(
            self,
            "Add Administrator",
            560,
            470
        )

        window.header(
            "Add Administrator",
            "Enter administrator information"
        )

        body = window.body()

        full_name = tk.StringVar()
        email = tk.StringVar()
        phone = tk.StringVar()

        window.field(
            body,
            "Full Name *",
            full_name
        )

        window.field(
            body,
            "Email",
            email
        )

        window.field(
            body,
            "Phone",
            phone
        )

        def save():

            try:

                if not full_name.get().strip():
                    raise ValueError(
                        "Full name is required."
                    )

                self.service.add_administrator(
                    full_name.get().strip(),
                    email.get().strip(),
                    phone.get().strip()
                )

                window.destroy()
                self.refresh()

                self.app.set_status(
                    "Administrator added successfully",
                    GREEN
                )

                messagebox.showinfo(
                    "Administrator Added",
                    "Administrator record added successfully."
                )

            except Exception as error:

                messagebox.showerror(
                    "Add Administrator Error",
                    f"Unable to add administrator.\n\n"
                    f"{type(error).__name__}: {error}"
                )

        window.buttons(body, save)

    def edit_record(self, row_id):

        try:

            admin = self.service.get_administrator(
                int(row_id)
            )

            if not admin:
                raise ValueError(
                    "Administrator record could not be found."
                )

        except Exception as error:

            messagebox.showerror(
                "Edit Administrator",
                f"Unable to load administrator.\n\n"
                f"{type(error).__name__}: {error}"
            )

            return

        window = FormWindow(
            self,
            "Edit Administrator",
            560,
            470
        )

        window.header(
            "Edit Administrator",
            f"Administrator ID: {row_id}"
        )

        body = window.body()

        full_name = tk.StringVar(
            value=safe_text(
                get_value(admin, "full_name")
            )
        )

        email = tk.StringVar(
            value=safe_text(
                get_value(admin, "email")
            )
        )

        phone = tk.StringVar(
            value=safe_text(
                get_value(admin, "phone")
            )
        )

        window.field(
            body,
            "Full Name *",
            full_name
        )

        window.field(
            body,
            "Email",
            email
        )

        window.field(
            body,
            "Phone",
            phone
        )

        def save():

            try:

                if not full_name.get().strip():
                    raise ValueError(
                        "Full name is required."
                    )

                self.service.update_administrator(
                    int(row_id),
                    full_name.get().strip(),
                    email.get().strip(),
                    phone.get().strip()
                )

                window.destroy()
                self.refresh()

                self.app.set_status(
                    "Administrator updated successfully",
                    GREEN
                )

                messagebox.showinfo(
                    "Administrator Updated",
                    "Administrator record updated successfully."
                )

            except Exception as error:

                messagebox.showerror(
                    "Edit Administrator Error",
                    f"Unable to update administrator.\n\n"
                    f"{type(error).__name__}: {error}"
                )

        window.buttons(body, save)

    def delete_record(self, row_id):

        self.service.delete_administrator(
            int(row_id)
        )


# ============================================================
# DASHBOARD
# ============================================================

class DashboardPage(BasePage):

    def __init__(self, parent, app):

        self.patient_service = PatientService()
        self.doctor_service = DoctorService()
        self.appointment_service = AppointmentService()
        self.record_service = MedicalRecordService()
        self.billing_service = BillingService()
        self.admin_service = AdministratorService()

        super().__init__(
            parent,
            app,
            "Dashboard",
            "Hospital Management System overview"
        )

        self.build_dashboard()

    def build_dashboard(self):

        welcome = tk.Frame(
            self,
            bg=NAVY,
            height=115
        )

        welcome.pack(
            fill="x",
            padx=25,
            pady=22
        )

        welcome.pack_propagate(False)

        tk.Label(
            welcome,
            text="Welcome to the Hospital Management System",
            font=(FONT, 20, "bold"),
            bg=NAVY,
            fg=WHITE
        ).pack(
            anchor="w",
            padx=25,
            pady=(23, 3)
        )

        tk.Label(
            welcome,
            text=(
                "Manage patients, doctors, appointments, "
                "medical records and billing efficiently."
            ),
            font=(FONT, 10),
            bg=NAVY,
            fg="#D9E7F2"
        ).pack(
            anchor="w",
            padx=25
        )

        self.date_label = tk.Label(
            welcome,
            text=datetime.now().strftime("%d %B %Y"),
            font=(FONT, 10, "bold"),
            bg=NAVY,
            fg=WHITE
        )

        self.date_label.place(
            relx=0.96,
            rely=0.35,
            anchor="e"
        )

        stats = tk.Frame(
            self,
            bg=BACKGROUND
        )

        stats.pack(
            fill="x",
            padx=20
        )

        self.patient_card = self.create_card(
            stats,
            "PATIENTS",
            "0",
            LIGHT_BLUE,
            0
        )

        self.doctor_card = self.create_card(
            stats,
            "DOCTORS",
            "0",
            LIGHT_GREEN,
            1
        )

        self.appointment_card = self.create_card(
            stats,
            "APPOINTMENTS",
            "0",
            LIGHT_ORANGE,
            2
        )

        self.record_card = self.create_card(
            stats,
            "MEDICAL RECORDS",
            "0",
            LIGHT_PURPLE,
            3
        )

        self.billing_card = self.create_card(
            stats,
            "TOTAL BILLING",
            "K 0.00",
            LIGHT_BLUE,
            4
        )

        self.admin_card = self.create_card(
            stats,
            "ADMINISTRATORS",
            "0",
            LIGHT_GREEN,
            5
        )

        info = tk.Frame(
            self,
            bg=BACKGROUND
        )

        info.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=22
        )

        appointment_box = tk.Frame(
            info,
            bg=WHITE,
            bd=1,
            relief="solid"
        )

        appointment_box.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        tk.Label(
            appointment_box,
            text="Today's Appointments",
            font=(FONT, 13, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 10)
        )

        appointment_table_frame = tk.Frame(
            appointment_box,
            bg=WHITE
        )

        appointment_table_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.appointment_tree = ttk.Treeview(
            appointment_table_frame,
            columns=(
                "time",
                "patient",
                "doctor",
                "status"
            ),
            show="headings",
            height=8
        )

        for column, heading, width in (
            ("time", "Time", 80),
            ("patient", "Patient", 150),
            ("doctor", "Doctor", 150),
            ("status", "Status", 100),
        ):

            self.appointment_tree.heading(
                column,
                text=heading
            )

            self.appointment_tree.column(
                column,
                width=width,
                minwidth=60
            )

        appointment_scroll = ttk.Scrollbar(
            appointment_table_frame,
            orient="vertical",
            command=self.appointment_tree.yview
        )

        self.appointment_tree.configure(
            yscrollcommand=appointment_scroll.set
        )

        self.appointment_tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        appointment_scroll.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        appointment_table_frame.rowconfigure(
            0,
            weight=1
        )

        appointment_table_frame.columnconfigure(
            0,
            weight=1
        )

        patient_box = tk.Frame(
            info,
            bg=WHITE,
            bd=1,
            relief="solid"
        )

        patient_box.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        tk.Label(
            patient_box,
            text="Recent Patients",
            font=(FONT, 13, "bold"),
            bg=WHITE,
            fg=NAVY
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 10)
        )

        patient_table_frame = tk.Frame(
            patient_box,
            bg=WHITE
        )

        patient_table_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        self.patient_tree = ttk.Treeview(
            patient_table_frame,
            columns=(
                "id",
                "name",
                "phone",
                "gender"
            ),
            show="headings",
            height=8
        )

        for column, heading, width in (
            ("id", "ID", 60),
            ("name", "Patient Name", 170),
            ("phone", "Phone", 130),
            ("gender", "Gender", 90),
        ):

            self.patient_tree.heading(
                column,
                text=heading
            )

            self.patient_tree.column(
                column,
                width=width,
                minwidth=50
            )

        patient_scroll = ttk.Scrollbar(
            patient_table_frame,
            orient="vertical",
            command=self.patient_tree.yview
        )

        self.patient_tree.configure(
            yscrollcommand=patient_scroll.set
        )

        self.patient_tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        patient_scroll.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        patient_table_frame.rowconfigure(
            0,
            weight=1
        )

        patient_table_frame.columnconfigure(
            0,
            weight=1
        )

        self.refresh()

    def create_card(
        self,
        parent,
        title,
        value,
        background,
        column
    ):

        card = tk.Frame(
            parent,
            bg=background,
            height=105,
            bd=1,
            relief="solid"
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=5
        )

        parent.columnconfigure(
            column,
            weight=1
        )

        card.grid_propagate(False)

        tk.Label(
            card,
            text=title,
            font=(FONT, 8, "bold"),
            bg=background,
            fg=MUTED
        ).pack(
            anchor="w",
            padx=15,
            pady=(14, 3)
        )

        label = tk.Label(
            card,
            text=value,
            font=(FONT, 21, "bold"),
            bg=background,
            fg=NAVY
        )

        label.pack(
            anchor="w",
            padx=15
        )

        return label

    def refresh(self):

        errors = []

        # ----------------------------------------------------
        # PATIENTS
        # ----------------------------------------------------

        try:

            patients = list(
                self.patient_service.get_all_patients()
            )

            self.patient_card.config(
                text=str(len(patients))
            )

            for item in self.patient_tree.get_children():
                self.patient_tree.delete(item)

            for patient in patients[-8:][::-1]:

                name = (
                    f"{get_value(patient, 'first_name')} "
                    f"{get_value(patient, 'last_name')}"
                ).strip()

                if not name:

                    name = (
                        f"Patient #{get_value(patient, 'patient_id', 'id')}"
                    )

                self.patient_tree.insert(
                    "",
                    "end",
                    values=(
                        get_value(
                            patient,
                            "patient_id",
                            "id"
                        ),
                        name,
                        get_value(patient, "phone"),
                        get_value(patient, "gender")
                    )
                )

        except Exception as error:

            self.patient_card.config(text="—")
            errors.append(f"Patients: {error}")

        # ----------------------------------------------------
        # DOCTORS
        # ----------------------------------------------------

        try:

            doctors = list(
                self.doctor_service.get_all_doctors()
            )

            self.doctor_card.config(
                text=str(len(doctors))
            )

        except Exception as error:

            self.doctor_card.config(text="—")
            errors.append(f"Doctors: {error}")

        # ----------------------------------------------------
        # APPOINTMENTS
        # ----------------------------------------------------

        try:

            appointments = list(
                self.appointment_service.get_all_appointments()
            )

            self.appointment_card.config(
                text=str(len(appointments))
            )

            for item in self.appointment_tree.get_children():
                self.appointment_tree.delete(item)

            today = datetime.now().strftime(
                "%Y-%m-%d"
            )

            for row in appointments:

                appointment_date = safe_text(
                    get_value(
                        row,
                        "appointment_date",
                        "date"
                    )
                )[:10]

                if appointment_date != today:
                    continue

                patient_name = get_value(
                    row,
                    "patient_name"
                )

                if not patient_name:

                    patient_name = (
                        f"{get_value(row, 'patient_first_name')} "
                        f"{get_value(row, 'patient_last_name')}"
                    ).strip()

                if not patient_name:

                    patient_name = (
                        f"Patient #{get_value(row, 'patient_id')}"
                    )

                doctor_name = get_value(
                    row,
                    "doctor_name"
                )

                if not doctor_name:

                    doctor_name = (
                        f"Dr. {get_value(row, 'doctor_first_name')} "
                        f"{get_value(row, 'doctor_last_name')}"
                    ).strip()

                if doctor_name == "Dr.":

                    doctor_name = (
                        f"Doctor #{get_value(row, 'doctor_id')}"
                    )

                self.appointment_tree.insert(
                    "",
                    "end",
                    values=(
                        get_value(
                            row,
                            "appointment_time",
                            "time"
                        ),
                        patient_name,
                        doctor_name,
                        get_value(
                            row,
                            "status",
                            default="Scheduled"
                        )
                    )
                )

        except Exception as error:

            self.appointment_card.config(text="—")
            errors.append(f"Appointments: {error}")

        # ----------------------------------------------------
        # MEDICAL RECORDS
        # ----------------------------------------------------

        try:

            records = list(
                self.record_service.get_all_medical_records()
            )

            self.record_card.config(
                text=str(len(records))
            )

        except Exception as error:

            self.record_card.config(text="—")
            errors.append(f"Medical Records: {error}")

        # ----------------------------------------------------
        # BILLING
        # ----------------------------------------------------

        try:

            bills = list(
                self.billing_service.get_all_bills()
            )

            total = 0.0

            for bill in bills:

                amount = get_value(
                    bill,
                    "amount",
                    "total",
                    "total_amount",
                    "bill_amount",
                    default=0
                )

                try:
                    total += float(amount)
                except (ValueError, TypeError):
                    pass

            self.billing_card.config(
                text=money(total)
            )

        except Exception as error:

            self.billing_card.config(text="—")
            errors.append(f"Billing: {error}")

        # ----------------------------------------------------
        # ADMINISTRATORS
        # ----------------------------------------------------

        try:

            administrators = list(
                self.admin_service.get_all_administrators()
            )

            self.admin_card.config(
                text=str(len(administrators))
            )

        except Exception as error:

            self.admin_card.config(text="—")
            errors.append(f"Administrators: {error}")

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        if errors:

            self.app.set_status(
                "Dashboard refreshed with some errors",
                ORANGE
            )

            print("\nDashboard errors:")

            for error in errors:
                print(f"  - {error}")

        else:

            self.app.set_status(
                "Dashboard refreshed successfully from MySQL",
                GREEN
            )


# ============================================================
# MAIN APPLICATION
# ============================================================

class HospitalApp(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title(APP_TITLE)

        self.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
        )

        self.minsize(
            1050,
            680
        )

        self.configure(
            bg=BACKGROUND
        )

        self.current_user = None
        self.pages = {}
        self.current_page = None

        self.setup_styles()

        self.show_login()

        self.protocol(
            "WM_DELETE_WINDOW",
            self.close_application
        )

    # ========================================================
    # STYLES
    # ========================================================

    def setup_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "TEntry",
            padding=8,
            font=(FONT, 10)
        )

        style.configure(
            "TCombobox",
            padding=7,
            font=(FONT, 10)
        )

        style.configure(
            "Treeview",
            font=(FONT, 9),
            rowheight=32,
            background=WHITE,
            fieldbackground=WHITE,
            foreground=TEXT
        )

        style.configure(
            "Treeview.Heading",
            font=(FONT, 9, "bold"),
            background=NAVY,
            foreground=WHITE,
            padding=8
        )

        style.configure(
            "Vertical.TScrollbar",
            width=14
        )

        style.configure(
            "Horizontal.TScrollbar",
            height=14
        )

        style.map(
            "Treeview",
            background=[
                ("selected", LIGHT_BLUE)
            ],
            foreground=[
                ("selected", NAVY)
            ]
        )

    # ========================================================
    # LOGIN
    # ========================================================

    def show_login(self):

        self.clear_window()

        self.current_user = None
        self.pages = {}
        self.current_page = None

        login_page = LoginPage(
            self,
            self
        )

        login_page.pack(
            fill="both",
            expand=True
        )

    def clear_window(self):

        for widget in self.winfo_children():
            widget.destroy()

    def login_successful(self, user):

        self.current_user = user

        self.build_interface()

        self.show_page("Dashboard")

        self.set_status(
            f"Signed in as {user['username']} ({user['role']})",
            GREEN
        )

    # ========================================================
    # MAIN INTERFACE
    # ========================================================

    def build_interface(self):

        self.clear_window()

        self.pages = {}
        self.current_page = None

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = tk.Frame(
            self,
            bg=NAVY,
            height=70
        )

        header.pack(
            side="top",
            fill="x"
        )

        header.pack_propagate(False)

        tk.Label(
            header,
            text="✚",
            font=(FONT, 27, "bold"),
            bg=NAVY,
            fg=WHITE
        ).pack(
            side="left",
            padx=(22, 10)
        )

        title_frame = tk.Frame(
            header,
            bg=NAVY
        )

        title_frame.pack(side="left")

        tk.Label(
            title_frame,
            text="HOSPITAL MANAGEMENT SYSTEM",
            font=(FONT, 14, "bold"),
            bg=NAVY,
            fg=WHITE
        ).pack(
            anchor="w",
            pady=(11, 0)
        )

        tk.Label(
            title_frame,
            text="Group 5 • Bachelor in Information Technology",
            font=(FONT, 8),
            bg=NAVY,
            fg="#D9E7F2"
        ).pack(anchor="w")

        tk.Button(
            header,
            text="↻  Refresh All",
            font=(FONT, 9, "bold"),
            bg=WHITE,
            fg=NAVY,
            activebackground=LIGHT_BLUE,
            activeforeground=NAVY,
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=6,
            command=self.refresh_all
        ).pack(
            side="right",
            padx=(10, 20)
        )

        user_frame = tk.Frame(
            header,
            bg=NAVY
        )

        user_frame.pack(
            side="right",
            padx=10
        )

        username = self.current_user.get(
            "username",
            "User"
        )

        role = self.current_user.get(
            "role",
            "Staff"
        )

        tk.Label(
            user_frame,
            text=username,
            font=(FONT, 10, "bold"),
            bg=NAVY,
            fg=WHITE
        ).pack(anchor="e")

        tk.Label(
            user_frame,
            text=role,
            font=(FONT, 8),
            bg=NAVY,
            fg="#D9E7F2"
        ).pack(anchor="e")

        # ----------------------------------------------------
        # BODY
        # ----------------------------------------------------

        body = tk.Frame(
            self,
            bg=BACKGROUND
        )

        body.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # SIDEBAR
        # ----------------------------------------------------

        sidebar = tk.Frame(
            body,
            bg=DARK_NAVY,
            width=235
        )

        sidebar.pack(
            side="left",
            fill="y"
        )

        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="MAIN MENU",
            font=(FONT, 8, "bold"),
            bg=DARK_NAVY,
            fg="#8FA9C1"
        ).pack(
            anchor="w",
            padx=23,
            pady=(25, 12)
        )

        menu = [
            ("⌂", "Dashboard"),
            ("♟", "Patients"),
            ("⚕", "Doctors"),
            ("▣", "Appointments"),
            ("▤", "Medical Records"),
            ("₭", "Billing"),
            ("♙", "Administrators"),
        ]

        self.nav_buttons = {}

        for icon, name in menu:

            button = tk.Button(
                sidebar,
                text=f"  {icon}    {name}",
                font=(FONT, 10, "bold"),
                bg=DARK_NAVY,
                fg="#D9E7F2",
                activebackground=NAVY,
                activeforeground=WHITE,
                relief="flat",
                bd=0,
                anchor="w",
                cursor="hand2",
                padx=15,
                pady=12,
                command=lambda page=name: self.show_page(page)
            )

            button.pack(
                fill="x",
                padx=10,
                pady=2
            )

            self.nav_buttons[name] = button

        # ----------------------------------------------------
        # LOGOUT
        # ----------------------------------------------------

        logout_frame = tk.Frame(
            sidebar,
            bg=DARK_NAVY
        )

        logout_frame.pack(
            side="bottom",
            fill="x",
            padx=10,
            pady=15
        )

        tk.Frame(
            logout_frame,
            bg="#29435F",
            height=1
        ).pack(
            fill="x",
            pady=(0, 12)
        )

        tk.Button(
            logout_frame,
            text="  ⎋    Logout",
            font=(FONT, 10, "bold"),
            bg=DARK_NAVY,
            fg="#F4B4B4",
            activebackground="#3A1F27",
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            anchor="w",
            cursor="hand2",
            padx=15,
            pady=11,
            command=self.logout
        ).pack(fill="x")

        # ----------------------------------------------------
        # CONTENT
        # ----------------------------------------------------

        content_area = tk.Frame(
            body,
            bg=BACKGROUND
        )

        content_area.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.content_canvas = tk.Canvas(
            content_area,
            bg=BACKGROUND,
            highlightthickness=0,
            bd=0
        )

        self.content_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.content_scrollbar = ttk.Scrollbar(
            content_area,
            orient="vertical",
            command=self.content_canvas.yview
        )

        self.content_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.content_canvas.configure(
            yscrollcommand=self.content_scrollbar.set
        )

        self.content = tk.Frame(
            self.content_canvas,
            bg=BACKGROUND
        )

        self.content_window = self.content_canvas.create_window(
            (0, 0),
            window=self.content,
            anchor="nw"
        )

        self.content.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.content_canvas.bind(
            "<Configure>",
            self.resize_content_width
        )

        self.content_canvas.bind(
            "<Enter>",
            self.enable_mousewheel
        )

        self.content_canvas.bind(
            "<Leave>",
            self.disable_mousewheel
        )

        # ----------------------------------------------------
        # STATUS BAR
        # ----------------------------------------------------

        status_bar = tk.Frame(
            self,
            bg=WHITE,
            height=30,
            bd=1,
            relief="solid"
        )

        status_bar.pack(
            side="bottom",
            fill="x"
        )

        status_bar.pack_propagate(False)

        self.status_label = tk.Label(
            status_bar,
            text="Ready",
            font=(FONT, 8),
            bg=WHITE,
            fg=MUTED
        )

        self.status_label.pack(
            side="left",
            padx=15
        )

        tk.Label(
            status_bar,
            text=(
                "Created by: Kimberly Saelon • Barbara • Rowen   |   "
                "Powered by Python & MySQL   |   "
                "PNG Kina (K)"
            ),
            font=(FONT, 8),
            bg=WHITE,
            fg=MUTED
        ).pack(
            side="right",
            padx=15
        )

        # ----------------------------------------------------
        # PAGES
        # ----------------------------------------------------

        self.pages["Dashboard"] = DashboardPage(
            self.content,
            self
        )

        self.pages["Patients"] = PatientsPage(
            self.content,
            self
        )

        self.pages["Doctors"] = DoctorsPage(
            self.content,
            self
        )

        self.pages["Appointments"] = AppointmentsPage(
            self.content,
            self
        )

        self.pages["Medical Records"] = MedicalRecordsPage(
            self.content,
            self
        )

        self.pages["Billing"] = BillingPage(
            self.content,
            self
        )

        self.pages["Administrators"] = AdministratorsPage(
            self.content,
            self
        )

    # ========================================================
    # SCROLLING
    # ========================================================

    def update_scroll_region(self, event=None):

        if hasattr(self, "content_canvas"):

            self.content_canvas.configure(
                scrollregion=self.content_canvas.bbox("all")
            )

    def resize_content_width(self, event):

        if hasattr(self, "content_canvas"):

            self.content_canvas.itemconfigure(
                self.content_window,
                width=event.width
            )

            self.after(
                10,
                self.update_scroll_region
            )

    def enable_mousewheel(self, event=None):

        if hasattr(self, "content_canvas"):

            self.content_canvas.bind_all(
                "<MouseWheel>",
                self.mousewheel
            )

    def disable_mousewheel(self, event=None):

        if hasattr(self, "content_canvas"):

            self.content_canvas.unbind_all(
                "<MouseWheel>"
            )

    def mousewheel(self, event):

        if hasattr(self, "content_canvas"):

            if event.delta:

                self.content_canvas.yview_scroll(
                    int(-1 * (event.delta / 120)),
                    "units"
                )

    # ========================================================
    # PAGE NAVIGATION
    # ========================================================

    def show_page(self, name):

        if name not in self.pages:
            return

        for page in self.pages.values():
            page.pack_forget()

        page = self.pages[name]

        page.pack(
            fill="both",
            expand=True
        )

        self.current_page = name

        for page_name, button in self.nav_buttons.items():

            if page_name == name:

                button.configure(
                    bg=NAVY,
                    fg=WHITE
                )

            else:

                button.configure(
                    bg=DARK_NAVY,
                    fg="#D9E7F2"
                )

        self.after(
            30,
            lambda: self.content_canvas.yview_moveto(0)
        )

        self.after(
            100,
            page.refresh
        )

    def refresh_current_page(self, event=None):

        if self.current_page in self.pages:

            self.pages[
                self.current_page
            ].refresh()

        self.after(
            50,
            self.update_scroll_region
        )

    def refresh_all(self):

        if not self.pages:
            return

        for name, page in self.pages.items():

            try:
                page.refresh()

            except Exception as error:

                print(
                    f"Refresh error in {name}: {error}"
                )

        self.after(
            100,
            self.update_scroll_region
        )

        self.set_status(
            "All hospital sections refreshed from MySQL",
            GREEN
        )

    # ========================================================
    # STATUS
    # ========================================================

    def set_status(
        self,
        message,
        colour=MUTED
    ):

        if hasattr(
            self,
            "status_label"
        ):

            self.status_label.configure(
                text=message,
                fg=colour
            )

    # ========================================================
    # LOGOUT
    # ========================================================

    def logout(self):

        answer = messagebox.askyesno(
            "Logout",
            "Are you sure you want to log out?"
        )

        if answer:
            self.show_login()

    # ========================================================
    # CLOSE
    # ========================================================

    def close_application(self):

        answer = messagebox.askyesno(
            "Exit",
            "Are you sure you want to close the Hospital Management System?"
        )

        if answer:
            self.destroy()


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    app = HospitalApp()

    app.bind(
        "<Control-r>",
        app.refresh_current_page
    )

    app.mainloop()