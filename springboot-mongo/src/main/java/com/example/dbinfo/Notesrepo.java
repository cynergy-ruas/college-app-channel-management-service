package com.example.dbinfo;


import com.example.model.NotesCollection;

import org.springframework.data.mongodb.repository.MongoRepository;

public interface Notesrepo extends MongoRepository<NotesCollection, String> {
}

