package com.smartcare.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import com.smartcare.model.Payment;

@Repository
public interface PaymentRepository extends JpaRepository<Payment, String> {

    /**
     * Used for Payment Flag = 1
     * Returns the latest successful payment of the patient.
     */
    @Query("""
        SELECT p
        FROM Payment p
        WHERE p.patientId = :patientId
        AND p.paymentStatus = 'SUCCESS'
        ORDER BY p.paymentDate DESC
    """)
    Optional<Payment> findLatestPayment(String patientId);


    /**
     * Used for Payment Flag = 2
     * Returns the latest successful payment of the patient
     * for a particular department.
     */
    @Query("""
        SELECT p
        FROM Payment p
        WHERE p.patientId = :patientId
        AND p.departmentId = :departmentId
        AND p.paymentStatus = 'SUCCESS'
        ORDER BY p.paymentDate DESC
    """)
    Optional<Payment> findLatestDepartmentPayment(
            String patientId,
            String departmentId
    );
}