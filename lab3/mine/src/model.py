from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    name = db.Column(db.String(256), primary_key=True)
    password = db.Column(db.String(256), nullable=False)

class Teachers(db.Model):
    __tablename__ = 'Teachers'

    工号 = db.Column(db.String(5), primary_key=True)
    姓名 = db.Column(db.String(256))
    性别 = db.Column(db.Integer)
    职称 = db.Column(db.Integer)

class Papers(db.Model):
    __tablename__ = 'Papers'

    序号 = db.Column(db.Integer, primary_key=True)
    论文名称 = db.Column(db.String(256), nullable=False)
    发表期刊 = db.Column(db.String(256), nullable=False)
    发表年份 = db.Column(db.Integer, nullable=False)
    论文类型 = db.Column(db.Integer, nullable=False)
    级别 = db.Column(db.Integer, nullable=False)
    # 工号 = db.Column(db.ForeignKey('Teachers.工号', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False)

class Projects(db.Model):
    __tablename__ = 'Projects'

    项目号 = db.Column(db.String(5), primary_key=True)
    项目名称 = db.Column(db.String(256), nullable=False)
    项目来源 = db.Column(db.String(256), nullable=False)
    项目类型 = db.Column(db.Integer, nullable=False)
    总经费 = db.Column(db.Float, nullable=False)
    起始年份 = db.Column(db.Integer, nullable=False)
    结束年份 = db.Column(db.Integer)
    # 工号 = db.Column(db.ForeignKey('Teachers.工号', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False)

class Courses(db.Model):
    __tablename__ = 'Courses'

    课程号 = db.Column(db.String(256), primary_key=True)
    课程名称 = db.Column(db.String(256), nullable=False)
    学时数 = db.Column(db.Integer, nullable=False)
    课程性质 = db.Column(db.Integer, nullable=False)
    # 工号 = db.Column(db.ForeignKey('Teachers.工号', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False)

class PublishingPapers(db.Model):
    __tablename__ = 'PublishingPapers'

    工号 = db.Column(db.ForeignKey('Teachers.工号', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)
    序号 = db.Column(db.ForeignKey('Papers.序号', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)
    排名 = db.Column(db.Integer, nullable=False)
    是否通讯作者 = db.Column(db.Boolean, nullable=False)

    teacher = db.relationship('Teachers', primaryjoin='PublishingPapers.工号 == Teachers.工号', backref='publishing_papers')
    paper = db.relationship('Papers', primaryjoin='PublishingPapers.序号 == Papers.序号', backref='publishing_papers')

class LeadingCourses(db.Model):
    __tablename__ = 'LeadingCourses'

    工号 = db.Column(db.ForeignKey('Teachers.工号', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)
    课程号 = db.Column(db.ForeignKey('Courses.课程号', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)
    年份 = db.Column(db.Integer, primary_key=True, nullable=False)
    学期 = db.Column(db.Integer, primary_key=True, nullable=False)
    承担学时 = db.Column(db.Integer, nullable=False)

    teacher = db.relationship('Teachers', primaryjoin='LeadingCourses.工号 == Teachers.工号', backref='leading_courses')
    course = db.relationship('Courses', primaryjoin='LeadingCourses.课程号 == Courses.课程号', backref='leading_courses')

class TakingProjects(db.Model):
    __tablename__ = 'TakingProjects'

    工号 = db.Column(db.ForeignKey('Teachers.工号', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)
    项目号 = db.Column(db.ForeignKey('Projects.项目号', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True, nullable=False)
    排名 = db.Column(db.Integer, nullable=False)
    承担经费 = db.Column(db.Float, nullable=False)

    teacher = db.relationship('Teachers', primaryjoin='TakingProjects.工号 == Teachers.工号', backref='taking_projects')
    project = db.relationship('Projects', primaryjoin='TakingProjects.项目号 == Projects.项目号', backref='taking_projects')

gender = {1: '男', 2: '女'}
title = {1: '博士后', 2: '助教', 3: '讲师', 4: '副教授', 5: '特任教授', 6: '教授', 7: '助理研究员', 8: '特任副研究员', 9: '副研究员', 10: '特任研究员', 11: '研究员'}
paper_type = {1: 'full paper', 2: 'short paper', 3: 'poster paper', 4: 'demo paper'}
paper_level = {1: 'CCF-A', 2: 'CCF-B', 3: 'CCF-C', 4: '中文 CCF-A', 5: '中文 CCF-B', 6: '无级别'}
project_type = {1: '国家级项目', 2: '省部级项目', 3: '市厅级项目', 4: '企业合作项目', 5: '其它类型项目'}
semester = {1: '春季学期', 2: '夏季学期', 3: '秋季学期'}
course_type = {1: '本科生课程', 2: '研究生课程'}

class Display():
    def __init__(self, query):
        self.工号 = None if not hasattr(query, '工号') else query.工号
        self.姓名 = None if not hasattr(query, '姓名') else query.姓名
        self.性别 = None if not hasattr(query, '性别') else gender[query.性别]
        self.职称 = None if not hasattr(query, '职称') else title[query.职称]
        self.序号 = None if not hasattr(query, '序号') else query.序号
        self.论文名称 = None if not hasattr(query, '论文名称') else query.论文名称
        self.发表期刊 = None if not hasattr(query, '发表期刊') else query.发表期刊
        self.发表年份 = None if not hasattr(query, '发表年份') else query.发表年份
        self.论文类型 = None if not hasattr(query, '论文类型') else paper_type[query.论文类型]
        self.级别 = None if not hasattr(query, '级别') else paper_level[query.级别]
        self.项目号 = None if not hasattr(query, '项目号') else query.项目号
        self.项目名称 = None if not hasattr(query, '项目名称') else query.项目名称
        self.项目来源 = None if not hasattr(query, '项目来源') else query.项目来源
        self.项目类型 = None if not hasattr(query, '项目类型') else project_type[query.项目类型]
        self.总经费 = None if not hasattr(query, '总经费') else query.总经费
        self.起始年份 = None if not hasattr(query, '起始年份') else query.起始年份
        self.结束年份 = None if not hasattr(query, '结束年份') else query.结束年份
        self.课程号 = None if not hasattr(query, '课程号') else query.课程号
        self.课程名称 = None if not hasattr(query, '课程名称') else query.课程名称
        self.学时数 = None if not hasattr(query, '学时数') else query.学时数
        self.课程性质 = None if not hasattr(query, '课程性质') else course_type[query.课程性质]
        self.排名 = None if not hasattr(query, '排名') else query.排名
        self.是否通讯作者 = None if not hasattr(query, '是否通讯作者') else query.是否通讯作者
        self.年份 = None if not hasattr(query, '年份') else query.年份
        self.学期 = None if not hasattr(query, '学期') else semester[query.学期]
        self.承担学时 = None if not hasattr(query, '承担学时') else query.承担学时
        self.承担经费 = None if not hasattr(query, '承担经费') else query.承担经费

def display(query_set):
    result = []
    for query in query_set:
        result.append(Display(query))
    return result

# # 账户
# class Account(db.Model):
#     __tablename__ = 'account'

#     A_ID = db.Column(db.String(50), primary_key=True)
#     B_Name = db.Column(db.ForeignKey('bank.B_Name', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False,
#                        index=True)
#     Balance = db.Column(db.Float)
#     Opening_Date = db.Column(db.Date)

#     bank = db.relationship('Bank', primaryjoin='Account.B_Name == Bank.B_Name', backref='accounts')


# # 支票账户
# class CheckingAccount(db.Model):
#     __tablename__ = 'checking_account'

#     A_ID = db.Column(db.ForeignKey('account.A_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True)
#     Overdraft = db.Column(db.Float)


# # 储蓄账户
# class SavingAccount(db.Model):
#     __tablename__ = 'saving_account'

#     A_ID = db.Column(db.ForeignKey('account.A_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True)
#     Interest_Rate = db.Column(db.Float)
#     Currency_Type = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'))


# # 贷款发放
# class Apply(db.Model):
#     __tablename__ = 'apply'

#     C_ID = db.Column(db.ForeignKey('client.C_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True,
#                      nullable=False)
#     L_ID = db.Column(db.ForeignKey('loan.L_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True,
#                      nullable=False, index=True)
#     P_ID = db.Column(db.String(50), primary_key=True)
#     P_Amount = db.Column(db.Float)
#     Pay_Date = db.Column(db.Date)

#     client = db.relationship('Client', primaryjoin='Apply.C_ID == Client.C_ID', backref='applies')
#     loan = db.relationship('Loan', primaryjoin='Apply.L_ID == Loan.L_ID', backref='applies')


# # 支行
# class Bank(db.Model):
#     __tablename__ = 'bank'

#     B_ID = db.Column(db.Integer, nullable=False, unique=True)
#     B_Name = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'), primary_key=True)
#     City = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'), nullable=False)
#     Assets = db.Column(db.Float, nullable=False)


# # 客户
# class Client(db.Model):
#     __tablename__ = 'client'

#     C_ID = db.Column(db.String(50), primary_key=True)
#     C_Name = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'), nullable=False)
#     C_Tel = db.Column(db.Integer)
#     C_Addr = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'))


# # 联系人
# class Contact(db.Model):
#     __tablename__ = 'contact'

#     C_ID = db.Column(db.ForeignKey('client.C_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True,
#                      nullable=False)
#     Co_Name = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'), primary_key=True, nullable=False)
#     Co_Email = db.Column(db.String(50))
#     Co_Tel = db.Column(db.Integer)
#     Relation = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'))

#     client = db.relationship('Client', primaryjoin='Contact.C_ID == Client.C_ID', backref='contacts')


# # 部门
# class Department(db.Model):
#     __tablename__ = 'department'

#     D_ID = db.Column(db.String(50), primary_key=True)
#     D_Name = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'), nullable=False)
#     D_Type = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'))
#     Manager_ID = db.Column(db.String(50))


# # 雇员
# class Employee(db.Model):
#     __tablename__ = 'employee'

#     E_ID = db.Column(db.String(50), primary_key=True)
#     E_Name = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'), nullable=False)
#     B_Name = db.Column(db.ForeignKey('bank.B_Name', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False,
#                        index=True)
#     D_ID = db.Column(db.ForeignKey('department.D_ID', ondelete='RESTRICT', onupdate='RESTRICT'), index=True)
#     E_Tel = db.Column(db.Integer)
#     E_Addr = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'))
#     Work_Date = db.Column(db.Date)

#     bank = db.relationship('Bank', primaryjoin='Employee.B_Name == Bank.B_Name', backref='employees')
#     department = db.relationship('Department', primaryjoin='Employee.D_ID == Department.D_ID', backref='employees')


# # 贷款
# class Loan(db.Model):
#     __tablename__ = 'loan'

#     L_ID = db.Column(db.String(50), primary_key=True)
#     B_Name = db.Column(db.ForeignKey('bank.B_Name', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False,
#                        index=True)
#     L_Amount = db.Column(db.Float, nullable=False)
#     L_Status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
#     P_already = db.Column(db.Float)

#     bank = db.relationship('Bank', primaryjoin='Loan.B_Name == Bank.B_Name', backref='loans')


# # 客户-账户
# class Own(db.Model):
#     __tablename__ = 'own'

#     C_ID = db.Column(db.ForeignKey('client.C_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True,
#                      nullable=False)
#     Visited_Date = db.Column(db.Date)
#     A_ID = db.Column(db.ForeignKey('account.A_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True)

#     account = db.relationship('Account', primaryjoin='Own.A_ID == Account.A_ID', backref='owns')
#     client = db.relationship('Client', primaryjoin='Own.C_ID == Client.C_ID', backref='owns')


# # 开户约束
# class Checking(db.Model):
#     __tablename__ = 'checking'

#     C_ID = db.Column(db.ForeignKey('client.C_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True,
#                      nullable=False)
#     B_Name = db.Column(db.ForeignKey('bank.B_Name', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True,
#                        nullable=False, index=True)
#     A_Type = db.Column(db.Integer, primary_key=True, nullable=False)
#     A_ID = db.Column(db.String(50), primary_key=True)

#     bank = db.relationship('Bank', primaryjoin='Checking.B_Name == Bank.B_Name', backref='checkings')
#     client = db.relationship('Client', primaryjoin='Checking.C_ID == Client.C_ID', backref='checkings')


# # 服务关系
# class Service(db.Model):
#     __tablename__ = 'service'

#     C_ID = db.Column(db.ForeignKey('client.C_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True,
#                      nullable=False)
#     E_ID = db.Column(db.ForeignKey('employee.E_ID', ondelete='RESTRICT', onupdate='RESTRICT'), primary_key=True,
#                      nullable=False, index=True)
#     S_Type = db.Column(db.String(15, 'utf8mb4_0900_ai_ci'))

#     client = db.relationship('Client', primaryjoin='Service.C_ID == Client.C_ID', backref='services')
#     employee = db.relationship('Employee', primaryjoin='Service.E_ID == Employee.E_ID', backref='services')
