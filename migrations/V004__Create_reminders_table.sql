CREATE TABLE reminders (
    id serial primary key,
    reminder_date text not null,
    date_of text not null,
    author text not null,
    reminder text not null,
    channel text not null
);