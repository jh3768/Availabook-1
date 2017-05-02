from django.db import models
from boto3.session import Session
import os
import sys
import json

"""reload intepretor, add credential path"""
reload(sys)
sys.setdefaultencoding('UTF8')

"""import credentials from root/AppCreds"""

print "path: " + os.path.dirname(sys.path[0])
with open(os.path.dirname(sys.path[0])+ '/Asite' + '/availabook/AppCreds/AWSAcct.json','r') as AWSAcct:
    awsconf = json.loads(AWSAcct.read())

dynamodb_session = Session(aws_access_key_id=awsconf["aws_access_key_id"],
              aws_secret_access_key=awsconf["aws_secret_access_key"],
              region_name="us-east-1")

dynamodb = dynamodb_session.resource('dynamodb')

user_table = dynamodb.Table("User")
event_table = dynamodb.Table("Event")
post_table = dynamodb.Table("Post")
# Create your models here.
class Users():
    #def __init__(self, id, passwd, passwd_again, firstname, lastname, age, city, zipcode):
    def __init__(self, id, passwd):
        self.id = id
        self.passwd = passwd
        #self.passwd_again = passwd_again
        #self.firstname = firstname
        #self.lastname = lastname
        #self.age = age
        #self.city = city
        #self.zipcode = zipcode
        self.verified = False


    def check_input_passwd(self, passwd, passwd_again):
        if passwd == passwd_again:
            return True
        else:
            return False

    def push_to_dynamodb(self, item):
        user_table.put_item(
            Item={
                'email': item['email'],
                'age': item['age'],
                'city':item['city'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'password': item['password'],
                'zipcode': item['zipcode'],
            }
        )

    def get_response_by_id(self, id):
        response = user_table.get_item(
            Key={
                'email': id
            }
        )
        return response

    def authen_user(self):
	    return self.verify_email() and self.verify_passwd()

    def verify_email(self):
    	#user_id = self.id
        response = self.get_response_by_id(self.id)
        if 'Item' in response:
            return True
        else:
            return False

    def verify_passwd(self):
    	#user_id = self.id
        response = self.get_response_by_id(self.id)
        item = response['Item']
        pwd = item['password']
        if pwd == self.passwd:
            return True
        else:
            return False
        return False

    def authorize(self):
        self.verified = True


class Event():
    def __init__(self,EId,content,date,time,label,like,place,):
        self.EId = EId  ### use hadhid, to be modify
        self.content = content
        self.date = date
        self.time = time
        self.label = label
        self.like = like
        self.place = place
        self.like_num = str(len(self.like))
    ### put function
    def put_into_db(self,timestamp,user_email):
        event_table.put_item(
        Item={
            'EId': self.EId,
            'content': self.content,
            'date': self.date,
            'time': self.time,
            'label': self.label,
            'like': self.like,
            'place': self.place,
        }
    )
        post_table.put_item(
        Item={
            'EId': self.EId,
            'email': user_email,
            'post_time': timestamp
        }
    )
    ### delete function
    def delete(EId):
        event_table.delete_item(
            Key={
                'EId': EId
            }
        )
    ### auxiliary function
    def add_like(user_email):
        self.like.append(user_email)
        self.like_num = str(len(self.like))

def get_event_list():
    ######## here need a iterator of dynamodb event table,then put them into event_list#######
    event_list = []
    response = event_table.scan(
    )
    tmp_list = response['Items']
    for e in tmp_list:
        event = Event(EId=e['EId'],content=e['content'],date=e['date'],time=e['time'],label=e['label'],like=e['like'],place=e['place'],)
        event_list.append(event)
    return event_list






