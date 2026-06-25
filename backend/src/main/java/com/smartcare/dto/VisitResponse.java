package com.smartcare.dto;

public class VisitResponse {
    private String patientId;
    private String visitId;
    private Integer queueNumber;
    private String department;

    public VisitResponse(
            String patientId,
            String visitId,
            Integer queueNumber,
            String department){

        this.patientId= patientId;
        this.visitId = visitId;
        this.queueNumber = queueNumber;
        this.department = department;
        }

        public String getPatientId(){
            return patientId;
        }
        public String getVisitId(){
            return visitId;
        }
        public Integer getQueueNumber(){
            return queueNumber;
        }
        public String getDepartment(){
            return department;
        }
}
