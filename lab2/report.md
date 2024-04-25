# 银行业务管理系统数据库设计

## PB21000164 来泽远

## 1 概念模型设计

### 1.1 实体设计

| 实体名         | 属性                                                         |
| -------------- | ------------------------------------------------------------ |
| 客户           | **身份证号**、姓名、电话、地址                               |
| 支行           | **名字**、城市、资产                                         |
| 联系人         | 姓名、电话、邮箱、与客户关系                                 |
| 部门           | **部门名**、部门类型、经理工号                               |
| 员工           | **工号**、姓名、电话、地址、入职日期、是否经理               |
| 贷款           | **合同号**、总额、申请支行                                   |
| 支付           | **支付号**、时间、金额、入款账户                             |
| 账户           | **账户号**、余额、开户日期、开户支行、最近访问时间           |
| 储蓄账户       | 利率、货币类型                                               |
| 贷款账户       | 透支额度                                                     |
| 客户-支行-储蓄 | 无（用于满足一个客户在一个支行内只能开设一个储蓄账户的需求） |
| 客户-支行-贷款 | 无（用于满足一个客户在一个支行内只能开设一个贷款账户的需求） |

其中加粗属性为主键

### 1.2 实体关系

| 联系              | 设计理由                               |
| ----------------- | -------------------------------------- |
| relation_custom   | 每一个客户需要有一个联系人             |
| custom_staff      | 员工对客户的服务关系，多对多           |
| branch_department | 支行下属各个部门                       |
| staff_department  | 员工在各个部门中工作                   |
| setup_custom_loan | 每个顾客只能申请一次贷款               |
| branch_loan       | 申请时对应的支行                       |
| custom_own_loan   | 一项贷款可以由多个顾客共有，多对多关系 |
| loan_pay          | 一项贷款会由多项支付完成               |
| saving_account    | 储蓄账户继承账户                       |
| loan_account      | 贷款账户继承账户                       |

关于own_i、own_saving_account、own_loan_account的解释如下。为了满足一个顾客在一个支行只能分别开设（拥有）一个储蓄账户和贷款账户，先将客户和支行做组合，以构成不重复的$<客户,支行>$二元组。在将该二元组与储蓄、贷款账户做多对一的关系，使得任意二元组最多只可对应一个账户，从而完成该需求，也同时满足了多个客户可以共有账户的需求。

### 1.3 ER图

![image-20240425211916022](C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\image-20240425211916022.png)

## 2  概念模型到逻辑模型的转换

### 2.1 实体转换

![image-20240425211929330](C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\image-20240425211929330.png)

概念图中的继承关系被转变为实体的包含关系。

若干实体被补充了属性。“员工”实体被补充了“部门”属性，“贷款申请”实体被补充了“合同号”、“身份证号”、“名字”属性，“支付”实体被补充了“合同号”属性，以及客户和支行的组合实体“客户-支行-储蓄”和“客户-支行-贷款”也补充了若干属性。

### 2.2 关系转变

多对多联系转化为关系模式，其属性包括联系的实体的主码，如“custom_staff”和“custom_own_loan”两种关系。

部分一对多关系保持不变，其余被归并进实体中利用属性进行联系，如原先“客户-支行-储蓄”实体与“储蓄账户”实体间的联系被转为为“客户-支行-储蓄”实体中的属性。

### 2.3 最终的关系模式

如上图所示。

## 3 MySQL 数据库结构实现

### 3.1 Power Designer 的 PDM 图

![image-20240425212056994](C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\image-20240425212056994.png)

### 3.2 数据库表定义

```sql
/*==============================================================*/
/* Table: account                                               */
/*==============================================================*/
create table account
(
   account_id           varchar(20) not null  comment '',
   money                float(20,0) not null  comment '',
   open_date            date not null  comment '',
   open_branch          varchar(20) not null  comment '',
   latest_date          date not null  comment '',
   primary key (account_id)
);

/*==============================================================*/
/* Table: branch_bank                                           */
/*==============================================================*/
create table branch_bank
(
   name                 varchar(20) not null  comment '',
   city                 varchar(20) not null  comment '',
   assets               float(20,0) not null  comment '',
   primary key (name)
);

/*==============================================================*/
/* Table: relation                                              */
/*==============================================================*/
create table relation
(
   relation_name        varchar(20) not null  comment '',
   relation_telephone   numeric(20,0) not null  comment '',
   email                varchar(20) not null  comment '',
   relationship         varchar(20) not null  comment '',
   primary key (relation_name)
);

/*==============================================================*/
/* Table: loan                                                  */
/*==============================================================*/
create table loan
(
   loan_id              varchar(20) not null  comment '',
   name                 varchar(20) not null  comment '',
   custom_id            varchar(20) not null  comment '',
   amount               float(20,0) not null  comment '',
   branch               varchar(20) not null  comment '',
   primary key (loan_id),
   constraint FK_LOAN_SETUP_CUS_CUSTOM foreign key (custom_id)
      references custom (custom_id) on delete restrict on update restrict,
   constraint FK_LOAN_BRANCH_LO_BRANCH_B foreign key (name)
      references branch_bank (name) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: custom                                                */
/*==============================================================*/
create table custom
(
   custom_id            varchar(20) not null  comment '',
   relation_name        varchar(20) not null  comment '',
   loan_id              varchar(20)  comment '',
   custom_name          varchar(20) not null  comment '',
   cunstom_telephone    numeric(20,0) not null  comment '',
   custom_address       varchar(20) not null  comment '',
   primary key (custom_id),
   constraint FK_CUSTOM_RELATION__RELATION foreign key (relation_name)
      references relation (relation_name) on delete restrict on update restrict,
   constraint FK_CUSTOM_SETUP_CUS_LOAN foreign key (loan_id)
      references loan (loan_id) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: loan_account                                          */
/*==============================================================*/
create table loan_account
(
   account_id           varchar(20) not null  comment '',
   money                float(20,0) not null  comment '',
   open_date            date not null  comment '',
   open_branch          varchar(20) not null  comment '',
   latest_date          date not null  comment '',
   borrow               float(20,0)  comment '',
   primary key (account_id),
   constraint FK_LOAN_ACC_LOAN_ACCO_ACCOUNT foreign key (account_id)
      references account (account_id) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: custom_branch_loan                                    */
/*==============================================================*/
create table custom_branch_loan
(
   name                 varchar(20) not null  comment '',
   custom_id            varchar(20) not null  comment '',
   account_id           varchar(20)  comment '',
   constraint FK_CUSTOM_B_OWN_3_CUSTOM foreign key (custom_id)
      references custom (custom_id) on delete restrict on update restrict,
   constraint FK_CUSTOM_B_OWN_4_BRANCH_B foreign key (name)
      references branch_bank (name) on delete restrict on update restrict,
   constraint FK_CUSTOM_B_OWN_LOAN__LOAN_ACC foreign key (account_id)
      references loan_account (account_id) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: saving_account                                        */
/*==============================================================*/
create table saving_account
(
   account_id           varchar(20) not null  comment '',
   money                float(20,0) not null  comment '',
   open_date            date not null  comment '',
   open_branch          varchar(20) not null  comment '',
   latest_date          date not null  comment '',
   interest_rate        float(20)  comment '',
   currency             varchar(20)  comment '',
   primary key (account_id),
   constraint FK_SAVING_A_SAVING_AC_ACCOUNT foreign key (account_id)
      references account (account_id) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: custom_branch_saving                                  */
/*==============================================================*/
create table custom_branch_saving
(
   custom_id            varchar(20) not null  comment '',
   name                 varchar(20) not null  comment '',
   account_id           varchar(20)  comment '',
   constraint FK_CUSTOM_B_OWN_1_CUSTOM foreign key (custom_id)
      references custom (custom_id) on delete restrict on update restrict,
   constraint FK_CUSTOM_B_OWN_2_BRANCH_B foreign key (name)
      references branch_bank (name) on delete restrict on update restrict,
   constraint FK_CUSTOM_B_OWN_SAVIN_SAVING_A foreign key (account_id)
      references saving_account (account_id) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: custom_own_loan                                       */
/*==============================================================*/
create table custom_own_loan
(
   custom_id            varchar(20) not null  comment '',
   loan_id              varchar(20) not null  comment '',
   primary key (custom_id, loan_id),
   constraint FK_CUSTOM_O_CUSTOM_OW_CUSTOM foreign key (custom_id)
      references custom (custom_id) on delete restrict on update restrict,
   constraint FK_CUSTOM_O_CUSTOM_OW_LOAN foreign key (loan_id)
      references loan (loan_id) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: department                                            */
/*==============================================================*/
create table department
(
   apartment            varchar(20) not null  comment '',
   name                 varchar(20) not null  comment '',
   type_apartment       varchar(20) not null  comment '',
   manager_id           varchar(20) not null  comment '',
   primary key (apartment),
   constraint FK_DEPARTME_BRANCH_DE_BRANCH_B foreign key (name)
      references branch_bank (name) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: staff                                                 */
/*==============================================================*/
create table staff
(
   staff_id             varchar(20) not null  comment '',
   apartment            varchar(20) not null  comment '',
   staff_name           varchar(20) not null  comment '',
   telephone            numeric(20,0) not null  comment '',
   staff_address        varchar(20) not null  comment '',
   start_date           date not null  comment '',
   is_manager           bool not null  comment '',
   primary key (staff_id),
   constraint FK_STAFF_STAFF_DEP_DEPARTME foreign key (apartment)
      references department (apartment) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: custom_staff                                          */
/*==============================================================*/
create table custom_staff
(
   custom_id            varchar(20) not null  comment '',
   staff_id             varchar(20) not null  comment '',
   primary key (custom_id, staff_id),
   constraint FK_CUSTOM_S_CUSTOM_ST_CUSTOM foreign key (custom_id)
      references custom (custom_id) on delete restrict on update restrict,
   constraint FK_CUSTOM_S_CUSTOM_ST_STAFF foreign key (staff_id)
      references staff (staff_id) on delete restrict on update restrict
);

/*==============================================================*/
/* Table: pay                                                   */
/*==============================================================*/
create table pay
(
   pay_date             date not null  comment '',
   pay_amout            float(20,0) not null  comment '',
   pay_account          varchar(20) not null  comment '',
   pay_id               varchar(20) not null  comment '',
   loan_id              varchar(20)  comment '',
   primary key (pay_id),
   constraint "FK_PAY_LOAN-PAY_LOAN" foreign key (loan_id)
      references loan (loan_id) on delete restrict on update restrict
);
```

## 4 总结与体会

在本次实验中，我根据实验需求设计了概念模型，完成了属性定义和实体间的关系依赖。同时依靠Powerdesign自动生成逻辑模型和物理模型，学习其转变过程和模型特点，最后导出为sql语言，定义了所有的表和表项，完成了从需求到sql语言的发开过程。

经过这次实验，我提升了依据需求设计模型的能力，熟悉了Powerdesign的开发流程，对于数据库的知识有了更深的理解和把握。