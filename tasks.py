import time
from celery import Celery

app = Celery('tasks', backend='amqp://guest@ec2-54-154-186-239.eu-west-1.compute.amazonaws.com//', broker='amqp://guest@ec2-54-154-186-239.eu-west-1.compute.amazonaws.com//')

@app.task
def add(x, y):
    return x + y

@app.task
def sleep(seconds):
    time.sleep(float(seconds))
    return seconds

if __name__ == "__main__":
    app.start()