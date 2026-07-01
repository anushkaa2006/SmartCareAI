package com.smartcare.repository;

import com.smartcare.model.Department;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface DepartmentRepository
        extends JpaRepository<Department,String> {

Department findByDepartmentName(String departmentName);
        }
