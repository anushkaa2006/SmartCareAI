package com.smartcare.service;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.smartcare.dto.PaymentValidationRequest;
import com.smartcare.dto.PaymentValidationResponse;
import com.smartcare.enums.BillingPolicy;
import com.smartcare.enums.PaymentFlag;
import com.smartcare.enums.PaymentStatus;
import com.smartcare.enums.WorkflowAction;
import com.smartcare.model.HospitalConfig;
import com.smartcare.model.Payment;
import com.smartcare.repository.PaymentRepository;

@Service
public class PaymentValidationService {

    @Autowired
    private PaymentRepository paymentRepository;

    @Autowired
    private HospitalConfigService hospitalConfigService;

    @Autowired
    private DepartmentFeeService departmentFeeService;

    public PaymentValidationResponse validatePayment(PaymentValidationRequest request) {

        HospitalConfig config = hospitalConfigService.getConfiguration();

        if (config.getPaymentFlag() == PaymentFlag.HOSPITAL_WISE.getValue()) {
            return validateHospitalWise(request, config);
        }

        return validateDepartmentWise(request, config);
    }



    private PaymentValidationResponse validateHospitalWise(
            PaymentValidationRequest request,HospitalConfig config) {

        BigDecimal consultationFee =getConsultationFee(request.getDepartmentId());

        Optional<Payment> payment =
                paymentRepository
                        .findFirstByPatientIdAndPaymentStatusOrderByPaymentDateDesc(
                                request.getPatientId(),
                                PaymentStatus.SUCCESS.name());

        if (payment.isEmpty()) {

            return buildResponse(
                    true,
                    consultationFee,
                    "No previous payment found.",
                    config.getValidityDays(),
                    BillingPolicy.HOSPITAL_WISE,
                    null,
                    WorkflowAction.PAYMENT_REQUIRED
            );
        }

        Payment latestPayment = payment.get();

        if (!latestPayment.getValidTill().isBefore(LocalDate.now())) {

            return buildResponse(
                    false,
                    consultationFee,
                    "Previous payment is still valid.",
                    config.getValidityDays(),
                    BillingPolicy.HOSPITAL_WISE,
                    latestPayment.getValidTill(),
                    WorkflowAction.CONTINUE
            );
        }

        return buildResponse(
                true,
                consultationFee,
                "Payment validity has expired.",
                config.getValidityDays(),
                BillingPolicy.HOSPITAL_WISE,
                latestPayment.getValidTill(),
                WorkflowAction.PAYMENT_REQUIRED
        );
    }



    private PaymentValidationResponse validateDepartmentWise(
            PaymentValidationRequest request,HospitalConfig config) {

        BigDecimal consultationFee = getConsultationFee(request.getDepartmentId());

        Optional<Payment> payment =
                paymentRepository
                        .findFirstByPatientIdAndDepartmentIdAndPaymentStatusOrderByPaymentDateDesc(
                                request.getPatientId(),
                                request.getDepartmentId(),
                                PaymentStatus.SUCCESS.name());

        if (payment.isEmpty()) {

            return buildResponse(
                    true,
                    consultationFee,
                    "No previous payment found for this department.",
                    config.getValidityDays(),
                    BillingPolicy.DEPARTMENT_WISE,
                    null,
                    WorkflowAction.PAYMENT_REQUIRED
            );
        }

        Payment latestPayment = payment.get();

        if (!latestPayment.getValidTill().isBefore(LocalDate.now())) {

            return buildResponse(
                    false,
                    consultationFee,
                    "Department payment is still valid.",
                    config.getValidityDays(),
                    BillingPolicy.DEPARTMENT_WISE,
                    latestPayment.getValidTill(),
                    WorkflowAction.CONTINUE
            );
        }

        return buildResponse(
                true,
                consultationFee,
                "Department payment validity has expired.",
                config.getValidityDays(),
                BillingPolicy.DEPARTMENT_WISE,
                latestPayment.getValidTill(),
                WorkflowAction.PAYMENT_REQUIRED
        );
    }



    private PaymentValidationResponse buildResponse(
            boolean paymentRequired,
            BigDecimal consultationFee,
            String message,
            Integer validityDays,
            BillingPolicy billingPolicy,
            LocalDate validTill,
            WorkflowAction action) {

        PaymentValidationResponse response = new PaymentValidationResponse();

        response.setPaymentRequired(paymentRequired);
        response.setConsultationFee(consultationFee);
        response.setMessage(message);
        response.setValidityDays(validityDays);
        response.setBillingPolicy(billingPolicy.name());
        response.setValidTill(validTill);
        response.setAction(action.name());

        return response;
    }



    private BigDecimal getConsultationFee(String departmentId) {

        return departmentFeeService.getConsultationFee(departmentId);
    }
}