package com.smartcare.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.smartcare.model.HospitalConfig;

@Repository
public interface HospitalConfigRepository
        extends JpaRepository<HospitalConfig, Integer> {

}