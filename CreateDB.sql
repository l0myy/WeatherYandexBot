create sequence subscriptions_id_seq;

CREATE TABLE IF NOT EXISTS public.subscriptions
(
    id integer NOT NULL DEFAULT nextval('subscriptions_id_seq'::regclass),
    user_id character varying COLLATE pg_catalog."default",
    status boolean DEFAULT true,
    notif_time time with time zone,
    city character varying COLLATE pg_catalog."default",
    CONSTRAINT subscriptions_pkey PRIMARY KEY (id)
);