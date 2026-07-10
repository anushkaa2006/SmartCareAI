package com.smartcare.service;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.smartcare.dto.PaymentRequest;
import com.smartcare.dto.PaymentResponse;
import com.smartcare.enums.PaymentStatus;
import com.smartcare.model.HospitalConfig;
import com.smartcare.model.Payment;
import com.smartcare.repository.PaymentRepository;

@Service
public class PaymentService {

    @Autowired
    private PaymentRepository paymentRepository;

    @Autowired
    private HospitalConfigService hospitalConfigService;

    public PaymentResponse savePayment(PaymentRequest request){
        Payment payment = new Payment();
        payment.setPaymentId(generatePaymentId());
        payment.setReceiptNumber(generateReceiptNumber());
        payment.setPatientId(request.getPatientId());
        payment.setDepartmentId(request.getDepartmentId());
        payment.setAmount(request.getAmount());
        payment.setPaymentMode(request.getPaymentMode());
        payment.setPaymentStatus(PaymentStatus.SUCCESS.name());
        payment.setPaymentDate(LocalDate.now());
        HospitalConfig config = hospitalConfigService.getConfiguration();
        payment.setValidTill(LocalDate.now().plusDays(config.getValidityDays()));

        paymentRepository.save(payment);
        return buildResponse(payment);
    }

    private PaymentResponse buildResponse(Payment payment) {

        PaymentResponse response = new PaymentResponse();

        response.setPaymentId(payment.getPaymentId());
        response.setReceiptNumber(payment.getReceiptNumber());
        response.setAmount(payment.getAmount());
        response.setPaymentStatus(payment.getPaymentStatus());
        response.setPaymentDate(payment.getPaymentDate());
        response.setValidTill(payment.getValidTill());
        response.setMessage("Payment Successful");

        return response;
    }
    private String generatePaymentId(){
        LocalDate today= LocalDate.now();
        String datePart = today.format(DateTimeFormatter.ofPattern("yyyyMMdd"));
        long todayCount = paymentRepository.countByPaymentDate(today);
        
        return "REC" + datePart + String.format("%06d", todayCount + 1);
    }
    private String generateReceiptNumber() {

        LocalDate today = LocalDate.now();
        String datePart =today.format(DateTimeFormatter.ofPattern("yyyyMMdd"));
        long todayCount =paymentRepository.countByPaymentDate(today);

        return "RCP"+ datePart+ String.format("%06d", todayCount + 1);
    }

}