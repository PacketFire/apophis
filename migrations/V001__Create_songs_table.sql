CREATE TABLE songs (
  id serial primary key,
  title text not null,
  link text not null,
  duration int not null,
  userid text not null,
  uploader varchar(25) not null
);

CREATE INDEX songs_title on songs (title);
CREATE INDEX songs_link on songs (link);
