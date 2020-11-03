package com.sadhana.channelmanagement.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import com.sadhana.channelmanagement.model.Channel;

//As our domain repository extends MongoRepository springboot provides you 
//with CRUD operations as well as methods for access to the entities.
// Working with the repository instance is just a matter of dependency injecting it into a client. 
@Repository
public interface ChannelRepository extends MongoRepository<Channel, String>{
	//public Channel findBytheId(String id);
	//public Optional<Channel> findById(String id);
	public Channel findByName(String name);
		
	}

