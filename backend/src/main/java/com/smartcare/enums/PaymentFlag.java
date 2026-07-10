package com.smartcare.enums;

public enum PaymentFlag {

    HOSPITAL_WISE(1),
    DEPARTMENT_WISE(2);

    private final int value;

    PaymentFlag(int value){
        this.value = value;
    }

    public int getValue(){
        return value;
    }
}