-- 创建商品分类表
CREATE TABLE IF NOT EXISTS goods_cates(
	`id` int UNSIGNED AUTO_INCREMENT NOT NULL,
	`name` varchar(40) NOT NULL,
	PRIMARY KEY(`id`)
);

-- 查询goods表中商品的种类
SELECT cate_name FROM goods GROUP BY cate_name;

-- 将分组结果写入到goods_cates数据表中
INSERT INTO goods_cates(name) SELECT cate_name FROM goods GROUP BY cate_name;

-- 同步表数据
-- 通过goods_cates表来更新goods表
UPDATE goods AS g INNER JOIN goods_cates AS c ON g.cate_name = c.name SET g.cate_name = c.id; 

-- 创建商品品牌表
CREATE TABLE IF NOT EXISTS goods_brands(
	`id` int UNSIGNED AUTO_INCREMENT NOT NULL,
	`name` varchar(40) NOT NULL,
	PRIMARY KEY(`id`)
);

-- 将goods表中的商品品牌写入goods_brand表中
INSERT INTO goods_brands(name) SELECT brand_name FROM goods GROUP BY brand_name;

-- -- 创建表+写入表可以一步到位
-- -- 注意这里需要对 brand_name 用 as 起别名，否则 name 字段就没有值
-- CREATE TABLE IF NOT EXISTS goods_brands(
-- 	`id` int UNSIGNED AUTO_INCREMENT NOT NULL,
-- 	`name` varchar(40) NOT NULL
-- ) SELECT brand_name AS name FROM goods GROUP BY brand_name;

-- 通过goods_brands表来更新goods表
UPDATE goods as g INNER JOIN goods_brands AS b ON g.brand_name = b.name SET g.brand_name = b.id;

-- 修改goods中的字段及约束
ALTER TABLE goods CHANGE cate_name cate_id INT UNSIGNED NOT NULL;
ALTER TABLE goods CHANGE brand_name brand_id INT UNSIGNED NOT NULL;

-- 将goods中的cate_id与bran_id设置为外键，并与goods_cates，goods_brands相关联
ALTER TABLE goods ADD FOREIGN KEY (cate_id) REFERENCES goods_cates(id); 
ALTER TABLE goods ADD FOREIGN KEY (brand_id) REFERENCES goods_brands(id); 

-- 删除外键, 分两步:
-- 1、查询外键名称
SHOW CREATE TABLE goods;

-- goods | CREATE TABLE `goods` (
--   `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
--   `name` varchar(150) NOT NULL,
--   `cate_id` int(10) unsigned NOT NULL,
--   `brand_id` int(10) unsigned NOT NULL,
--   `price` decimal(10,3) NOT NULL,
--   `is_show` bit(1) NOT NULL DEFAULT b'1',
--   `is_saleoff` bit(1) NOT NULL DEFAULT b'0',
--   PRIMARY KEY (`id`),
--   KEY `cate_id` (`cate_id`),
--   KEY `brand_id` (`brand_id`),
--   CONSTRAINT `goods_ibfk_1` FOREIGN KEY (`cate_id`) REFERENCES `goods_cates` (`id`),
--   CONSTRAINT `goods_ibfk_2` FOREIGN KEY (`brand_id`) REFERENCES `goods_brands` (`id`)
-- ) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8 |


-- 2、根据名称删除外键 
ALTER TABLE goods DROP FOREIGN KEY goods_ibfk_1;
-- 在实际开发中尽量少使用外键，外键的存在会极大的降低SQL的运行效率
