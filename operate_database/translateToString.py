from pymongo import MongoClient
#连接数据库
client=MongoClient('localhost',27017)
db=client.smart_question_bank
users=db.users
for user in users.find():
    users.update_one({'_id':user['_id']},{'$set':{'student_id':user['student_id'][:10]}})