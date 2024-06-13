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
    发表年份 INT NOT NULL,
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
    起始年份 INT NOT NULL,
    结束年份 INT
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
INSERT INTO Teachers VALUES ('00004', '赵六', 2, 4);

INSERT INTO Teachers VALUES ('00005', '小A', 1, 4);

INSERT INTO Papers VALUES (1, '基于Transformer的Diffusion Model', 'ICLR', 2019, 1, 1);
INSERT INTO Papers VALUES (2, '层剪枝Transformer', 'AAAI', 2020, 2, 2);
INSERT INTO Papers VALUES (3, 'Video Diffuison Model', 'NIPS', 2021, 3, 3);

INSERT INTO Projects VALUES ('A0001', 'Mate60研发', '华为', 1, 100000, 2018, 2020);
INSERT INTO Projects VALUES ('A0002', '小米Sui7研发', '小米', 2, 200000, 2021, 2023);
INSERT INTO Projects VALUES ('A0003', '中科大高新区建设', '中科大', 3, 300000, 2020, 2024);

INSERT INTO Courses VALUES ('B0001', '计算机网络', 3, 1);
INSERT INTO Courses VALUES ('B0002', '数据库', 4, 1);
INSERT INTO Courses VALUES ('B0003', '操作系统', 4, 1);

INSERT INTO PublishingPapers VALUES ('00001', 1, 1, TRUE);
INSERT INTO PublishingPapers VALUES ('00002', 1, 2, FALSE);
INSERT INTO PublishingPapers VALUES ('00003', 2, 1, TRUE);
INSERT INTO PublishingPapers VALUES ('00001', 2, 2, FALSE);


INSERT INTO LeadingCourses VALUES ('00001', 'B0001', 2023, 1, 3);
INSERT INTO LeadingCourses VALUES ('00002', 'B0002', 2023, 3, 4);
INSERT INTO LeadingCourses VALUES ('00003', 'B0003', 2023, 1, 4);

INSERT INTO TakingProjects VALUES ('00001', 'A0001', 1, 50000);
INSERT INTO TakingProjects VALUES ('00002', 'A0001', 2, 50000);
INSERT INTO TakingProjects VALUES ('00003', 'A0003', 1, 3000);
