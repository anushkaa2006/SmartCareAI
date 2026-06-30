package com.smartcare.dto;

public class ExistingPatientCheckRequest {
    private String name;
    private String fatherSpouseName;
    private String dob;
    private String phone;


    public String getName(){
        return name;
    }
    public void setName(String name){
        this.name = name;
    }
    public String getFatherSpouseName(){
        return fatherSpouseName;
    }
    public void setFatherSpouseName(String fatherSpouseName){
        this.fatherSpouseName = fatherSpouseName;
    }
    public String getDob(){
        return dob;
    }
    public void setDob(String dob){
    this.dob = dob;
    }
    public String getPhone(){
        return phone;
    }
    public void setPhone(String phone){
        this.phone = phone;
    }
}
