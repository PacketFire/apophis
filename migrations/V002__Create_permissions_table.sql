CREATE TABLE permissions (
  id serial primary key,
  username varchar(25) not null,
  level int not null
);

CREATE UNIQUE INDEX permissions_username on permissions (username);
