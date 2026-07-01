package com.smartcare.service;

import com.smartcare.dto.PatientRequest;
import com.smartcare.dto.PatientResponse;
import com.smartcare.model.Patient;
import com.smartcare.model.Queue;
import com.smartcare.model.Visit;
import com.smartcare.repository.PatientRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import com.smartcare.repository.VisitRepository;
import com.smartcare.repository.QueueRepository;


@Service
public class PatientService {
    
    @Autowired
    private PatientRepository patientRepository;

     @Autowired
    private VisitRepository visitRepository;

    @Autowired
    private QueueRepository queueRepository;

    public PatientResponse registerPatient(PatientRequest request) {
       Patient patient = new Patient();
       patient.setPatientId(generatePatientId());
       patient.setName(request.getName());
       patient.setFatherSpouseName(request.getFatherSpouseName());
       patient.setAge(request.getAge());
       patient.setGender(request.getGender());
       patient.setCategory(request.getCategory());
       patient.setDob(request.getDob());
       patient.setPhone(request.getPhone());
       patient.setAddress(request.getAddress());
       patient.setState(request.getState());
       patient.setDistrict(request.getDistrict());
       patient.setPincode(request.getPincode());
            
        patient.setRegistrationDate(
                LocalDate.now().format(DateTimeFormatter.ofPattern("yyyyMMdd"))
            );
            
            patientRepository.save(patient);

        Visit visit = new Visit();

        LocalDate today = LocalDate.now();

        Long lastSequence =
                    visitRepository.findMaxSequenceForDate(today);

        long nextSequence =(lastSequence == null)? 1 : lastSequence + 1;

        visit.setVisitSequence(nextSequence);

        visit.setVisitId(generateVisitId(nextSequence));

        visit.setPatientId(patient.getPatientId());

        visit.setVisitDate(today);

        visit.setDepartmentId(request.getDepartment());

        visit.setVisitStatus("ACTIVE");
                                

        visit.setRegistrationDate(LocalDate.now().format(DateTimeFormatter.ofPattern("yyyyMMdd")) );
   
        visitRepository.save(visit);

            Queue queue = new Queue();
            queue.setQueueId(generateQueueId());
            queue.setVisitId(visit.getVisitId());
            queue.setDepartmentId(request.getDepartment());
            Integer lastQueue =queueRepository.findLastQueueNumber(request.getDepartment(),LocalDate.now() );

            int nextQueue =(lastQueue == null) ? 1: lastQueue + 1;

            queue.setQueueNumber(nextQueue);

            queue.setQueueDate(LocalDate.now());
            queue.setQueueStatus(("WAITING"));
            queue.setRegistrationDate(LocalDate.now().format(DateTimeFormatter.ofPattern("yyyyMMdd")));
            queueRepository.save(queue);

            System.out.println("VISIT SAVED : " + visit.getVisitId());

            return new PatientResponse( patient.getPatientId(), visit.getVisitId(), "Registration successful",queue.getQueueNumber(), request.getDepartment());
               
        }
    private String generatePatientId() {

        LocalDate today =LocalDate.now();
                

        String datePart =today.format(DateTimeFormatter.ofPattern(  "yyyyMMdd"  ));

        long todayCount = patientRepository.countByRegistrationDate(datePart);
                
        long sequence =todayCount + 1;
                

        String sequencePart =String.format( "%06d",sequence);

        return datePart + sequencePart;
    }


    private String generateVisitId(Long sequence) {

            String datePart =LocalDate.now().format( DateTimeFormatter.ofPattern("yyyyMMdd") );

            return "VID" + datePart +String.format("%06d", sequence);
        }
   
    private String generateQueueId() {

            String datePart = LocalDate.now().format( DateTimeFormatter.ofPattern("yyyyMMdd"));

            long count =queueRepository.countByRegistrationDate(datePart );

            return "QID" +datePart + String.format("%06d", count + 1);
        }


        public PatientResponse createVisitForExistingPatient(
            String patientId,
            String department
        ){
            Visit visit = new Visit();

        LocalDate today = LocalDate.now();

        Long lastSequence =
                    visitRepository.findMaxSequenceForDate(today);

        long nextSequence =(lastSequence == null)? 1 : lastSequence + 1;

        visit.setVisitSequence(nextSequence);

        visit.setVisitId(generateVisitId(nextSequence));

        visit.setPatientId(patientId);

        visit.setVisitDate(today);

        visit.setDepartmentId(department);

        visit.setVisitStatus("ACTIVE");
                                

        visit.setRegistrationDate(LocalDate.now().format(DateTimeFormatter.ofPattern("yyyyMMdd")) );
   
        visitRepository.save(visit);

            Queue queue = new Queue();
            queue.setQueueId(generateQueueId());
            queue.setVisitId(visit.getVisitId());
            queue.setDepartmentId(department);
            Integer lastQueue =queueRepository.findLastQueueNumber(department,LocalDate.now() );

            int nextQueue =(lastQueue == null) ? 1: lastQueue + 1;

            queue.setQueueNumber(nextQueue);

            queue.setQueueDate(LocalDate.now());
            queue.setQueueStatus(("WAITING"));
            queue.setRegistrationDate(LocalDate.now().format(DateTimeFormatter.ofPattern("yyyyMMdd")));

            queueRepository.save(queue);
            
            return new PatientResponse(
            patientId,
            visit.getVisitId(),
            "Visit Generated Successfully",
            queue.getQueueNumber(),
            department
            );
        }

    public Patient checkExistingPatient(
        String name,
        String fatherSpouseName,
        String dob,
        String phone
    ){
        System.out.println("Searching:");
        System.out.println("Name = " + name);
        System.out.println("Father = " + fatherSpouseName);
        System.out.println("DOB = " + dob);
        System.out.println("Phone = " + phone);

        Patient patient = patientRepository.findByNameAndFatherSpouseNameAndDobAndPhone(
                name,
                fatherSpouseName,
                dob,
                phone
        );

        System.out.println("Found = " + patient);

        return patient;
    }  
}
