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
    title varchar(100) not null,
    cartoonid int not null,
    primary key(storyid),
    foreign key(cartoonid) references cartoon(cartoonid)
);