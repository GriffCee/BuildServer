USE build_stats_db;

DROP TABLE IF EXISTS build_stats;

CREATE TABLE IF NOT EXISTS build_stats (
    rdi_id               INT             NOT NULL AUTO_INCREMENT,
    commit_tag           VARCHAR(45)     NOT NULL,
    upload_time          DATETIME            NOT NULL,
    build_time           DATETIME,
    build_end_time       DATETIME,           
    status               VARCHAR(10),
    artifacts_dir_name   VARCHAR(25),
    PRIMARY KEY (rdi_id) 
);
