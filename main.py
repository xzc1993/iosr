import os

import tornado.ioloop
import tornado.web
import tornado.gen
import tasks

class MainHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        self.render( os.path.join( os.path.dirname(__file__), 'templates/index.html'))

    def post(self):
        print 'Executing task'
        result = tasks.add.apply_async([int(self.get_argument("a")), int(self.get_argument("b"))])
        message = "Hello world and sum is {}".format(result.get(timeout=10))
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
