CREATE TABLE songs (
 id serial not null primary key,
 title text not null,
 link text not null,
 duration int not null,
 userid text not null,
 uploader varchar(25) not null
);

CREATE INDEX songs_title on songs (title);

CREATE TABLE permissions (
    id serial not null primary key,
    username varchar(25) not null,
    level int not null
);