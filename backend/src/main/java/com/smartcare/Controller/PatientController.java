package com.smartcare.Controller;

import com.smartcare.dto.FaceDataRequest;
import com.smartcare.dto.PatientRequest;
import com.smartcare.dto.PatientResponse;
import com.smartcare.model.FaceData;
import com.smartcare.model.Patient;
import com.smartcare.service.FaceService;
import com.smartcare.service.PatientService;
import com.smartcare.service.PatientVerificationService;

import java.util.List;
import com.smartcare.repository.PatientRepository;
import com.smartcare.dto.ExistingPatientCheckRequest;
import org.springframework.http.ResponseEntity;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/patients")
public class PatientController {
    @Autowired
    private PatientService patientService;

    @Autowired
    private PatientVerificationService patientVerificationService;

    @Autowired
    private FaceService faceService;

    @Autowired
    private PatientRepository patientRepository;        



    @PostMapping("/register/basic")
        public PatientResponse registerBasicPatient(@RequestBody PatientRequest request) {
        return patientService.registerBasicPatient(request);
        }

    @PostMapping("/face/save")
        public String saveFace(@RequestBody FaceDataRequest request) {
        return faceService.saveFace(request);
        }


        @PutMapping("/face/update")
                public String updateFace(@RequestBody FaceDataRequest request) {
                return faceService.updateFace(request);
                }


        @GetMapping("/faces")
                public List<FaceData> getAllFaces() {
                return faceService.getAllFaces();
        }
        @GetMapping("/{patientId}")
        public Patient getPatientById(@PathVariable String patientId) {

                return patientRepository.findById(patientId).orElse(null);
        }

       

        @PostMapping("/check-existing")
        public ResponseEntity<Patient> checkExistingPatient(@RequestBody ExistingPatientCheckRequest request){

                
                Patient patient = patientVerificationService.verifyByPersonalDetails(
                        request.getName(),
                        request.getFatherSpouseName(),
                        request.getDob(),
                        request.getPhone()
                );  
                 if(patient == null){
                        return ResponseEntity.noContent().build();  
                }

                return ResponseEntity.ok(patient);
        }

}
