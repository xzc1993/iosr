import os
import base64
import tornado.ioloop
import tornado.web
import tornado.gen
import tasks
import json

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class LoginHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        self.render( os.path.join( os.path.dirname(__file__), 'templates/login.html'))

    def post(self):
        if( self.get_argument("username")[0] == 'k' and self.get_argument("password")[0] == 'k'):
            self.set_secure_cookie('user', self.get_argument("username"))
            self.redirect(self.get_argument("next", "/"))
        else:
            raise tornado.web.HTTPError(403)

class LogoutHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    @tornado.web.authenticated
    def get(self):
        self.clear_cookie("user")
        self.redirect("/login")

class MainHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    @tornado.web.authenticated
    def get(self):
        self.render( os.path.join( os.path.dirname(__file__), 'templates/index.html'), filters=self.__getFilters())

    @tornado.web.authenticated
    def post(self):
        filters = json.loads(self.get_argument("selectedFilters"))
        fileinfo = self.request.files['filearg'][0]
        data = base64.b64encode(self.__processRequest(fileinfo['body'], filters))
        self.write(data)
        self.add_header('Content-Type', 'image/png,base64')
        self.finish()

    def __processRequest(self, imageData, filters):
        filters = self.__clearFilters(filters)
        for filter in filters:
            imageData = getattr(tasks, filter['filterName'])(imageData, **(filter.get('args', {})))
        return imageData

    def __clearFilters(self, filters):
        clearedFilters = list()
        for filter in filters:
            if 'filterName' in filter:
                del filter['$$hashKey']
                clearedFilters.append(filter)
        return clearedFilters

    def __getFilters(self):
        return tasks.filters.values()

def make_app():
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        "login_url": "/login",
        "xsrf_cookies": True,
        "debug": True,
        "autoreload": False,
    }
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
    ], **settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
