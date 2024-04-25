-- Active: 1712909736541@@127.0.0.1@3306@db

create table Book(
    ID char(8) primary key,
    name varchar(10) not null,
    author varchar(10),
    price float,
    status int default 0,
    times int default 0
);
create table Reader(
    ID char(8) primary key,
    name varchar(10),
    age int,
    address varchar(20)
);
create table Borrow(
    book_ID char(8),
    Reader_ID char(8),
    Borrow_Date date,
    Return_Date date,
    primary key(book_ID, Reader_ID),
    foreign key(book_ID) references Book(ID),
    foreign key(Reader_ID) references Reader(ID)
);

-- (1)
select ID, address from Reader where name = 'Rose';
-- (2)
select b.name, Borrow_Date from Book b, Borrow br, Reader r where r.name = 'Rose' and r.ID = br.Reader_ID and b.ID = br.book_ID;
-- (3)
select name from Reader where ID not in (select Reader_ID from Borrow);
-- (4)
select name, price from Book where author = 'Ullman';
-- (5)
select b.ID, b.name from Book b, Borrow br, Reader r where r.name = '李林' and r.ID = br.Reader_ID and b.ID = br.book_ID and br.Return_Date is null;
-- (6)
select r.name from Reader r, Borrow br where r.ID = br.Reader_ID group by br.Reader_ID having count(*) > 3;
-- (7)
select r.name, r.ID from Reader r where r.ID not in (select Reader_ID from Borrow where book_ID in (select book_ID from Borrow b,Reader r where r.name = '李林' and b.Reader_ID = r.ID));
-- (8)
select ID, name from Book where name like '%MySQL%';
-- (9)
select Reader_ID, name, age, count(*) as borrow_num from Borrow b, Reader r where b.Reader_ID = r.ID and Borrow_Date between '2021-01-01' and '2021-12-31' group by Reader_ID order by borrow_num desc limit 20;
-- (10)
create view BorrowInfo as select r.ID, r.name as reader_name, br.book_ID, b.name as book_name, Borrow_Date from Reader r, Borrow br, Book b where r.ID = br.Reader_ID and b.ID = br.book_ID;
select ID, count(distinct book_ID) as borrow_num from BorrowInfo where Borrow_Date between '2022-01-01' and '2022-12-31' group by ID;


create procedure updateBookID(IN oldID char(8), IN newID char(8))
begin
    if oldID like '00%' then
        signal sqlstate '45000' set message_text = 'Can not update super ID to super ID';
    else
        if newID like '00%' then
            signal sqlstate '45000' set message_text = 'Can not update normal ID to super ID';
        else
            SET FOREIGN_KEY_CHECKS = 0;
            update Book set ID = newID where ID = oldID;
            SET FOREIGN_KEY_CHECKS = 1;
        end if;
    end if;
end;

CALL updateBookID('00b00001', '00b00002');
CALL updateBookID('b1', '00b00001');
CALL updateBookID('00b00001', 'b3');
CALL updateBookID('b10000', '00b10000');


create trigger updateStatusAndTimes after insert on Borrow
for each row
begin
    update Book set status = 1, times = times + 1 where ID = new.book_ID;
end;
create trigger updateStatus after update on Borrow
for each row
begin
    update Book set status = 0 where ID = new.book_ID and new.Return_Date is not null;
end;

insert into Borrow value('00b00001', 'r1', '2024-04-8', NULL);
update Borrow set Return_Date = '2024-04-8' where book_ID = '00b00001' and Reader_ID = 'r1';

insert into Borrow value('00b00002', 'r1', '2024-04-9', NULL);

