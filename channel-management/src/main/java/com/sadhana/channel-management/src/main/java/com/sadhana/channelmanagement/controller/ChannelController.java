package com.sadhana.channelmanagement.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.sadhana.channelmanagement.model.Channel;
import com.sadhana.channelmanagement.service.ChannelService;

//Spring RestController annotation is used to create RESTful web services 
//using Spring MVC. 
//Spring RestController takes care of mapping request data to the defined 
//request handler method.
@RestController
//RequestMapping annotation maps HTTP requests to handler methods of MVC and 
//REST controllers.
@RequestMapping("/channel")
public class ChannelController {
	
	//The @Autowired annotation in spring automatically injects the dependent beans into the associated references of a POJO class. 
	//This annotation will inject the dependent beans by matching the data-type 
	@Autowired
	private ChannelService channelService;

	@PostMapping("/create")
	public Channel postChannel (@RequestBody Channel channel) {
		return channelService.createaChannel(channel);
	}
	
	@GetMapping("/get")
	public Channel getChannel(@RequestParam String name) {
		return channelService.getByName(name);
	}
	
	//getAll
	@GetMapping("/all")
	public List<Channel> getAll(){
		return channelService.getAll();
	}
	
	//update
//	@RequestMapping("/update")
//	public String update(@RequestParam String channelName,@RequestParam String channelId,@RequestParam String channelType) {
//		Channel c = channelService.update(channelName, channelId, channelType);
//		return c.toString();
//	}
	
	@DeleteMapping("/delete")
	public String delete(@RequestParam String name) {
		channelService.delete(name);
		return "Deleted "+name;
	}
	
	@DeleteMapping("/deleteAll")
	public String deleteAll() {
		channelService.deleteAll();
		return "Deleted  all info";
	}
	
	
	
}
