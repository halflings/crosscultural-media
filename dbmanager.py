#!/usr/bin/python

from pymongo import MongoClient



def get_db():
	client=MongoClient('localhost:27017')
	db=client.testDB
	return db

def add_post(db,post):
	db.crossculture.insert(post)

def get_post(db,searchFor):
	res=db.crossculture.find_one(searchFor)
	return res

def get_first(db):
	res=db.crossculture.find_one()
	return res

#testing
if __name__=="__main__":
	
	db=get_db();
	randomPost={"Name":"Random2","type":"Two"}
	add_post(db,randomPost)
	res=get_post(db,{"type":"Two"})
	print res
