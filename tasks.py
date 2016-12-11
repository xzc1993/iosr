from celery import Celery
from pymongo import MongoClient
from datetime import datetime

app = Celery('tasks',
             backend='amqp://kotek:kotek@rabbitmq-1321755515.eu-west-1.elb.amazonaws.com//',
             broker='amqp://kotek:kotek@rabbitmq-1321755515.eu-west-1.elb.amazonaws.com//'
             )

@app.task
def add(x, y):
    client = MongoClient([
        'ec2-54-154-102-56.eu-west-1.compute.amazonaws.com',
        'ec2-54-171-39-125.eu-west-1.compute.amazonaws.com',
        'ec2-54-154-102-29.eu-west-1.compute.amazonaws.com']
    )
    db = client.primer
    coll = db.log
    coll.insert_one({
        "a" : x,
        "b" : y,
        'timestamp' : datetime.utcnow()
    })
    return x + y + 1000


client = MongoClient([
    'ec2-54-154-102-56.eu-west-1.compute.amazonaws.com',
    'ec2-54-171-39-125.eu-west-1.compute.amazonaws.com',
    'ec2-54-154-102-29.eu-west-1.compute.amazonaws.com']
)
db = client.primer
coll = db.log
coll.insert_one({
    "a": 1,
    "b": 2,
    'timestamp': datetime.utcnow()
})