from celery import Celery

app = Celery('tasks', backend='amqp://kotek:kotek@ec2-54-154-186-239.eu-west-1.compute.amazonaws.com//', broker='amqp://kotek:kotek@ec2-54-154-186-239.eu-west-1.compute.amazonaws.com//')

@app.task
def add(x, y):
    return x + y


