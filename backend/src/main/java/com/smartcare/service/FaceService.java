package com.smartcare.service;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.smartcare.dto.FaceDataRequest;
import com.smartcare.model.FaceData;
import com.smartcare.repository.FaceDataRepository;

@Service
public class FaceService {

    @Autowired
    private FaceDataRepository faceDataRepository;

    public String saveFace(FaceDataRequest request) {

        FaceData faceData = new FaceData();

        faceData.setFaceId(UUID.randomUUID().toString());
        faceData.setPatientId(request.getPatientId());
        faceData.setImagePath(request.getImagePath());
        faceData.setEmbeddingVector(request.getEmbeddingVector());
        faceData.setEnrollmentDate(LocalDate.now().toString());

        faceDataRepository.save(faceData);

        return "Face Saved Successfully";
    }

    public String updateFace(FaceDataRequest request) {

        FaceData faceData =
                faceDataRepository.findByPatientId(request.getPatientId());

        if (faceData == null) {
            return "Face record not found";
        }

        faceData.setImagePath(request.getImagePath());
        faceData.setEmbeddingVector(request.getEmbeddingVector());
        faceData.setEnrollmentDate(LocalDate.now().toString());

        faceDataRepository.save(faceData);

        return "Face Updated Successfully";
    }

    public List<FaceData> getAllFaces() {
        return faceDataRepository.findAll();
    }
}