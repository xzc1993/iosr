import datetime
import time
import StringIO

from celery import Celery
from PIL import Image
from PIL import ImageFilter
from pymongo import MongoClient
from functools import wraps

app = Celery('tasks',
     backend='amqp://kotek:kotek@rabbitmq-1321755515.eu-west-1.elb.amazonaws.com//',
     broker='amqp://kotek:kotek@rabbitmq-1321755515.eu-west-1.elb.amazonaws.com//'
)

client = MongoClient([
     'ec2-54-154-185-177.eu-west-1.compute.amazonaws.com',
     'ec2-54-171-78-179.eu-west-1.compute.amazonaws.com',
     'ec2-54-229-174-78.eu-west-1.compute.amazonaws.com'
])

filters = {
    'takeCPU' : {
        'id' : 'takeCPU',
        'args': [{
            'name': 'period',
            'type': 'number',
            'label': 'Period [s]:',
            'default': 10,
        }]
    },
    'rotate': {
        'id': 'rotate',
        'args': [{
            'name': 'angle',
            'type': 'number',
            'label': 'Angle:',
            'default': 45,
        }]
    }
}

@app.task
def add(x, y):
    db = client.primer
    coll = db.log
    coll.insert_one({
        "a" : x,
        "b" : y,
        'timestamp' : datetime.datetime.utcnow()
    })
    return x + y + 1000

def remoteImageConverter(fn):
    if fn.__name__ not in filters:
        filters[fn.__name__] = {
            "id": fn.__name__
        }
    @wraps(fn)
    def wrappedConverter(imageData, *args, **kwars):
        buff = StringIO.StringIO(imageData)
        buff.seek(0)
        image = Image.open(buff)
        convertedImage = fn(image, *args, **kwars)
        buff = StringIO.StringIO()
        convertedImage.save(buff, format="PNG")
        outputImageData = buff.getvalue()
        buff.close()
        logToDatabase(fn.__name__)
        return outputImageData
    return wrappedConverter


def logToDatabase(operationName):
    db = client.iosr
    coll = db.log
    coll.insert_one({
        'operationName': operationName,
        'timestamp': datetime.datetime.utcnow(),
    })

@app.task
@remoteImageConverter
def takeCPU(image, period=10):
    start = time.time()
    while start + period > time.time():
        x = (1+3)/5
    return image


@app.task
@remoteImageConverter
def rotate(image, angle):
    return image.rotate(angle)


@app.task
@remoteImageConverter
def convertToGreyscale(image):
    return image.convert('L')


@app.task
@remoteImageConverter
def blur(image):
    return image.filter(ImageFilter.BLUR)


@app.task
@remoteImageConverter
def contour(image):
    return image.filter(ImageFilter.CONTOUR)



