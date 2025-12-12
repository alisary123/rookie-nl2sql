# M0 环境准备

开始学习前，请确保你的开发环境已经准备就绪。

## 系统要求

### 操作系统
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu 20.04+, CentOS 8+)

### 软件要求
- **Python**: 3.8 或更高版本
- **Git**: 2.0 或更高版本
- **代码编辑器**: VS Code 推荐（或任何你喜欢的编辑器）

## 安装步骤

### 1. 安装 Python

#### Windows
从 [python.org](https://www.python.org/downloads/) 下载并安装。

**验证安装**:
```bash
python --version  # 应显示 Python 3.8+
```

#### macOS
```bash
# 使用 Homebrew
brew install python@3.11
```

#### Linux (Ubuntu)
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

### 2. 安装 Git

#### Windows
从 [git-scm.com](https://git-scm.com/) 下载并安装。

#### macOS
```bash
brew install git
```

#### Linux
```bash
sudo apt install git
```

**验证安装**:
```bash
git --version  # 应显示 git version 2.x
```

### 3. 克隆项目

```bash
# 克隆仓库
git clone https://github.com/alisary123/rookie-nl2sql.git

# 进入项目目录
cd rookie-nl2sql

# 切换到 M0 分支
git checkout 00-scaffold
```

### 4. 创建虚拟环境

**推荐使用虚拟环境**，避免包冲突。

#### Windows
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate
```

#### macOS / Linux
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate
```

**验证**:
```bash
# 激活后，命令行前面应显示 (venv)
(venv) $ python --version
```

### 5. 安装依赖

```bash
# 确保虚拟环境已激活
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt
```

## 验证安装

运行 M0 验收测试，确保一切正常：

```bash
# 确保在 M0 分支
git checkout 00-scaffold

# 运行验收测试
python tests/test_m0_acceptance.py
```

**预期输出**:
```
======================================================================
M0 验收测试 - 项目脚手架与基线
======================================================================

✓ 测试用例 1 通过
✓ 测试用例 2 通过
✓ 测试用例 3 通过

通过: 3/3

🎉 恭喜! M0 验收测试全部通过!
```

如果看到这个输出，说明环境准备完毕！

## 推荐的开发工具

### VS Code 插件

推荐安装以下插件提升开发体验：

- **Python** (Microsoft): Python 语言支持
- **Pylance**: 类型检查和智能提示
- **GitLens**: Git 增强
- **Markdown All in One**: Markdown 编辑

## 常见问题

### Q: M0 需要 API Key 吗？
A: **不需要**。M0 只是搭建框架，不调用 LLM。

### Q: 虚拟环境激活后怎么退出？
A: 输入 `deactivate` 命令。

### Q: pip 安装很慢怎么办？
A: 使用国内镜像：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 下一步

环境准备完成后：

👉 开始学习 M0: 项目脚手架

如果遇到问题：
👉 [GitHub Issues](https://github.com/alisary123/rookie-nl2sql/issues)