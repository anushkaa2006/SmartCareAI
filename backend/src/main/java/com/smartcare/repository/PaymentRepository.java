package com.smartcare.repository;

import java.time.LocalDate;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.smartcare.model.Payment;

@Repository
public interface PaymentRepository extends JpaRepository<Payment,String> {

    Optional<Payment> findFirstByPatientIdAndPaymentStatusOrderByPaymentDateDesc(
            String patientId,
            String paymentStatus
    );

    Optional<Payment> findFirstByPatientIdAndDepartmentIdAndPaymentStatusOrderByPaymentDateDesc(
            String patientId,
            String departmentId,
            String paymentStatus
    );
    long countByPaymentDate(LocalDate paymentDate);

    Optional<Payment> findFirstByPatientIdAndDepartmentIdOrderByPaymentDateDesc(
                String patientId,
                String departmentId
    );
   
    
}