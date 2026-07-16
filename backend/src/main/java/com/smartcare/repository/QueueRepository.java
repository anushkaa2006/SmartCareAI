package com.smartcare.repository;
import com.smartcare.model.Queue;
import java.time.LocalDate;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository

public interface QueueRepository
        extends JpaRepository<Queue,String> {

    long countByRegistrationDate(
            String registrationDate
    );

    long countByDepartmentIdAndRegistrationDate(
            String departmentId,
            String registrationDate
    );

    @Query("""
        SELECT MAX(q.queueNumber)
        FROM Queue q
        WHERE q.departmentId = :departmentId
        AND q.queueDate = :queueDate
    """)
    Integer findLastQueueNumber(
            String departmentId,
            LocalDate queueDate
    );

    Optional<Queue> findByVisitId(String visitId);
}