import sys
sys.path.append("C:\\users\lenovo\\appdata\\local\\programs\\python\\python310\\lib\\site-packages")
from flask import Flask, render_template, request, abort, redirect, url_for
import config
import numpy as np
import datetime
from db_init import db, db2
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from models import User, Teachers, Papers, Projects, Courses, PublishingPapers, LeadingCourses, TakingProjects
# from models import User, Teachers, Papers
import time
import copy

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

cursor = db2.cursor()

gender = {1: '男', 2: '女'}
title = {1: '博士后', 2: '助教', 3: '讲师', 4: '副教授', 5: '特任教授', 6: '教授', 7: '助理研究员', 8: '特任副研究员', 9: '副研究员', 10: '特任研究员', 11: '研究员'}
paper_type = {1: 'full paper', 2: 'short paper', 3: 'poster paper', 4: 'demo paper'}
paper_level = {1: 'CCF-A', 2: 'CCF-B', 3: 'CCF-C', 4: '中文 CCF-A', 5: '中文 CCF-B', 6: '无级别'}
project_type = {1: '国家级项目', 2: '省部级项目', 3: '市厅级项目', 4: '企业合作项目', 5: '其它类型项目'}
course_type = {1: '本科生课程', 2: '研究生课程'}

def trans(dic):
    # return dic
    dic = copy.deepcopy(dic)
    for i in dic:
        if getattr(i, "性别", None): i.性别 = gender[i.性别]
        if getattr(i, "职称", None): i.职称 = title[i.职称]
        if getattr(i, "论文类型", None): i.论文类型 = paper_type[i.论文类型]
        if getattr(i, "级别", None): i.级别 = paper_level[i.级别]
        if getattr(i, "项目类型", None): i.项目类型 = project_type[i.项目类型]
        if getattr(i, "课程性质", None): i.课程性质 = course_type[i.课程性质]
    return dic      

@app.route('/')
def hello_world():
    return redirect( url_for('teacher') )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        if request.form.get('type') == 'signup':
            name = request.form.get('name')
            password = request.form.get('password')
            newUser = User(
                name=name,
                password=password,
            )
            db.session.add(newUser)
            db.session.commit()
            return render_template('login.html')
        elif request.form.get('type') == 'login':

            name = request.form.get('name')
            key = request.form.get('password')
            UserNotExist = db.session.query(User).filter_by(name=name).scalar() is None

            if UserNotExist == 1:
                error_title = '登录错误'
                error_message = '用户名不存在'
                return render_template('404.html', error_title=error_title, error_message=error_message)

            user_result = db.session.query(User).filter_by(name=name).first()
            if user_result.password == key:
                return render_template('index.html')
            else:
                error_title = '登录错误'
                error_message = '密码错误'
                return render_template('404.html', error_title=error_title, error_message=error_message)
    return render_template('login.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/teacher', methods=['GET', 'POST'])
def teacher():
    labels = ['工号', '姓名', '职称', '性别']
    result_query = db.session.query(Teachers)
    if request.method == 'POST':
        if request.form.get('type') == 'query':
            for i in range(len(labels)):
                req_id = request.form.get(labels[i])
                if req_id != "":
                    result_query = result_query.filter(Teachers.__table__.columns[labels[i]] == req_id)
        elif request.form.get('type') == 'delete':
            idx = request.form.get('key')
            teacher_result = db.session.query(Teachers).filter_by(工号=idx).first()
            db.session.delete(teacher_result)
            db.session.commit()
        elif request.form.get('type') == 'update':
            idx = request.form.get('key')
            teacher_result = db.session.query(Teachers).filter_by(工号=idx).first()
            for i in range(len(labels)):
                update_value = request.form.get(labels[i])
                if update_value != "":
                    teacher_result.__setattr__(labels[i], update_value)
            db.session.commit()
        elif request.form.get('type') == 'insert':
            new = Teachers(
                工号=request.form.get('工号'),
                姓名=request.form.get('姓名'),
                性别=request.form.get('性别'),
                职称=request.form.get('职称')
            )
            db.session.add(new)
            db.session.commit()
    result = trans(result_query.all())
    return render_template('teacher.html', labels=labels, content=result)

@app.route('/paper', methods=['GET', 'POST'])
def paper():
    labels = ['序号', '论文名称', '发表期刊', '发表年份', '论文类型', '级别']
    result_query = db.session.query(Papers)
    labels1 = ['工号', '姓名', '序号', '论文名称', '排名', '是否通讯作者']
    result_query1 = db.session.query(None)
    labels2 = ['工号', '论文序号', '排名', '是否通讯作者']
    print(f"\n{request.form.get('type')}\n")
    if request.method == 'POST':
        if request.form.get('type') == 'query':
            idx = []
            for i in range(len(labels)):
                req_id = request.form.get(labels[i])
                if req_id != "":
                    result_query = result_query.filter(Papers.__table__.columns[labels[i]] == req_id)
        elif request.form.get('type') == 'delete':
            idx = request.form.get('key')
            paper_result = db.session.query(Papers).filter_by(序号=idx).first()
            db.session.delete(paper_result)
            db.session.commit()
        elif request.form.get('type') == 'update':
            idx = request.form.get('key')
            paper_result = db.session.query(Papers).filter_by(序号=idx).first()
            for i in range(len(labels)):
                update_value = request.form.get(labels[i])
                if update_value != "":
                    paper_result.__setattr__(labels[i], update_value)
            db.session.commit()
        elif request.form.get('type') == 'insert':
            new = Papers(
                序号=request.form.get('序号'),
                论文名称=request.form.get('论文名称'),
                发表期刊=request.form.get('发表期刊'),
                发表年份=request.form.get('发表年份'),
                论文类型=request.form.get('论文类型'),
                级别=request.form.get('级别')
            )
            db.session.add(new)
            db.session.commit()
        elif request.form.get('type') == 'query_1':
            teacher = request.form.get('工号')
            num = request.form.get('序号')
            if teacher != "" or num != "":
                result_query1 = db.session.query(Teachers.工号, Teachers.姓名, Papers.序号, Papers.论文名称, PublishingPapers.排名, PublishingPapers.是否通讯作者).join(PublishingPapers, Teachers.工号 == PublishingPapers.工号).join(Papers, Papers.序号 == PublishingPapers.序号)
                if teacher != "": result_query1 = result_query1.filter(Teachers.工号 == teacher)
                if num != "": result_query1 = result_query1.filter(Papers.序号 == num)
        elif request.form.get('type') == 'delete_1':
            idx = request.form.get('key')
            paper_result = db.session.query(PublishingPapers).filter_by(工号=idx).first()
            db.session.delete(paper_result)
            db.session.commit()
        elif request.form.get('type') == 'update_1':
            idx = request.form.get('key')
            paper_result = db.session.query(PublishingPapers).filter_by(工号=idx).first()
            for i in range(len(labels2)):
                update_value = request.form.get(labels2[i])
                if update_value != "":
                    if update_value == 'True': update_value = True
                    if update_value == 'False': update_value = False
                    paper_result.__setattr__(labels2[i], update_value)
            db.session.commit()
        elif request.form.get('type') == 'insert_1':
            paramlen = request.form.get('cnt')
            num = request.form.get('序号')
            for i in range(int(paramlen)):
                contact = request.form.get('是否通讯作者'+str(i+1))
                if contact == 'True': contact = True
                if contact == 'False': contact = False
                pub = PublishingPapers(
                    工号 = request.form.get('工号'+str(i+1)),
                    序号 = num,
                    排名 = request.form.get('排名'+str(i+1)),
                    是否通讯作者 = contact
                )
                db.session.add(pub)
            db.session.commit()
                
    result = trans(result_query.all())
    result1 = trans(result_query1.all())
    return render_template('paper.html', labels=labels, content=result, labels1=labels1, content1=result1)

@app.route('/course', methods=['GET', 'POST'])
def course():
    labels = ['课程号', '课程名称', '学时数', '课程性质']
    result_query = db.session.query(Courses)
    labels1 = ['工号', '姓名', '课程号', '课程名', '年份', '学期', '承担学时']
    result_query1 = db.session.query(None)
    labels2 = ['工号', '课程号', '年份', '学期', '承担学时']
    if request.method == 'POST':
        if request.form.get('type') == 'query':
            idx = []
            for i in range(len(labels)):
                req_id = request.form.get(labels[i])
                if req_id != "":
                    result_query = result_query.filter(Courses.__table__.columns[labels[i]] == req_id)
        elif request.form.get('type') == 'delete':
            idx = request.form.get('key')
            course_result = db.session.query(Courses).filter_by(课程号=idx).first()
            db.session.delete(course_result)
            db.session.commit()
        elif request.form.get('type') == 'update':
            idx = request.form.get('key')
            course_result = db.session.query(Courses).filter_by(课程号=idx).first()
            for i in range(len(labels)):
                update_value = request.form.get(labels[i])
                if update_value != "":
                    course_result.__setattr__(labels[i], update_value)
            db.session.commit()
        elif request.form.get('type') == 'insert':
            new = Courses(
                课程号=request.form.get('课程号'),
                课程名称=request.form.get('课程名称'),
                学时数=request.form.get('学时数'),
                课程性质=request.form.get('课程性质')
            )
            db.session.add(new)
            db.session.commit()
        elif request.form.get('type') == 'query_1':
            teacher = request.form.get('工号')
            num = request.form.get('课程号')
            if teacher != "" or num != "":
                result_query1 = db.session.query(Teachers.工号, Teachers.姓名, Courses.课程号, Courses.课程名称, LeadingCourses.年份, LeadingCourses.学期, LeadingCourses.承担学时).join(LeadingCourses, Teachers.工号 == LeadingCourses.工号).join(Courses, Courses.课程号 == LeadingCourses.课程号)
                if teacher != "": result_query1 = result_query1.filter(Teachers.工号 == teacher)
                if num != "": result_query1 = result_query1.filter(Courses.课程号 == num)
        elif request.form.get('type') == 'delete_1':
            idx = request.form.get('key')
            course_result = db.session.query(LeadingCourses).filter_by(工号=idx).first()
            db.session.delete(course_result)
            db.session.commit()
        elif request.form.get('type') == 'update_1':
            idx = request.form.get('key')
            course_result = db.session.query(LeadingCourses).filter_by(工号=idx).first()
            for i in range(len(labels2)):
                update_value = request.form.get(labels2[i])
                if update_value != "":
                    course_result.__setattr__(labels2[i], update_value)
            db.session.commit()
        elif request.form.get('type') == 'insert_1':
            paramlen = request.form.get('cnt')
            num = request.form.get('课程号')
            for i in range(int(paramlen)):
                course = LeadingCourses(
                    工号 = request.form.get('工号'+str(i+1)),
                    课程号 = num,
                    年份 = request.form.get('年份'+str(i+1)),
                    学期 = request.form.get('学期'+str(i+1)),
                    承担学时 = request.form.get('承担学时'+str(i+1))
                )
                db.session.add(course)
            db.session.commit()

    result = trans(result_query.all())
    result1 = trans(result_query1.all())
    return render_template('course.html', labels=labels, content=result, labels1=labels1, content1=result1)

@app.route('/project', methods=['GET', 'POST'])
def project():
    labels = ['项目号', '项目名称', '项目来源', '项目类型', '总经费', '起始月份', '结束月份']
    result_query = db.session.query(Projects)
    labels1 = ['工号', '姓名', '项目号', '项目名称', '排名', '承担经费']
    result_query1 = db.session.query(None)
    labels2 = ['工号', '项目号', '排名', '承担经费']
    if request.method == 'POST':
        if request.form.get('type') == 'query':
            idx = []
            for i in range(len(labels)):
                req_id = request.form.get(labels[i])
                if req_id != "":
                    result_query = result_query.filter(Projects.__table__.columns[labels[i]] == req_id)
        elif request.form.get('type') == 'delete':
            idx = request.form.get('key')
            project_result = db.session.query(Projects).filter_by(项目号=idx).first()
            db.session.delete(project_result)
            db.session.commit()
        elif request.form.get('type') == 'update':
            idx = request.form.get('key')
            project_result = db.session.query(Projects).filter_by(项目号=idx).first()
            for i in range(len(labels)):
                update_value = request.form.get(labels[i])
                if update_value != "":
                    project_result.__setattr__(labels[i], update_value)
            db.session.commit()
        elif request.form.get('type') == 'insert':
            new = Projects(
                项目号=request.form.get('项目号'),
                项目名称=request.form.get('项目名称'),
                项目来源=request.form.get('项目来源'),
                项目类型=request.form.get('项目类型'),
                总经费=request.form.get('总经费'),
                起始月份=request.form.get('起始月份'),
                结束月份=request.form.get('结束月份')
            )
            db.session.add(new)
            db.session.commit()
        elif request.form.get('type') == 'query_1':
            teacher = request.form.get('工号')
            num = request.form.get('项目号')
            if teacher != "" or num != "":
                result_query1 = db.session.query(Teachers.工号, Teachers.姓名, Projects.项目号, Projects.项目名称, TakingProjects.排名, TakingProjects.承担经费).join(TakingProjects, Teachers.工号 == TakingProjects.工号).join(Projects, Projects.项目号 == TakingProjects.项目号)
                if teacher != "": result_query1 = result_query1.filter(Teachers.工号 == teacher)
                if num != "": result_query1 = result_query1.filter(Projects.项目号 == num)
        elif request.form.get('type') == 'delete_1':
            idx = request.form.get('key')
            course_result = db.session.query(TakingProjects).filter_by(工号=idx).first()
            db.session.delete(course_result)
            db.session.commit()
        elif request.form.get('type') == 'update_1':
            idx = request.form.get('key')
            course_result = db.session.query(TakingProjects).filter_by(工号=idx).first()
            for i in range(len(labels2)):
                update_value = request.form.get(labels2[i])
                if update_value != "":
                    course_result.__setattr__(labels2[i], update_value)
            db.session.commit()
        elif request.form.get('type') == 'insert_1':
            paramlen = request.form.get('cnt')
            num = request.form.get('项目号')
            for i in range(int(paramlen)):
                project = TakingProjects(
                    工号 = request.form.get('工号'+str(i+1)),
                    项目号 = num,
                    排名 = request.form.get('排名'+str(i+1)),
                    承担经费 = request.form.get('承担经费'+str(i+1))
                )
                db.session.add(project)
            db.session.commit()

    result = trans(result_query.all())
    result1 = trans(result_query1.all())
    return render_template('project.html', labels=labels, content=result, labels1=labels1, content1=result1)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)



# @app.route('/404', methods=['GET', 'POST'])
# def not_found():
#     return render_template('404.html', error_title='错误标题', error_message='错误信息')


# @app.errorhandler(Exception)
# def err_handle(e):
#     error_message = 'ttt'
#     error_title = 'ttt'
#     if (type(e) == IndexError):
#         error_title = '填写错误'
#         error_message = '日期格式错误! (yyyy-mm-dd)'
#     elif (type(e) == AssertionError):
#         error_title = '删除错误'
#         error_message = '删除条目仍有依赖！'
#     # elif (type(e) == SQLAlchemy.exc.IntegrityError):
#     #     error_title = '更新/插入错误'
#     #     error_message = str(e._message())
#     else:
#         error_title = '更新/插入错误'
#         error_message = str(e)

#     return render_template('404.html', error_title=error_title, error_message=error_message)


