drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title string not null,
  done integer default '0'
);