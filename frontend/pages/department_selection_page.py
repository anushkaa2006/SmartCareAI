import customtkinter as ctk
import requests
from tkinter import messagebox

BG = ("#F0F4F8", "#0B1121")
SURFACE = ("#FFFFFF", "#151E32")
PRIMARY = ("#0D9488", "#14B8A6")
PRIMARY_H = ("#0F766E", "#0D9488")
TEXT = ("#0F172A", "#F8FAFC")
TEXT_SOFT = ("#475569", "#94A3B8")


class DepartmentSelectionPage(ctk.CTkFrame):

    def __init__(self, parent, go_back, open_department_landing):
        super().__init__(parent, fg_color=BG)

        self.go_back = go_back
        self.open_department_landing = open_department_landing

        self.department_map = {}

        self.pack(fill="both", expand=True)

        self.build_header()
        self.build_ui()
        self.load_departments()

    def build_header(self):

        header = ctk.CTkFrame(
            self,
            fg_color=PRIMARY,
            height=70,
            corner_radius=0
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkButton(
            header,
            text="← Back",
            width=90,
            command=self.go_back,
            fg_color="transparent",
            hover_color=PRIMARY_H
        ).pack(side="left", padx=20, pady=15)

        ctk.CTkLabel(
            header,
            text="Department Check-In",
            font=("Segoe UI", 24, "bold"),
            text_color="white"
        ).pack(side="left", padx=20)

    def build_ui(self):

        card = ctk.CTkFrame(
            self,
            width=500,
            height=350,
            fg_color=SURFACE,
            corner_radius=20
        )

        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text="Select Department",
            font=("Segoe UI", 28, "bold"),
            text_color=TEXT
        ).pack(pady=(40, 20))

        ctk.CTkLabel(
            card,
            text="Choose the department for patient check-in",
            font=("Segoe UI", 14),
            text_color=TEXT_SOFT
        ).pack()

        self.department_dropdown = ctk.CTkComboBox(
            card,
            width=320,
            values=["Loading..."]
        )

        self.department_dropdown.pack(pady=35)

        ctk.CTkButton(
            card,
            text="Continue",
            width=220,
            height=45,
            fg_color=PRIMARY,
            hover_color=PRIMARY_H,
            command=self.continue_clicked
        ).pack()

    def load_departments(self):

        try:

            response = requests.get(
                "http://localhost:9090/departments"
            )

            if response.status_code != 200:
                messagebox.showerror(
                    "Error",
                    "Unable to load departments."
                )
                return

            departments = response.json()

            names = []

            for dept in departments:

                if dept["departmentStatus"] == "ACTIVE":

                    names.append(
                        dept["departmentName"]
                    )

                    self.department_map[
                        dept["departmentName"]
                    ] = dept["departmentId"]

            if len(names) == 0:

                names = ["No Active Department"]

            self.department_dropdown.configure(
                values=names
            )

            self.department_dropdown.set(
                names[0]
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    def continue_clicked(self):

        department_name = self.department_dropdown.get()

        department_id = self.department_map.get(
            department_name
        )

        if department_id is None:

            messagebox.showerror(
                "Error",
                "Please select a department."
            )

            return

        self.open_department_landing(
            department_id,
            department_name
        )