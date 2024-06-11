import sys
sys.path.append("C:\\users\lenovo\\appdata\\local\\programs\\python\\python310\\lib\\site-packages")
from flask import Flask, render_template, request, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from model import User, Teachers, Papers, Projects, Courses, PublishingPapers, LeadingCourses, TakingProjects, display
import os
import sys
path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:123456@localhost:3306/teacher"
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_connect = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    passwd='123456',
    database='teacher'
)
db = SQLAlchemy()
db.init_app(app)

# cursor = db2.cursor()

def exist(type, id):
    if type == 'teacher':
        return db.session.query(Teachers).filter_by(工号=id).scalar() is not None
    if type == 'paper':
        return db.session.query(Papers).filter_by(序号=id).scalar() is not None
    if type == 'project':
        return db.session.query(Projects).filter_by(项目号=id).scalar() is not None
    if type == 'course':
        return db.session.query(Courses).filter_by(课程号=id).scalar() is not None
    if type == 'publishingpaper':
        return db.session.query(PublishingPapers).filter_by(序号=id).scalar() is not None
    if type == 'leadingcourse':
        return db.session.query(LeadingCourses).filter_by(课程号=id).scalar() is not None
    if type == 'takingproject':
        return db.session.query(TakingProjects).filter_by(项目号=id).scalar() is not None
    if type == 'user':
        return db.session.query(User).filter_by(name=id).scalar() is not None

lasttemplate = 'login'

@app.route('/')
def hello_world():
    return redirect( url_for('login') )

@app.route('/login', methods=['GET', 'POST'])
def login():
    global lasttemplate
    lasttemplate = 'login'
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
            if not exist('user', name): return render_template('error.html', message1='缺少条目', message2='用户不存在', message3='请先注册')
            user_result = db.session.query(User).filter_by(name=name).first()
            if user_result.password == key:
                return render_template('index.html')
            else:
                return render_template('error.html', message1='密码错误', message2='请重新输入')
    return render_template('login.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    global lasttemplate
    lasttemplate = 'index'
    return render_template('index.html')

@app.route('/teacher', methods=['GET', 'POST'])
def teacher():
    global lasttemplate
    lasttemplate = 'teacher'
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
    result = display(result_query.all())
    return render_template('teacher.html', labels=labels, content=result)

@app.route('/paper', methods=['GET', 'POST'])
def paper():
    global lasttemplate
    lasttemplate = 'paper'
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
            if not exist('paper', num):
                return render_template('error.html', message1='缺少条目', message2='论文不存在', message3='请先添加论文')
            if not exist('publishingpaper', num):
                return render_template('error.html', message1='重复条目', message2='论文的作者已经添加', message3='请勿重复添加或者删除后重试')
            contact_flag = False
            rank_set = {}
            for i in range(int(paramlen)):
                contact = request.form.get('是否通讯作者'+str(i+1))
                if contact == 'True': contact = True
                if contact == 'False': contact = False
                rank = request.form.get('排名'+str(i+1))
                pub = PublishingPapers(
                    工号 = request.form.get('工号'+str(i+1)),
                    序号 = num,
                    排名 = rank,
                    是否通讯作者 = contact
                )
                if contact == True:
                    if contact_flag == False: contact_flag = True
                    else: return render_template('error.html', message1='数据检查失败', message2='一篇论文只能有一位通讯作者',message3=f'第{i+1}位作者为重复通讯作者')
                if rank in rank_set:
                    return render_template('error.html', message1='数据检查失败', message2='论文的作者排名不能有重复', message3=f'第{i+1}位作者的排名重复')
                rank_set[rank] = True
                db.session.add(pub)
            if contact_flag == False:
                return render_template('error.html', message1='数据检查失败', message2='一篇论文必须有一位通讯作者', message3='请添加通讯作者')
            db.session.commit()
                
    result = display(result_query.all())
    result1 = display(result_query1.all())
    return render_template('paper.html', labels=labels, content=result, labels1=labels1, content1=result1)

@app.route('/course', methods=['GET', 'POST'])
def course():
    global lasttemplate
    lasttemplate = 'course'
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
            if not exist('course', num):
                return render_template('error.html', message1='缺少条目', message2='课程不存在', message3='请先添加课程')
            if not exist('leadingcourse', num):
                return render_template('error.html', message1='重复条目', message2='课程的教师已经添加', message3='请勿重复添加或者删除后重试')
            record = {}
            course_result = db.session.query(Courses).filter_by(课程号=num).first()
            total = course_result.学时数
            for i in range(int(paramlen)):
                year = request.form.get('年份'+str(i+1))
                term = request.form.get('学期'+str(i+1))
                credit_hour = request.form.get('承担学时'+str(i+1))
                course = LeadingCourses(
                    工号 = request.form.get('工号'+str(i+1)),
                    课程号 = num,
                    年份 = year,
                    学期 = term,
                    承担学时 = credit_hour
                )
                db.session.add(course)
                if year not in record: record[year] = {}
                if term not in record[year]: record[year][term] = 0
                record[year][term] += credit_hour
            for year in record:
                for term in record[year]:
                    if abs(record[year][term] - total) > 1e-4:
                        return render_template('error.html', message1='数据检查失败', message2='课程的总学时与教师的承担学时不匹配', message3=f'{year}年{term}学期的教师承担学时总额为{record[year][term]},课程总学时为{total}')
            db.session.commit()

    result = display(result_query.all())
    result1 = display(result_query1.all())
    return render_template('course.html', labels=labels, content=result, labels1=labels1, content1=result1)

@app.route('/project', methods=['GET', 'POST'])
def project():
    global lasttemplate
    lasttemplate = 'project'
    labels = ['项目号', '项目名称', '项目来源', '项目类型', '总经费', '起始年份', '结束年份']
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
                起始年份=request.form.get('起始年份'),
                结束年份=request.form.get('结束年份')
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
            if not exist('project', num):
                return render_template('error.html', message1='缺少条目', message2='项目不存在', message3='请先添加项目')
            if not exist('takingproject', num):
                return render_template('error.html', message1='重复条目', message2='项目的教师已经添加', message3='请勿重复添加或者删除后重试')
            project_result = db.session.query(Projects).filter_by(项目号=num).first()
            total = project_result.总经费
            rank_set = {}
            for i in range(int(paramlen)):
                rank = request.form.get('排名'+str(i+1))
                money = request.form.get('承担经费'+str(i+1))
                project = TakingProjects(
                    工号 = request.form.get('工号'+str(i+1)),
                    项目号 = num,
                    排名 = rank,
                    承担经费 = money
                )
                db.session.add(project)
                if rank in rank_set:
                    return render_template('error.html', message1='数据检查失败', message2='项目的教师排名不能有重复', message3=f'第{i+1}位教师的排名重复')
                rank_set[rank] = True
                total -= money
            if abs(total) > 1e-4:
                return render_template('error.html', message1='数据检查失败', message2='项目的总经费与教师的承担经费不匹配', message3=f'项目的总经费为{project_result.总经费},教师的承担经费总额为{total}')
            db.session.commit()

    result = display(result_query.all())
    result1 = display(result_query1.all())
    return render_template('project.html', labels=labels, content=result, labels1=labels1, content1=result1)

def output(content, path, year):
    with open(path, 'w') as f:
        year0 = year[0]
        year1 = year[1]
        if year[0] == 0: year0 = ''
        if year[1] == 9999: year1= ''
        f.write(f'# 教师科学研究统计工作 （{year0}-{year1}）\n')
        f.write('\n')
        f.write('## 教师基本信息\n')
        f.write('\n')
        f.write(f'#### 工号:{content[0][0].工号}\t\t姓名:{content[0][0].姓名}\t\t职称:{content[0][0].职称}\t\t性别:{content[0][0].性别}\n')
        f.write('\n')
        f.write('## 教学情况\n')
        f.write('\n')
        #表格
        f.write('| 课程号 | 课程名称 | 学时数 | 课程性质 | 年份 | 学期 | 承担学时 |\n')
        f.write('| --- | --- | --- | --- | --- | --- | --- |\n')
        for i in range(len(content[1])):
            f.write(f'| {content[1][i].课程号} | {content[1][i].课程名称} | {content[1][i].学时数} | {content[1][i].课程性质} | {content[1][i].年份} | {content[1][i].学期} | {content[1][i].承担学时} |\n')
        # for i in range(len(content[1])):
        #     f.write(f'课程号:{content[1][i].课程号}\t\t课程名称:{content[1][i].课程名称}\t\t学时数:{content[1][i].学时数}\t\t课程性质:{content[1][i].课程性质}\t\t年份:{content[1][i].年份}\t\t学期:{content[1][i].学期}\t\t承担学时:{content[1][i].承担学时}\n')
        f.write('\n')
        f.write('## 发表论文情况\n')
        f.write('\n')
        for i in range(len(content[2])):
            content[2][i].是否通讯作者 = ', 通讯作者' if content[2][i].是否通讯作者 else ''
            f.write(f'{i+1}. {content[2][i].论文名称}, {content[2][i].发表期刊}, {content[2][i].发表年份}, {content[2][i].论文类型}, {content[2][i].级别}, 排名第{content[2][i].排名}{content[2][i].是否通讯作者}\n')
        f.write('\n')
        f.write('## 承担项目情况\n')
        f.write('\n')
        for i in range(len(content[3])):
            f.write(f'{i+1}. {content[3][i].项目名称}, {content[3][i].项目来源}, {content[3][i].项目类型}, 总经费:{content[3][i].总经费}, {content[3][i].起始年份}-{content[3][i].结束年份}, 排名第{content[3][i].排名}, 承担经费:{content[3][i].承担经费}\n')
    print(f'output style: markdown\noutput path:{path}')
    pass

@app.route('/statistic', methods=['GET', 'POST'])
def statistic():
    labels = {}
    content = {}
    if request.method == 'POST':
        if request.form.get('type') == 'query':
            num = request.form.get('工号')
            start = request.form.get('起始年份')
            if start == '': start = 0
            end = request.form.get('结束年份')
            if end == '': end = 9999
            # 查询基本信息
            labels[0] = ['工号', '姓名', '职称', '性别']
            result_query = db.session.query(Teachers).filter(Teachers.工号 == num)
            content[0] = display(result_query.all())
            # 查询课程信息
            labels[1] = ['课程号', '课程名称', '学时数', '课程性质', '年份', '学期', '承担学时']
            result_query = db.session.query(Teachers.工号, Courses.课程号, Courses.课程名称, Courses.学时数, Courses.课程性质, LeadingCourses.年份, LeadingCourses.学期, LeadingCourses.承担学时).join(LeadingCourses, Teachers.工号 == LeadingCourses.工号).join(Courses, Courses.课程号 == LeadingCourses.课程号).filter(Teachers.工号 == num).filter(LeadingCourses.年份 >= start, LeadingCourses.年份 <= end)
            content[1] = display(result_query.all())
            # 查询论文信息
            labels[2] = ['序号', '论文名称', '发表期刊', '发表年份', '论文类型', '级别', '排名', '是否通讯作者']
            result_query = db.session.query(Teachers.工号, Papers.序号, Papers.论文名称, Papers.发表期刊, Papers.发表年份, Papers.论文类型, Papers.级别, PublishingPapers.排名, PublishingPapers.是否通讯作者).join(PublishingPapers, Teachers.工号 == PublishingPapers.工号).join(Papers, Papers.序号 == PublishingPapers.序号).filter(Teachers.工号 == num).filter(Papers.发表年份 >= start, Papers.发表年份 <= end)
            content[2] = display(result_query.all())
            # 查询项目信息
            labels[3] = ['项目号', '项目名称', '项目来源', '项目类型', '总经费', '起始年份', '结束年份', '排名', '承担经费']
            result_query = db.session.query(Teachers.工号, Projects.项目号, Projects.项目名称, Projects.项目来源, Projects.项目类型, Projects.总经费, Projects.起始年份, Projects.结束年份, TakingProjects.排名, TakingProjects.承担经费).join(TakingProjects, Teachers.工号 == TakingProjects.工号).join(Projects, Projects.项目号 == TakingProjects.项目号).filter(Teachers.工号 == num)
            t1 = result_query.filter(Projects.起始年份 >= start, Projects.起始年份 <= end)
            t2 = result_query.filter(Projects.结束年份 >= start, Projects.结束年份 <= end)
            t3 = result_query.filter(Projects.起始年份 <= start, Projects.结束年份 >= end)
            result_query = t1.union(t2).union(t3)
            content[3] = display(result_query.all())
            output(content, path + '\\teach.md', (start, end))
    return render_template('statistic.html', labels=labels, content=content, path=path + '\\teach.md')

@app.route('/error', methods=['GET', 'POST'])
def error():
    if request.method == 'POST':
        return redirect( url_for(lasttemplate) )
    # return render_template('error.html')

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


