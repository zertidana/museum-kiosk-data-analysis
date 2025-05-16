
DROP TABLE IF EXISTS exhibition CASCADE;
DROP TABLE IF EXISTS department CASCADE;
DROP TABLE IF EXISTS floor CASCADE;
DROP TABLE IF EXISTS rating_interaction CASCADE;
DROP TABLE IF EXISTS request_interaction;
DROP TABLE IF EXISTS rating CASCADE;
DROP TABLE IF EXISTS request CASCADE;


CREATE TABLE rating (
    rating_id BIGINT NOT NULL,
    rating_type VARCHAR (30) NOT NULL,
    PRIMARY KEY (rating_id),

    CONSTRAINT rating_constraint CHECK (
        rating_id IN (-1, 0, 1, 2, 3, 4)
    )
);

CREATE TABLE request (
    request_id DECIMAL NOT NULL,
    request_type VARCHAR(30) NOT NULL UNIQUE,
    PRIMARY KEY (request_id),

    CONSTRAINT request_constraint CHECK (
        request_id IN (0.0, 1.0)
    )
);

CREATE TABLE request_interaction (
    request_interaction_id BIGINT GENERATED ALWAYS AS IDENTITY,
    request_id DECIMAL NOT NULL,
    request_at TIMESTAMP NOT NULL,
    PRIMARY KEY (request_interaction_id),
    FOREIGN KEY (request_id) REFERENCES request(request_id)
);

CREATE TABLE floor (
    floor_id BIGINT GENERATED ALWAYS AS IDENTITY,
    floor_name VARCHAR(30) NOT NULL UNIQUE,
    PRIMARY KEY (floor_id)
);

CREATE TABLE department (
    department_id BIGINT GENERATED ALWAYS AS IDENTITY,
    department_name VARCHAR(30) NOT NULL UNIQUE,
    PRIMARY KEY (department_id)
);

CREATE TABLE exhibition (
    exhibition_id BIGINT,
    exhibition_code VARCHAR (30) NOT NULL,
    exhibition_name VARCHAR (30) NOT NULL,
    start_date DATE NOT NULL,
    description TEXT NOT NULL,
    floor_id BIGINT NOT NULL,
    department_id BIGINT NOT NULL,
    PRIMARY KEY (exhibition_id),
    FOREIGN KEY (floor_id) REFERENCES floor(floor_id),
    FOREIGN KEY (department_id) REFERENCES department(department_id)
);

CREATE TABLE rating_interaction (
    rating_interaction_id BIGINT GENERATED ALWAYS AS IDENTITY,
    rating_at TIMESTAMP NOT NULL,
    exhibition_id BIGINT NOT NULL,
    rating_id BIGINT DEFAULT -1,
    request_id DECIMAL,
    PRIMARY KEY (rating_interaction_id),
    FOREIGN KEY (rating_id) REFERENCES rating(rating_id),
    FOREIGN KEY (request_id) REFERENCES request(request_id),
    FOREIGN KEY (exhibition_id) REFERENCES exhibition(exhibition_id)
);

-- Adding master data
INSERT INTO request (request_id, request_type) VALUES (1, 'emergency'), (0, 'assistance');

INSERT INTO rating (rating_id, rating_type) VALUES (-1, 'request'), (0, 'terrible'), (1, 'bad'), (2, 'neutral'), (3, 'good'), (4, 'amazing');

INSERT INTO department (department_name) VALUES ('entomology'), ('geology'), ('paleontology'), ('zoology'), ('ecology');

INSERT INTO floor (floor_name) VALUES ('vault'), ('1'), ('2'), ('3');

INSERT INTO exhibition (exhibition_id, exhibition_name, exhibition_code, start_date, description, floor_id, department_id) VALUES
(0, 'Adaptation', 'EXH_01', '2019-07-01', 'How insect evolution has kept pace with an industrialised world.', 1, 1),
(1, 'Measureless to Man', 'EXH_00', '2021-08-23', 'An immersive 3D experience: delve deep into a previously-inaccessible cave system.', 2, 2),
(2, 'Thunder Lizards', 'EXH_05', '2023-02-01', 'How new research is making scientists rethink what dinosaurs really looked like.', 2, 3),
(3, 'The Crenshaw Collection', 'EXH_02', '2021-03-01', 'An exhibition of 18th Century watercolours, mostly focused on South American wildlife.', 3, 4),
(4, 'Cetacean Sensations', 'EXH_03', '2019-07-01', 'Whales: from ancient myth to critically endangered.', 2, 4),
(5, 'Our Polluted World', 'EXH_04', '2021-05-12', 'A hard-hitting exploration of humanity impact on the environment.', 4, 5);


