CREATE TABLE users (
  id bigint GENERATED ALWAYS AS IDENTITY,
  sub VARCHAR(255) NOT NULL UNIQUE,
  PRIMARY KEY(id)
);

CREATE TABLE user_login (
  id bigint GENERATED ALWAYS AS IDENTITY,
  user_id bigint NOT NULL,
  login_time timestamp NOT NULL DEFAULT DATE_TRUNC('second', NOW()),
  oidc_login_time timestamp NOT NULL,
  PRIMARY KEY(id),
  CONSTRAINT fk_user
    FOREIGN KEY(user_id)
        REFERENCES users
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE smartland_values (
    id bigint GENERATED ALWAYS AS IDENTITY,
    current_value DECIMAL NOT NULL,
    user_id bigint NOT NULL,
    upload_time timestamp NOT NULL DEFAULT DATE_TRUNC('second', NOW()),
    accounting_period INTEGER NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT fk_user
        FOREIGN KEY(user_id)
            REFERENCES users
            ON DELETE CASCADE
            ON UPDATE CASCADE
);