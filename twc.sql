create schema twc;

create table twc.customer(
    id serial primary key,
    first_name text not null,
    last_name text not null,
    display_name text not null,
    default_email text not null,
    client_id text not null,
    login text not null,
    expires_in text not null,
    access_token text not null,
    refresh_token text not null,
    created timestamp not null default now()
);
