import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import os.path
import base64,uuid
from pymongo import MongoClient
import tornado.gen
import motor.motor_tornado

from tornado.options import define,options
define('port',default = 8000 ,help='run on the given port',type=int)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('username')

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html',message = '',account = None)

    @tornado.gen.coroutine
    def post(self):
        account = self.get_argument('account')
        password = self.get_argument('password')
        teachers = self.application.db.teachers
        students = self.application.db.students
        student = yield students.find_one({'student_id':account})
        teacher = yield teachers.find_one({'teacher_id':account})
        if student and password == '123456':
            self.set_secure_cookie('username',student['name'] + 'student',expires_days = 1)
            self.render('index_student.html',username = student['name'],page_title = '欢迎',tests =[{'title':'第一个试题'},{'title':'第二个试题'}])
        elif teacher and password == '123456':
            self.set_secure_cookie('username',teacher['name'] + 'teacher',expires_days = 1)
            self.render('index_teacher.html',username = teacher['name'],page_title = '欢迎',tests =[{'title':'第一个试题'},{'title':'第二个试题'}])
        else:
            self.render('login.html',message = '用户名或密码错误',account = account)


class WelcomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if self.current_user[-7:] == 'student':
            self.render('index_student.html',username = self.current_user[:-7],page_title = '欢迎',tests =[{'title':'第一个试题'},{'title':'第二个试题'}])
        else:
            self.render('index_teacher.html',username = self.current_user[:-7],page_title = '欢迎',tests =[{'title':'第一个试题'},{'title':'第二个试题'}])

    def post(self):
        self.clear_cookie('username')
        self.render('login.html',message = '',account = None)
        #self.redirect('/')

class AddTestHandler(BaseHandler):
    def get(self):
        self.render('add_test.html')

class TestModule(tornado.web.UIModule):
    def render(self,test):
        return self.render_string(
            'modules/test.html',
            test = test,
        )

    def css_files(self):
        return 'css/test_list.css'

    def javascript_files(self):
        return 'js/test_list.js'


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
        (r'/',WelcomeHandler),
        (r'/login',LoginHandler),
        (r'/add_test',AddTestHandler)
    ]
        settings = {
        'template_path':os.path.join(os.path.dirname(__file__),'templates'),
        'static_path':os.path.join(os.path.dirname(__file__), "static"),
        'ui_modules':{'Test':TestModule},
        'cookie_secret':base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
        'xsrf_cookies':True,
        'login_url':'/login',
        'debug':True
    }
        #client=MongoClient('localhost',27017)
        client = motor.motor_tornado.MotorClient('mongodb://localhost:27017/')
        self.db = client.smart_question_bank
        tornado.web.Application.__init__(self,handlers,**settings)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()