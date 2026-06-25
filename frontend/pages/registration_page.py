

"""
SmartCare ID — Patient Registration Page
Theme: Midnight Ocean & Electric Teal
"""

import customtkinter as ctk
from datetime import datetime
import cv2
from PIL import Image, ImageOps
import os
import requests
from tkinter import messagebox
import qrcode
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as PDFImage
from reportlab.lib.styles import getSampleStyleSheet
import subprocess
import sys
import shutil
import face_recognition

# =====================================================================
# DESIGN TOKENS  (Light, Dark) - Midnight Ocean & Electric Teal
# =====================================================================
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


class RegistrationPage(ctk.CTkFrame):
    def __init__(self, parent, go_back):
        super().__init__(parent, fg_color=BG)
        self.go_back = go_back
        self.pack(fill="both", expand=True)

        self.form_data = {}
        self.cap = None
        self.current_frame = None

        self._build_header()
        self._build_stepper()

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=48, pady=(4, 12))

        self.page1_frame = ctk.CTkFrame(
            self.main_container, fg_color=SURFACE, corner_radius=18,
            border_width=1, border_color=BORDER,
        )
        self.page2_frame = ctk.CTkFrame(
            self.main_container, fg_color=SURFACE, corner_radius=18,
            border_width=1, border_color=BORDER,
        )

        self._build_page1()
        self._build_page2()
        self.show_page1()

    # ---------- HEADER ----------

    def _build_header(self):
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

    def _build_stepper(self):
        wrap = ctk.CTkFrame(self, fg_color="transparent")
        wrap.pack(fill="x", pady=(18, 4))
        inner = ctk.CTkFrame(wrap, fg_color="transparent")
        inner.pack(anchor="center")

        self.step1_dot = self._step_dot(inner, "1", True)
        self.step1_dot.pack(side="left", padx=(0, 10))
        self.step1_lbl = ctk.CTkLabel(inner, text="Patient details",
                                      font=(FONT_DISPLAY, 13), text_color=TEXT)
        self.step1_lbl.pack(side="left", padx=(0, 18))

        ctk.CTkFrame(inner, width=64, height=2, fg_color=BORDER).pack(
            side="left", padx=6, pady=10)

        self.step2_dot = self._step_dot(inner, "2", False)
        self.step2_dot.pack(side="left", padx=(18, 10))
        self.step2_lbl = ctk.CTkLabel(inner, text="Biometric enrollment",
                                      font=(FONT_BODY, 13), text_color=TEXT_SOFT)
        self.step2_lbl.pack(side="left")

    def _step_dot(self, parent, text, active):
        return ctk.CTkLabel(
            parent, text=text, width=28, height=28, corner_radius=14,
            fg_color=PRIMARY if active else SURFACE_ALT,
            text_color=("#FFFFFF", "#0B1121") if active else TEXT_SOFT,
            font=(FONT_DISPLAY, 12),
        )

    def _set_step(self, step):
        if step == 1:
            self.step1_dot.configure(fg_color=PRIMARY, text_color=("#FFFFFF", "#0B1121"))
            self.step1_lbl.configure(text_color=TEXT, font=(FONT_DISPLAY, 13))
            self.step2_dot.configure(fg_color=SURFACE_ALT, text_color=TEXT_SOFT)
            self.step2_lbl.configure(text_color=TEXT_SOFT, font=(FONT_BODY, 13))
        else:
            self.step2_dot.configure(fg_color=PRIMARY, text_color=("#FFFFFF", "#0B1121"))
            self.step2_lbl.configure(text_color=TEXT, font=(FONT_DISPLAY, 13))
            self.step1_dot.configure(fg_color=SURFACE_ALT, text_color=TEXT_SOFT)
            self.step1_lbl.configure(text_color=TEXT_SOFT, font=(FONT_BODY, 13))

    def toggle_theme(self):
        ctk.set_appearance_mode("dark" if self.theme_switch.get() == 1 else "light")

    # ---------- PAGE 1 ----------
    def _build_page1(self):
        inner = ctk.CTkFrame(self.page1_frame, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=36, pady=8)
        for i in range(8):
            inner.grid_columnconfigure(i, weight=1, uniform="col", pad=4)

        row = 0
        self._section(inner, "Personal Details",
                      "Basic identity information about the patient.", row); row += 1

        self.full_name   = self._entry(inner, "Full Name *", row, 0, colspan=3)
        self.gender      = self._dropdown(inner, "Gender *",
                                          ["Select", "Male", "Female", "Other"], row, 4, colspan=2)
        self.category    = self._dropdown(inner, "Category *",
                                          ["Select", "BPL", "General", "Ayushman", "JSY","PMJY", "Armed Forces","Freedom Fighter"], row, 6, colspan=2)
        row += 1

        self.dob         = self._entry(inner, "DOB ", row, 0, colspan=2, placeholder="DD/MM/YYYY")
        self.dob.bind(
            "<FocusOut>",
            self.calculate_age
        )
        self.age         = self._entry(inner, "Age *", row, 2, colspan=1)
        self.father_name = self._entry(inner, "Father / Spouse Name *", row, 4, colspan=3)
        row += 1

        ctk.CTkFrame(inner, height=1, fg_color=BORDER_SOFT).grid(
            row=row, column=0, columnspan=8, sticky="ew", pady=(10, 4)); row += 1

        self._section(inner, "Contact & Address",
                      "Where can we reach the patient if needed?", row); row += 1

        self.phone    = self._entry(inner, "Mobile number *", row, 0, colspan=3)
        self.state    = self._entry(inner, "State *",         row, 3, colspan=2)
        self.district = self._entry(inner, "District *",      row, 5, colspan=2)
        row += 1

        self.address  = self._entry(inner, "Full address *", row, 0, colspan=5)
        self.pincode  = self._entry(inner, "Pincode *",      row, 5, colspan=2)
        row += 1

        ctk.CTkFrame(inner, height=1, fg_color=BORDER_SOFT).grid(
            row=row, column=0, columnspan=8, sticky="ew", pady=(10, 4)); row += 1


        self.department = self._dropdown(inner, "Visiting Department *",
                                         self.load_departments(), row, 0, colspan=3)
        self.symptoms   = self._entry(inner, "Visit Reason (optional)", row, 4, colspan=4)
        row += 1

        action = ctk.CTkFrame(inner, fg_color="transparent")
        action.grid(row=row, column=0, columnspan=8, pady=(12, 4), sticky="ew")
        
        self.error_label1 = ctk.CTkLabel(action, text="", text_color=DANGER, font=(FONT_BODY, 12))
        self.error_label1.pack(side="left")
        
        ctk.CTkButton(
            action, text="Continue  →", height=40, corner_radius=12,
            font=(FONT_DISPLAY, 14), fg_color=PRIMARY, hover_color=PRIMARY_H,
            text_color=("#FFFFFF", "#0B1121"), command=self.validate_and_next,
        ).pack(side="right")

    def _section(self, parent, title, subtitle, row):
        wrap = ctk.CTkFrame(parent, fg_color="transparent")
        wrap.grid(row=row, column=0, columnspan=8, sticky="ew", pady=(4, 6))
        chip = ctk.CTkFrame(wrap, fg_color=PRIMARY_SOFT, corner_radius=6, width=4, height=24)
        chip.pack(side="left", padx=(0, 12))
        chip.pack_propagate(False)
        text = ctk.CTkFrame(wrap, fg_color="transparent")
        text.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(text, text=title, font=(FONT_DISPLAY, 15), text_color=TEXT).pack(anchor="w")
        ctk.CTkLabel(text, text=subtitle, font=(FONT_BODY, 12), text_color=TEXT_FAINT).pack(anchor="w")

    def _entry(self, parent, label, row, col, colspan=1, placeholder=""):
        wrap = ctk.CTkFrame(parent, fg_color="transparent")
        wrap.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=6, pady=4)
        ctk.CTkLabel(wrap, text=label, font=(FONT_BODY, 12),
                     text_color=TEXT_SOFT).pack(anchor="w", pady=(0, 2))
        entry = ctk.CTkEntry(
            wrap, height=36, corner_radius=10, 
            fg_color=SURFACE_ALT, border_color=BORDER, border_width=1,
            text_color=TEXT, placeholder_text=placeholder, font=(FONT_BODY, 13),
        )
        entry.pack(fill="x")
        return entry

    def _dropdown(self, parent, label, values, row, col, colspan=1):
        wrap = ctk.CTkFrame(parent, fg_color="transparent")
        wrap.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=6, pady=4)
        ctk.CTkLabel(wrap, text=label, font=(FONT_BODY, 12),
                     text_color=TEXT_SOFT).pack(anchor="w", pady=(0, 2))
        dd = ctk.CTkOptionMenu(
            wrap, values=values, height=36, corner_radius=10, 
            fg_color=SURFACE_ALT, button_color=SURFACE_ALT,
            button_hover_color=BORDER, text_color=TEXT,
            dropdown_fg_color=SURFACE, dropdown_text_color=TEXT,
            font=(FONT_BODY, 13),
        )
        dd.pack(fill="x")
        return dd

    # ---------- PAGE 2 ----------
    def _build_page2(self):
        self.page2_frame.pack_propagate(False)
        top = ctk.CTkFrame(self.page2_frame, fg_color="transparent")
        top.pack(fill="x", padx=36, pady=(16, 4))
        ctk.CTkLabel(top, text="Biometric enrollment", font=(FONT_DISPLAY, 18),
                     text_color=TEXT).pack(anchor="w")
        ctk.CTkLabel(top, text="Position the patient's face within the frame and capture a clear photo.",
                     font=(FONT_BODY, 12), text_color=TEXT_FAINT).pack(anchor="w", pady=(2, 0))

        cam_wrap = ctk.CTkFrame(
            self.page2_frame, fg_color=SURFACE_ALT, corner_radius=16,
            border_width=1, border_color=BORDER,
        )
        cam_wrap.pack(fill="x", padx=36, pady=8)

        self.camera_frame = ctk.CTkFrame(
            cam_wrap, height=360, fg_color=("#0B1121", "#04070D"), corner_radius=12,
        )
        self.camera_frame.pack(fill="x", padx=14, pady=14)
        self.camera_frame.pack_propagate(False)
        self.camera_label = ctk.CTkLabel(
            self.camera_frame, text="◉  Camera offline",
            text_color=TEXT_FAINT, font=(FONT_BODY, 14),
        )
        self.camera_label.pack(fill="both", expand=True)

        self.status_label = ctk.CTkLabel(
            self.page2_frame, text="  ⏳  Face not captured yet  ",
            text_color=WARNING, font=(FONT_DISPLAY, 12),
            fg_color=PRIMARY_SOFT, corner_radius=999,
            padx=14, pady=6,
        )
        self.status_label.pack(pady=(4, 8))

        btns = ctk.CTkFrame(self.page2_frame, fg_color="transparent")
        btns.pack(pady=0)
        ctk.CTkButton(btns, text="← Back", height=42, width=120, corner_radius=12,
                      fg_color="transparent", border_width=1, border_color=BORDER,
                      text_color=TEXT_SOFT, hover_color=SURFACE_ALT,
                      font=(FONT_BODY, 13), command=self.show_page1).pack(side="left", padx=8)
        ctk.CTkButton(btns, text="◉  Open camera", height=42, corner_radius=12,
                      fg_color=SURFACE_ALT, hover_color=BORDER, text_color=TEXT,
                      border_width=1, border_color=BORDER,
                      font=(FONT_BODY, 13), command=self.open_camera).pack(side="left", padx=8)
        ctk.CTkButton(btns, text="✓  Capture face", height=42, corner_radius=12,
                      fg_color=PRIMARY, hover_color=PRIMARY_H,
                      text_color=("#FFFFFF", "#0B1121"),
                      font=(FONT_DISPLAY, 13), command=self.capture_face).pack(side="left", padx=8)

        submit = ctk.CTkFrame(self.page2_frame, fg_color="transparent")
        submit.pack(fill="x", side="bottom", pady=12, padx=36)
        self.generate_btn = ctk.CTkButton(
            submit, text="Complete Registration & Generate Slip  →",
            height=50, corner_radius=14, font=(FONT_DISPLAY, 15),
            fg_color=PRIMARY, hover_color=PRIMARY_H,
            text_color=("#FFFFFF", "#0B1121"),
            state="normal", command=self.register_patient_api,
        )
        self.generate_btn.pack(side="right")

    # ---------- NAVIGATION ----------
    def show_page1(self):
        if self.cap:
            self.cap.release()
            self.cap = None
        self.page2_frame.pack_forget()
        self.page1_frame.pack(fill="both", expand=True)
        self._set_step(1)

    def show_page2(self):
        self.page1_frame.pack_forget()
        self.page2_frame.pack(fill="both", expand=True)
        self._set_step(2)

    def validate_and_next(self):
        self.error_label1.configure(text="")
        mandatory = [self.full_name, self.age, self.father_name, self.phone,
                     self.state, self.district, self.pincode, self.address]
        for f in mandatory:
            if not f.get().strip():
                self.error_label1.configure(text="Please fill all mandatory fields marked with *")
                return
        
        if self.gender.get() == "Select" or self.category.get() == "Select":
            self.error_label1.configure(text="Please select valid options for gender & category")
            return
            
        if len(self.dob.get().split('/')) != 3:
            self.error_label1.configure(text="Date of birth must be in DD/MM/YYYY format")
            return
            
        if self.department.get() == "Select Department":
            self.error_label1.configure(text="Please select a visiting department")
            return
            
        self.show_page2()

    # ---------- HARDWARE & API ----------
    def load_departments(self):
        default_deps = ["General Medicine", "Orthopedics", "Pediatrics", "Cardiology", "Neurology", "Oncology"]
        departments = ["Select Department"] + default_deps
        try:
            res = requests.get("http://localhost:9090/departments", timeout=2)
            if res.status_code == 200:
                api_deps = [item.get("departmentName") for item in res.json()]
                if len(api_deps) > 0:
                    departments = ["Select Department"] + api_deps
        except Exception as e:
            pass
        return departments

    def open_camera(self):
        if self.cap is not None:
            self.cap.release()
        self.cap = cv2.VideoCapture(0)
        self.show_camera()

    def show_camera(self):
        if self.cap is None:
            return
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            self.current_frame = frame.copy()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            img = Image.fromarray(frame)
            
            # --- Aspect Ratio Fix ---
            # RGB color (4, 7, 13) matches the #04070D deep midnight background perfectly
            img = ImageOps.pad(img, (900, 350), color=(4, 7, 13))
            
            ctk_image = ctk.CTkImage(light_image=img, dark_image=img, size=(900, 350))
            self.camera_label.configure(image=ctk_image, text="")
            self.camera_label.image = ctk_image
            
        self.after(33, self.show_camera)

    def capture_face(self):
        if self.current_frame is None:
            return
        os.makedirs("captured_faces", exist_ok=True)
        cv2.imwrite(os.path.join("captured_faces", "patient_face.jpg"), self.current_frame)
        if self.cap:
            self.cap.release()
            self.cap = None
        self.status_label.configure(
            text="  ✓  Face captured successfully  ",
            text_color=SUCCESS, fg_color=PRIMARY_SOFT,
        )
        self.generate_btn.configure(state="normal")

    def register_patient_api(self):
        self.generate_btn.configure(text="Processing...", state="disabled")
        self.update() 

        try:
            day, month, year = self.dob.get().strip().split('/')
            formatted_dob = f"{year}-{month.zfill(2)}-{day.zfill(2)}"

            payload = {
                "name": self.full_name.get().strip(),
                "fatherSpouseName": self.father_name.get().strip(),
                "age": int(self.age.get()),
                "gender": self.gender.get(),
                "category": self.category.get(),
                "dob": formatted_dob,
                "phone": self.phone.get().strip(),
                "address": self.address.get().strip(),
                "state": self.state.get().strip(),
                "district": self.district.get().strip(),
                "pincode": self.pincode.get().strip(),
                "department": self.department.get()
            }

            try:
                response = requests.post("http://localhost:9090/patients/register", json=payload, timeout=3)

                if response.status_code == 200:
                    data = response.json()
                    patient_id = data["patientId"]
                    visit_id = data["visitId"]
                    queue_number = data["queueNumber"]
                    department = data["department"]
                   
                    source = "captured_faces/patient_face.jpg"
                    destination = f"captured_faces/{patient_id}.jpg"
                    shutil.copy(source, destination)
                    
                    image = face_recognition.load_image_file(source)
                    encodings = face_recognition.face_encodings(image)

                    if len(encodings) == 0:
                        messagebox.showerror("Face Error", "No face detected in captured image")
                        self.generate_btn.configure(text="Complete Registration & Generate Slip  →", state="normal")
                        return

                    embedding = encodings[0].tolist()
                    embedding_string = ",".join(map(str, embedding))

                    face_payload = {
                        "patientId": patient_id,
                        "imagePath": destination,
                        "embeddingVector": embedding_string
                    }

                    requests.post("http://localhost:9090/patients/face/save", json=face_payload, timeout=3)
                    self.registration_success(patient_id, visit_id, queue_number, department)

                else:
                    messagebox.showerror("Server Error", f"Failed with status code: {response.status_code}")

            except requests.exceptions.ConnectionError:
                print("⚠️ Spring Boot API is offline. Running in UI Test Mode.")
                self.registration_success(
                    patient_id="CR-TEST-999", 
                    visit_id="VID-0001", 
                    queue_number="14", 
                    department=self.department.get()
                )

        except Exception as e:
            messagebox.showerror("Application Error", f"An error occurred:\n{str(e)}")
        finally:
            self.generate_btn.configure(text="Complete Registration & Generate Slip  →", state="normal")

    # ---------- SUCCESS POPUP MODAL ----------
    def registration_success(self, patient_id, visit_id, queue_number, department):
        qr_path = self.generate_qr_code(patient_id, visit_id, queue_number, department)

        self.success_popup = ctk.CTkFrame(self, fg_color=SURFACE, corner_radius=20, border_width=1, border_color=BORDER)
        self.success_popup.place(relx=0.5, rely=0.5, anchor="center")

        close_btn = ctk.CTkButton(
            self.success_popup, text="✕", width=32, height=32, corner_radius=16,
            fg_color="transparent", hover_color=SURFACE_ALT, text_color=TEXT_SOFT,
            font=(FONT_DISPLAY, 16), command=self.close_success_popup
        )
        close_btn.pack(anchor="ne", padx=16, pady=(16, 0))

        badge = ctk.CTkLabel(
            self.success_popup, text="✓", width=64, height=64, corner_radius=32,
            fg_color=PRIMARY_SOFT, text_color=PRIMARY, font=(FONT_DISPLAY, 30)
        )
        badge.pack(pady=(0, 10))

        ctk.CTkLabel(self.success_popup, text="Registration successful", font=(FONT_DISPLAY, 22), text_color=TEXT).pack()
        ctk.CTkLabel(self.success_popup, text="Patient details captured and saved.", font=(FONT_BODY, 13), text_color=TEXT_SOFT).pack(pady=(4, 16))

        card = ctk.CTkFrame(self.success_popup, corner_radius=12, fg_color=SURFACE_ALT, border_width=1, border_color=BORDER_SOFT)
        card.pack(fill="x", padx=40, pady=10)

        qr_ctk_image = ctk.CTkImage(
            light_image=Image.open(qr_path), dark_image=Image.open(qr_path),
            size=(130, 130),
        )
        qr_label = ctk.CTkLabel(card, image=qr_ctk_image, text="")
        qr_label.image = qr_ctk_image
        qr_label.pack(pady=(20, 10))

        details = ctk.CTkFrame(card, fg_color="transparent")
        details.pack(fill="x", padx=24, pady=(0, 20))
        for label, value in [
            ("Patient ID",   patient_id),
            ("Visit ID",     visit_id),
            ("Queue number", f"Q-{queue_number}"),
            ("Department",   department),
        ]:
            row = ctk.CTkFrame(details, fg_color="transparent")
            row.pack(fill="x", pady=4)
            ctk.CTkLabel(row, text=label, font=(FONT_BODY, 12), text_color=TEXT_FAINT).pack(side="left")
            ctk.CTkLabel(row, text=value, font=(FONT_DISPLAY, 13), text_color=TEXT).pack(side="right")

        btn_frame = ctk.CTkFrame(self.success_popup, fg_color="transparent")
        btn_frame.pack(fill="x", padx=40, pady=(10, 30))

        ctk.CTkButton(
            btn_frame, text="Generate & print slip", height=46, corner_radius=12,
            font=(FONT_DISPLAY, 14), fg_color=PRIMARY, hover_color=PRIMARY_H, text_color=("#FFFFFF", "#0B1121"),
            command=lambda: self.download_slip(patient_id, visit_id, queue_number, department, qr_path),
        ).pack(fill="x", pady=(0, 10))
        
        ctk.CTkButton(
            btn_frame, text="Done (New Patient)", height=46, corner_radius=12,
            font=(FONT_DISPLAY, 14), fg_color="transparent", hover_color=SURFACE_ALT,
            text_color=TEXT_SOFT, border_width=1, border_color=BORDER,
            command=self.close_success_popup
        ).pack(fill="x")

    def close_success_popup(self):
        if hasattr(self, 'success_popup'):
            self.success_popup.destroy()
        self.show_page1()

    # ---------- PDF & QR UTILS ----------
    def generate_qr_code(self, patient_id, visit_id, queue_number, department):
        qr_data = (
            f"Patient ID: {patient_id}\n"
            f"Visit ID: {visit_id}\n"
            f"Department: {department}\n"
            f"Queue Number: {queue_number}"
        )
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        qr_filename = f"{patient_id}_qr.png"
        img.save(qr_filename)
        return qr_filename

    def generate_pdf_slip(self, patient_id, visit_id, queue_number, department, qr_path):
        pdf_file = f"{patient_id}_Slip.pdf"
        doc = SimpleDocTemplate(pdf_file)
        styles = getSampleStyleSheet()
        elements = [
            Paragraph("SMARTCARE ID", styles['Title']),
            Paragraph("Hospital Registration Slip", styles['Heading2']),
            Spacer(1, 20),
            Paragraph(f"<b>Patient ID:</b> {patient_id}", styles['Normal']),
            Paragraph(f"<b>Visit ID:</b> {visit_id}", styles['Normal']),
            Paragraph(f"<b>Department:</b> {department}", styles['Normal']),
            Paragraph(f"<b>Queue Number:</b> Q-{queue_number}", styles['Normal']),
            Spacer(1, 20),
            PDFImage(qr_path, width=150, height=150),
        ]
        doc.build(elements)
        return pdf_file

    def download_slip(self, patient_id, visit_id, queue_number, department, qr_path):
        pdf_file = self.generate_pdf_slip(patient_id, visit_id, queue_number, department, qr_path)
        try:
            if sys.platform == "darwin":
                subprocess.Popen(["open", pdf_file])
            elif sys.platform == "win32":
                os.startfile(pdf_file)
            else:
                subprocess.Popen(["xdg-open", pdf_file])
        except Exception as e:
            print(f"Error opening PDF: {e}")

    def calculate_age(self, event=None):

        dob = self.dob.get().strip()

        if not dob:
            return

        try:

            birth_date = datetime.strptime(
                dob,
                "%d/%m/%Y"
            )

            today = datetime.today()

            age = (
                today.year
                - birth_date.year
                - (
                    (today.month, today.day)
                    <
                    (birth_date.month, birth_date.day)
                )
            )

            self.age.delete(0, "end")

            self.age.insert(
                0,
                str(age)
            )

        except:
            pass


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    app = ctk.CTk()
    app.geometry("1280x820")
    app.title("SmartCare ID — Registration")
    RegistrationPage(app, go_back=app.destroy)
    app.mainloop()