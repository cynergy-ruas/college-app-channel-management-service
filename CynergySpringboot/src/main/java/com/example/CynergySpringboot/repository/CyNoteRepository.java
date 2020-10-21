package com.example.CynergySpringboot.repository;

import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import com.example.CynergySpringboot.model.CyNote;

@Repository
public interface CyNoteRepository extends MongoRepository<CyNote,String>{
	public CyNote findByTitle(String title);
	public List<CyNote> findByDescription(String description);
}
