package com.smartcare.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.smartcare.model.DepartmentFee;

@Repository
public interface DepartmentFeeRepository
        extends JpaRepository<DepartmentFee, String> {

}