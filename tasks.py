import datetime
import StringIO

from celery import Celery
from PIL import Image
from PIL import ImageFilter
from pymongo import MongoClient

app = Celery('tasks',
     backend='amqp://kotek:kotek@rabbitmq-1321755515.eu-west-1.elb.amazonaws.com//',
     broker='amqp://kotek:kotek@rabbitmq-1321755515.eu-west-1.elb.amazonaws.com//'
)

client = MongoClient(
    # 'ec2-54-154-102-56.eu-west-1.compute.amazonaws.com',
    # 'ec2-54-171-39-125.eu-west-1.compute.amazonaws.com',
    # 'ec2-54-154-102-29.eu-west-1.compute.amazonaws.com']
)


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
def takeCPU(time):
    start = time.time()
    while start + time > time.time():
        x = (1+3)/5
    return x


@app.task
@remoteImageConverter
def convertToGreyscale(image):
    return image.convert('L')


@app.task
@remoteImageConverter
def blur(image):
    return image.filter(ImageFilter.BLUR)





