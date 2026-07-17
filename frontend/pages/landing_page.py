import customtkinter as ctk
import cv2
from PIL import Image
import threading

from services.face_identifier import FaceIdentifier
# =====================================================================
# DESIGN TOKENS  (Light, Dark) - Sophisticated Nordic Sage & Warm Stone
# =====================================================================
BG          = ("#F0F4F8", "#0B1121") 
SURFACE     = ("#FFFFFF", "#151E32")  
SURFACE_ALT = ("#E2E8F0", "#1E293B") 
BORDER      = ("#CBD5E1", "#334155")  
BORDER_SOFT = ("#E2E8F0", "#1E293B")  


PRIMARY     = ("#0D9488", "#14B8A6")  
PRIMARY_H   = ("#0F766E", "#0D9488")  
PRIMARY_SOFT= ("#CCFBF1", "#134E4A")  

SUCCESS     = ("#10B981", "#10B981")  
WARNING     = ("#F59E0B", "#FBBF24")  
DANGER      = ("#EF4444", "#F87171")  
SUCCESS_H   = ("#426956", "#74B395")  

TEXT        = ("#0F172A", "#F8FAFC")  
TEXT_SOFT   = ("#475569", "#94A3B8")  
TEXT_FAINT  = ("#64748B", "#64748B")  

FONT_DISPLAY = "Segoe UI Semibold"
FONT_BODY    = "Segoe UI"


class LandingPage(ctk.CTkFrame):
    def __init__(self, parent, open_registration, open_identify_patient, open_patient_recovery, open_face_update,mode="REGISTRATION",department_id =None,department_name=None,open_department_checkin=None):
        super().__init__(parent, fg_color=BG)

        self.open_registration = open_registration
        self.open_identify_patient = open_identify_patient
        self.open_patient_recovery = open_patient_recovery
        self.open_face_update = open_face_update
        self.mode = mode

        self.department_id = department_id
        self.department_name = department_name

        self.open_department_checkin = open_department_checkin

        self.face_identifier = FaceIdentifier()

        self.cap = None
        self.current_frame =None

        self.is_scanning = False

        self.pack(fill="both", expand=True)
        self.patient_found = False

        self.scan_counter = 0

        self.is_processing = False

        # # ── Top bar (Centered Layout) ─────────────────────────
        header = ctk.CTkFrame(
            self,
            fg_color=PRIMARY,
            height=90,
            corner_radius=0
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        title_frame = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        title_frame.pack(
            side="left",
            padx=25
        )

        ctk.CTkLabel(
            title_frame,
            text="SMARTCARE ID",
            font=("Segoe UI", 28, "bold"),
            text_color="white"
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="AI Face Recognition Patient Identification System",
            font=("Segoe UI", 13),
            text_color="#D1FAE5"
        ).pack(anchor="w")

        # Theme Switch

        self.theme_switch = ctk.CTkSwitch(
            header,
            text="Dark Mode",
            command=self.toggle_theme,
            progress_color="#FFFFFF",
            text_color="white"
        )

        self.theme_switch.pack(
            side="right",
            padx=20
        )


        if ctk.get_appearance_mode() == "Dark":
            self.theme_switch.select()

        # ── Hero ─────────────────────────────────────────────
        hero = ctk.CTkFrame(self, fg_color="transparent")
        hero.pack(fill="both", expand=True, padx=80, pady=(10, 20))

        left = ctk.CTkFrame(hero, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True, pady=30)

        pill = ctk.CTkLabel(
            left, text="  ⚡  Powered by AI Face Recognition  ",
            font=(FONT_DISPLAY, 11),
            text_color=PRIMARY, fg_color=PRIMARY_SOFT,
            corner_radius=20, height=30
        )
        pill.pack(anchor="w", pady=(15, 20))

        ctk.CTkLabel(
            left, text="Healthcare,",
            font=(FONT_DISPLAY, 54), text_color=TEXT
        ).pack(anchor="w")
        ctk.CTkLabel(
            left, text="reimagined.",
            font=(FONT_DISPLAY, 54), text_color=PRIMARY
        ).pack(anchor="w")

        ctk.CTkLabel(
            left,
            text="Smart patient identification and queue management\nthat feels effortless — for everyone.",
            font=(FONT_BODY, 15),
            text_color=TEXT_SOFT, justify="left"
        ).pack(anchor="w", pady=(14, 28))

        for icon, text in [("🤖", "AI Face Recognition"),
                           ("⏱", "Real-time Queue Management"),
                           ("🔒", "Secure Patient Records")]:
            

            row = ctk.CTkFrame(left, fg_color="transparent")
            row.pack(anchor="w", pady=4)
            ctk.CTkLabel(row, text=icon, font=(FONT_DISPLAY, 16)).pack(side="left", padx=(0, 10))
            ctk.CTkLabel(row, text=text, font=(FONT_BODY, 14),
                         text_color=TEXT_FAINT).pack(side="left")
        
        status_card = ctk.CTkFrame(
            left,
            fg_color=SURFACE,
            corner_radius=18,
            border_width=1,
            border_color=BORDER
        )

        status_card.pack(
            fill="x",
            pady=(30,0)
        )

        ctk.CTkLabel(
            status_card,
            text="SYSTEM STATUS",
            font=(FONT_DISPLAY,15),
            text_color=PRIMARY
        ).pack(
            pady=(20,10)
        )


        self.status_label = ctk.CTkLabel(
            status_card,
            text="🟢 Waiting for Patient...",
            font=(FONT_BODY,18),
            text_color=SUCCESS
        )

        self.status_label.pack()

        self.info_label = ctk.CTkLabel(
            status_card,
            text="Camera initializing...",
            font=(FONT_BODY,13),
            text_color=TEXT_SOFT
        )

        self.info_label.pack(
            pady=(5,20)
        )

        # ── Right side cards ────────────────────────────────
        right = ctk.CTkFrame(hero, fg_color="transparent", width=480)
        right.pack(side="right", fill="y", padx=(20, 0))
        right.pack_propagate(False)

        camera_card = ctk.CTkFrame(
            right,fg_color=SURFACE,
            corner_radius=20,
            border_width=1,
            border_color=BORDER,
            height=640
        )

        camera_card.pack(
            fill= "both",
            expand= True,
            pady=20
        )

        camera_card.pack_propagate(False)

        ctk.CTkLabel(
            camera_card,
            text="Live Patient Scanner",
            font=(FONT_DISPLAY,18),
            text_color=TEXT
        ).pack(
            pady=(20,10)
        )

        self.camera_label = ctk.CTkLabel(
            camera_card,
            text=""
        )

        self.camera_label.pack(
            pady=20
        )

        # ── Footer ───────────────────────────────────────────
        ctk.CTkLabel(
            self,
            text="© 2026 SmartCare ID  •  Secure  •  Reliable  •  Lightning Fast",
            font=(FONT_BODY, 11), text_color=TEXT_FAINT
        ).pack(side="bottom", pady=14)

        self.after(
            500,
            self.start_camera
        )

    def toggle_theme(self):
        ctk.set_appearance_mode("dark" if self.theme_switch.get() == 1 else "light")

    
    def start_camera(self):

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

        self.is_scanning = True
        self.show_camera()
       
        

    

    def show_camera(self):

        if self.cap is None:
            return

        ret, frame = self.cap.read()

        if not ret:
            self.after(30, self.show_camera)
            return

        frame = cv2.flip(frame, 1)

        self.current_frame = frame.copy()


        self.scan_counter += 1
        if self.scan_counter >30 and not self.is_processing:

            self.scan_counter = 0

            self.is_processing = True

            self.status_label.configure(
                text="🟡 Checking Face..."
            )

            self.info_label.configure(
                text="Comparing with registered patients..."
            )
            result = self.face_identifier.identify(
                self.current_frame
            )

            if result is not None and result["found"]:

                self.patient_found = True

                self.status_label.configure(
                    text="🟢 Patient Identified"
                )

                self.info_label.configure(
                    text=f"Patient ID : {result['patientId']}"
                )

                if self.cap:
                    self.cap.release()
                    self.cap = None

                if self.mode == "REGISTRATION":

                    self.after(
                        700,
                        lambda: self.open_identify_patient(
                            result["patientId"]
                        )
                    )

                else:

                    self.after(
                        700,
                        lambda: self.open_department_checkin(
                            result["patientId"],
                            self.department_id,
                            self.department_name
                        )
                    )

                return

            else:

                self.status_label.configure(
                    text="🔴 Patient Not Found"
                )

                self.info_label.configure(
                    text="Opening Patient Recovery..."
                )

                if self.cap:
                    self.cap.release()
                    self.cap = None

                if self.mode == "REGISTRATION":

                    self.after(
                        700,
                        self.open_patient_recovery
                    )

                else:

                    self.after(
                        700,lambda: self.open_patient_recovery(
                            "DEPARTMENT",self.department_id,self.department_name
                        )
                    )
                return
        
        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        image = Image.fromarray(rgb)

        image.thumbnail((760,560), Image.LANCZOS)

        ctk_image = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size= image.size
        )

        self.camera_label.configure(
            image=ctk_image,
            text=""
        )

        self.camera_label.image = ctk_image

        self.after(
            30,
            self.show_camera
        )


    def stop_camera(self):

        self.is_scanning = False

        if self.cap is not None:

            self.cap.release()

            self.cap = None

    

    