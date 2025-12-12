# NL2SQL 学习项目

从零开始学习自然语言转 SQL (NL2SQL) 的实践项目。

## 项目概述

本项目采用模块化学习方式，从基础框架开始，逐步构建完整的 NL2SQL 系统：

- **M0**: 项目脚手架与基线
- **M1**: 提示工程实现 NL2SQL
- **M2**: Function Call 实现数据库查询

## 快速开始

### 1. 环境准备

详细的环境配置说明请查看 [环境准备指南](guide/setup.md)。

### 2. M0 验收测试

```bash
# 克隆项目
git clone https://github.com/alisary123/rookie-nl2sql.git
cd rookie-nl2sql

# 切换到 M0 分支
git checkout 00-scaffold

# 创建虚拟环境并安装依赖
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 运行验收测试
python tests/test_m0_acceptance.py
```

### 3. 验收标准

M0 验收测试应该全部通过：
- ✓ 基础State结构正常
- ✓ LangGraph图结构运行正常
- ✓ 意图解析功能正常

## 项目结构

```
rookie-nl2sql/
├── configs/          # 配置文件
├── graphs/           # 图结构和状态定义
├── tests/            # 测试文件
├── docs/             # 文档
├── requirements.txt  # Python 依赖
├── .env.example      # 环境变量模板
└── README.md         # 项目说明
```

## 学习路径

### M0: 项目脚手架 (当前)

目标：建立基础框架和测试环境。

**验收标准**：
- 基础 State 结构
- LangGraph 工作流
- 意图解析节点

### M1: 提示工程

目标：使用提示工程实现自然语言转 SQL。

**主要内容**：
- LLM 客户端集成
- 提示词模板设计
- SQL 生成节点

### M2: 数据库集成

目标：实现真实的数据库查询功能。

**主要内容**：
- Function Call 集成
- 数据库工具
- SQL 执行节点

## 技术栈

- **Python**: 主要编程语言
- **LangGraph**: 工作流编排
- **LangChain**: LLM 集成框架
- **SQLite**: 示例数据库

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License