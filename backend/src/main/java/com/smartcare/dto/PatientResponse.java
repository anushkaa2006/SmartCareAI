package com.smartcare.dto;

public class PatientResponse {

    private String patientId;
    private String message;
    private String visitId;
    private Integer queueNumber;
    private String department;

    public PatientResponse() {
    }

    public PatientResponse(
            String patientId,
            String visitId,
            String message,
            Integer queueNumber,
            String department
    ) {

        this.patientId = patientId;
        this.visitId = visitId;
        this.message = message;
        this.queueNumber = queueNumber;
        this.department= department;
    }

    public String getPatientId() {
        return patientId;
    }

    public void setPatientId(String patientId) {
        this.patientId = patientId;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }
    public String getVisitId() {
    return visitId;
}

    public void setVisitId(String visitId) {
        this.visitId = visitId;
    }
    public Integer getQueueNumber(){
        return queueNumber;
    }
    public void setQueueNumber(Integer queueNumber){
        this.queueNumber = queueNumber;
    }
    public String getDepartment(){
        return department;
    }
    public void setDepartment(String department){
        this.department = department;
    }
}
