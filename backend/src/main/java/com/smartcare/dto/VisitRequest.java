package com.smartcare.dto;

public class VisitRequest {
    private String patientId;
    private String departmentId;

    public String getPatientId(){
        return patientId;
    }
    public void setPatientId(String patientId){
        this.patientId = patientId;
    }

    public String getDepartmentId(){
        return departmentId;
    }
    public void setDepartmentId(String departmentId){
        this.departmentId = departmentId;
    }
}
