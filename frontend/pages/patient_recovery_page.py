import customtkinter as ctk
import requests
from tkinter import messagebox

# -------------------------
# COLORS
# -------------------------

BG          = ("#F0F4F8", "#0B1121")  # Soft ice blue / Deep midnight navy
SURFACE     = ("#FFFFFF", "#151E32")  # Pure white / Rich navy
SURFACE_ALT = ("#E2E8F0", "#1E293B")  # Soft slate / Elevated slate blue
BORDER      = ("#CBD5E1", "#334155")  # Light slate border / Dark slate border
BORDER_SOFT = ("#E2E8F0", "#1E293B")  # Softer boundary

PRIMARY     = ("#0D9488", "#14B8A6")  # Electric Teal (Light / Dark)
PRIMARY_H   = ("#0F766E", "#0D9488")  # Hover Teal
PRIMARY_SOFT= ("#CCFBF1", "#134E4A")  # Very pale teal / Deepest teal green

SUCCESS     = ("#10B981", "#10B981")  # Emerald
WARNING     = ("#F59E0B", "#FBBF24")  # Amber
DANGER      = ("#EF4444", "#F87171")  # Coral Red

TEXT        = ("#0F172A", "#F8FAFC")  # Almost black / Crisp off-white
TEXT_SOFT   = ("#475569", "#94A3B8")  # Slate gray / Light slate
TEXT_FAINT  = ("#64748B", "#64748B")  # Mid slate

FONT_DISPLAY = "Segoe UI Semibold"
FONT_BODY    = "Segoe UI"
ACCENT = ("#2563EB", "#3B82F6")


class PatientRecoveryPage(ctk.CTkFrame):
    def __init__(self,parent,go_back,open_registration,open_face_update):
        super().__init__(parent, fg_color=BG)

        self.go_back = go_back
        self.open_registration = open_registration
        self.open_face_update = open_face_update
        self.department_map ={}

        self.pack(fill="both", expand=True)
        self.build_header()
        self.build_ui()

    
    def build_header(self):
        header = ctk.CTkFrame(self, fg_color=SURFACE, height=45, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkFrame(self, height=1, fg_color=BORDER, corner_radius=0).pack(fill="x")

        left_frame = ctk.CTkFrame(header, fg_color="transparent")
        left_frame.pack(side="left", padx=24, fill="y")
        
        ctk.CTkButton(
            left_frame, text="← Back", width=70, height=28, corner_radius=6,
            fg_color="transparent", text_color=TEXT_SOFT, hover_color=SURFACE_ALT, 
            font=(FONT_BODY, 12), command=self.go_back
        ).pack(side="left", pady=8)

        right_frame = ctk.CTkFrame(header, fg_color="transparent")
        right_frame.pack(side="right", padx=24, fill="y")
        
        self.theme_switch = ctk.CTkSwitch(
            right_frame, text="Dark mode", command=self.toggle_theme, 
            progress_color=PRIMARY, font=(FONT_BODY, 11), text_color=TEXT_SOFT
        )
        self.theme_switch.pack(side="right", pady=10)

        brand_frame = ctk.CTkFrame(header, fg_color="transparent")
        brand_frame.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(brand_frame, text="⚕", font=(FONT_DISPLAY, 20), text_color=PRIMARY).pack(side="left", padx=(0, 6))
        ctk.CTkLabel(brand_frame, text="SMARTCARE ID", font=(FONT_DISPLAY, 14), text_color=TEXT).pack(side="left")


    def build_ui(self):
        card = ctk.CTkFrame(self,fg_color=SURFACE,
                            corner_radius= 20, width=700,height=500)
        
        card.place(relx=0.5,rely=0.5,anchor= "center")

        card.pack_propagate(False)
        ctk.CTkLabel(card, text ="Patient Not Recognized",
                     font=("Segoe UI",28,"bold"),text_color=TEXT
        ).pack(pady=(40,15))

        ctk.CTkLabel(card,text ="Already have a Patient ID?", 
                     font=(" Segoe UI",15), text_color=TEXT_SOFT).pack()
        
        self.patient_id = ctk.CTkEntry(
            card,
            width=350,
            height=45,
            placeholder_text="Enter Patient ID"
        )

        self.patient_id.pack(
            pady=20
        )

        ctk.CTkButton(
            card,
            text="Verify Patient",
            width=250,
            height=45,
            fg_color=PRIMARY,
            hover_color=PRIMARY_H,
            command=self.verify_patient
        ).pack( pady=10)

        ctk.CTkLabel(card, text="──────── OR ────────", 
                     font=("Segoe UI",14), text_color=TEXT_SOFT).pack(pady=25)
        
        ctk.CTkButton(
            card,
            text="Register as New Patient",
            width=250,
            height=45,
            fg_color=PRIMARY,
            hover_color=PRIMARY_H,
            command=self.open_registration
        ).pack()

    
    def verify_patient(self):
        patient_id = self.patient_id.get().strip()

        if patient_id =="":
            messagebox.showerror("Error","Please enter Patient ID")
            return
        
        try:
            response = requests.get(f"http://localhost:9090/patients/{patient_id}")
            if response.status_code != 200:
                messagebox.showerror("Not Found","Patient ID doea not exist")
                return
            patient = response.json()
            self.open_face_update(patient)
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

    
    def toggle_theme(self):

        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")


    def load_departments(self):
        try:
            response = requests.get("http://localhost:9090/departments", timeout=5)
            if response.status_code != 200:
                return

            departments = response.json()
            department_names = []
            self.department_map = {}

            for dept in departments:
                status = dept.get("departmentStatus", "")
                if status.upper() == "ACTIVE":
                    department_name = dept.get("departmentName","")
                    department_id = dept.get("departmentId","")
                    department_names.append(department_name)
                    self.department_map[department_name]=department_id

            if len(department_names) > 0:
                self.department_dropdown.configure(values=department_names)
                self.department_dropdown.set(department_names[0])
            else:
                self.department_dropdown.configure(values=["No Departments"])
                self.department_dropdown.set("No Departments")

        except Exception as e:
            import traceback
            traceback.print_exc()