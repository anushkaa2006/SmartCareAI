package com.smartcare.repository;

import java.time.LocalDate;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import com.smartcare.model.Payment;

@Repository
public interface PaymentRepository extends JpaRepository<Payment, String> {

    // Latest payment made by a patient (Flag 1)
    @Query("""
        SELECT MAX(p.paymentDate)
        FROM Payment p
        WHERE p.patientId = :patientId
        AND p.paymentStatus = 'SUCCESS'
    """)
    LocalDate findLastPaymentDate(String patientId);


    // Latest payment made by a patient in a department (Flag 2)
    @Query("""
        SELECT MAX(p.paymentDate)
        FROM Payment p
        WHERE p.patientId = :patientId
        AND p.departmentId = :departmentId
        AND p.paymentStatus = 'SUCCESS'
    """)
    LocalDate findLastPaymentDateByDepartment(
            String patientId,
            String departmentId
    );
    Payment findTopByReceiptNumber(String receiptNumber);
    long countByPaymentDate(LocalDate paymentDate);
}