# ebhs
在mac上可用的ebhs可视化库-自用版
![Test](https://github.com/ArtificialYi/PyEbhs/actions/workflows/test.yml/badge.svg?branch=master)
![Lint](https://github.com/ArtificialYi/PyEbhs/actions/workflows/lint.yml/badge.svg?branch=master)

## MYSQL相关
```
CREATE TABLE `active_schedule` (
    `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '唯一的自增标识',
    `time_node` datetime NOT NULL COMMENT '时间节点',
    `time_except` datetime NOT NULL COMMENT '时间节点',
    `cycle` integer UNSIGNED NOT NULL DEFAULT 1 COMMENT '周期',
    `deleted_date` datetime NOT NULL DEFAULT '9999-12-31 23:59:59' COMMENT '数据删除时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `idx_node` (`time_node`,`deleted_date`) COMMENT '有效的相同活跃时间节点只能存在一个',
    KEY `idx_cur` (`time_except`,`deleted_date`) COMMENT '数据展示使用'
) ENGINE=InnoDB
DEFAULT CHARACTER SET=utf8mb4 COLLATE=utf8mb4_0900_as_cs
COMMENT='活跃时间表';
```
```
CREATE TABLE `history_schedule` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '唯一的自增标识',
  `time_node` date NOT NULL COMMENT '时间节点',
  `time_real` date NOT NULL COMMENT '实际回顾时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_cur` (`time_real`,`time_node`) USING BTREE COMMENT '数据展示使用'
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_as_cs
COMMENT='历史回顾时间表';
```