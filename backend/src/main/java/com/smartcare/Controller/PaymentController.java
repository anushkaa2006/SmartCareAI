package com.smartcare.Controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.smartcare.dto.PaymentRequest;
import com.smartcare.dto.PaymentResponse;
import com.smartcare.dto.PaymentValidationRequest;
import com.smartcare.dto.PaymentValidationResponse;
import com.smartcare.model.Payment;
import com.smartcare.service.PaymentService;
import com.smartcare.service.PaymentValidationService;

@RestController
@RequestMapping("/payment")
@CrossOrigin("*")
public class PaymentController {

    @Autowired
    private PaymentValidationService paymentValidationService;

    @Autowired
    private PaymentService paymentService;

    @PostMapping("/validate")
    public PaymentValidationResponse validatePayment(
            @RequestBody PaymentValidationRequest request) {

        return paymentValidationService.validatePayment(request);
    }

    @PostMapping("/save")
    public PaymentResponse savePayment(
            @RequestBody PaymentRequest request) {

        return paymentService.savePayment(request);
    }

    @GetMapping("/latest")
    public ResponseEntity<PaymentResponse> getLatestPayment(
            @RequestParam String patientId,
            @RequestParam String departmentId
    ) {

        Payment payment = paymentService.getLatestPayment(patientId, departmentId);

        PaymentResponse response = new PaymentResponse();

        response.setPaymentId(payment.getPaymentId());
        response.setReceiptNumber(payment.getReceiptNumber());
        response.setAmount(payment.getAmount());
        response.setPaymentStatus(payment.getPaymentStatus());
        response.setPaymentMode(payment.getPaymentMode());
        response.setValidTill(payment.getValidTill());

        return ResponseEntity.ok(response);
    }
}