package com.sadhana.channelmanagement.service;

import java.util.List;//imports Lists

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.sadhana.channelmanagement.repository.ChannelRepository;
import com.sadhana.channelmanagement.model.Channel;

//Service Components are the class file which contains @Service annotation.
// These class files are used to write business logic in a different layer, 
//separated from @RestController class file
@Service
public class ChannelService {
	
	@Autowired
	//creating an object instance of ChannelRepositary Class
	private ChannelRepository channelRepository;
	
//create
//	public Channel create(String name,String members ,String type, String dp, String admins) {
//		return channelRepository.save(new Channel(name,members,type,dp,admins));
//	}

	//gets all channel
	public List<Channel> getAll(){
		return channelRepository.findAll();
	}

	//gets a channel by its name
	public Channel getByName(String name) {
		return channelRepository.findByName(name);	
	}
	
	//deletes all channels
	public void deleteAll() {
		channelRepository.deleteAll();
	}

	//deletes a channel by its name
	public void delete(String name) {
		Channel c = channelRepository.findByName(name);
		channelRepository.delete(c);
	}

	//creates a new channel
	public Channel createaChannel(Channel channel) {
		// TODO Auto-generated method stub		
		return channelRepository.insert(channel);
    }
}
