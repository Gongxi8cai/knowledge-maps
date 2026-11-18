# MySQL 知识地图

> 按「你要干什么」找工具。SQL 本身很小，真正的难点是索引、事务、以及「写得出结果但慢得不能用」——所以这三块在多个域里重复出现。

**12 个功能域 · 103 个条目 · 10 条基础通用 · 7 组交叉概念 · 12 条备注**　（自学 · 数据库入门）

按「你要干什么」找工具，而不是按语法书目录背。同一个功能若跨多个域，会在多个域里重复出现，并在「交叉」列标出它还在哪出现；基础通用与备注各自单列。

## 0.5 一页提纲（先扫这个）

- **安装与连接**：服务端与客户端 · 命令行登录 · 默认端口 · 看版本与状态 · 配置文件 · 图形客户端 · 连接串 · 远程连不上
- **库与表**：建库与切库 · 建表 · 常用类型 · 主键与自增 · 字符集 · 存储引擎 · 改表 · 看表结构 · 删表与删库
- **增删改**：插入一行 · 批量插入 · 更新 · 删除 · 存在则更新 · `REPLACE INTO` · 清空表 · 受影响行数 · 在事务里批量改
- **查询基础**：基本骨架 · 条件组合 · 范围与集合 · 模糊匹配 · 空值判断 · 去重 · 排序 · 分页 · 别名
- **聚合与分组**：五个聚合函数 · `COUNT(*)` vs `COUNT(列)` · 分组 · 分组后过滤 · 小计与总计 · 条件聚合 · 去重计数 · 聚合与 NULL
- **多表连接**：`INNER JOIN` · `LEFT JOIN` · 条件放 `ON` 还是 `WHERE` · 表别名 · 自连接 · 子查询 · `EXISTS` · `UNION` / `UNION ALL` · 笛卡尔积
- **索引与执行计划**：索引是什么 · 主键索引 · 唯一索引 · 联合索引 · 最左前缀 · 覆盖索引 · `EXPLAIN` · 索引失效 · 不要滥建
- **事务与锁**：ACID · 开始与提交 · 回滚 · 隔离级别 · 三种读异常 · 锁的粒度 · 死锁 · MVCC 快照 · 长事务的危害
- **约束与设计**：非空与默认 · 唯一约束 · 外键 · 检查约束 · 三范式 · 反范式 · 主键选择 · 命名规范 · ER 图 · 软删除
- **视图与存储程序**：视图 · 视图的代价 · 存储过程 · 触发器 · 事件调度 · 函数
- **用户与权限**：建用户 · 授权 · 收权 · 看权限 · 备份 · 恢复 · 只备份结构/数据 · 审计与日志
- **性能与优化**：慢查询日志 · 别 `SELECT *` · 深分页 · 避免列上运算 · 隐式转换 · 批量写入 · 连接池 · 看连接数 · 分表分库

## 1. 基础通用（第 0 层，单列）

| 条目 | 说明 | 例子 |
|---|---|---|
| SQL 的四类语句 | DDL 建表、DML 增删改、DQL 查询、DCL 权限 | `CREATE` / `INSERT` / `SELECT` / `GRANT` |
| 分号结束，大小写不敏感 | 关键字大小写都行，按团队规范统一即可 | `select * from buch;` |
| 字符串用单引号 | `'Hobbit'`；双引号在 ANSI 模式下会当标识符 | `WHERE titel = 'Hobbit'` |
| 标识符用反引号 | 表名/列名与关键字撞车时用反引号包起来 | `` `order` `` |
| `NULL` 不是 0、不是空串 | `= NULL` 永远不成立，要用 `IS NULL` | `WHERE autor IS NULL` |
| `WHERE` 过滤行，`HAVING` 过滤分组 | 聚合结果的条件写 `HAVING` | `HAVING COUNT(*) > 2` |
| 注释 | `-- 注释`（后面要有空格）、`/* 块注释 */` | `-- 按年份统计` |
| 改数据前先 `SELECT` | `UPDATE`/`DELETE` 不带 `WHERE` 会动全表 | 先查条件命中几行 |
| `EXPLAIN` 是诊断第一步 | 看它有没有走索引、扫了多少行 | `EXPLAIN SELECT ...` |
| 备份先于改结构 | `mysqldump` 一份再动 `ALTER` | `mysqldump -u root -p db > b.sql` |

## 2. 功能域（第 1 层）

第 2 列前面的〔〕是这一条的性质：〔SQL 关键字〕 / 〔函数〕 / 〔命令〕 / 〔写法〕——〔SQL 关键字〕要自己写，其余是现成的名字（查文档 / 查手册就行）。

### 2.1 安装与连接　<sub>Verbindung</sub>

先能连上：服务、端口、账号、客户端工具。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| 服务端与客户端 | 〔命令〕`mysqld` 是服务、`mysql` 是命令行客户端 | 装 MySQL Server 才有服务；只装 Workbench 连不上 | 入门 | 用户与权限 |
| 命令行登录 | 〔命令〕`mysql -u root -p`、`-h 主机 -P 端口` | `-p` 后不要跟密码（会留在历史里） | 入门 | — |
| 默认端口 | 〔写法〕`3306` | 被占用或改了端口就连不上 | 入门 | — |
| 看版本与状态 | 〔SQL 关键字〕`SELECT VERSION();`、`SHOW STATUS;` | 确认引擎与版本（8.0 vs 5.7 语法有差） | 常用 | — |
| 配置文件 | 〔函数〕`my.ini`（Windows）/ `my.cnf`（Linux） | 字符集、端口、数据目录都在这里 | 进阶 | 性能与优化 |
| 图形客户端 | 〔命令〕Workbench / DBeaver / Navicat / VS Code 插件 | 看表结构与数据更快；生产环境慎用「一键删库」 | 常用 | — |
| 连接串 | 〔命令〕`mysql://user:pw@host:3306/db` | 写代码时驱动用得到（pymysql/connector） | 常用 | — |
| 远程连不上 | 〔函数〕检查 `bind-address`、防火墙、用户 `host` 是否为 `%` | 三者任一为本地就拒外网 | 进阶 | 用户与权限 |

### 2.2 库与表　<sub>Schema</sub>

建库建表、选对数据类型——类型选错后面全是补丁。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| 建库与切库 | 〔SQL 关键字〕`CREATE DATABASE db CHARACTER SET utf8mb4;`、`USE db;` | 字符集在建库时就定好 | 入门 | — |
| 建表 | 〔SQL 关键字〕`CREATE TABLE buch (id INT PRIMARY KEY AUTO_INCREMENT, titel VARCHAR(200) NOT NULL);` | 列名、类型、约束一次写清 | 入门 | 约束与设计 |
| 常用类型 | 〔函数〕`INT` `BIGINT` `VARCHAR(n)` `TEXT` `DATE` `DATETIME` `DECIMAL(p,s)` `TINYINT(1)` | 金额用 `DECIMAL`，时间用 `DATETIME` | 入门 | — |
| 主键与自增 | 〔函数〕`id BIGINT PRIMARY KEY AUTO_INCREMENT` | 自增简单高效；分布式才考虑 UUID | 常用 | 索引 |
| 字符集 | 〔函数〕`utf8mb4` + `utf8mb4_0900_ai_ci` | MySQL 的 `utf8` 只有 3 字节，存不了 emoji | 常用 | — |
| 存储引擎 | 〔函数〕`ENGINE=InnoDB` | InnoDB 有事务、行锁、外键；MyISAM 没有 | 常用 | 事务与锁 |
| 改表 | 〔SQL 关键字〕`ALTER TABLE buch ADD COLUMN jahr INT;` | 大表加列会锁表，生产要挑时间 | 进阶 | 性能与优化 |
| 看表结构 | 〔SQL 关键字〕`SHOW TABLES;`、`DESCRIBE buch;`、`SHOW CREATE TABLE buch;` | 最后一条能看到完整 DDL 与索引 | 常用 | — |
| 删表与删库 | 〔SQL 关键字〕`DROP TABLE`、`DROP DATABASE` | 不可回滚——先备份 | 入门 | — |

### 2.3 增删改　<sub>DML</sub>

写入数据的三种动作；`UPDATE`/`DELETE` 的条件是命门。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| 插入一行 | 〔SQL 关键字〕`INSERT INTO buch (titel, jahr) VALUES ('Hobbit', 1937);` | 列名写全，避免表结构一变就错位 | 入门 | — |
| 批量插入 | 〔SQL 关键字〕`INSERT INTO buch (titel) VALUES ('A'),('B'),('C');` | 一次多行比循环快一个数量级 | 常用 | 性能与优化 |
| 更新 | 〔SQL 关键字〕`UPDATE buch SET jahr = 1937 WHERE id = 1;` | 先 `SELECT` 同样条件确认命中几行 | 入门 | — |
| 删除 | 〔SQL 关键字〕`DELETE FROM buch WHERE id = 1;` | 不带 `WHERE` 就是清空表 | 入门 | — |
| 存在则更新 | 〔SQL 关键字〕`INSERT ... ON DUPLICATE KEY UPDATE n = n + 1` | 计数器、幂等导入常用 | 进阶 | 索引 |
| `REPLACE INTO` | 〔SQL 关键字〕先删后插 | 会触发删除副作用，慎用 | 进阶 | — |
| 清空表 | 〔SQL 关键字〕`TRUNCATE TABLE buch;` | 比 `DELETE` 快，但不可回滚、重置自增 | 常用 | — |
| 受影响行数 | 〔函数〕`ROW_COUNT()`、客户端会打印 `Rows matched` | 0 行说明条件写错了 | 常用 | — |
| 在事务里批量改 | 〔SQL 关键字〕`START TRANSACTION; ... COMMIT;` | 要么全成要么全不成 | 进阶 | 事务与锁 |

### 2.4 查询基础　<sub>SELECT</sub>

`SELECT` 的骨架：选列、筛行、排序、限条数。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| 基本骨架 | 〔SQL 关键字〕`SELECT titel, jahr FROM buch WHERE jahr > 1900 ORDER BY jahr DESC LIMIT 10;` | 书写顺序固定，执行顺序是 FROM→WHERE→SELECT→ORDER→LIMIT | 入门 | — |
| 条件组合 | 〔SQL 关键字〕`AND` `OR` `NOT`，括号改变优先级 | `AND` 比 `OR` 优先，混用要括号 | 入门 | — |
| 范围与集合 | 〔SQL 关键字〕`BETWEEN 1 AND 5`、`IN (1,2,3)` | `IN` 里别放子查询的大结果集 | 常用 | 多表连接 |
| 模糊匹配 | 〔SQL 关键字〕`LIKE 'Hob%'`、`LIKE '%bit'` | 前置 `%` 用不上索引 | 常用 | 索引 |
| 空值判断 | 〔SQL 关键字〕`IS NULL` / `IS NOT NULL` | `= NULL` 永远假 | 常用 | — |
| 去重 | 〔SQL 关键字〕`SELECT DISTINCT autor FROM buch;` | `DISTINCT` 作用于整行组合 | 常用 | — |
| 排序 | 〔SQL 关键字〕`ORDER BY jahr DESC, titel ASC` | 多列排序按顺序生效；NULL 默认排最前 | 入门 | — |
| 分页 | 〔SQL 关键字〕`LIMIT 20 OFFSET 40` | 深分页很慢，见性能域 | 常用 | 性能与优化 |
| 别名 | 〔SQL 关键字〕`SELECT titel AS 书名` | 让结果列名可读；也给表起短别名 | 入门 | 多表连接 |

### 2.5 聚合与分组　<sub>Aggregation</sub>

把多行压成一行：计数、求和、分组统计。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| 五个聚合函数 | 〔函数〕`COUNT` `SUM` `AVG` `MAX` `MIN` | `AVG`/`SUM` 忽略 NULL | 入门 | — |
| `COUNT(*)` vs `COUNT(列)` | 〔函数〕前者数行，后者只数该列非 NULL 的行 | 想数总数就用 `COUNT(*)` | 常用 | — |
| 分组 | 〔SQL 关键字〕`SELECT autor, COUNT(*) FROM buch GROUP BY autor;` | SELECT 里非聚合列必须出现在 GROUP BY 中 | 入门 | 多表连接 |
| 分组后过滤 | 〔SQL 关键字〕`HAVING COUNT(*) >= 2` | `WHERE` 在分组前、`HAVING` 在分组后 | 常用 | 查询基础 |
| 小计与总计 | 〔SQL 关键字〕`GROUP BY ... WITH ROLLUP` | 多出一行汇总；也可用 `UNION` 拼 | 进阶 | — |
| 条件聚合 | 〔函数〕`SUM(CASE WHEN jahr < 1900 THEN 1 ELSE 0 END)` | 一行里算多个指标，避免多次扫表 | 进阶 | — |
| 去重计数 | 〔函数〕`COUNT(DISTINCT autor)` | 比 `COUNT(*)` 慢，数据量大要考虑预聚合 | 常用 | — |
| 聚合与 NULL | 〔函数〕`SUM` 全 NULL 时返回 NULL 而不是 0 | 要 0 用 `COALESCE(SUM(x), 0)` | 进阶 | — |

### 2.6 多表连接　<sub>JOIN</sub>

把表按关系拼起来；`LEFT JOIN` 与「过滤条件放 WHERE 还是 ON」是分水岭。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| `INNER JOIN` | 〔SQL 关键字〕`FROM buch b JOIN autor a ON b.autor_id = a.id` | 只保留两边都匹配的行 | 入门 | — |
| `LEFT JOIN` | 〔SQL 关键字〕`FROM autor a LEFT JOIN buch b ON ...` | 左表全保留，右表没有就补 NULL | 常用 | — |
| 条件放 `ON` 还是 `WHERE` | 〔SQL 关键字〕`LEFT JOIN` 的右表条件写 `ON` 才保留左表 | 放 `WHERE` 会退化成内连接——最常见的错 | 进阶 | 查询基础 |
| 表别名 | 〔SQL 关键字〕`FROM buch AS b` | 多表时必写，避免歧义 | 入门 | — |
| 自连接 | 〔SQL 关键字〕`FROM buch b1 JOIN buch b2 ON b1.autor_id = b2.autor_id` | 同一张表当两张用（找同作者的其他书） | 进阶 | — |
| 子查询 | 〔SQL 关键字〕`WHERE autor_id IN (SELECT id FROM autor WHERE land = 'DE')` | 能写但常比 JOIN 慢；相关子查询更慢 | 常用 | — |
| `EXISTS` | 〔SQL 关键字〕`WHERE EXISTS (SELECT 1 FROM ...)` | 只判断存在性，半连接常用 | 进阶 | — |
| `UNION` / `UNION ALL` | 〔SQL 关键字〕两个结果集上下拼接 | `UNION` 去重（有排序开销），能不去重就用 `ALL` | 常用 | — |
| 笛卡尔积 | 〔SQL 关键字〕`FROM a, b` 忘了写连接条件 | 行数 = 两表行数相乘，会把数据库拖死 | 入门 | 性能与优化 |

### 2.7 索引与执行计划　<sub>Index</sub>

索引用 B+ 树把「扫全表」换成「走树」；建什么索引取决于查询。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| 索引是什么 | 〔SQL 关键字〕`CREATE INDEX idx_autor ON buch(autor_id);` | 额外的一棵排序树，指向数据行 | 入门 | — |
| 主键索引 | 〔函数〕InnoDB 的主键就是聚簇索引 | 数据和主键存在一起，所以主键要短 | 常用 | 库与表 |
| 唯一索引 | 〔SQL 关键字〕`UNIQUE KEY uk_isbn (isbn)` | 既加速又保证唯一 | 常用 | 约束与设计 |
| 联合索引 | 〔SQL 关键字〕`INDEX idx_a_b (autor_id, jahr)` | 按「最左前缀」生效：能用在 `(autor_id)`、`(autor_id, jahr)` | 进阶 | — |
| 最左前缀 | 〔SQL 关键字〕`WHERE jahr = 1937` 用不上 `(autor_id, jahr)` | 列顺序按「等值在前、范围在后」设计 | 进阶 | 查询基础 |
| 覆盖索引 | 〔写法〕查询的列全在索引里，就不用回表 | `EXPLAIN` 里显示 `Using index` | 进阶+ | 性能与优化 |
| `EXPLAIN` | 〔SQL 关键字〕`EXPLAIN SELECT ...` 看 `type`/`key`/`rows`/`Extra` | `type=ALL` 是全表扫，`ref`/`range` 较好 | 常用 | 性能与优化 |
| 索引失效 | 〔函数〕列上套函数、隐式类型转换、前置 `%`、`OR` 混用 | 这四条能解释九成「明明有索引还是慢」 | 进阶 | — |
| 不要滥建 | 〔写法〕每个索引都拖慢写入、占空间 | 按真实查询建，定期清理不用的 | 常用 | 性能与优化 |

### 2.8 事务与锁　<sub>Transaktionen</sub>

一组操作要么全成要么全不成；隔离级别决定你能看见别人的什么。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| ACID | 〔写法〕原子性、一致性、隔离性、持久性 | InnoDB 用 redo/undo log + MVCC 实现 | 入门 | — |
| 开始与提交 | 〔SQL 关键字〕`START TRANSACTION; ... COMMIT;` / `ROLLBACK;` | 默认 autocommit=1，每条语句自己提交 | 入门 | — |
| 回滚 | 〔函数〕出错就 `ROLLBACK` | DDL 不能回滚（隐式提交） | 常用 | — |
| 隔离级别 | 〔SQL 关键字〕`READ UNCOMMITTED` `READ COMMITTED` `REPEATABLE READ`（默认）`SERIALIZABLE` | 级别越高越安全、并发越低 | 进阶 | — |
| 三种读异常 | 〔写法〕脏读、不可重复读、幻读 | 默认 RR 能挡住前两个，幻读靠间隙锁 | 进阶 | — |
| 锁的粒度 | 〔函数〕行锁（InnoDB）、表锁（MyISAM） | 没走索引的 `UPDATE` 可能锁一大片 | 进阶 | 索引 |
| 死锁 | 〔写法〕两个事务互相等对方的锁 | `SHOW ENGINE INNODB STATUS` 看最近一次；重试或统一加锁顺序 | 进阶+ | — |
| MVCC 快照 | 〔写法〕读不加锁，看到事务开始时的版本 | 所以「读」不会阻塞「写」 | 进阶+ | — |
| 长事务的危害 | 〔函数〕占着 undo、阻塞 DDL、放大死锁概率 | 事务里别做网络请求和等待 | 常用 | 性能与优化 |

### 2.9 约束与设计　<sub>Design</sub>

用约束把「不可能的数据」挡在数据库外；表结构决定后面好不好查。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| 非空与默认 | 〔SQL 关键字〕`NOT NULL DEFAULT 0` | 能非空就非空，NULL 会让查询与聚合变复杂 | 入门 | — |
| 唯一约束 | 〔SQL 关键字〕`UNIQUE (isbn)` | 业务唯一键要落到数据库 | 常用 | 索引 |
| 外键 | 〔SQL 关键字〕`FOREIGN KEY (autor_id) REFERENCES autor(id)` | 保证引用完整性；高并发系统常在应用层做 | 进阶 | — |
| 检查约束 | 〔SQL 关键字〕`CHECK (jahr > 0)` | 8.0.16+ 才真正生效 | 进阶 | — |
| 三范式 | 〔函数〕1NF 原子、2NF 无部分依赖、3NF 无传递依赖 | 先按范式设计，再按查询反范式 | 常用 | — |
| 反范式 | 〔函数〕冗余一列省一次 JOIN | 要有明确的性能理由，并保证一致性 | 进阶 | 多表连接 |
| 主键选择 | 〔函数〕自增 BIGINT vs UUID | 自增短、顺序写入快；UUID 便于分布式但索引更大 | 常用 | 库与表 |
| 命名规范 | 〔函数〕表名小写下划线、主键统一 `id`、外键 `xx_id` | 统一比「好看」重要 | 入门 | — |
| ER 图 | 〔写法〕实体—关系—基数 | 先画清楚一对多/多对多，再建表 | 常用 | — |
| 软删除 | 〔函数〕`deleted_at` 而不是真删 | 查询要处处带条件，别忘 | 进阶 | — |

### 2.10 视图与存储程序　<sub>Views</sub>

把复杂查询封成视图；把逻辑放进数据库要谨慎。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| 视图 | 〔SQL 关键字〕`CREATE VIEW v_buch AS SELECT ...` | 简化常用查询、限制可见列 | 常用 | — |
| 视图的代价 | 〔写法〕每次查询都重新执行 | 复杂视图套视图会变得很慢 | 进阶 | 性能与优化 |
| 存储过程 | 〔SQL 关键字〕`CREATE PROCEDURE p() BEGIN ... END` | 把多步逻辑放服务端；调试和版本管理更难 | 进阶 | — |
| 触发器 | 〔SQL 关键字〕`CREATE TRIGGER ... AFTER INSERT` | 隐式副作用，排错困难——能不用就不用 | 进阶+ | — |
| 事件调度 | 〔SQL 关键字〕`CREATE EVENT ... ON SCHEDULE EVERY 1 DAY` | 库内定时任务；要开 `event_scheduler` | 进阶+ | — |
| 函数 | 〔SQL 关键字〕`CREATE FUNCTION f(x INT) RETURNS INT` | 可在 SQL 里调用；注意确定性标记 | 进阶+ | — |

### 2.11 用户与权限　<sub>Rechte</sub>

最小权限、能备份能恢复——这两件事比会写复杂 SQL 更重要。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| 建用户 | 〔SQL 关键字〕`CREATE USER 'app'@'%' IDENTIFIED BY '强密码';` | `%` 允许远程，`localhost` 只本地 | 入门 | 安装与连接 |
| 授权 | 〔SQL 关键字〕`GRANT SELECT, INSERT ON db.* TO 'app'@'%';` | 只给需要的权限，别给 `ALL` | 常用 | — |
| 收权 | 〔SQL 关键字〕`REVOKE DELETE ON db.* FROM 'app'@'%';` | `FLUSH PRIVILEGES` 在直接改表时才需要 | 常用 | — |
| 看权限 | 〔SQL 关键字〕`SHOW GRANTS FOR 'app'@'%';` | 排查「为什么他能删我不能」 | 常用 | — |
| 备份 | 〔命令〕`mysqldump -u root -p --single-transaction db > b.sql` | InnoDB 加 `--single-transaction` 得到一致快照 | 常用 | — |
| 恢复 | 〔命令〕`mysql -u root -p db < b.sql` | 先建库再导入；大文件用 `source` | 常用 | — |
| 只备份结构/数据 | 〔函数〕`--no-data` / `--no-create-info` | 迁移表结构时很有用 | 进阶 | — |
| 审计与日志 | 〔函数〕`general_log`、`slow_query_log` | 生产只开慢查询日志，general_log 太重 | 进阶 | 性能与优化 |

### 2.12 性能与优化　<sub>Performance</sub>

先看慢查询日志，再 `EXPLAIN`，最后才改索引或改 SQL。

| 功能 | 关键字 / API | 用来做什么 | 阶段 | 交叉 |
|---|---|---|---|---|
| 慢查询日志 | 〔函数〕`slow_query_log = ON`、`long_query_time = 1` | 优化的入口：先知道哪条慢 | 常用 | — |
| 别 `SELECT *` | 〔写法〕只取需要的列 | 减少 IO，还可能走上覆盖索引 | 入门 | 索引 |
| 深分页 | 〔SQL 关键字〕`LIMIT 100000, 20` 会扫掉前 10 万行 | 用「记住上次最大 id」的游标分页 | 进阶 | 查询基础 |
| 避免列上运算 | 〔SQL 关键字〕`WHERE YEAR(datum) = 2026` 用不上索引 | 改成范围：`datum >= '2026-01-01' AND datum < '2027-01-01'` | 进阶 | 索引 |
| 隐式转换 | 〔写法〕字符串列传数字会全表扫 | 类型要对齐 | 进阶 | — |
| 批量写入 | 〔函数〕多行 `INSERT`、或 `LOAD DATA INFILE` | 减少往返与事务开销 | 常用 | 增删改 |
| 连接池 | 〔函数〕应用侧复用连接，别每条 SQL 连一次 | 连接建立比查询还贵 | 进阶 | — |
| 看连接数 | 〔SQL 关键字〕`SHOW PROCESSLIST;`、`max_connections` | 卡住时先看有没有长事务/锁等待 | 常用 | 事务与锁 |
| 分表分库 | 〔写法〕单表过千万再考虑 | 先优化索引与 SQL，别过早分片 | 进阶+ | — |

## 3. 交叉项总表（同一概念出现在多个域）

| 概念 | 出现在 | 为什么重复出现 |
|---|---|---|
| 索引 | 索引与执行计划「索引是什么」 · 查询基础「模糊匹配」 · 多表连接「连接列要建索引」 · 性能与优化「避免列上运算」 | 「为什么慢」九成是索引问题；建索引、用得上索引、别破坏索引，是三件不同的事 |
| 主键 | 库与表「主键与自增」 · 索引与执行计划「主键索引」 · 约束与设计「主键选择」 | 主键同时是约束、是聚簇索引、是设计决策——三处都得想一遍 |
| 事务 | 事务与锁「开始与提交」 · 增删改「在事务里批量改」 · 约束与设计「外键」 | 写操作要么成组提交、要么全回滚；约束检查也在事务里发生 |
| 字符集 | 库与表「字符集」 · 安装与连接「配置文件」 · 性能与优化「隐式转换」 | 建库时定错字符集，后面每次插入 emoji 都会报错；跨字符集比较还会让索引失效 |
| `NULL` 的语义 | 查询基础「空值判断」 · 聚合与分组「聚合与 NULL」 · 约束与设计「非空与默认」 | `NULL` 表示「未知」，参与比较与聚合都特殊——能非空就非空 |
| 分组 + 连接 | 聚合与分组「分组」 · 多表连接「`INNER JOIN`」 · 聚合与分组「分组后过滤」 | 统计报表几乎都是「先 JOIN 再 GROUP BY」，所以这两个域总一起出现 |
| 权限 | 用户与权限「授权」 · 安装与连接「远程连不上」 · 性能与优化「看连接数」 | 连不上、删不掉、看不到——很多「故障」其实是权限 |

## 4. 备注（易错点 / 取舍 / 顺序）

1. **`UPDATE`/`DELETE` 不带 `WHERE` 会动全表**：先写 `SELECT` 用同一个 `WHERE` 看命中行数，再改成 `UPDATE`。
2. **MySQL 的 `utf8` 只有 3 字节**：要存 emoji 与生僻字必须 `utf8mb4`；建库时就定，后面改很痛。
3. **`COUNT(col)` 不数 `NULL`**：数行数用 `COUNT(*)`。
4. **隐式类型转换让索引失效**：字符串列与数字比较、`WHERE id = '1'` 这类都会。
5. **列上套函数让索引失效**：`YEAR(d) = 2026` → 改成日期范围。
6. **`LIMIT` 深分页很慢**：游标分页（`WHERE id > 上次最大`）才是正解。
7. **索引不是越多越好**：每个索引都让写入变慢、占空间；按查询建，定期清理。
8. **`LEFT JOIN` 的右表条件写 `ON`**：写进 `WHERE` 会退化成内连接，把左表不匹配的行滤掉。
9. **金额用 `DECIMAL`**：`FLOAT/DOUBLE` 会有精度误差，钱不能这么存。
10. **`TRUNCATE` 不可回滚**：还会重置自增；要能后悔就用 `DELETE`。
11. **DDL 会隐式提交**：事务里混 `ALTER` 会让前面的操作提前提交。
12. **学 MySQL 的顺序**：①建表与 CRUD ②查询与聚合 ③JOIN ④索引与 EXPLAIN ⑤事务 ⑥权限与备份。

## 5. 反向查：我要做 X，去哪个域

| 我要…… | 去这里 |
|---|---|
| 建一个带主键的表 | 库与表（`CREATE TABLE` + `AUTO_INCREMENT`） |
| 统计每个作者有几本书 | 聚合与分组（`GROUP BY` + `COUNT`） |
| 把两张表拼起来查 | 多表连接（`JOIN`/`LEFT JOIN`） |
| 查某条 SQL 为什么慢 | 性能与优化（慢查询日志）+ 索引与执行计划（`EXPLAIN`） |
| 给查询加索引 | 索引与执行计划（联合索引、最左前缀） |
| 保证一组写入不出错 | 事务与锁（`START TRANSACTION`/`COMMIT`） |
| 让别人只能读不能写 | 用户与权限（`GRANT SELECT`） |
| 备份整个库 | 用户与权限（`mysqldump --single-transaction`） |
| 表里存 emoji 报错 | 库与表（`utf8mb4`） |
| 让接口不重复插入 | 增删改（`ON DUPLICATE KEY UPDATE`）+ 约束与设计（`UNIQUE`） |

---

*由 `mapkit.py` 生成（单一数据源，Markdown 与 HTML 内容一致）。共 103 条。*
