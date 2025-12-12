# M2: 实践任务

通过以下任务，巩固M2模块学到的Function Call和数据库执行知识。

## 任务 1: 实现连接池优化

### 背景
当前实现每次查询都创建新的数据库连接，在高并发场景下效率较低。

### 任务要求
1. **实现连接池**
   - 支持SQLite连接复用
   - 配置最大连接数
   - 连接健康检查

2. **添加配置选项**
   - 连接池开关
   - 连接数量限制
   - 超时设置

### 实施步骤

```python
# 1. 创建tools/connection_pool.py
class ConnectionPool:
    def __init__(self, max_connections=10, timeout=30):
        self.pool = []
        self.max_connections = max_connections
        self.timeout = timeout
        self.lock = threading.Lock()
    
    def get_connection(self):
        # 实现连接获取逻辑
        pass
    
    def return_connection(self, conn):
        # 实现连接归还逻辑
        pass

# 2. 修改tools/db.py使用连接池
class DatabaseClient:
    def __init__(self, use_pool=True):
        self.use_pool = use_pool
        if use_pool:
            self.pool = ConnectionPool()
```

### 验收标准
- 连接池正常工作
- 并发查询性能提升 ≥ 50%
- 连接数量不超过限制

---

## 任务 2: 添加查询缓存机制

### 背景
相同查询的重复执行浪费资源，需要实现查询结果缓存。

### 任务要求
1. **实现LRU缓存**
   - 基于SQL语句的缓存键
   - 自动过期机制
   - 内存使用控制

2. **缓存策略**
   - 只缓存成功查询
   - 设置过期时间
   - 支持缓存清理

### 实施步骤

```python
# 1. 创建tools/query_cache.py
from functools import lru_cache
from hashlib import md5
import time

class QueryCache:
    def __init__(self, max_size=1000, ttl=300):
        self.cache = {}
        self.max_size = max_size
        self.ttl = ttl
    
    def get_cache_key(self, sql: str) -> str:
        return md5(sql.encode()).hexdigest()
    
    def get(self, sql: str) -> Optional[Dict]:
        # 实现缓存获取逻辑
        pass
    
    def set(self, sql: str, result: Dict):
        # 实现缓存设置逻辑
        pass

# 2. 集成到DatabaseClient
class DatabaseClient:
    def query(self, sql: str):
        # 先检查缓存
        cached = self.cache.get(sql)
        if cached:
            return cached
        
        # 执行查询
        result = self._execute_query(sql)
        
        # 缓存结果
        if result["ok"]:
            self.cache.set(sql, result)
        
        return result
```

### 验收标准
- 缓存命中率 ≥ 60%
- 内存使用控制在合理范围
- 缓存过期机制正常工作

---

## 任务 3: 实现异步查询支持

### 背景
在Web应用场景中，需要支持异步数据库查询以提升并发性能。

### 任务要求
1. **异步接口设计**
   - 使用asyncio实现
   - 支持async/await语法
   - 保持接口兼容性

2. **异步连接管理**
   - 异步连接池
   - 非阻塞查询
   - 异常处理

### 实施步骤

```python
# 1. 创建tools/async_db.py
import asyncio
import aiosqlite

class AsyncDatabaseClient:
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    async def query(self, sql: str) -> Dict[str, Any]:
        """异步查询接口"""
        try:
            async with aiosqlite.connect(self.db_path) as conn:
                conn.row_factory = aiosqlite.Row
                cursor = await conn.execute(sql)
                rows = await cursor.fetchall()
                
                return {
                    "ok": True,
                    "rows": [dict(row) for row in rows],
                    "row_count": len(rows)
                }
        except Exception as e:
            return {"ok": False, "error": str(e)}

# 2. 创建异步执行节点
async def async_execute_sql_node(state: NL2SQLState) -> NL2SQLState:
    """异步SQL执行节点"""
    sql = state.get("candidate_sql")
    result = await async_db_client.query(sql)
    
    return {
        **state,
        "execution_result": result,
        "executed_at": datetime.now().isoformat()
    }
```

### 验收标准
- 异步接口正常工作
- 并发查询性能提升 ≥ 100%
- 错误处理机制完善

---

## 任务 4: 构建查询分析器

### 背景
需要分析查询的复杂度和性能特征，为优化提供依据。

### 任务要求
1. **查询复杂度分析**
   - 识别查询类型（SELECT, JOIN, AGGREGATE等）
   - 计算复杂度评分
   - 预估执行时间

2. **性能监控**
   - 查询执行时间统计
   - 资源使用监控
   - 慢查询识别

### 实施步骤

```python
# 1. 创建tools/query_analyzer.py
import re
from typing import Dict, List, Tuple

class QueryAnalyzer:
    def __init__(self):
        self.complexity_weights = {
            "SELECT": 1,
            "JOIN": 3,
            "GROUP_BY": 2,
            "ORDER_BY": 1,
            "SUBQUERY": 4
        }
    
    def analyze_complexity(self, sql: str) -> Dict[str, Any]:
        """分析查询复杂度"""
        analysis = {
            "query_type": self._detect_query_type(sql),
            "tables": self._extract_tables(sql),
            "joins": self._count_joins(sql),
            "aggregations": self._count_aggregations(sql),
            "subqueries": self._count_subqueries(sql),
            "complexity_score": 0
        }
        
        # 计算复杂度评分
        analysis["complexity_score"] = self._calculate_score(analysis)
        
        return analysis
    
    def _detect_query_type(self, sql: str) -> str:
        """检测查询类型"""
        if "JOIN" in sql.upper():
            return "JOIN"
        elif "GROUP BY" in sql.upper():
            return "AGGREGATE"
        else:
            return "SIMPLE"
    
    def _calculate_score(self, analysis: Dict) -> int:
        """计算复杂度评分"""
        score = 0
        score += analysis["joins"] * 3
        score += analysis["aggregations"] * 2
        score += analysis["subqueries"] * 4
        return score

# 2. 集成到执行节点
def execute_sql_node(state: NL2SQLState) -> NL2SQLState:
    sql = state.get("candidate_sql")
    
    # 分析查询复杂度
    analysis = query_analyzer.analyze_complexity(sql)
    print(f"Query complexity: {analysis['complexity_score']}")
    
    # 执行查询并计时
    start_time = time.time()
    result = db_client.query(sql)
    execution_time = time.time() - start_time
    
    result["execution_time"] = execution_time
    result["analysis"] = analysis
    
    return {**state, "execution_result": result}
```

### 验收标准
- 准确识别查询类型
- 复杂度评分合理
- 执行时间监控准确

---

## 任务 5: 实现多数据库支持

### 背景
当前只支持SQLite，需要扩展支持MySQL和PostgreSQL。

### 任务要求
1. **数据库适配器**
   - MySQL适配器实现
   - PostgreSQL适配器实现
   - 统一接口设计

2. **配置管理**
   - 多数据库配置
   - 动态切换机制
   - 连接参数管理

### 实施步骤

```python
# 1. 创建tools/adapters.py
import sqlite3
import mysql.connector
import psycopg2
from abc import ABC, abstractmethod

class DatabaseAdapter(ABC):
    @abstractmethod
    def connect(self, config: Dict) -> Any:
        pass
    
    @abstractmethod
    def execute(self, conn: Any, sql: str) -> Any:
        pass
    
    @abstractmethod
    def close(self, conn: Any) -> None:
        pass

class MySQLAdapter(DatabaseAdapter):
    def connect(self, config: Dict):
        return mysql.connector.connect(**config)
    
    def execute(self, conn, sql):
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        return cursor.fetchall()

class PostgreSQLAdapter(DatabaseAdapter):
    def connect(self, config: Dict):
        return psycopg2.connect(**config)
    
    def execute(self, conn, sql):
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(sql)
        return cursor.fetchall()

# 2. 更新DatabaseClient
class DatabaseClient:
    def __init__(self, db_type: str, config: Dict):
        self.db_type = db_type
        self.adapter = self._get_adapter(db_type)
        self.config = config
    
    def _get_adapter(self, db_type: str) -> DatabaseAdapter:
        adapters = {
            "sqlite": SQLiteAdapter(),
            "mysql": MySQLAdapter(),
            "postgresql": PostgreSQLAdapter()
        }
        return adapters.get(db_type, SQLiteAdapter())
```

### 验收标准
- 支持MySQL和PostgreSQL
- 接口保持一致性
- 配置切换正常工作

---

## 任务 6: 构建数据库管理CLI工具

### 背景
需要一个命令行工具来管理数据库，方便开发和测试。

### 任务要求
1. **CLI工具设计**
   - 查询执行命令
   - 表结构查看
   - 数据库导出导入
   - 性能统计

2. **交互式功能**
   - SQL REPL环境
   - 命令历史记录
   - 结果格式化输出

### 实施步骤

```python
# 1. 创建tools/db_cli.py
import cmd
import sys
from typing import List

class DatabaseCLI(cmd.Cmd):
    intro = "Database CLI Tool. Type help or ? to list commands.\n"
    prompt = "db> "
    
    def __init__(self):
        super().__init__()
        self.client = DatabaseClient()
    
    def do_query(self, sql: str):
        """Execute SQL query: query SELECT * FROM Album"""
        if not sql:
            print("Please provide SQL query")
            return
        
        result = self.client.query(sql)
        if result["ok"]:
            self._format_output(result)
        else:
            print(f"Error: {result['error']}")
    
    def do_tables(self, args: str):
        """List all tables: tables"""
        tables = self.client.get_table_names()
        for table in tables:
            print(f"  - {table}")
    
    def do_schema(self, table_name: str):
        """Show table schema: schema Album"""
        if not table_name:
            print("Please provide table name")
            return
        
        schema = self.client.get_table_schema(table_name)
        self._format_schema(schema)
    
    def do_export(self, filename: str):
        """Export database to CSV: export output.csv"""
        # 实现导出功能
        pass
    
    def _format_output(self, result: Dict):
        """格式化输出结果"""
        if not result["rows"]:
            print("No rows returned")
            return
        
        # 打印表头
        headers = result["columns"]
        print(" | ".join(f"{h:20}" for h in headers))
        print("-" * (len(headers) * 23))
        
        # 打印数据行
        for row in result["rows"][:10]:  # 只显示前10行
            values = [str(row.get(col, ""))[:20] for col in headers]
            print(" | ".join(f"{v:20}" for v in values))
        
        if len(result["rows"]) > 10:
            print(f"... and {len(result['rows']) - 10} more rows")

if __name__ == "__main__":
    cli = DatabaseCLI()
    cli.cmdloop()
```

### 验收标准
- CLI工具功能完整
- 交互式体验良好
- 输出格式清晰

---

## 高级任务（可选）

### 任务 7: 实现数据库迁移工具

支持数据库结构的版本管理和迁移。

### 任务 8: 构建查询优化器

基于统计信息自动优化SQL查询性能。

### 任务 9: 添加数据库监控面板

实时监控数据库查询性能和状态。

## 提交要求

### 基础任务（1-6）
选择至少3个基础任务完成，每个任务提供：

1. **代码实现**
   - 完整的Python代码
   - 单元测试覆盖
   - 性能测试报告

2. **文档说明**
   - API文档
   - 使用示例
   - 配置说明

3. **测试报告**
   - 功能验证
   - 性能对比
   - 问题分析

### 高级任务（7-9）
作为额外挑战，可以尝试实现并提交到课程仓库。

## 评分标准

| 评分项 | 权重 | 说明 |
|--------|------|------|
| 功能完整性 | 40% | 任务要求的全部功能实现 |
| 性能提升 | 30% | 相比基准的性能改进 |
| 代码质量 | 20% | 代码结构、测试覆盖 |
| 文档完整性 | 10% | API文档、使用指南 |

## 提交方式

1. **Fork仓库**
2. **创建特性分支**
   ```bash
   git checkout -b m2-task-solutions
   ```
3. **提交代码**
   ```bash
   git add .
   git commit -m "M2 tasks: 实现数据库优化功能"
   git push origin m2-task-solutions
   ```
4. **创建Pull Request**
   - 详细说明实现的功能
   - 附上性能测试结果
   - 提出改进建议

## 学习资源

- [Database Connection Pooling](https://en.wikipedia.org/wiki/Connection_pool)
- [Query Optimization](https://use-the-index-luke.com/)
- [Async Database Programming](https://docs.python.org/3/library/asyncio.html)
- [CLI Design Best Practices](https://clig.dev/)

## 常见问题

### Q: 如何选择合适的任务？
A: 
- **初学者**：选择任务1、2、4
- **有经验者**：选择任务3、5、6
- **挑战者**：尝试高级任务

### Q: 性能测试如何进行？
A: 
1. 使用timeit模块测量执行时间
2. 使用memory_profiler监控内存使用
3. 使用concurrent.futures测试并发性能

### Q: 如何保证代码质量？
A: 
1. 遵循PEP 8编码规范
2. 编写完整的单元测试
3. 使用类型提示和文档字符串
4. 进行代码审查

开始你的实践之旅吧！🚀