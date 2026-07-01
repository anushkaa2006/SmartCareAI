package com.smartcare.repository;

import com.smartcare.model.Patient;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface PatientRepository
        extends JpaRepository<Patient, String> {

    long countByRegistrationDate(String registrationDate);
    List<Patient> findByPhone(String phone);
        
}