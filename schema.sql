create table test.telegram_users
(
    id         integer not null
        constraint telegram_users_pk
            primary key,
    created_at timestamp default now()
);