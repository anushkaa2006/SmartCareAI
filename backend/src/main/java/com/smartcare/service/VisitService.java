package com.smartcare.service;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.smartcare.dto.VisitResponse;
import com.smartcare.model.Queue;
import com.smartcare.model.Visit;
import com.smartcare.repository.QueueRepository;
import com.smartcare.repository.VisitRepository;
import com.smartcare.enums.VisitStatus;

@Service
public class VisitService {

    @Autowired
    private VisitRepository visitRepository;

    @Autowired
    private QueueRepository queueRepository;

    public VisitResponse createVisit(
            String patientId,
            String departmentId
    ) {

        LocalDate today = LocalDate.now();

        Long lastSequence =visitRepository.findMaxSequenceForDate(today);

        long nextSequence =(lastSequence == null)? 1: lastSequence + 1;

        Visit visit = new Visit();

        visit.setVisitSequence(nextSequence);

        visit.setVisitId(generateVisitId(nextSequence) );

        visit.setPatientId(patientId);

        visit.setVisitDate(today);

        visit.setDepartmentId(departmentId);

        visit.setVisitStatus(VisitStatus.REGISTERED.name());

        visit.setRegistrationDate(today.format(DateTimeFormatter.ofPattern("yyyyMMdd")) );

        visitRepository.save(visit);

        Queue queue = new Queue();

        queue.setQueueId(generateQueueId());

        queue.setVisitId(visit.getVisitId());

        queue.setDepartmentId(departmentId);

        Integer lastQueue =queueRepository.findLastQueueNumber(departmentId,today );

        int nextQueue =(lastQueue == null)? 1: lastQueue + 1;

        queue.setQueueNumber(nextQueue);

        queue.setQueueDate(today);

        queue.setQueueStatus("WAITING");

        queue.setRegistrationDate(today.format(DateTimeFormatter.ofPattern("yyyyMMdd")));

        queueRepository.save(queue);

        return new VisitResponse(
                patientId,
                visit.getVisitId(),
                queue.getQueueNumber(),
                departmentId
        );
    }

    private String generateVisitId( Long sequence ) {

        String datePart = LocalDate.now().format(DateTimeFormatter.ofPattern("yyyyMMdd"));

        return "VID" + datePart +String.format("%06d", sequence);
    }

    private String generateQueueId() {

        String datePart = LocalDate.now().format(DateTimeFormatter.ofPattern("yyyyMMdd"));

        long count =queueRepository.countByRegistrationDate(datePart);

        return "QID" +datePart +String.format("%06d", count + 1);
    }
}