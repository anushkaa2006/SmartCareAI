import customtkinter as ctk
from pages.landing_page import LandingPage
from pages.registration_page import RegistrationPage
from pages.identify_patient_page import IdentifyPatientPage
from pages.patient_recovery_page import PatientRecoveryPage
from pages.payment_page import PaymentPage

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("SmartCare ID — AI Healthcare Platform")
app.geometry("1400x850")
app.minsize(1200, 800)

current_page = None

def show_registration():
    global current_page
    if current_page:
        current_page.destroy()
    current_page = RegistrationPage(app, go_back=show_landing)

def show_identify_patient(patient_id=None, department_id=None, department_name=None):
    global current_page

    if current_page:
        current_page.destroy()

    current_page = IdentifyPatientPage(app, go_back=show_landing,open_payment_page=show_payment_page,
        patient_id=patient_id, department_id= department_id, department_name = department_name)


def show_patient_recovery():
    global current_page

    if current_page:
        current_page.destroy()
    
    current_page = PatientRecoveryPage(app,go_back= show_landing,open_registration= show_registration, open_face_update= show_face_update)
    

def show_face_update(patient, department_id, department_name):
    global current_page
    if current_page:
        current_page.destroy()

    print("Main.py Department ID:", department_id)
    print("Main.py Department Name:", department_name)
    
    current_page = RegistrationPage(app, go_back= show_landing,update_mode=True,patient=patient, department_id = department_id, department_name = department_name, skip_summary= True)

def show_payment_page(
            patient,
            validation_response,
            payment_success_callback,
            patient_id
    ):

        global current_page

        if current_page:
            current_page.destroy()

        current_page = PaymentPage(
            app,
            patient=patient,
            validation_response=validation_response,
            go_back=lambda: show_identify_patient(patient_id=patient_id),
            payment_success_callback=payment_success_callback
        )

def show_landing():
    global current_page
    if current_page:
        current_page.destroy()
    current_page = LandingPage(app, open_registration=show_registration, 
                               open_identify_patient=show_identify_patient, 
                               open_patient_recovery=show_patient_recovery,
                               open_face_update = show_face_update )

show_landing()
app.mainloop()
