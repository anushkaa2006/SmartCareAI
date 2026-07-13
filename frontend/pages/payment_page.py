import customtkinter as ctk
from tkinter import messagebox
import requests
import qrcode
import os

from PIL import Image

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image as PDFImage
)

from reportlab.lib.styles import getSampleStyleSheet

# =====================================================================
# DESIGN TOKENS
# =====================================================================

BG          = ("#F0F4F8", "#0B1121")
SURFACE     = ("#FFFFFF", "#151E32")
SURFACE_ALT = ("#E2E8F0", "#1E293B")
BORDER      = ("#CBD5E1", "#334155")

PRIMARY      = ("#0D9488", "#14B8A6")
PRIMARY_H    = ("#0F766E", "#0D9488")
PRIMARY_SOFT = ("#CCFBF1", "#134E4A")

SUCCESS = ("#10B981", "#10B981")
WARNING = ("#F59E0B", "#FBBF24")
DANGER  = ("#EF4444", "#F87171")

TEXT       = ("#0F172A", "#F8FAFC")
TEXT_SOFT  = ("#475569", "#94A3B8")
TEXT_FAINT = ("#64748B", "#64748B")

FONT_DISPLAY = "Segoe UI Semibold"
FONT_BODY = "Segoe UI"


class PaymentPage(ctk.CTkFrame):

    def __init__( self,parent, patient,validation_response,go_back,
            payment_success_callback, visit = None,payment=None,already_paid = False
    ):

        super().__init__(parent, fg_color=BG)

        self.patient = patient
        self.validation = validation_response
        self.go_back = go_back
        self.payment_success_callback = payment_success_callback
        self.visit = visit
        self.payment = payment
        self.already_paid = already_paid

        self.payment_mode = ctk.StringVar(value="CASH")

        self.pack(fill="both", expand=True)

        self.build_header()
        self.build_ui()

    
    def build_header(self):

            header = ctk.CTkFrame(
                self,
                fg_color=PRIMARY,
                height=45,
                corner_radius=0
            )

            header.pack(fill="x")
            header.pack_propagate(False)

            ctk.CTkFrame(
                self,
                height=1,
                fg_color=BORDER,
                corner_radius=0
            ).pack(fill="x")

            left = ctk.CTkFrame(header, fg_color="transparent")
            left.pack(side="left", padx=24)

            ctk.CTkButton(
                left,
                text="← Back",
                width=70,
                height=28,
                fg_color="transparent",
                hover_color=SURFACE_ALT,
                text_color=SURFACE,
                command=self.back
            ).pack(pady=8)

            brand = ctk.CTkFrame(header, fg_color="transparent")
            brand.place(relx=0.5, rely=0.5, anchor="center")

            ctk.CTkLabel(
                brand,
                text="⚕",
                font=(FONT_DISPLAY,20),
                text_color=SURFACE
            ).pack(side="left", padx=(0,8))

            ctk.CTkLabel(
                brand,
                text="SMARTCARE ID",
                font=(FONT_DISPLAY,15),
                text_color=SURFACE
            ).pack(side="left")
    
    def build_ui(self):

        container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        container.pack(
            fill="both",
            expand=True,
            padx=40,
            pady=30
        )

        left = ctk.CTkFrame(
            container,
            fg_color="transparent"
        )

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0,20)
        )

        right = ctk.CTkFrame(
            container,
            fg_color="transparent"
        )

        right.pack(
            side="right",
            fill="y"
        )

        self.build_patient_card(left)

        self.build_payment_method(left)

        self.build_fee_card(right)

        self.build_receipt_card(right)

        self.build_buttons(right)

    
    def build_patient_card(self,parent):

        card = ctk.CTkFrame(
            parent,
            fg_color=SURFACE,
            corner_radius=18,
            border_width=1,
            border_color=BORDER
        )

        card.pack(fill="x")

        ctk.CTkLabel(
            card,
            text="👤 Patient Information",
            font=(FONT_DISPLAY,20),
            text_color=TEXT
        ).pack(anchor="w", padx=24, pady=(20,20))

        fields = [

            ("Patient ID", self.patient["patientId"]),

            ("Patient Name", self.patient["name"]),

            ("Department", self.patient["departmentName"]),

            ("Billing Policy",self.validation["billingPolicy"].replace("_"," ").title())

        ]

        for title,value in fields:

            row = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            row.pack(fill="x", padx=30, pady=8)

            ctk.CTkLabel(
                row,
                text=title,
                width=140,
                anchor="w",
                font=(FONT_DISPLAY,14),
                text_color=TEXT_SOFT
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=value,
                font=(FONT_BODY,15),
                text_color=TEXT
            ).pack(side="left")


    def build_payment_method(self,parent):

        card = ctk.CTkFrame(
            parent,
            fg_color=SURFACE,
            corner_radius=18,
            border_width=1,
            border_color=BORDER
        )

        card.pack(fill="x", pady=20)

        ctk.CTkLabel(
            card,
            text="💳 Payment Method",
            font=(FONT_DISPLAY,20),
            text_color=TEXT
        ).pack(anchor="w", padx=24, pady=(20,20))

        payment_modes = {
            "CASH": "💵 Cash",
            "UPI": "📱 UPI",
            "CARD": "💳 Card"
        }

        for key, value in payment_modes.items():

            rb = ctk.CTkRadioButton(
                card,
                text=value,
                variable=self.payment_mode,
                value=key,
                font=(FONT_BODY,15),
                text_color=TEXT,
                fg_color=PRIMARY
            )

            rb.pack(anchor="w", padx=30, pady=10)


    def build_fee_card(self,parent):

        card = ctk.CTkFrame(
            parent,
            width=300,
            height=180,
            fg_color=PRIMARY_SOFT,
            corner_radius=20
        )

        card.pack()

        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text="Consultation Fee",
            font=(FONT_DISPLAY,18),
            text_color=PRIMARY
        ).pack(pady=(35,15))

        ctk.CTkLabel(
            card,
            text=f"₹ {self.validation['consultationFee']}",
            font=(FONT_DISPLAY,38),
            text_color=PRIMARY
        ).pack()


    def build_receipt_card(self,parent):

        card = ctk.CTkFrame(
            parent,
            fg_color=SURFACE,
            corner_radius=18,
            border_width=1,
            border_color=BORDER
        )

        card.pack(fill="x", pady=20)

        ctk.CTkLabel(
            card,
            text="Receipt Summary",
            font=(FONT_DISPLAY,18),
            text_color=TEXT
        ).pack(anchor="w", padx=20, pady=(20,15))

        amount = float(self.validation["consultationFee"])

        rows = [

            ("Consultation Fee",f"₹ {amount:.2f}"),

            ("Discount","₹ 0"),

            ("Total",f"₹ {amount:.2f}")

        ]

        for label,value in rows:

            row = ctk.CTkFrame(card, fg_color="transparent")

            row.pack(fill="x", padx=20, pady=8)

            ctk.CTkLabel(
                row,
                text=label,
                font=(FONT_BODY,14),
                text_color=TEXT_SOFT
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=value,
                font=(FONT_DISPLAY,15),
                text_color=TEXT
            ).pack(side="right")



    def build_buttons(self,parent):

        btn_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        btn_frame.pack(fill="x", pady=10)

        self.cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            fg_color=DANGER,
            hover_color="#d62828",
            width=130,
            command=self.back
        )
        self.cancel_btn.pack(side="left", padx=5)

        self.confirm_btn= ctk.CTkButton(
            btn_frame,
            text=("Continue"
                if self.validation["billingPolicy"] == "ALREADY_PAID"
                else "Confirm Payment"
            ),
            fg_color=PRIMARY,
            hover_color=PRIMARY_H,
            width=170,
            command=self.confirm_payment
        )
        self.confirm_btn.pack(side="right", padx=5)

    def back(self):

        self.destroy()

        self.go_back()


    def confirm_payment(self):

        if self.validation["billingPolicy"] == "ALREADY_PAID":

            payment = {

                "paymentId":"-",

                "receiptNumber":"-",

                "paymentStatus":"ALREADY PAID",

                "amount":0,

                "validTill":"-"

            }

            visit = self.payment_success_callback(payment)

            self.final_receipt_popup(payment, visit)

            return

        payload = {

            "patientId": self.patient["patientId"],

            "departmentId": self.patient["departmentId"],

            "amount": self.validation["consultationFee"],

            "paymentMode": self.payment_mode.get()

        }

        try:

            self.confirm_btn.configure(state="disabled",text="Processing...")

            self.cancel_btn.configure(state="disabled")
            self.configure(cursor="watch")

            response = requests.post("http://localhost:9090/payment/save",
                json=payload,timeout=10)


            if response.status_code != 200:

                self.confirm_btn.configure(
                    state="normal",
                    text="Confirm Payment"
                )
                self.configure(cursor="")          

                messagebox.showerror(
                    "Payment Failed",
                    "Unable to save payment."
                )

                return

            payment = response.json()

            print("Calling callback...")
            print(self.payment_success_callback)

            visit = self.payment_success_callback(payment)

            print("Callback returned:", visit)
            
            self.final_receipt_popup(payment,visit)

        except Exception as e:

            self.confirm_btn.configure(
                state="normal",
                text="Confirm Payment"
            )

            self.cancel_btn.configure(state="normal")
            self.configure(cursor="")

            messagebox.showerror(
                "Network Error",
                str(e)
            )

    
    def payment_success(self, payment):

        popup = ctk.CTkToplevel(self)

        popup.title("Payment Successful")

        popup.geometry("520x580")
        popup.resizable(False, False)

        popup.grab_set()

        popup.configure(fg_color=BG)

        badge = ctk.CTkLabel(
            popup,
            text="✓",
            width=80,
            height=80,
            corner_radius=40,
            fg_color=PRIMARY_SOFT,
            text_color=PRIMARY,
            font=(FONT_DISPLAY,36)
        )

        badge.pack(pady=(35,15))

        ctk.CTkLabel(
            popup,
            text="Payment Successful",
            font=(FONT_DISPLAY,22),
            text_color=TEXT
        ).pack()

        ctk.CTkLabel(
            popup,
            text=payment["message"],
            font=(FONT_BODY,14),
            text_color=TEXT_SOFT
        ).pack(pady=(5,25))

        card = ctk.CTkFrame(
            popup,
            fg_color=SURFACE,
            border_width=1,
            border_color=BORDER,
            corner_radius=18
        )

        card.pack(fill="x", padx=35)

        rows = [

            ("Payment ID", payment["paymentId"]),

            ("Receipt No", payment["receiptNumber"]),

            ("Status", payment["paymentStatus"]),

            ("Valid Till", payment["validTill"])

        ]

        for label,value in rows:

            row = ctk.CTkFrame(card,fg_color="transparent")

            row.pack(fill="x", padx=20, pady=8)

            ctk.CTkLabel(
                row,
                text=label,
                font=(FONT_BODY,13),
                text_color=TEXT_SOFT
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=str(value),
                font=(FONT_DISPLAY,13),
                text_color=TEXT
            ).pack(side="right")

        ctk.CTkButton(
            popup,
            text="Continue",
            height=45,
            fg_color=PRIMARY,
            hover_color=PRIMARY_H,
            command=lambda:self.finish_payment(
                popup,
                payment
            )
        ).pack(pady=30,padx=35,fill="x")


    def finish_payment(self, popup, payment):

        popup.destroy()

        self.confirm_btn.configure(
            state="normal",
            text="Confirm Payment"
        )

        self.cancel_btn.configure(state="normal")

        self.configure(cursor="")

        visit = self.payment_success_callback(payment)

        popup.destroy()

        self.final_receipt_popup(payment, visit)

    
    def final_receipt_popup(self, payment, visit):

        print("========== RECEIPT ==========")
        print("Patient:", self.patient)
        print("Payment:", payment)
        print("Visit:", visit)
        popup = ctk.CTkToplevel(self)
        popup.title("Registration Completed")

        popup.geometry("650x900")

        popup.grab_set()

        popup.configure(fg_color=BG)

        qr_path = self.generate_qr_code(payment, visit)

        badge = ctk.CTkLabel(
            popup,
            text="✓",
            width=80,
            height=80,
            corner_radius=40,
            fg_color=PRIMARY_SOFT,
            text_color=PRIMARY,
            font=(FONT_DISPLAY,36)
        )

        badge.pack(pady=(25,10))


        title = (
            "Visit Generated Successfully"
            if payment["paymentStatus"] == "ALREADY PAID"
            else "Registration Completed Successfully"
        )
        ctk.CTkLabel(
            popup,
            text=title,
            font=(FONT_DISPLAY,22),
            text_color=TEXT
        ).pack()

        card = ctk.CTkFrame(
            popup,
            fg_color=SURFACE,
            border_width=1,
            border_color=BORDER,
            corner_radius=18
        )

        card.pack(fill="both", padx=30, pady=20, expand=True)    
        qr_image = ctk.CTkImage(
            light_image=Image.open(qr_path),
            dark_image=Image.open(qr_path),
            size=(120, 120)
        )

        ctk.CTkLabel(
            card,
            image=qr_image,
            text=""
        ).pack(pady=(20, 10))


        try:
            rows = [

                ("Patient ID", self.patient["patientId"]),

                ("Patient Name", self.patient["name"]),

                ("Visit ID", visit["visitId"]),

                ("Queue Number", f"Q-{visit['queueNumber']}"),

                ("Department", self.patient["departmentName"]),

                ("Payment ID", payment["paymentId"]),

                ("Receipt No", payment["receiptNumber"]),

                ("Amount", f"₹ {payment['amount']}"),

                ("Status", payment["paymentStatus"]),

                ("Valid Till", payment["validTill"])

            ]

        except Exception as e:
            import traceback
            traceback.print_exc()
            print("ERROR BUILDING ROWS:", e)
            raise

        for label, value in rows:

            row = ctk.CTkFrame(
                card,
                fg_color="transparent"
            )

            row.pack(fill="x", padx=25, pady=5)

            ctk.CTkLabel(
                row,
                text=label,
                width=140,
                anchor="w",
                font=(FONT_DISPLAY, 13),
                text_color=TEXT_SOFT
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=str(value),
                font=(FONT_BODY, 13),
                text_color=TEXT
            ).pack(side="right")
        
        button_frame = ctk.CTkFrame(
            popup,
            fg_color="transparent"
        )

        button_frame.pack(
            fill="x",
            padx=35,
            pady=(10,25)
        )

        ctk.CTkButton(

            button_frame,

            text="Generate & Print Slip",

            height=45,

            fg_color=PRIMARY,

            hover_color=PRIMARY_H,

            command=lambda:self.generate_pdf_slip(

                self.patient["patientId"],

                visit["visitId"],

                visit["queueNumber"],

                self.patient["departmentName"],

                payment, visit

            )

        ).pack(fill="x", pady=(0,10))

        ctk.CTkButton(

            button_frame,

            text="Done",

            height=45,

            fg_color="transparent",

            border_width=1,

            border_color=BORDER,

            text_color=TEXT,

            command=lambda: self.finish_registration(popup)

        ).pack(fill="x")


    def generate_qr_code(self, payment, visit):

            qr_data = f"""
        SMARTCARE ID

        Patient ID : {visit['patientId']}
        Patient Name : {self.patient['name']}
        Visit ID : {visit['visitId']}
        Department : {self.patient['departmentName']}
        Queue Number : Q-{visit['queueNumber']}

        Payment ID : {payment['paymentId']}
        Receipt No : {payment['receiptNumber']}
        Amount : ₹ {payment['amount']}
        Status : {payment['paymentStatus']}
        Valid Till : {payment['validTill']}
        """

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=5
            )

            qr.add_data(qr_data)
            qr.make(fit=True)

            img = qr.make_image(
                fill_color="black",
                back_color="white"
            )

            filename = f"{visit['patientId']}_qr.png"

            img.save(filename)

            return filename

    def generate_pdf_slip(self,patient_id,visit_id,queue_number,department,payment,visit):

        qr_path = self.generate_qr_code(payment, visit)

        pdf_file = f"{patient_id}_Slip.pdf"

        doc = SimpleDocTemplate(pdf_file)

        styles = getSampleStyleSheet()

        elements = [

            Paragraph("SMARTCARE ID", styles["Title"]),

            Paragraph("Patient Receipt", styles["Heading2"]),

            Spacer(1,20),

            Paragraph(f"<b>Patient ID:</b> {patient_id}", styles["Normal"]),

            Paragraph(f"<b>Visit ID:</b> {visit_id}", styles["Normal"]),

            Paragraph(f"<b>Department:</b> {department}", styles["Normal"]),

            Paragraph(f"<b>Queue Number:</b> Q-{queue_number}", styles["Normal"]),

            Spacer(1,15),

            Paragraph(f"<b>Payment ID:</b> {payment['paymentId']}", styles["Normal"]),

            Paragraph(f"<b>Receipt No:</b> {payment['receiptNumber']}", styles["Normal"]),

            Paragraph(f"<b>Amount:</b> ₹ {payment['amount']}", styles["Normal"]),

            Paragraph(f"<b>Status:</b> {payment['paymentStatus']}", styles["Normal"]),

            Paragraph(f"<b>Valid Till:</b> {payment['validTill']}", styles["Normal"]),

            Spacer(1,20),

            PDFImage(qr_path,width=150,height=150)

        ]

        doc.build(elements)

        os.system(f'open "{pdf_file}"')


    def finish_registration(self, popup):

        popup.destroy()

        self.destroy()

        self.go_back()