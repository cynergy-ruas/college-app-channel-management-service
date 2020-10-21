package com.example.CynergySpringboot.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.example.CynergySpringboot.model.CyNote;
import com.example.CynergySpringboot.service.CyNoteService;

@RestController
public class CyNoteController {
	
	@Autowired
	private CyNoteService cyNoteService;
	
	@RequestMapping("/create")
	public String create(@RequestParam String title, @RequestParam String description ) {
		CyNote p = cyNoteService.create(title,description);
		return p.toString();
	}
	
	@RequestMapping("/get")
	public CyNote getCyNote(@RequestParam String title) {
		return cyNoteService.getByTitle(title);
	}
	
	@RequestMapping("/getAll")
	public List<CyNote> getAll(){
		return cyNoteService.getAll();
	}

	@RequestMapping("/update")
	public String update(@RequestParam String title, @RequestParam String description) {
		CyNote p = cyNoteService.update(title,description);
		return p.toString();
	}
	
	@RequestMapping("/delete")
	public String delete(@RequestParam String title) {
		cyNoteService.delete(title);
		return "Deleted "+title;
	}

	@RequestMapping ("/deleteAll")
	public String deleteAll() {
		cyNoteService.deleteAll();
		return "Deleted all records";
	}
}
