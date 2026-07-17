# import customtkinter as ctk
# from pages.landing_page import LandingPage
# from pages.registration_page import RegistrationPage
# from pages.identify_patient_page import IdentifyPatientPage
# from pages.patient_recovery_page import PatientRecoveryPage
# from pages.payment_page import PaymentPage

# ctk.set_appearance_mode("light")
# ctk.set_default_color_theme("blue")

# app = ctk.CTk()
# app.title("SmartCare ID — AI Healthcare Platform")
# app.geometry("1400x850")
# app.minsize(1200, 800)

# current_page = None

# def show_registration():
#     global current_page
#     if current_page:
#         current_page.destroy()
#     current_page = RegistrationPage(app, go_back=show_landing,open_payment_page=show_payment_page)

# def show_identify_patient(patient_id=None, department_id=None, department_name=None):
#     global current_page

#     if current_page:
#         current_page.destroy()

#     current_page = IdentifyPatientPage(app, go_back=show_landing,open_payment_page=show_payment_page,
#         patient_id=patient_id, department_id= department_id, department_name = department_name)


# def show_patient_recovery():
#     global current_page

#     if current_page:
#         current_page.destroy()
    
#     current_page = PatientRecoveryPage(app,go_back= show_landing,open_registration= show_registration, open_face_update= show_face_update)
    

# def show_face_update(patient, department_id, department_name):
#     global current_page
#     if current_page:
#         current_page.destroy()

#     print("Main.py Department ID:", department_id)
#     print("Main.py Department Name:", department_name)

#     current_page = RegistrationPage(app, go_back= show_landing,open_payment_page=show_payment_page,update_mode=True,patient=patient, department_id = department_id, department_name = department_name, skip_summary= True)

# def show_payment_page(patient,validation_response, payment_success_callback,
#         go_back_page, visit = None,payment=None,already_paid=False
# ):

#     global current_page

#     if current_page:
#         current_page.destroy()

#     current_page = PaymentPage(
#         app, patient=patient,
#         validation_response=validation_response,
#         go_back=go_back_page,
#         payment_success_callback=payment_success_callback,visit=visit,payment=payment,already_paid=already_paid
#     )

# def show_landing():
#     global current_page
#     if current_page:
#         current_page.destroy()
#     current_page = LandingPage(app, open_registration=show_registration, 
#                                open_identify_patient=show_identify_patient, 
#                                open_patient_recovery=show_patient_recovery,
#                                open_face_update = show_face_update )

# show_landing()
# app.mainloop()

import customtkinter as ctk

from pages.home_page import HomePage
from pages.department_selection_page import DepartmentSelectionPage
from pages.landing_page import LandingPage
from pages.registration_page import RegistrationPage
from pages.identify_patient_page import IdentifyPatientPage
from pages.patient_recovery_page import PatientRecoveryPage
from pages.payment_page import PaymentPage
from pages.department_checkin_result_page import DepartmentCheckInResultPage
import requests
from tkinter import messagebox

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("SmartCare ID — AI Healthcare Platform")
app.geometry("1400x850")
app.minsize(1200, 800)

current_page = None


# =====================================================
# Utility
# =====================================================

def clear_page():
    global current_page

    if current_page:
        current_page.destroy()


# =====================================================
# HOME PAGE
# =====================================================

def show_home():

    global current_page

    clear_page()

    current_page = HomePage(
        app,
        open_registration_mode=show_registration_landing,
        open_department_mode=show_department_selection
    )


# =====================================================
# REGISTRATION CAMERA FLOW
# =====================================================

def show_registration_landing():

    global current_page

    clear_page()

    current_page = LandingPage(
        app,
        open_registration=show_registration,
        open_identify_patient=show_identify_patient,
        open_patient_recovery=show_patient_recovery,
        open_face_update=show_face_update,
        mode="REGISTRATION"
    )


# =====================================================
# DEPARTMENT FLOW
# =====================================================

def show_department_selection():

    global current_page

    clear_page()

    current_page = DepartmentSelectionPage(
        app,
        go_back=show_home,
        open_department_landing=show_department_landing
    )


def show_department_landing(department_id, department_name):

    global current_page

    clear_page()

    current_page = LandingPage(
        app,
        open_registration=show_registration,
        open_identify_patient=show_identify_patient,
        open_patient_recovery=show_patient_recovery,
        open_face_update=show_face_update,
        mode="DEPARTMENT",
        department_id=department_id,
        department_name=department_name,
        open_department_checkin=show_department_checkin
    )


# =====================================================
# REGISTRATION
# =====================================================

def show_registration():

    global current_page

    clear_page()

    current_page = RegistrationPage(
        app,
        go_back=show_home,
        open_payment_page=show_payment_page
    )


# =====================================================
# IDENTIFY PATIENT
# =====================================================

def show_identify_patient(
    patient_id=None,
    department_id=None,
    department_name=None
):

    global current_page

    clear_page()

    current_page = IdentifyPatientPage(
        app,
        go_back=show_home,
        open_payment_page=show_payment_page,
        patient_id=patient_id,
        department_id=department_id,
        department_name=department_name
    )


# =====================================================
# PATIENT RECOVERY
# =====================================================

def show_patient_recovery(
    mode="REGISTRATION",
    department_id=None,
    department_name=None
):

    global current_page

    clear_page()

    current_page = PatientRecoveryPage(
        app,
        go_back=show_home,
        open_registration=show_registration,
        open_face_update=show_face_update,
        mode=mode,
        department_id=department_id,
        department_name=department_name,
        open_department_checkin=show_department_checkin
    )


# =====================================================
# FACE UPDATE
# =====================================================

def show_face_update(
    patient,
    department_id,
    department_name
):

    global current_page

    clear_page()

    current_page = RegistrationPage(
        app,
        go_back=show_home,
        open_payment_page=show_payment_page,
        update_mode=True,
        patient=patient,
        department_id=department_id,
        department_name=department_name,
        skip_summary=True
    )


# =====================================================
# PAYMENT PAGE
# =====================================================

def show_payment_page(
    patient,
    validation_response,
    payment_success_callback,
    go_back_page,
    visit=None,
    payment=None,
    already_paid=False
):

    global current_page

    clear_page()

    current_page = PaymentPage(
        app,
        patient=patient,
        validation_response=validation_response,
        go_back=go_back_page,
        payment_success_callback=payment_success_callback,
        visit=visit,
        payment=payment,
        already_paid=already_paid
    )


# =====================================================
# DEPARTMENT CHECK-IN
# =====================================================

def show_department_checkin(
    patient_id,
    department_id,
    department_name
):

    try:

        payload = {
            "patientId": patient_id,
            "departmentId": department_id
        }

        response = requests.post(
            "http://localhost:9090/visits/department/checkin",
            json=payload
        )

        if response.status_code != 200:

            messagebox.showerror(
                "Error",
                "Unable to perform department check-in."
            )
            return

        data = response.json()

        show_department_result(
            patient_name=data.get("patientName"),
            patient_id=data.get("patientId"),
            department_name=data.get("departmentName"),
            queue_number=data.get("queueNumber"),
            message=data.get("message"),
            action=data.get("action")
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )
        

def show_department_result(
    patient_name,
    patient_id,
    department_name,
    queue_number,
    message,
    action
):

    global current_page

    clear_page()

    current_page = DepartmentCheckInResultPage(
        app,
        patient_name=patient_name,
        patient_id=patient_id,
        department_name=department_name,
        queue_number=queue_number,
        message=message,
        action=action,
        done_callback=show_department_selection
    )
# =====================================================
# START APPLICATION
# =====================================================

show_home()

app.mainloop()
