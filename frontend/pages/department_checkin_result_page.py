import customtkinter as ctk

# =====================================================
# COLORS
# =====================================================

BG = ("#F0F4F8", "#0B1121")
SURFACE = ("#FFFFFF", "#151E32")
SURFACE_ALT = ("#E2E8F0", "#1E293B")
BORDER = ("#CBD5E1", "#334155")

PRIMARY = ("#0D9488", "#14B8A6")
PRIMARY_H = ("#0F766E", "#0D9488")

SUCCESS = ("#10B981", "#10B981")
WARNING = ("#F59E0B", "#FBBF24")
DANGER = ("#EF4444", "#F87171")

TEXT = ("#0F172A", "#F8FAFC")
TEXT_SOFT = ("#475569", "#94A3B8")

FONT_DISPLAY = "Segoe UI Semibold"
FONT_BODY = "Segoe UI"


class DepartmentCheckInResultPage(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        patient_name,
        patient_id,
        department_name,
        queue_number,
        message,
        action,
        done_callback
    ):

        super().__init__(parent, fg_color=BG)

        self.pack(fill="both", expand=True)

        # =========================
        # Decide Status
        # =========================

        if action == "CHECK_IN_SUCCESS":

            icon = "✅"
            title = "Department Check-In Successful"
            color = SUCCESS

        elif action == "ALREADY_CHECKED_IN":

            icon = "🟡"
            title = "Already Checked In"
            color = WARNING

        elif action == "WRONG_DEPARTMENT":

            icon = "❌"
            title = "Wrong Department"
            color = DANGER

        else:

            icon = "❌"
            title = "No Active Visit Found"
            color = DANGER

        # =========================
        # Header
        # =========================

        header = ctk.CTkFrame(
            self,
            fg_color=PRIMARY,
            height=85,
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

        # =========================
        # Card
        # =========================

        card = ctk.CTkFrame(
            self,
            width=700,
            height=520,
            fg_color=SURFACE,
            corner_radius=20,
            border_width=1,
            border_color=BORDER
        )

        card.place(relx=0.5, rely=0.52, anchor="center")
        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=icon,
            font=("Segoe UI Emoji", 55)
        ).pack(pady=(30, 5))

        ctk.CTkLabel(
            card,
            text=title,
            font=(FONT_DISPLAY, 28),
            text_color=color
        ).pack()

        # =========================
        # Information Box
        # =========================

        info = ctk.CTkFrame(
            card,
            fg_color=SURFACE_ALT,
            corner_radius=15
        )

        info.pack(fill="x", padx=35, pady=30)

        rows = [

            ("Patient Name", patient_name),
            ("Patient ID", patient_id),
            ("Department", department_name),
            ("Queue Number", queue_number),
            ("Message", message)

        ]

        for label, value in rows:

            row = ctk.CTkFrame(
                info,
                fg_color="transparent"
            )

            row.pack(
                fill="x",
                padx=20,
                pady=8
            )

            ctk.CTkLabel(
                row,
                text=label + " :",
                width=150,
                anchor="w",
                font=("Segoe UI", 14, "bold"),
                text_color=TEXT
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=str(value if value else "-"),
                anchor="w",
                font=("Segoe UI", 14),
                text_color=TEXT_SOFT
            ).pack(side="left")

        # =========================
        # Done Button
        # =========================

        ctk.CTkButton(
            card,
            text="Done",
            width=220,
            height=45,
            fg_color=PRIMARY,
            hover_color=PRIMARY_H,
            font=("Segoe UI", 15, "bold"),
            command=done_callback
        ).pack(pady=30)

        # =========================
        # Footer
        # =========================

        ctk.CTkLabel(
            self,
            text="© 2026 SmartCare ID • Secure • Reliable • AI Powered",
            font=("Segoe UI", 11),
            text_color=TEXT_SOFT
        ).pack(side="bottom", pady=15)