package com.ulca.dataset.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.ulca.dataset.request.DatasetSubmitRequest;
import com.ulca.dataset.response.DatasetListByUserIdResponse;
import com.ulca.dataset.response.DatasetSubmitResponse;
import com.ulca.dataset.service.DatasetService;

import lombok.extern.slf4j.Slf4j;



@Slf4j
@CrossOrigin(origins = "*", allowedHeaders = "*")
@RestController
@RequestMapping(value= "/dataset")
public class DatasetController {
	
	@Autowired
	DatasetService datasetService;
	
	@PostMapping("/corpus/submit")
	public DatasetSubmitResponse datasetSubmit(@RequestBody DatasetSubmitRequest request, @RequestHeader("userId") String userId) {
		
		
	    log.info("******** Entry DatasetController:: datasetSubmit *******" );
	    return datasetService.datasetSubmit(request, userId);
	  }

	@GetMapping("/publish/{name}")
	public String publishMessage(@PathVariable String name) {
		//template.send(topic, "Hi " + name + " Welcome to java techie");
		log.info("*********************");
		log.info("test publishmessage");
		return "Data published";
	}
	
	@GetMapping("/listByUserId")
	public List<DatasetListByUserIdResponse> listByUserId(@RequestParam String userId) {
		log.info("******** Entry DatasetController:: listByUserId *******" );
		
		return datasetService.dataSetListByUserId(userId);
	}

}
