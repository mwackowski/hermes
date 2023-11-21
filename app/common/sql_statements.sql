create database aidevs;

\c aidevs

create table knowledge_simple (
uuid varchar(36),
insert_date date,
content text,
source varchar(100));
