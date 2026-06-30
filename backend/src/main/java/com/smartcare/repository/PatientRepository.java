package com.smartcare.repository;

import com.smartcare.model.Patient;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PatientRepository
        extends JpaRepository<Patient, String> {

    long countByRegistrationDate(String registrationDate);
    Patient findByNameAndFatherSpouseNameAndDobAndPhone(
        String name,
        String fatherSpouseName,
        String dob,
        String phone
    );
        
}