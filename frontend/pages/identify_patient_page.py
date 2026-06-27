

import customtkinter as ctk
import cv2
import face_recognition
from tkinter import messagebox
import requests
import numpy as np
from PIL import Image, ImageTk, ImageOps
import shutil
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image as PDFImage
)
import subprocess
from reportlab.lib.styles import getSampleStyleSheet
import os
import sys
import qrcode

# =====================================================================
# DESIGN TOKENS
# =====================================================================
BG          = ("#F7F7F5", "#1A1C1B")  
SURFACE     = ("#FFFFFF", "#232625")  
SURFACE_ALT = ("#F0F0EB", "#2E3330")  
BORDER      = ("#E0E0D8", "#404743")  
BORDER_SOFT = ("#EBEBE6", "#353B38")  

PRIMARY     = ("#78938A", "#8BA89F")  
PRIMARY_H   = ("#637C74", "#9EBEB4")  
PRIMARY_SOFT= ("#E8F0ED", "#263B34")  

SUCCESS     = ("#52826B", "#629E82")  
WARNING     = ("#B58C57", "#D1A466")  
DANGER      = ("#AD5C5C", "#CC6D6D")  

TEXT        = ("#2D302E", "#F0F2F1")  
TEXT_SOFT   = ("#69706C", "#A9B3AE")  
TEXT_FAINT  = ("#98A19D", "#7A827E")  

FONT_DISPLAY = "Segoe UI Semibold"
FONT_BODY    = "Segoe UI"


class IdentifyPatientPage(ctk.CTkFrame):

    def __init__(self, parent, go_back,patient_id=None):
        super().__init__(parent, fg_color=BG)
        self.go_back_command = go_back
        self.patient_id = patient_id
        self.pack(fill="both", expand=True)

        self.cap = None
        self.current_frame = None
        self.current_patient_id = None
      

        self.build_header()

        self.split_container = ctk.CTkFrame(self, fg_color="transparent")
        self.split_container.pack(fill="both", expand=True)
        
        # --- SWAPPED LAYOUT ---
        # LEFT PANE: Patient Details (Expands)
        self.left_pane = ctk.CTkFrame(self.split_container, fg_color="transparent")
        self.left_pane.pack(side="left", fill="both", expand=True, padx=50, pady=40)

        # RIGHT PANE: Camera (Fixed Width)
        self.right_pane = ctk.CTkFrame(self.split_container, fg_color=SURFACE, width=420, corner_radius=0)
        self.right_pane.pack(side="right", fill="y")
        self.right_pane.pack_propagate(False)
        
        # Left border for the right pane
        ctk.CTkFrame(self.right_pane, width=1, fg_color=BORDER).pack(side="left", fill="y")

        self.build_form_pane()
        self.build_camera_pane()

        if self.patient_id is not None:

            self.fetch_patient_details(self.patient_id)

            self.camera_frame.pack_forget()

            self.open_cam_btn.pack_forget()

            self.capture_btn.pack_forget()

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
            font=(FONT_BODY, 12), command=self.go_back_safe
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

    def build_camera_pane(self):
        # Uses self.right_pane
        ctk.CTkLabel(self.right_pane, text="🤖 Face Identification", font=(FONT_DISPLAY, 22), text_color=TEXT).pack(anchor="w", padx=30, pady=(40, 5))
        ctk.CTkLabel(self.right_pane, text="Position patient's face and capture.", font=(FONT_BODY, 14), text_color=TEXT_SOFT).pack(anchor="w", padx=30, pady=(0, 30))

        cam_container = ctk.CTkFrame(self.right_pane, fg_color="transparent")
        cam_container.pack(fill="x", padx=30)

        self.camera_frame = ctk.CTkFrame(cam_container, width=320, height=320, fg_color=("#111312", "#090A0A"), corner_radius=16)
        self.camera_frame.pack()
        self.camera_frame.pack_propagate(False)

        self.camera_label = ctk.CTkLabel(self.camera_frame, text="◉ Camera offline", text_color=TEXT_FAINT, font=(FONT_BODY, 14))
        self.camera_label.pack(fill="both", expand=True)

        btn_frame = ctk.CTkFrame(self.right_pane, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=(30, 5))

        self.open_cam_btn = ctk.CTkButton(btn_frame, text="📸 Open Camera", height=45, font=(FONT_DISPLAY, 14), fg_color=SURFACE_ALT, hover_color=BORDER, text_color=TEXT, command=self.open_camera)
        self.open_cam_btn.pack(fill="x", pady=(0, 10))
        self.capture_btn = ctk.CTkButton(btn_frame, text="✓ Capture Face", height=45, font=(FONT_DISPLAY, 14), fg_color=PRIMARY, hover_color=PRIMARY_H, text_color=("#FFFFFF", "#1A1C1B"), command=self.capture_face)
        self.capture_btn.pack(fill="x")
        ctk.CTkLabel(self.right_pane, text="(Or press the SPACE bar to capture)", text_color=TEXT_FAINT, font=(FONT_BODY, 12)).pack(pady=(10, 0))

    def build_form_pane(self):
        # Uses self.left_pane
        ctk.CTkLabel(self.left_pane, text="Scan Status", font=(FONT_DISPLAY, 14), text_color=TEXT_FAINT).pack(anchor="w")
        self.status_label = ctk.CTkLabel(self.left_pane, text="Waiting for face scan...", font=(FONT_DISPLAY, 24), text_color=WARNING)
        self.status_label.pack(anchor="w", pady=(0, 30))

        self.patient_card = ctk.CTkFrame(self.left_pane, fg_color=SURFACE, corner_radius=20, border_width=1, border_color=BORDER)
        self.patient_card.pack(fill="x", pady=(0, 20))
        ctk.CTkLabel(self.patient_card, text="👤 Patient Information", font=(FONT_DISPLAY, 20), text_color=TEXT).pack(anchor="w", padx=24, pady=(20, 15))
        self.patient_info_label = ctk.CTkLabel(self.patient_card, text="No patient identified yet.\nPlease scan a face to retrieve details.", justify="left", font=(FONT_BODY, 15), text_color=TEXT_SOFT)
        self.patient_info_label.pack(anchor="w", padx=24, pady=(0, 24))

        self.department_card = ctk.CTkFrame(self.left_pane, fg_color=SURFACE, corner_radius=20, border_width=1, border_color=BORDER)
        self.department_card.pack(fill="x")
        ctk.CTkLabel(self.department_card, text="🏥 Select Department", font=(FONT_DISPLAY, 20), text_color=TEXT).pack(anchor="w", padx=24, pady=(20, 15))
        self.department_dropdown = ctk.CTkComboBox(self.department_card, values=["Loading..."], width=350, height=45, fg_color=SURFACE_ALT, border_color=BORDER, text_color=TEXT)
        self.department_dropdown.pack(anchor="w", padx=24, pady=(0, 20))

        self.department_map = {}
        self.load_departments()
        self.proceed_btn = ctk.CTkButton(self.department_card, text="Proceed To Visit →", width=220, height=45, font=(FONT_DISPLAY, 14), fg_color=PRIMARY, hover_color=PRIMARY_H, text_color=("#FFFFFF", "#1A1C1B"), command=lambda: self.generate_visit(self.current_patient_id))
        self.proceed_btn.pack(anchor="w", padx=24, pady=(0, 24))

    # --- RETAINED LOGIC ---
    def toggle_theme(self): ctk.set_appearance_mode("dark" if self.theme_switch.get() == 1 else "light")

    
    def go_back_safe(self):
        try: self.winfo_toplevel().unbind('<space>')
        except: pass
        if self.cap is not None: self.cap.release()
        self.go_back_command()


    def open_camera(self):
        self.status_label.configure(text="Opening camera...", text_color=WARNING)
        if self.cap is not None: self.cap.release()
        self.cap = cv2.VideoCapture(0)
        self.winfo_toplevel().bind('<space>', self._handle_spacebar_capture)
        self.show_camera()


    def _handle_spacebar_capture(self, event=None):
        if self.cap is not None: self.capture_face()

        
    def show_camera(self):
        if self.cap is None: return
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            self.current_frame = frame.copy()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageOps.pad(img, (320, 320), color=(17, 19, 18))
            ctk_image = ctk.CTkImage(light_image=img, dark_image=img, size=(320, 320))
            self.camera_label.configure(image=ctk_image, text="")
            self.camera_label.image = ctk_image
        self.after(33, self.show_camera)



    def capture_face(self):
        if self.current_frame is None:
            messagebox.showerror("Error", "Please open the camera first!")
            return
        try: self.winfo_toplevel().unbind('<space>')
        except: pass
        self.camera_frame.configure(border_width=4, border_color=SUCCESS)
        self.after(250, lambda: self.camera_frame.configure(border_width=0))
        image_path = "captured_faces/registered_patient.jpg"
        os.makedirs("captured_faces", exist_ok=True)
        cv2.imwrite(image_path, self.current_frame)
        if self.cap:
            self.cap.release()
            self.cap = None
        self.generate_embedding(image_path)


    # ... (Rest of the logic methods remain identical)
    # =========================
    # GENERATE EMBEDDING & IDENTIFY
    # =========================

    def generate_embedding(self, image_path):
        self.status_label.configure(text="Processing face data...", text_color=WARNING)
        self.update()

        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)

        if len(encodings) == 0:
            messagebox.showerror("Face Error", "No face detected in captured frame.")
            self.status_label.configure(text="No face detected", text_color=DANGER)
            return

        current_embedding = encodings[0]
        self.status_label.configure(text="Face captured successfully ✓", text_color=SUCCESS)
        self.find_patient(current_embedding)
    
    def find_patient(self, current_embedding):
        try:
            url = "http://localhost:9090/patients/faces"
            response = requests.get(url)
            faces = response.json()

            if response.status_code != 200 or len(faces) == 0:
                messagebox.showerror("Error", "No registered patient found in database.")
                self.status_label.configure(text="No Matching Patient Found", text_color=DANGER)
                return
            
            known_embeddings = []
            valid_faces = []

            for face in faces:
                embedding_string = face["embeddingVector"]
                if embedding_string is None or embedding_string.strip() == "":
                    continue
                try:
                    embedding = np.array(list(map(float, embedding_string.split(","))))
                    known_embeddings.append(embedding)
                    valid_faces.append(face)
                except ValueError:
                    continue

            if len(known_embeddings) == 0:
                messagebox.showerror("Error","No valid face embeddings found in database")
                return
            
            print("Total registered embeddings:", len(known_embeddings))

            distances = face_recognition.face_distance(known_embeddings, current_embedding)
            best_match_index = np.argmin(distances)
            best_distance = distances[best_match_index]

            if best_distance < 0.45:
                patient_id = valid_faces[best_match_index]["patientId"]
                self.fetch_patient_details(patient_id)
            else:
                self.status_label.configure(text="No Matching Patient Found", text_color=DANGER)

        except Exception as e:
            messagebox.showerror("Application Error", f"An error occurred:\n{str(e)}")
            import traceback
            traceback.print_exc()
    
    def fetch_patient_details(self, patient_id):
        try:
            response = requests.get(f"http://localhost:9090/patients/{patient_id}")
            if response.status_code != 200:
                messagebox.showerror("Error", "Unable to fetch patient details")
                return
            
            patient = response.json()
            self.current_patient_id = patient["patientId"]
         
            self.patient_info_label.configure(
                text=
                f"ID       : {patient['patientId']}\n\n"
                f"Name     : {patient['name']}\n\n"
                f"Age      : {patient['age']}\n\n"
                f"Gender   : {patient['gender']}\n\n"
                f"Phone    : {patient['phone']}",
                text_color=TEXT
            )
            self.status_label.configure(
                text="✅ Registered Patient",
                text_color=SUCCESS
            )

        except Exception as e:
            print(e)    

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
    
    def generate_visit(self, patient_id):
        if self.current_patient_id is None:
            messagebox.showerror("Error", "Please scan a patient first")
            return

        department_name = self.department_dropdown.get()
        department_id = self.department_map.get(department_name)

        if not department_id:
            messagebox.showerror("Error", "Invalid department selected.")
            return

        payload = {
            "patientId": patient_id,
            "departmentId": department_id
        }

        try:
            response = requests.post("http://localhost:9090/visits/create", json=payload)
            data = response.json()
            self.registration_success(data["patientId"], data["visitId"], data["queueNumber"], department_name)
        except Exception as e:
            messagebox.showerror("Network Error", "Could not connect to visit generation API.")
    
    def registration_success(self, patient_id, visit_id, queue_number, department):
        qr_path = self.generate_qr_code(patient_id, visit_id, queue_number, department)

        popup = ctk.CTkToplevel(self)
        popup.title("Visit Created")
        popup.geometry("520x720")
        popup.grab_set()
        popup.configure(fg_color=BG)

        badge = ctk.CTkLabel(
            popup, text="✓", width=72, height=72, corner_radius=36,
            fg_color=PRIMARY_SOFT, text_color=PRIMARY, font=(FONT_DISPLAY, 34)
        )
        badge.pack(pady=(36, 14))

        ctk.CTkLabel(popup, text="Visit Created Successfully", font=(FONT_DISPLAY, 22), text_color=TEXT).pack()
        ctk.CTkLabel(popup, text="Patient has been added to the queue.", font=(FONT_BODY, 13), text_color=TEXT_SOFT).pack(pady=(4, 22))

        card = ctk.CTkFrame(popup, corner_radius=16, fg_color=SURFACE, border_width=1, border_color=BORDER)
        card.pack(fill="x", padx=44, pady=8)

        qr_ctk_image = ctk.CTkImage(
            light_image=Image.open(qr_path), dark_image=Image.open(qr_path), size=(130, 130)
        )
        qr_label = ctk.CTkLabel(card, image=qr_ctk_image, text="")
        qr_label.image = qr_ctk_image
        qr_label.pack(pady=(20, 14))

        details = ctk.CTkFrame(card, fg_color="transparent")
        details.pack(fill="x", padx=28, pady=(0, 22))
        for label, value in [
            ("Patient ID",   patient_id),
            ("Visit ID",     visit_id),
            ("Queue number", f"Q-{queue_number}"),
            ("Department",   department),
        ]:
            row = ctk.CTkFrame(details, fg_color="transparent")
            row.pack(fill="x", pady=5)
            ctk.CTkLabel(row, text=label, font=(FONT_BODY, 12), text_color=TEXT_FAINT).pack(side="left")
            ctk.CTkLabel(row, text=value, font=(FONT_DISPLAY, 13), text_color=TEXT).pack(side="right")

        ctk.CTkButton(
            popup, text="Generate & print slip", height=46, corner_radius=12,
            font=(FONT_DISPLAY, 14), fg_color=PRIMARY, hover_color=PRIMARY_H,
            text_color=("#FFFFFF", "#1A1C1B"),
            command=lambda: self.download_slip(patient_id, visit_id, queue_number, department, qr_path),
        ).pack(pady=24, padx=44, fill="x")
    
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
        img.save(f"{patient_id}_qr.png")
        return f"{patient_id}_qr.png"
    
    def generate_pdf_slip(self, patient_id, visit_id, queue_number, department, qr_path):
        pdf_file = f"{patient_id}_Slip.pdf"
        doc = SimpleDocTemplate(pdf_file)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("SMARTCARE ID", styles['Title']))
        elements.append(Paragraph("Hospital Visit Slip", styles['Heading2']))
        elements.append(Spacer(1,20))
        elements.append(Paragraph(f"<b>Patient ID:</b> {patient_id}", styles['Normal']))
        elements.append(Paragraph(f"<b>Visit ID:</b> {visit_id}", styles['Normal']))
        elements.append(Paragraph(f"<b>Department:</b> {department}",styles['Normal']))
        elements.append(Paragraph(f"<b>Queue Number:</b> Q-{queue_number}",styles['Normal']))
        elements.append(Spacer(1,20))
        elements.append(PDFImage(qr_path,width=150,height=150))

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
