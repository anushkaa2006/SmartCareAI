package com.smartcare.service;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.smartcare.dto.DepartmentCheckInRequest;
import com.smartcare.dto.DepartmentCheckInResponse;
import com.smartcare.dto.VisitResponse;
import com.smartcare.model.Patient;
import com.smartcare.model.Payment;
import com.smartcare.model.Queue;
import com.smartcare.model.Visit;
import com.smartcare.repository.DepartmentRepository;
import com.smartcare.repository.PatientRepository;

import com.smartcare.repository.QueueRepository;
import com.smartcare.repository.VisitRepository;
import com.smartcare.enums.VisitStatus;

import com.smartcare.enums.CheckInAction;

import com.smartcare.model.Department;
import java.util.Optional;

@Service
public class VisitService {

    @Autowired
    private VisitRepository visitRepository;

    @Autowired
    private QueueRepository queueRepository;

    @Autowired
    private PatientRepository patientRepository;

    // @Autowired
    // private PaymentRepository paymentRepository;

    @Autowired
    private DepartmentRepository departmentRepository;

    @Autowired
    private PaymentValidationService paymentValidationService;

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


    public DepartmentCheckInResponse verifyDepartmentVisit(
            DepartmentCheckInRequest request
    ) {
        DepartmentCheckInResponse response =new DepartmentCheckInResponse();
        LocalDate today =  LocalDate.now();
        Optional<Visit> optionalVisit = visitRepository.findFirstByPatientIdAndVisitDate(request.getPatientId(), today);
        if (optionalVisit.isEmpty()) {

            response.setAction(CheckInAction.NO_VISIT_FOUND.name());

            response.setMessage("No active visit found for today.");

            return response;
        }

        Visit visit = optionalVisit.get();
        if (!visit.getDepartmentId().equals(request.getDepartmentId())) {

            response.setAction(CheckInAction.WRONG_DEPARTMENT.name());

            response.setMessage("Patient has an active visit for another department.");

            return response;
        }
   

        Optional<Queue> optionalQueue =queueRepository.findByVisitId(visit.getVisitId());
        System.out.println("Queue Found");

        if(optionalQueue.isEmpty()){

            throw new RuntimeException("Queue not found.");

        }

        Queue queue = optionalQueue.get();

        Patient patient = patientRepository.findById(visit.getPatientId()
            ).orElseThrow(() -> new RuntimeException("Patient not found."));
        

        Payment payment = paymentValidationService.getValidPayment(
                visit.getPatientId(),
                visit.getDepartmentId()
        );

        
        Department department = departmentRepository.findById(visit.getDepartmentId())
                .orElseThrow(() -> new RuntimeException("Department not found."));


            
        if (visit.getVisitStatus().equals(VisitStatus.ARRIVED.name())) {

            buildDepartmentCheckInResponse(response,patient,visit,queue,payment,department);

            response.setAction(CheckInAction.ALREADY_CHECKED_IN.name());

            response.setMessage("Patient has already checked in.");

            return response;
        }


        visit.setVisitStatus(VisitStatus.ARRIVED.name());
        visitRepository.save(visit);

        buildDepartmentCheckInResponse(response,patient,visit,queue,payment,department);
        response.setAction(CheckInAction.CHECK_IN_SUCCESS.name());

        response.setMessage( "Department Check-in Successful." );

        return response;
        
       
    }

    private void buildDepartmentCheckInResponse(

            DepartmentCheckInResponse response,

            Patient patient,

            Visit visit,

            Queue queue,

            Payment payment,

            Department department

    ) {

        response.setPatientId(patient.getPatientId());

        response.setPatientName(patient.getName());

        response.setVisitId(visit.getVisitId());

        response.setDepartmentId(visit.getDepartmentId());

        response.setDepartmentName(
                department.getDepartmentName()
        );

        response.setQueueNumber(
                queue.getQueueNumber()
        );

        response.setQueueStatus(
                queue.getQueueStatus()
        );

        response.setPaymentId(
                payment.getPaymentId()
        );

        response.setPaymentStatus(
                payment.getPaymentStatus()
        );

        response.setVisitStatus(
                visit.getVisitStatus()
        );

}
}