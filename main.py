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
        return self.get_secure_cookie('account')

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
            self.set_secure_cookie('account',student['student_id'] + 'student',expires_days = 1)
            self.render('student_index.html',username = student['name'],page_title = '欢迎',tests =[{'title':'第一个试题'},{'title':'第二个试题'}])
        elif teacher and password == '123456':
            self.set_secure_cookie('account',teacher['teacher_id'] + 'teacher',expires_days = 1)
            self.render('teacher_index.html',username = teacher['name'],page_title = '欢迎',tests =[{'title':'第一个试题'},{'title':'第二个试题'}])
        else:
            self.render('login.html',message = '用户名或密码错误',account = account)

class TestHandler(BaseHandler):
    def get(self):
        self.render('test.html')

class WelcomeHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        if self.current_user[-7:] == b'student':
            student = yield self.application.db.students.find_one({'student_id':self.current_user[:-7].decode('utf-8')})
            self.render('student_index.html',username = student['name'],page_title = '欢迎',tests =[{'title':'第一个试题'},{'title':'第二个试题'}])
        else:
            teacher = yield self.application.db.teachers.find_one({'teacher_id':self.current_user[:-7].decode('utf-8')})
            self.render('teacher_index.html',username = teacher['name'],page_title = '欢迎',tests =[{'title':'第一个试题'},{'title':'第二个试题'}])

class TeacherTestAddedHandler(BaseHandler):
    @tornado.gen.coroutine
    @tornado.web.authenticated
    def get(self):
        teachers = self.application.db.teachers
        account = self.current_user[:-7].decode('utf-8')
        teacher = yield teachers.find_one({'teacher_id':account})
        self.render('teacher_test_added.html',username = teacher['name'],page_title = '已添加的习题',tests =[{'title':'第一个试题'},{'title':'第二个试题'}])

    @tornado.gen.coroutine
    def post(self):
        teachers = self.application.db.teachers
        account = self.current_user[:-7].decode('utf-8')
        teacher = yield teachers.find_one({'teacher_id':account})
        self.render('teacher_test_added.html',username = teacher['name'],page_title = '已添加的习题',tests =[{'title':'第一个试题'},{'title':'第二个试题'}])


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

class DoTestModule(tornado.web.UIModule):
    def render(self,add_test):
        return self.render_string(
            'modules/do_test.html',
            add_test = add_test
        )
    def css_files(self):
        return 'css/do_test.css'

    def javascript_files(self):
        return 'js/do_test.js'

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('account')
        self.redirect('/login')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
        (r'/',WelcomeHandler),
        (r'/test',TestHandler),
        (r'/login',LoginHandler),
        (r'/teacher_test_added',TeacherTestAddedHandler),
        (r'/logout',LogoutHandler),
    ]
        settings = {
        'template_path':os.path.join(os.path.dirname(__file__),'templates'),
        'static_path':os.path.join(os.path.dirname(__file__), "static"),
        'ui_modules':{'Test':TestModule,'DoTest':DoTestModule},
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