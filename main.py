import tornado.ioloop
import tornado.web
import tornado.gen
import tasks
import tcelery

tcelery.setup_nonblocking_producer()

class MainHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        print 'Executing task'
        result = tasks.add.apply_async([4, 5])
        message = "Hello world {}".format(result.get(timeout=10))
        print (message)
        self.write(message)
        self.finish()

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
