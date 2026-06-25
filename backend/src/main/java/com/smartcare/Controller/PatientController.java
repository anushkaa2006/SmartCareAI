package com.smartcare.Controller;

import com.smartcare.dto.FaceDataRequest;
import com.smartcare.dto.PatientRequest;
import com.smartcare.dto.PatientResponse;
import com.smartcare.model.FaceData;
import com.smartcare.model.Patient;
import com.smartcare.repository.FaceDataRepository;
import com.smartcare.service.PatientService;
import java.util.List;
import com.smartcare.repository.PatientRepository;

import java.time.LocalDate;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/patients")
public class PatientController {
    @Autowired
    private PatientService patientService;

    @Autowired
    private FaceDataRepository faceDataRepository;

    @Autowired
    private PatientRepository patientRepository;    

    @PostMapping("/register")
    public PatientResponse registerPatient(@RequestBody PatientRequest request) {
        return patientService.registerPatient(request);
    }
    @PostMapping("/face/save")
    public String saveFace(@RequestBody FaceDataRequest request) {
            

        FaceData faceData = new FaceData();

        faceData.setFaceId(UUID.randomUUID().toString());

        faceData.setPatientId(request.getPatientId());

        faceData.setImagePath(request.getImagePath());

        faceData.setEmbeddingVector(request.getEmbeddingVector());

        faceData.setEnrollmentDate(LocalDate.now().toString());

        System.out.println("Patient ID: " + request.getPatientId());

        System.out.println("Embedding Length: "+ request.getEmbeddingVector().length());
                        

        System.out.println("First 100 chars: " + request.getEmbeddingVector().substring(0, 100));
                       

        faceDataRepository.save(faceData);

        return "Face Saved Successfully";
        }
        @GetMapping("/faces")
        public List<FaceData> getAllFaces() {
                return faceDataRepository.findAll();
        }
        @GetMapping("/{patientId}")
        public Patient getPatientById(@PathVariable String patientId) {

                return patientRepository.findById(patientId).orElse(null);
        }

}
