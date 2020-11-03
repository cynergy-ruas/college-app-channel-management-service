package com.sadhana.channelmanagement.model;

import org.springframework.data.annotation.Id; //imports id
import org.springframework.data.mongodb.core.mapping.Document;//imports Document

//document annotation marks a class as an domain object that we want to connect to the database.
//It also allows us to choose the name of the collection we want to use.
@Document
public class Channel {
	//@Id annotation marks a field in a model class as the primary key.
	@Id
	String id;
	String name;
	String members;
	String type;
	String dp;
	String admins;
	
	//constructer of main class is created to intialize the object of the Channel class
	//assigning values to the instance variables 
	public Channel( String name, String members,String type,String dp,String admins) {
		this.name = name;
		this.members = members;
		this.type = type;
		this.dp = dp;
		this.admins = admins;
	}

	//We have created getters and setters methods. 
	//The getter method returns the value of the attribute. 
	//The setter method takes a parameter and assigns it to the attribute.

    public String getId() {
		return id;
	}
	
	public String getName() {
		return name;
	}
	
	public void setName(String name) {
		this.name = name;
	}
	
	public String getMembers() {
		return members;
	}
	
	public void setMembers(String members) {
		this.members = members;
	}
	
	public String getType() {
		return type;
	}
	
	public void setType(String type) {
		this.type = type;
	}
	
	public String getDp() {
		return dp;
	}
	
	public void setDp(String dp) {
		this.dp = dp;
	}
	
	public String getAdmins() {
		return admins;
	}
	
	public void setAdmins(String admins) {
		this.admins = admins;
	}

}
