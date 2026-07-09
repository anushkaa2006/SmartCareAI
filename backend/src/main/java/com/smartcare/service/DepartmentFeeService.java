package com.smartcare.service;

import java.math.BigDecimal;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.smartcare.model.DepartmentFee;
import com.smartcare.repository.DepartmentFeeRepository;

@Service
public class DepartmentFeeService {

    @Autowired
    private DepartmentFeeRepository repository;

    public BigDecimal getConsultationFee(String departmentId){

        DepartmentFee fee =
                repository.findByDepartmentId(departmentId);

        if(fee == null){
            throw new RuntimeException("Department fee not configured.");
        }

        return fee.getConsultationFee();
    }

}