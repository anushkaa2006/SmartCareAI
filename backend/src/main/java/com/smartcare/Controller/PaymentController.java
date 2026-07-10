package com.smartcare.Controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import com.smartcare.dto.PaymentRequest;
import com.smartcare.dto.PaymentResponse;
import com.smartcare.dto.PaymentValidationRequest;
import com.smartcare.dto.PaymentValidationResponse;
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
}