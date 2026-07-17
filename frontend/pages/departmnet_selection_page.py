import customtkinter as ctk
import requests
from tkinter import messagebox

# -------------------------
# COLORS
# -------------------------

BG          = ("#F0F4F8", "#0B1121")
SURFACE     = ("#FFFFFF", "#151E32")
BORDER      = ("#CBD5E1", "#334155")

PRIMARY     = ("#0D9488", "#14B8A6")
PRIMARY_H   = ("#0F766E", "#0D9488")

TEXT        = ("#0F172A", "#F8FAFC")
TEXT_SOFT   = ("#475569", "#94A3B8")

FONT_DISPLAY = "Segoe UI Semibold"
FONT_BODY    = "Segoe UI"


class DepartmentSelectionPage(ctk.CTkFrame):

    def __init__(self, parent, go_back, open_department_identification):
        super().__init__(parent, fg_color=BG)

        self.go_back = go_back
        self.open_department_identification = open_department_identification

        self.department_map = {}

        self.pack(fill="both", expand=True)

        self.build_header()
        self.build_ui()

        self.load_departments()

    def build_header(self):

        header = ctk.CTkFrame(
            self,
            fg_color=PRIMARY,
            height=45,
            corner_radius=0
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left", padx=20)

        ctk.CTkButton(
            left,
            text="← Back",
            width=70,
            fg_color="transparent",
            hover_color=PRIMARY_H,
            command=self.go_back
        ).pack(pady=8)

        ctk.CTkLabel(
            header,
            text="Department Check-In",
            font=(FONT_DISPLAY, 18),
            text_color="white"
        ).place(relx=0.5, rely=0.5, anchor="center")

    def build_ui(self):

        card = ctk.CTkFrame(
            self,
            width=650,
            height=350,
            corner_radius=20,
            fg_color=SURFACE
        )

        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text="Select Department",
            font=(FONT_DISPLAY, 28),
            text_color=TEXT
        ).pack(pady=(45, 20))

        self.department_dropdown = ctk.CTkComboBox(
            card,
            width=350,
            height=45,
            values=["Loading..."]
        )

        self.department_dropdown.pack(pady=20)

        ctk.CTkButton(
            card,
            text="Continue →",
            width=220,
            height=45,
            fg_color=PRIMARY,
            hover_color=PRIMARY_H,
            command=self.continue_clicked
        ).pack(pady=35)

    def load_departments(self):

        try:

            response = requests.get(
                "http://localhost:9090/departments",
                timeout=5
            )

            if response.status_code != 200:
                return

            departments = response.json()

            names = []

            self.department_map = {}

            for dept in departments:

                if dept["departmentStatus"] == "ACTIVE":

                    names.append(
                        dept["departmentName"]
                    )

                    self.department_map[
                        dept["departmentName"]
                    ] = dept["departmentId"]

            self.department_dropdown.configure(values=names)

            if len(names) > 0:
                self.department_dropdown.set(names[0])

        except Exception:

            messagebox.showerror(
                "Error",
                "Unable to load departments."
            )

    def continue_clicked(self):

        department_name = self.department_dropdown.get()

        department_id = self.department_map.get(
            department_name
        )

        self.open_department_identification(
            department_id,
            department_name
        )