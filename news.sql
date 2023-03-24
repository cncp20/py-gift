CREATE DATABASE vega;
USE vega;
CREATE TABLE t_type(
	id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
	type VARCHAR(20) NOT NULL UNIQUE
);

INSERT INTO t_type(type) VALUE("要闻"), ("体育"),("科技"),("娱乐"),("历史");

CREATE TABLE t_role(
	id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
	role VARCHAR(20) NOT NULL UNIQUE
);

INSERT INTO t_role(role) VALUE("管理员"), ("新闻编辑");

CREATE TABLE t_user(
	id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
	username VARCHAR(20) NOT NULL UNIQUE,
	password VARCHAR(500) NOT NULL,
	email VARCHAR(100) NOT NULL,
	role_id INT UNSIGNED NOT NULL,
	INDEX(username)
);

INSERT INTO t_user(username, password, email, role_id)
VALUES("editor", HEX(AES_ENCRYPT("123456","HelloWorld")), "editor@126.com",2);

CREATE TABLE t_news(
	id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
	title VARCHAR(40) NOT NULL,
	editor_id INT UNSIGNED NOT NULL,
	type_id INT UNSIGNED NOT NULL,
	content_id CHAR(12) NOT NULL,
	is_top TINYINT UNSIGNED NOT NULL,
	create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	update_time TIMESTAMP	NOT NULL DEFAULT CURRENT_TIMESTAMP,
	state ENUM("草稿", "待审批", "已审批", "隐藏") NOT NULL,
	INDEX(editor_id),
	INDEX(type_id),
	INDEX(state),
	INDEX(create_time),
	INDEX(is_top)
);