package com.smartcare.dto;

import java.math.BigDecimal;
import java.time.LocalDate;



public class PaymentValidationResponse {

    private boolean paymentRequired;

    private BigDecimal consultationFee;

    private String billingPolicy;

    private String message;

    private Integer validityDays;

    private LocalDate validTill;

    private String action;

    public boolean isPaymentRequired() {
        return paymentRequired;
    }

    public void setPaymentRequired(boolean paymentRequired) {
        this.paymentRequired = paymentRequired;
    }

    public BigDecimal getConsultationFee() {
        return consultationFee;
    }

    public void setConsultationFee(BigDecimal consultationFee) {
        this.consultationFee = consultationFee;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public Integer getValidityDays() {
        return validityDays;
    }

    public void setValidityDays(Integer validityDays) {
        this.validityDays = validityDays;
    }

    public String getBillingPolicy() {
        return billingPolicy;
    }

    public void setBillingPolicy(String billingPolicy) {
        this.billingPolicy = billingPolicy;
    }
    public LocalDate getValidTill(){
        return validTill;
    }
    public void setValidTill(LocalDate validTill){
        this.validTill = validTill;
    }
    public String getAction(){
        return action;
    }
    public void setAction(String action){
        this.action =action;
    }
}