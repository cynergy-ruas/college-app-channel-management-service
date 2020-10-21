package com.example.CynergySpringboot.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Document
public class CyNote {
	@Id
	String id;
	String title ;
	String description;
	
public CyNote(String title,String description) {
	this.title = title;
	this.description = description;
	
}

public String getTitle() {
	return title;
}

public void setTitle(String title) {
	this.title = title;
}

public String getDescription() {
	return description;
}

public void setDescription(String description) {
	this.description = description;
}

public String toString() {
	return "Note { title: "+title+" description: "+description+" }";
	
}
}
