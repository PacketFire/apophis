CREATE TABLE insults (
    id serial primary key,
    insult text not null,
    author text not null,
    added_on text not null
);
