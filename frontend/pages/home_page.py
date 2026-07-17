import customtkinter as ctk

BG = ("#F0F4F8", "#0B1121")
SURFACE = ("#FFFFFF", "#151E32")
PRIMARY = ("#0D9488", "#14B8A6")
PRIMARY_H = ("#0F766E", "#0D9488")
TEXT = ("#0F172A", "#F8FAFC")
TEXT_SOFT = ("#475569", "#94A3B8")


class HomePage(ctk.CTkFrame):

    def __init__(self, parent, open_registration_mode, open_department_mode):
        super().__init__(parent, fg_color=BG)

        self.open_registration_mode = open_registration_mode
        self.open_department_mode = open_department_mode

        self.pack(fill="both", expand=True)

        # Header
        header = ctk.CTkFrame(
            self,
            fg_color=PRIMARY,
            height=90,
            corner_radius=0
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="SMARTCARE ID",
            font=("Segoe UI", 28, "bold"),
            text_color="white"
        ).pack(pady=(15, 0))

        ctk.CTkLabel(
            header,
            text="AI Healthcare Platform",
            font=("Segoe UI", 14),
            text_color="#D1FAE5"
        ).pack()

        # Body
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(expand=True)

        ctk.CTkLabel(
            body,
            text="Choose Workflow",
            font=("Segoe UI", 34, "bold"),
            text_color=TEXT
        ).pack(pady=(20, 10))

        ctk.CTkLabel(
            body,
            text="Select the required operation",
            font=("Segoe UI", 15),
            text_color=TEXT_SOFT
        ).pack(pady=(0, 40))

        cards = ctk.CTkFrame(body, fg_color="transparent")
        cards.pack()

        # Registration Card
        reg = ctk.CTkFrame(
            cards,
            width=320,
            height=260,
            fg_color=SURFACE,
            corner_radius=20
        )
        reg.grid(row=0, column=0, padx=25)
        reg.pack_propagate(False)

        ctk.CTkLabel(
            reg,
            text="📝",
            font=("Segoe UI", 48)
        ).pack(pady=(30, 10))

        ctk.CTkLabel(
            reg,
            text="Registration Desk",
            font=("Segoe UI", 22, "bold")
        ).pack()

        ctk.CTkLabel(
            reg,
            text="New Registration\nExisting Patient\nPayment",
            justify="center"
        ).pack(pady=15)

        ctk.CTkButton(
            reg,
            text="Open",
            width=180,
            height=42,
            fg_color=PRIMARY,
            hover_color=PRIMARY_H,
            command=self.open_registration_mode
        ).pack(pady=20)

        # Department Card
        dept = ctk.CTkFrame(
            cards,
            width=320,
            height=260,
            fg_color=SURFACE,
            corner_radius=20
        )
        dept.grid(row=0, column=1, padx=25)
        dept.pack_propagate(False)

        ctk.CTkLabel(
            dept,
            text="🏥",
            font=("Segoe UI", 48)
        ).pack(pady=(30, 10))

        ctk.CTkLabel(
            dept,
            text="Department Check-In",
            font=("Segoe UI", 22, "bold")
        ).pack()

        ctk.CTkLabel(
            dept,
            text="Department Arrival\nQueue Update\nPatient Verification",
            justify="center"
        ).pack(pady=15)

        ctk.CTkButton(
            dept,
            text="Open",
            width=180,
            height=42,
            fg_color=PRIMARY,
            hover_color=PRIMARY_H,
            command=self.open_department_mode
        ).pack(pady=20)