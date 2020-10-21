package com.example.CynergySpringboot.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.CynergySpringboot.model.CyNote;
import com.example.CynergySpringboot.repository.CyNoteRepository;

@Service
public class CyNoteService {
	
	@Autowired
	private  CyNoteRepository cyNoteRepository;
	
	//create operation
	public CyNote create(String title,String description ) {
		return cyNoteRepository.save(new CyNote (title,description));
	}
	//Retrieve 
	public List<CyNote> getAll(){
		return cyNoteRepository.findAll();
	}
	public CyNote getByTitle(String title) {
		return cyNoteRepository.findByTitle(title);
	}
	//Update operation
	public CyNote update(String title, String description) {
		CyNote p = cyNoteRepository.findByTitle(title);
		p.setDescription(description);
		return cyNoteRepository.save(p);
	}
	//Delete operation
	public void deleteAll() {
		cyNoteRepository.deleteAll();
	}

	public void delete(String title) {
		CyNote p = cyNoteRepository.findByTitle(title);
		cyNoteRepository.delete(p);
	}
	
}
