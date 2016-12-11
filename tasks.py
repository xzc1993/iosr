from celery import Celery
from pymongo import MongoClient
from datetime import datetime

app = Celery('tasks',
             backend='amqp://kotek:kotek@rabbitmq-1321755515.eu-west-1.elb.amazonaws.com//',
             broker='amqp://kotek:kotek@rabbitmq-1321755515.eu-west-1.elb.amazonaws.com//'
             )

@app.task
def add(x, y):
    client = MongoClient("mongodb://mongo-1541864808.eu-west-1.elb.amazonaws.com:27017")
    db = client.primer
    coll = db.log
    coll.insert_one({
        "a" : x,
        "b" : y,
        'timestamp' : datetime.utcnow()
    })
    return x + y + 1000


