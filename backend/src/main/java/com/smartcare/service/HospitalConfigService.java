package com.smartcare.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.smartcare.model.HospitalConfig;
import com.smartcare.repository.HospitalConfigRepository;

@Service
public class HospitalConfigService {

    @Autowired
    private HospitalConfigRepository repository;

    public HospitalConfig getConfiguration() {

        HospitalConfig config = repository.findByActive("Y");

        if(config == null){
            throw new RuntimeException("Hospital configuration not found.");
        }

        return config;
    }

    public Integer getPaymentFlag() {
        return getConfiguration().getPaymentFlag();
    }

    public Integer getValidityDays() {
        return getConfiguration().getValidityDays();
    }

    public String getHospitalName() {
        return getConfiguration().getHospitalName();
    }
}