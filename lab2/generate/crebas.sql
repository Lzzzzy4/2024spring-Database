/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2024/4/25 21:30:52                           */
/*==============================================================*/


alter table custom 
   drop foreign key FK_CUSTOM_RELATION__RELATION;

alter table custom 
   drop foreign key FK_CUSTOM_SETUP_CUS_LOAN;

alter table custom_branch_loan 
   drop foreign key FK_CUSTOM_B_OWN_3_CUSTOM;

alter table custom_branch_loan 
   drop foreign key FK_CUSTOM_B_OWN_4_BRANCH_B;

alter table custom_branch_loan 
   drop foreign key FK_CUSTOM_B_OWN_LOAN__LOAN_ACC;

alter table custom_branch_saving 
   drop foreign key FK_CUSTOM_B_OWN_1_CUSTOM;

alter table custom_branch_saving 
   drop foreign key FK_CUSTOM_B_OWN_2_BRANCH_B;

alter table custom_branch_saving 
   drop foreign key FK_CUSTOM_B_OWN_SAVIN_SAVING_A;

alter table custom_own_loan 
   drop foreign key FK_CUSTOM_O_CUSTOM_OW_CUSTOM;

alter table custom_own_loan 
   drop foreign key FK_CUSTOM_O_CUSTOM_OW_LOAN;

alter table custom_staff 
   drop foreign key FK_CUSTOM_S_CUSTOM_ST_CUSTOM;

alter table custom_staff 
   drop foreign key FK_CUSTOM_S_CUSTOM_ST_STAFF;

alter table department 
   drop foreign key FK_DEPARTME_BRANCH_DE_BRANCH_B;

alter table loan 
   drop foreign key FK_LOAN_BRANCH_LO_BRANCH_B;

alter table loan 
   drop foreign key FK_LOAN_SETUP_CUS_CUSTOM;

alter table loan_account 
   drop foreign key FK_LOAN_ACC_LOAN_ACCO_ACCOUNT;

alter table pay 
   drop foreign key "FK_PAY_LOAN-PAY_LOAN";

alter table saving_account 
   drop foreign key FK_SAVING_A_SAVING_AC_ACCOUNT;

alter table staff 
   drop foreign key FK_STAFF_STAFF_DEP_DEPARTME;

drop table if exists account;

drop table if exists branch_bank;


alter table custom 
   drop foreign key FK_CUSTOM_RELATION__RELATION;

alter table custom 
   drop foreign key FK_CUSTOM_SETUP_CUS_LOAN;

drop table if exists custom;


alter table custom_branch_loan 
   drop foreign key FK_CUSTOM_B_OWN_3_CUSTOM;

alter table custom_branch_loan 
   drop foreign key FK_CUSTOM_B_OWN_4_BRANCH_B;

alter table custom_branch_loan 
   drop foreign key FK_CUSTOM_B_OWN_LOAN__LOAN_ACC;

drop table if exists custom_branch_loan;


alter table custom_branch_saving 
   drop foreign key FK_CUSTOM_B_OWN_1_CUSTOM;

alter table custom_branch_saving 
   drop foreign key FK_CUSTOM_B_OWN_2_BRANCH_B;

alter table custom_branch_saving 
   drop foreign key FK_CUSTOM_B_OWN_SAVIN_SAVING_A;

drop table if exists custom_branch_saving;


alter table custom_own_loan 
   drop foreign key FK_CUSTOM_O_CUSTOM_OW_CUSTOM;

alter table custom_own_loan 
   drop foreign key FK_CUSTOM_O_CUSTOM_OW_LOAN;

drop table if exists custom_own_loan;


alter table custom_staff 
   drop foreign key FK_CUSTOM_S_CUSTOM_ST_CUSTOM;

alter table custom_staff 
   drop foreign key FK_CUSTOM_S_CUSTOM_ST_STAFF;

drop table if exists custom_staff;


alter table department 
   drop foreign key FK_DEPARTME_BRANCH_DE_BRANCH_B;

drop table if exists department;


alter table loan 
   drop foreign key FK_LOAN_SETUP_CUS_CUSTOM;

alter table loan 
   drop foreign key FK_LOAN_BRANCH_LO_BRANCH_B;

drop table if exists loan;


alter table loan_account 
   drop foreign key FK_LOAN_ACC_LOAN_ACCO_ACCOUNT;

drop table if exists loan_account;


alter table pay 
   drop foreign key "FK_PAY_LOAN-PAY_LOAN";

drop table if exists pay;

drop table if exists relation;


alter table saving_account 
   drop foreign key FK_SAVING_A_SAVING_AC_ACCOUNT;

drop table if exists saving_account;


alter table staff 
   drop foreign key FK_STAFF_STAFF_DEP_DEPARTME;

drop table if exists staff;

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

