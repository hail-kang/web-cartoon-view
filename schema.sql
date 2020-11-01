create table author(
    authorid int not null auto_increment,
    name varchar(50) not null,
    primary key(authorid)
);

create table cartoon(
    cartoonid int not null auto_increment,
    title varchar(100) not null,
    complete int not null,
    platform int not null,
    authorid int not null,
    primary key(cartoonid),
    foreign key(authorid) references author(authorid)
);

create table genre(
    genreid int not null auto_increment,
    name varchar(30) not null,
    primary key(genreid)
);

create table cartoon_genre(
    cartoon_genre_id int not null auto_increment,
    cartoonid int not null,
    genreid int not null,
    primary key(cartoon_genre_id),
    foreign key(cartoonid) references cartoon(cartoonid),
    foreign key(genreid) references genre(genreid)
);

create table story(
    storyid int not null auto_increment,
    number int not null,
    cartoonid int not null,
    primary key(storyid),
    foreign key(cartoonid) references cartoon(cartoonid)
);

insert into author(name) values('김규삼')
insert into cartoon(title, complete, platform, authorid) values('개장수', 2, 2, 2);
insert into cartoon(title, complete, platform, authorid) values('하이브1~2', 2, 2, 2);
insert into cartoon(title, complete, platform, authorid) values('하이브3', 2, 2, 2);
insert into cartoon(title, complete, platform, authorid) values('쌉니다 천리마마트', 2, 2, 2);

insert into story(number, cartoonid) values(1, 2);
insert into story(number, cartoonid) values(2, 2);
insert into story(number, cartoonid) values(3, 2);
insert into story(number, cartoonid) values(4, 2);
insert into story(number, cartoonid) values(5, 2);
insert into story(number, cartoonid) values(6, 2);
insert into story(number, cartoonid) values(7, 2);
insert into story(number, cartoonid) values(8, 2);
insert into story(number, cartoonid) values(9, 2);
insert into story(number, cartoonid) values(10, 2);
insert into story(number, cartoonid) values(11, 2);
insert into story(number, cartoonid) values(12, 2);
insert into story(number, cartoonid) values(13, 2);
insert into story(number, cartoonid) values(14, 2);
insert into story(number, cartoonid) values(15, 2);
insert into story(number, cartoonid) values(16, 2);
insert into story(number, cartoonid) values(17, 2);
insert into story(number, cartoonid) values(18, 2);
insert into story(number, cartoonid) values(19, 2);
insert into story(number, cartoonid) values(20, 2);
insert into story(number, cartoonid) values(21, 2);
insert into story(number, cartoonid) values(22, 2);
insert into story(number, cartoonid) values(23, 2);
insert into story(number, cartoonid) values(24, 2);
insert into story(number, cartoonid) values(25, 2);
insert into story(number, cartoonid) values(26, 2);
insert into story(number, cartoonid) values(27, 2);
insert into story(number, cartoonid) values(28, 2);
insert into story(number, cartoonid) values(29, 2);
insert into story(number, cartoonid) values(30, 2);
insert into story(number, cartoonid) values(31, 2);