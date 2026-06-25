package com.smartcare.Controller;



import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import com.smartcare.dto.VisitRequest;
import com.smartcare.dto.VisitResponse;
import com.smartcare.service.VisitService;

@RestController
@RequestMapping("/visits")
@CrossOrigin("*")
public class VisitController {

    @Autowired
    private VisitService visitService;

    
    @PostMapping("/create")
    public VisitResponse createVisit(@RequestBody VisitRequest request){
        return visitService.createVisit(request.getPatientId(),request.getDepartmentId());
    }
}
