create table users(
    id integer primary key autoincrement,
    username varchar(1, 30) unique,
    display_name varchar(1, 30),
    password varchar(8, 50),
    email varchar(1, 50),
    phone_number varchar(1, 20)
);

create table permissions(
    id integer primary key autoincrement,
    permission_name varchar(1, 20) unique not null
);

create table user_permissions(
    user_id integer,
    permission_id integer,
    constraint pk_user_perms primary key(user_id, permission_id),
    constraint fk_user_perms_user foreign key(user_id)
        references users(id) on delete cascade,
    constraint fk_user_perms_perm foreign key(permission_id)
        references permissions(id) on delete cascade
);

create table threads(
    id integer primary key autoincrement,
    author_id integer,
    date_posted timestamp not null default current_timestamp,
    title varchar(1, 100) not null,
    description text not null,
    constraint fk_threads_author foreign key(author_id)
        references users(id) on delete set null
);

create table tags(
    id integer primary key autoincrement,
    tag_name varchar(1, 20),
    color char(7, 7)
);

create table thread_tags(
    thread_id integer,
    tag_id integer,
    constraint pk_thread_tags primary key(thread_id, tag_id),
    constraint fk_thread_tags_thread foreign key(thread_id)
        references threads(id) on delete cascade,
    constraint fk_thread_tags_tag foreign key(tag_id)
        references tags(id) on delete cascade
);

create table comments(
    id integer primary key autoincrement,
    thread_id integer not null,
    user_id integer,
    date_posted timestamp not null default current_timestamp,
    comment_text text not null,
    constraint fk_comments_thread foreign key(thread_id)
        references threads(id) on delete cascade,
    constraint fk_comments_user foreign key(user_id)
        references users(id) on delete set null
);
