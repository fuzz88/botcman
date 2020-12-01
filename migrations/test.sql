create table avatars (id SERIAL PRIMARY KEY, filename varchar(256), bin_data bytea);
create table bot_users (id SERIAL PRIMARY KEY, username varchar(256), first_name varchar(256), last_name varchar(256), chat_id bigint NOT NULL, ava_id int references avatars (id) ON DELETE CASCADE);

create table bot_users (id SERIAL PRIMARY KEY, username varchar(256), first_name varchar(256), last_name varchar(256), chat_id bigint NOT NULL);
create table avatars (id SERIAL PRIMARY KEY, user_id int references bot_users(id) on delete cascade NOT NULL, filename varchar(256) NOT NULL, bin_data bytea NOT NULL);
