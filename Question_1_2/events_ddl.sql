--Colors
CREATE TABLE colors (
    id smallint NOT NULL UNIQUE,
    color_name character varying NOT NULL
);
CREATE SEQUENCE colors_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE colors_id_seq OWNED BY colors.id;
ALTER TABLE ONLY colors ALTER COLUMN id SET DEFAULT nextval('colors_id_seq'::regclass);
ALTER TABLE ONLY colors ADD CONSTRAINT colors_pkey PRIMARY KEY (color_name);

-- Event Types
CREATE TABLE event_types (
    id smallint NOT NULL UNIQUE,
    event_name character varying NOT NULL
);
CREATE SEQUENCE event_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE event_types_id_seq OWNED BY event_types.id;
ALTER TABLE ONLY event_types ALTER COLUMN id SET DEFAULT nextval('event_types_id_seq'::regclass);
ALTER TABLE ONLY event_types ADD CONSTRAINT event_types_pkey PRIMARY KEY (event_name);

--Events (Half Normalized)
CREATE TABLE events (
    id bigint NOT NULL,
    event_type_id smallint NOT NULL,
    user_name character varying,
    password character varying(100),
    color_id smallint NOT NULL,
    name character varying NOT NULL,
    food character varying(50) NOT NULL,
    confirmed boolean DEFAULT false NOT NULL,
    signup_date date NOT NULL 
);
CREATE SEQUENCE events_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE events_id_seq OWNED BY events.id;
ALTER TABLE ONLY events ALTER COLUMN id SET DEFAULT nextval('events_id_seq'::regclass);
ALTER TABLE ONLY events ADD CONSTRAINT events_pkey PRIMARY KEY (id);
CREATE INDEX idx_color ON events USING btree (color_id);
CREATE INDEX idx_name ON events USING btree (name varchar_ops);
ALTER TABLE ONLY events ADD CONSTRAINT events_color_fkey FOREIGN KEY (color_id) REFERENCES colors(id);
ALTER TABLE ONLY events ADD CONSTRAINT events_event_type_id_fkey FOREIGN KEY (event_type_id) REFERENCES event_types(id);


--Events (JSONB version)
CREATE TABLE events_json (
    id bigint NOT NULL,
    event_type character varying(50) NOT NULL,
    user_name character varying(50),
    password character varying(100),
    event jsonb NOT NULL,
    metadata_name character varying(50),
    metadata_last_name character varying(50),
    metadata_color character varying(50)
);
CREATE SEQUENCE events_json_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE events_json_id_seq OWNED BY events_json.id;
ALTER TABLE ONLY events_json ALTER COLUMN id SET DEFAULT nextval('events_json_id_seq'::regclass);
ALTER TABLE ONLY events_json ADD CONSTRAINT events_json_pkey PRIMARY KEY (id);
CREATE INDEX idx_json_color ON events_json USING btree (metadata_color varchar_ops);
CREATE INDEX idx_json_last_name ON events_json USING btree (metadata_last_name varchar_ops);
CREATE INDEX idx_json_name ON events_json USING btree (metadata_name varchar_ops);
CREATE INDEX idx_jsonb_name ON events_json USING gin (((event -> 'name'::text)));




