DROP TABLE IF EXISTS message_meta;
DROP TABLE IF EXISTS message_type_meta;
DROP TABLE IF EXISTS message_text;

CREATE TABLE message_meta (
    mssg_id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    from_pvt_id BINARY(16) NOT NULL,
    to_pvt_id BINARY(16) NOT NULL,
    mssg_status ENUM ('sent', 'delivered', 'read') NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE message_type_meta (
    mssg_id BIGINT UNSIGNED PRIMARY KEY,
    mssg_type ENUM ('normal', 'reply', 'reaction') NOT NULL,
    attach_mssg_id BIGINT UNSIGNED,
    CONSTRAINT mssg_id_type_fk FOREIGN KEY (mssg_id) REFERENCES message_meta(mssg_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT attach_mssg_id_fk FOREIGN KEY (attach_mssg_id) REFERENCES message_meta(mssg_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE message_text (
    mssg_id BIGINT UNSIGNED PRIMARY KEY,
    mssg_body TEXT NOT NULL,
    CONSTRAINT mssg_id_text_fk FOREIGN KEY (mssg_id) REFERENCES message_meta(mssg_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
