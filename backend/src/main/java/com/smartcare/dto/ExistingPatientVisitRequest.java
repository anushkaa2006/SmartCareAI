package com.smartcare.dto;

public class ExistingPatientVisitRequest {
    private String patientId;
    private String department;

    public String getPatientId(){
        return patientId;
    }

    public void setPatientId(String patientId){
        this.patientId = patientId;
    }

    public String getDepartment(){
        return department;
    }
    public void setDepartment(String department){
        this.department = department;
    }
}

