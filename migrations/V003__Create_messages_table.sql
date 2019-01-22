CREATE TABLE messages (
  id serial primary key,
  guildid text not null,
  guildname text not null,
  userid text not null,
  username text not null,
  content text not null
);