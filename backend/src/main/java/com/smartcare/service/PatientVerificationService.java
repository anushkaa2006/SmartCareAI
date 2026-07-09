package com.smartcare.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.smartcare.model.Patient;
import com.smartcare.repository.PatientRepository;

@Service
public class PatientVerificationService {

    @Autowired
    private PatientRepository patientRepository;

    /**
     * Verify patient using Name + Father/Spouse Name + DOB + Phone
     * Used during new patient registration to detect duplicates.
     */
    public Patient verifyByPersonalDetails(
            String name,
            String fatherSpouseName,
            String dob,
            String phone
    ) {

        List<Patient> patients = patientRepository.findByPhone(phone);

        if (patients.isEmpty()) {
            return null;
        }

        for (Patient patient : patients) {

            boolean sameName =
                    patient.getName().trim().equalsIgnoreCase(name.trim());

            boolean sameFather =
                    patient.getFatherSpouseName().trim()
                            .equalsIgnoreCase(fatherSpouseName.trim());

            boolean sameDob =
                    patient.getDob().trim().equals(dob.trim());

            if (sameName && sameFather && sameDob) {
                return patient;
            }
        }

        return null;
    }

}