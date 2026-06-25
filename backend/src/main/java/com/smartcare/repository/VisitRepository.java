package com.smartcare.repository;

import com.smartcare.model.Visit;

import java.time.LocalDate;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

@Repository
public interface VisitRepository extends JpaRepository<Visit,String> {

        @Query("""
            SELECT MAX(v.visitSequence)
            FROM Visit v
            WHERE v.visitDate = :visitDate
        """)
        Long findMaxSequenceForDate(LocalDate visitDate);
}