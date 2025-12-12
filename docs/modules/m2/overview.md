# M2: Function Call

::: tip 学习目标
通过本模块，你将学会：
- ✅ 实现安全的SQL执行机制
- ✅ 构建统一的数据库客户端接口
- ✅ 掌握Function Call设计模式
- ✅ 处理查询结果和错误管理
:::

## 模块概述

**M2模块** 是NL2SQL系统的执行层，通过**Function Call**模式安全地执行M1生成的SQL查询。

### 为什么需要Function Call？

传统的直接执行方式：
```python
# 危险的做法
sql = "SELECT * FROM users WHERE id = " + user_input
cursor.execute(sql)  # 可能导致SQL注入
```

**Function Call模式的优势**：
- ✅ **安全性**：统一的安全检查
- ✅ **可控性**：可监控和审计
- ✅ **可测试**：每个环节独立验证
- ✅ **可扩展**：支持多种数据库类型

## 核心概念

### Function Call模式

Function Call是将"执行动作"封装成函数调用的设计模式：

```python
# 传统的直接调用
def direct_execute(sql):
    return cursor.execute(sql)  # 危险

# Function Call模式
def safe_execute(sql, client):
    # 安全检查
    if not is_safe(sql):
        return {"ok": False, "error": "Unsafe SQL"}
    
    # 统一执行
    return client.query(sql)  # 安全
```

**好处**：
1. **安全控制集中化**
2. **接口标准化**
3. **错误处理统一化**
4. **审计和监控**

### 数据库客户端设计

我们的数据库客户端设计原则：

1. **统一接口**：屏蔽不同数据库的差异
2. **安全第一**：只读模式，结果限制
3. **错误友好**：清晰的错误信息
4. **易于扩展**：支持多种数据库

```python
class DatabaseClient:
    def query(self, sql: str) -> Dict[str, Any]:
        """
        统一查询接口
        返回标准化结果格式
        """
        pass
    
    def get_schema(self, table: str) -> Dict[str, Any]:
        """
        获取表结构信息
        """
        pass
```

## 项目结构

M2模块的核心文件：

```
rookie-nl2sql/
├── tools/
│   └── db.py                  # 数据库客户端 - Function Call实现
├── graphs/
│   ├── nodes/
│   │   └── execute_sql.py     # SQL执行节点
│   ├── state.py               # 扩展State定义
│   └── base_graph.py          # 更新图流程
├── tests/
│   └── test_m2_acceptance.py  # M2验收测试
└── data/
    └── chinook.db            # Chinook示例数据库
```

## 核心实现

### 1. 数据库客户端 (`tools/db.py`)

**统一接口设计**：
```python
class DatabaseClient:
    def query(
        self,
        sql: str,
        params: Optional[Tuple] = None,
        fetch_limit: int = 100
    ) -> Dict[str, Any]:
        """
        执行SQL查询的安全接口
        
        Args:
            sql: SQL查询语句
            params: 查询参数（防注入）
            fetch_limit: 最大返回行数
            
        Returns:
            {
                "ok": bool,
                "rows": List[Dict],
                "columns": List[str], 
                "row_count": int,
                "error": str
            }
        """
```

**安全检查**：
```python
# 只允许SELECT查询
if not sql.strip().upper().startswith("SELECT"):
    return {"ok": False, "error": "Only SELECT queries allowed"}

# 限制结果行数
rows = cursor.fetchmany(fetch_limit)
```

**多数据库支持准备**：
```python
if self.db_type == "sqlite":
    conn = sqlite3.connect(self.db_path)
elif self.db_type == "mysql":
    conn = mysql.connector.connect(**config)
elif self.db_type == "postgresql":
    conn = psycopg2.connect(**config)
```

### 2. SQL执行节点 (`graphs/nodes/execute_sql.py`)

**执行流程**：
```python
def execute_sql_node(state: NL2SQLState) -> NL2SQLState:
    """执行SQL查询的安全节点"""
    
    # 1. 获取生成的SQL
    candidate_sql = state.get("candidate_sql")
    
    # 2. 验证SQL存在
    if not candidate_sql:
        return error_result("No SQL to execute")
    
    # 3. 安全执行（Function Call）
    result = db_client.query(candidate_sql)
    
    # 4. 格式化结果
    return {
        **state,
        "execution_result": result,
        "executed_at": datetime.now().isoformat()
    }
```

**结果处理**：
```python
if result["ok"]:
    print(f"✓ Query successful")
    print(f"  Rows returned: {result['row_count']}")
    print(f"  Columns: {', '.join(result['columns'])}")
else:
    print(f"✗ Query failed: {result['error']}")
```

### 3. 状态扩展

M2新增执行相关字段：
```python
class NL2SQLState(TypedDict):
    # 原有字段...
    
    # SQL Generation (M1)
    candidate_sql: Optional[str]
    sql_generated_at: Optional[str]
    
    # SQL Execution (M2) ✓ 新增
    execution_result: Optional[Dict[str, Any]]  # 执行结果
    executed_at: Optional[str]                  # 执行时间戳
```

## Chinook数据库

我们使用Chinook音乐商店数据库作为示例：

### 数据库结构

**核心表关系**：
```
Artist (1) ──< (N) Album ──< (N) Track
    │                  │           │
    │                  │           └──< InvoiceLine >── Invoice ──> Customer
    │                  │
    └───────────< PlaylistTrack < Playlist
```

**表概览**：
- **Artist**: 艺术家信息
- **Album**: 专辑信息  
- **Track**: 歌曲信息
- **Customer**: 客户信息
- **Invoice**: 发票信息
- **Genre**: 音乐类型

### 为什么选择Chinook？

1. **真实数据**：来自真实音乐商店
2. **丰富关系**：包含各种JOIN场景
3. **合适规模**：不大不小，便于测试
4. **标准SQL**：广泛使用的示例数据库

## 使用指南

### 1. 环境准备

```bash
# 1. 创建数据目录
mkdir -p data

# 2. 下载Chinook数据库
cd data
wget https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite
mv Chinook_Sqlite.sqlite chinook.db

# 3. 验证数据库
python tools/db.py
```

### 2. 测试组件

```bash
# 测试SQL执行节点
python graphs/nodes/execute_sql.py

# 测试完整流程
python graphs/base_graph.py

# 运行验收测试
python tests/test_m2_acceptance.py
```

### 3. 自定义查询

```python
from tools.db import db_client

# 执行自定义查询
result = db_client.query("SELECT * FROM Artist LIMIT 5")
if result["ok"]:
    print(f"Found {result['row_count']} artists")
    for artist in result['rows']:
        print(f"  {artist['Name']}")
```

## 验收测试

### 测试用例设计

8个全面的测试用例：

| 类型 | 测试用例 | 验证点 |
|------|----------|--------|
| 简单查询 | `Show all albums` | 基础SELECT |
| 聚合查询 | `How many tracks are there?` | COUNT函数 |
| 排序限制 | `What are the top 5 longest tracks?` | ORDER BY + LIMIT |
| 条件过滤 | `Show albums by AC/DC` | WHERE子句 |
| 表连接 | `Show all albums with their artist names` | JOIN查询 |
| 分组聚合 | `Count albums by artist` | GROUP BY |
| 多表查询 | `Show customer names and their total invoice amounts` | 复杂JOIN |
| 日期过滤 | `Show invoices from 2010` | 日期条件 |

### 验收标准

- ✅ **100%通过率**：所有测试必须成功
- ✅ **结果正确性**：返回正确的行数和数据
- ✅ **安全性**：阻止非SELECT查询

### 测试输出示例

```
Test 1/8: Simple SELECT
Question: Show all albums
✓ Test PASSED
  SQL: SELECT * FROM Album LIMIT 100
  Rows: 5

Test 2/8: Count aggregation  
Question: How many tracks are there?
✓ Test PASSED
  SQL: SELECT COUNT(*) as total FROM Track
  Rows: 1
```

## 设计模式

### 1. Strategy Pattern（策略模式）

用于支持多种数据库：

```python
class DatabaseStrategy:
    def connect(self, config): pass
    def execute(self, sql): pass

class SQLiteStrategy(DatabaseStrategy):
    def connect(self, config):
        return sqlite3.connect(config["path"])

class MySQLStrategy(DatabaseStrategy):
    def connect(self, config):
        return mysql.connector.connect(**config)
```

### 2. Template Method Pattern（模板方法）

统一的查询流程：

```python
def query(self, sql: str):
    # 模板方法：定义执行流程
    sql = self.validate_sql(sql)      # 验证
    conn = self.get_connection()      # 连接
    result = self.execute_query(conn, sql)  # 执行
    conn.close()                     # 清理
    return self.format_result(result)  # 格式化
```

### 3. Result Pattern（结果模式）

标准化的结果格式：

```python
class QueryResult:
    def __init__(self, ok=False, rows=None, error=None):
        self.ok = ok
        self.rows = rows or []
        self.error = error
        self.row_count = len(rows) if rows else 0
    
    def to_dict(self):
        return {
            "ok": self.ok,
            "rows": self.rows,
            "row_count": self.row_count,
            "error": self.error
        }
```

## 性能优化

### 1. 连接管理

```python
# 简单实现：每次查询都创建新连接
conn = sqlite3.connect(db_path)

# 优化方向：连接池（未来版本）
class ConnectionPool:
    def get_connection(self):
        # 复用连接
        pass
```

### 2. 结果限制

```python
# 防止返回过多数据
def query(self, sql: str, fetch_limit: int = 100):
    cursor = conn.cursor()
    cursor.execute(sql)
    
    # 限制结果行数
    return cursor.fetchmany(fetch_limit)
```

### 3. 缓存策略

```python
# 为M3预留的缓存接口
class QueryCache:
    def get(self, sql: str) -> Optional[Dict]:
        # 获取缓存结果
        pass
    
    def set(self, sql: str, result: Dict):
        # 设置缓存
        pass
```

## 安全机制

### 1. SQL注入防护

```python
# 危险的做法
sql = f"SELECT * FROM users WHERE id = {user_id}"  # 注入风险

# 安全的做法
def query(self, sql: str, params=None):
    cursor.execute(sql, params)  # 参数化查询
```

### 2. 权限控制

```python
# 只读模式检查
if not sql.strip().upper().startswith("SELECT"):
    return {"ok": False, "error": "Only SELECT queries allowed"}

# 阻止危险关键词
dangerous_keywords = ["DROP", "DELETE", "UPDATE", "INSERT"]
for kw in dangerous_keywords:
    if kw in sql.upper():
        return {"ok": False, "error": f"Dangerous keyword: {kw}"}
```

### 3. 资源限制

```python
# 查询时间限制
def query_with_timeout(self, sql: str, timeout: int = 30):
    # 设置查询超时
    pass

# 结果行数限制
def query(self, sql: str, max_rows: int = 100):
    # 限制返回行数
    pass
```

## 常见问题

### Q: 如何添加新数据库支持？

A: 扩展DatabaseClient类：

```python
def __init__(self):
    if self.db_type == "mysql":
        self.connector = MySQLConnector()
    elif self.db_type == "postgresql":
        self.connector = PostgreSQLConnector()
```

### Q: 如何处理大量数据查询？

A: 
1. 使用分页：`LIMIT offset, count`
2. 添加查询超时
3. 实现流式处理

### Q: 如何提升查询性能？

A: 
1. 添加索引（数据库层面）
2. 实现查询缓存
3. 优化SQL生成（M3模块）

### Q: 如何确保数据安全？

A: 
1. 只读权限
2. SQL白名单
3. 参数化查询
4. 审计日志

## 下一步

完成M2后，你掌握了：

- ✅ **Function Call**的设计模式
- ✅ **数据库安全执行**的完整方案
- ✅ **错误处理**和**结果管理**
- ✅ **标准化接口**的设计能力

**接下来**：
- 👉 [M3: Schema感知](/modules/m3/overview.md) - 注入真实数据库结构
- 👉 [M4: SQL校验](/modules/m4/overview.md) - 执行前质量检查
- 👉 [M5: 执行沙箱](/modules/m5/overview.md) - 更强的安全控制

## 扩展阅读

- [Database Design Patterns](https://refactoring.guru/design-patterns/catalog)
- [SQL Injection Prevention](https://owasp.org/www-project-cheat-sheets/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [Chinook Database Documentation](https://github.com/lerocha/chinook-database)
- [Function Calling Best Practices](https://platform.openai.com/docs/guides/function-calling)