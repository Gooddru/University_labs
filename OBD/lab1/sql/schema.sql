CREATE TABLE accounts
(
    account_id        SERIAL PRIMARY KEY,
    email             VARCHAR(255) UNIQUE                 NOT NULL CHECK (email ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'),
    password_hash     VARCHAR(255)                        NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);


CREATE TABLE channels
(
    channel_id    SERIAL PRIMARY KEY,
    account_id    INT                                 NOT NULL REFERENCES accounts (account_id),
    name          VARCHAR(100)                        NOT NULL CHECK (length(name) > 0),
    description   TEXT,
    avatar_url    VARCHAR(500),
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE channel_statistics
(
    channel_id        INT PRIMARY KEY REFERENCES channels (channel_id),
    total_views       BIGINT DEFAULT 0 NOT NULL CHECK (total_views >= 0),
    total_subscribers INT    DEFAULT 0 NOT NULL CHECK (total_subscribers >= 0),
    strikes_count     INT    DEFAULT 0 NOT NULL CHECK (strikes_count >= 0)
);

CREATE TABLE subscriptions
(
    subscriber_channel_id INT REFERENCES channels (channel_id),
    target_channel_id     INT REFERENCES channels (channel_id),
    subscription_date     TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (subscriber_channel_id, target_channel_id),
    CHECK (subscriber_channel_id != target_channel_id)
);

CREATE TABLE videos
(
    video_id    SERIAL PRIMARY KEY,
    channel_id  INT                                 NOT NULL REFERENCES channels (channel_id),
    title       VARCHAR(200)                        NOT NULL CHECK (length(title) > 0),
    video_url   VARCHAR(500) UNIQUE                 NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE comments
(
    comment_id SERIAL PRIMARY KEY,
    video_id   INT                                 NOT NULL REFERENCES videos (video_id),
    channel_id INT                                 NOT NULL REFERENCES channels (channel_id),
    content    TEXT                                NOT NULL CHECK (length(content) > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE video_likes
(
    channel_id INT REFERENCES channels (channel_id),
    video_id   INT REFERENCES videos (video_id),
    liked_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (channel_id, video_id)
);

CREATE TABLE channel_roles
(
    channel_id             INT REFERENCES channels (channel_id),
    participant_channel_id INT REFERENCES channels (channel_id),
    role                   VARCHAR(20)                         NOT NULL CHECK (role IN ('creator', 'moderator', 'user')),
    assigned_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (channel_id, participant_channel_id)
);

CREATE UNIQUE INDEX one_creator_per_channel_idx
    ON channel_roles (channel_id)
    WHERE role = 'creator';