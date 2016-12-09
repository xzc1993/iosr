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
        response = yield tornado.gen.Task(tasks.add.apply_async, args=[3])
        self.write(str(response.result))
        self.finish()
        self.write("Hello world ")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
