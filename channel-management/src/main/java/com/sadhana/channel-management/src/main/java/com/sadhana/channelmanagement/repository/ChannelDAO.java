//package com.sadhana.channelmanagement.repository;
//
//import org.springframework.beans.factory.annotation.Autowired;
//import org.springframework.stereotype.Component;
//import com.sadhana.channelmanagement.model.Channel;
//
//import java.util.Collection;
//import java.util.Optional;
//
//@Component
//public class ChannelDAO {
//	
//	@Autowired
//	private ChannelRepository channelRepository;
//
//	    public Collection<Channel> getChannels() {
//	        return channelRepository.findAll();
//	    }
//
//	    public Channel createChannel(Channel channel) {
//	        return channelRepository.insert(channel);
//	    }
//
//	    public Optional<Channel> getChannelById(String id) {
//	        return channelRepository.findById(id);
//	    }
//
//	    public Optional<Channel> deleteBookById(int id) {
//	         Optional<Channel> channel = channelRepository.findById(id);
//	         channel.ifPresent(b -> channelRepository.delete(b));
//	         return channel;
//	    }
//
//	    public Optional<Channel> updateChannelBookById(int id, BookUpdatePayload bookUpdatePayload) {
//	        Optional<Book> book = channelRepository.findById(id);
//	        book.ifPresent(b -> b.setTitle(bookUpdatePayload.getTitle()));
//	        book.ifPresent(b -> b.setAuthor(bookUpdatePayload.getAuthor()));
//	        book.ifPresent(b -> channelRepository.save(b));
//	        return book;
//	    }
//	}
//
//
//
