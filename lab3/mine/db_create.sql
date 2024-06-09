-- Active: 1712909736541@@127.0.0.1@3306@teacher
/* user */
/* CREATE TABLE user (
    name VARCHAR(256) PRIMARY KEY,
    password VARCHAR(256) NOT NULL
); */
drop table PublishingPapers;
drop table LeadingCourses;
drop table TakingProjects;
drop table Projects;
drop table Papers;
drop table Courses;
drop table Teachers;
CREATE TABLE Teachers (
    工号 CHAR(5) PRIMARY KEY,
    姓名 VARCHAR(256) NOT NULL,
    性别 INT CHECK (性别 IN (1, 2)),
    职称 INT CHECK (职称 IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11))
);

-- Table for Papers
CREATE TABLE Papers (
    序号 INT PRIMARY KEY,
    论文名称 VARCHAR(256) NOT NULL,
    发表期刊 VARCHAR(256) NOT NULL,
    发表年份 DATE NOT NULL,
    论文类型 INT CHECK (论文类型 IN (1, 2, 3, 4)),
    级别 INT CHECK (级别 IN (1, 2, 3, 4, 5, 6))
);

-- Table for Projects
CREATE TABLE Projects (
    项目号 CHAR(5) PRIMARY KEY,
    项目名称 VARCHAR(256) NOT NULL,
    项目来源 VARCHAR(256) NOT NULL,
    项目类型 INT CHECK (项目类型 IN (1, 2, 3, 4, 5)),
    总经费 FLOAT NOT NULL,
    起始月份 DATE NOT NULL,
    结束月份 DATE
);

-- Table for Courses
CREATE TABLE Courses (
    课程号 VARCHAR(256) PRIMARY KEY,
    课程名称 VARCHAR(256) NOT NULL,
    学时数 INT NOT NULL,
    课程性质 INT CHECK (课程性质 IN (1, 2))
);

-- Table for Publishing Papers

CREATE TABLE PublishingPapers (
    工号 CHAR(5),
    序号 INT,
    排名 INT CHECK (排名 > 0),
    是否通讯作者 BOOLEAN,
    PRIMARY KEY (工号, 序号),
    FOREIGN KEY (工号) REFERENCES Teachers(工号),
    FOREIGN KEY (序号) REFERENCES Papers(序号)
);

-- Table for Leading Courses
CREATE TABLE LeadingCourses (
    工号 CHAR(5),
    课程号 VARCHAR(256),
    年份 INT,
    学期 INT CHECK (学期 IN (1, 2, 3)),
    承担学时 INT,
    PRIMARY KEY (工号, 课程号, 年份, 学期),
    FOREIGN KEY (工号) REFERENCES Teachers(工号),
    FOREIGN KEY (课程号) REFERENCES Courses(课程号)
);

-- Table for Taking Projects
CREATE TABLE TakingProjects (
    工号 CHAR(5),
    项目号 CHAR(5),
    排名 INT CHECK (排名 > 0),
    承担经费 FLOAT,
    PRIMARY KEY (工号, 项目号),
    FOREIGN KEY (工号) REFERENCES Teachers(工号),
    FOREIGN KEY (项目号) REFERENCES Projects(项目号)
);

#sample data
INSERT INTO Teachers VALUES ('00001', '张三', 1, 1);
INSERT INTO Teachers VALUES ('00002', '李四', 1, 2);
INSERT INTO Teachers VALUES ('00003', '王五', 1, 3);

INSERT INTO Papers VALUES (1, '论文1', '期刊1', '2020-01-01', 1, 1);
INSERT INTO Papers VALUES (2, '论文2', '期刊2', '2020-01-01', 2, 2);
INSERT INTO Papers VALUES (3, '论文3', '期刊3', '2020-01-01', 3, 3);

INSERT INTO Projects VALUES ('A0001', '项目1', '来源1', 1, 100, '2020-01-01', '2020-01-01');
INSERT INTO Projects VALUES ('A0002', '项目2', '来源2', 2, 200, '2020-01-01', '2020-01-01');
INSERT INTO Projects VALUES ('A0003', '项目3', '来源3', 3, 300, '2020-01-01', '2020-01-01');

INSERT INTO Courses VALUES ('B0001', '课程1', 1, 1);
INSERT INTO Courses VALUES ('B0002', '课程2', 2, 2);
INSERT INTO Courses VALUES ('B0003', '课程3', 3, 1);

INSERT INTO PublishingPapers VALUES ('00001', 1, 1, TRUE);
INSERT INTO PublishingPapers VALUES ('00002', 2, 2, FALSE);
INSERT INTO PublishingPapers VALUES ('00003', 3, 3, TRUE);

INSERT INTO LeadingCourses VALUES ('00001', 'B0001', 2020, 1, 1);
INSERT INTO LeadingCourses VALUES ('00002', 'B0002', 2020, 2, 2);
INSERT INTO LeadingCourses VALUES ('00003', 'B0003', 2020, 1, 3);

INSERT INTO TakingProjects VALUES ('00001', 'A0001', 1, 1.0);
INSERT INTO TakingProjects VALUES ('00002', 'A0002', 2, 2.0);
INSERT INTO TakingProjects VALUES ('00003', 'A0003', 3, 3.0);
