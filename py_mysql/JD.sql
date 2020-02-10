-- 创建 “京东” 数据库
DROP DATABASE IF EXISTS `JD`;
CREATE DATABASE `JD` CHARSET=utf8;

-- 使用 “京东” 数据库
use JD;

-- 创建一个商品goods数据表
DROP TABLE IF EXISTS `goods`; 
CREATE TABLE goods(
	`id` INT UNSIGNED AUTO_INCREMENT NOT NULL,
	`name` VARCHAR(150) NOT NULL,
	`cate_name` VARCHAR(40) NOT NULL,
	`brand_name` VARCHAR(40) NOT NULL,
	`price` DECIMAL(10, 3) NOT NULL,
	`is_show` BIT NOT NULL DEFAULT 1,
	`is_saleoff` BIT NOT NULL DEFAULT 0,
	PRIMARY KEY(`id`)
);

-- 向goods表中插入数据
INSERT INTO goods VALUES(0, "r510v 15.6英寸笔记本电脑", "笔记本", "联想", "3399", DEFAULT,DEFAULT);
INSERT INTO goods VALUES(0, "y440 14.0英寸笔记本电脑", "笔记本", "联想", "4999", DEFAULT, DEFAULT);
INSERT INTO goods VALUES(0, "g150th 15.6英寸笔记本电脑", "游戏本", "雷神", "8499", DEFAULT, DEFAULT);
INSERT INTO goods VALUES(0, "x550cc 15.6英寸笔记本电脑", "笔记本", "华硕", "2799", DEFAULT, DEFAULT);
INSERT INTO goods VALUES(0, "x240 超级本", "笔记本", "联想", "4880", DEFAULT, DEFAULT);
INSERT INTO goods VALUES(0, "u330p 13.3英寸超级本", "超级本", "联想", "4299", DEFAULT, DEFAULT);
INSERT INTO goods VALUES(0, "svp13226scb 触控超级本", "超级本", "索尼", "7999", DEFAULT, DEFAULT);
INSERT INTO goods VALUES(0, "ipad mini 7.9英寸平板电脑", "平板电脑", "苹果", "1998", DEFAULT, DEFAULT);
INSERT INTO goods VALUES(0, "ipad air2 9.7英寸平板电脑", "平板电脑", "苹果", "3888", DEFAULT, DEFAULT);
INSERT INTO goods VALUES(0, "ideacentre c340 20英寸一体电脑", "台式机", "联想", "3499", DEFAULT, DEFAULT);
INSERT INTO goods VALUES(0, "vastro 3800-r1026 台式电脑", "台式机", "戴尔", "2899", DEFAULT, DEFAULT);
INSERT INTO goods VALUES(0, "imac mc086cb/a 21.5英寸一体电脑", "台式机", "苹果", "9188", DEFAULT, DEFAULT);
INSERT INTO goods VALUES(0, "at7-7474lp 台式电脑 linux", "台式机", "宏基", "3699", DEFAULT, DEFAULT);
INSERT INTO goods VALUES(0, "z220sff f4f06pg工作站", "服务器/工作站", "惠普", "4288", DEFAULT, DEFAULT);
INSERT INTO goods VALUES(0, "poweredgeii 服务器", "服务器/工作站", "戴尔", "5388", DEFAULT, DEFAULT);
INSERT INTO goods VALUES(0, "mac pro专业级台式电脑", "服务器/工作站", "苹果", "28888", DEFAULT, DEFAULT);
INSERT INTO goods VALUES(0, "hmz-t3w 头戴显示器", "笔记本配件", "索尼", "6999", DEFAULT, DEFAULT);
INSERT INTO goods VALUES(0, "商务双肩包", "笔记本配件", "索尼", "99", DEFAULT, DEFAULT);
INSERT INTO goods VALUES(0, "x3250 m4机架式服务器", "服务器/工作站", "索尼", "99", DEFAULT, DEFAULT);
INSERT INTO goods VALUES(0, "商务双肩包", "笔记本配件", "戴尔", "99", DEFAULT, DEFAULT);
