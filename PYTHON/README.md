# Python 学习笔记

本仓库包含 Python 代码示例，涵盖基础概念和实际应用。

## 文件概览

- **101.py**: 基础变量和算术运算
- **102.py**: 使用 f-string 进行字符串格式化
- **gim.py**: HTTP 请求和 JSON 处理的 API 调用

---

## Python 知识点

### 101.py - 基础操作

#### 1. 变量赋值
```python
x = 1
y = 2
```
- **概念**: 变量用于存储数据值
- **语法**: `变量名 = 值`
- **命名规则**: 使用字母、数字和下划线（必须以字母或下划线开头）

#### 2. 数据类型 - 整数
```python
x = 1  # int（整数）
y = 2  # int（整数）
```
- **类型**: `int` - 整数（正数、负数或零）
- **动态类型**: Python 会自动推断数据类型

#### 3. 算术运算
```python
print(x + y)  # 加法运算：结果为 3
```
- **运算符**: `+` 执行加法运算
- **其他运算符**: `-`（减法）、`*`（乘法）、`/`（除法）、`//`（整除）、`%`（取余）、`**`（幂运算）

#### 4. 内置函数
```python
print(x + y)
```
- **`print()`**: 将值输出到控制台
- **表达式求值**: Python 先计算 `x + y`（结果为 3），然后将其传递给 `print()`

---

### 102.py - 字符串格式化

#### 1. 字符串数据类型
```python
name = "Zhixuan Hong"
```
- **类型**: `str`（字符串）- 字符序列
- **语法**: 用单引号 `'...'` 或双引号 `"..."` 括起来
- **不可变性**: 字符串创建后不能修改

#### 2. F-字符串（格式化字符串字面量）
```python
print(f"Hello, {name}")
```
- **语法**: 在字符串前加 `f` 或 `F` 前缀
- **插值**: 使用 `{变量名}` 插入变量值
- **引入版本**: Python 3.6+
- **优势**: 比其他字符串格式化方法更易读且更高效

#### 3. 字符串格式化方法对比
```python
# f-string（推荐）
f"Hello, {name}"

# .format() 方法
"Hello, {}".format(name)

# % 格式化（旧式）
"Hello, %s" % name
```

---

### gim.py - 高级概念

#### 1. 模块导入
```python
import requests
import json
```
- **作用**: 导入外部库/模块
- **`requests`**: 用于 HTTP 请求的第三方库（需要安装：`pip install requests`）
- **`json`**: 用于处理 JSON 数据的内置模块
- **语法**: `import 模块名`

#### 2. 函数定义
```python
def call_zhipu_api(messages, model="glm-4.5-flash"):
```
- **关键字**: `def` 用于定义函数
- **函数名**: `call_zhipu_api` - 遵循命名规范（小写字母加下划线）
- **参数**: 
  - `messages` - 必需参数
  - `model="glm-4.5-flash"` - 带默认值的可选参数
- **默认参数**: 带默认值的参数必须放在必需参数之后

#### 3. 字典数据结构
```python
headers = {
    "Authorization": "...",
    "Content-Type": "application/json"
}

data = {
    "model": model,
    "messages": messages,
    "temperature": 0.5
}
```
- **类型**: `dict` - 键值对集合
- **语法**: `{键: 值, ...}`
- **访问**: `字典名['键']` 或 `字典名.get('键')`
- **可变性**: 可以添加、修改或删除项
- **键的要求**: 必须是不可变类型（字符串、数字、元组）

#### 4. HTTP 请求
```python
response = requests.post(url, headers=headers, json=data)
```
- **方法**: `requests.post()` 发送 POST 请求
- **参数**:
  - `url`: API 端点地址
  - `headers`: HTTP 请求头（字典格式）
  - `json`: 请求体，以 JSON 格式发送（自动序列化）
- **响应对象**: 包含状态码、响应头和内容

#### 5. 条件语句
```python
if response.status_code == 200:
    return response.json()
else:
    raise Exception(...)
```
- **`if/else`**: 基于条件的控制流
- **比较运算符**: `==` 检查相等性（不是 `=`，`=` 是赋值）
- **缩进**: Python 使用缩进（4个空格）定义代码块
- **返回语句**: 退出函数并返回值

#### 6. 异常处理
```python
raise Exception(f"API调用失败: {response.status_code}, {response.text}")
```
- **`raise`**: 手动抛出异常
- **`Exception`**: 基础异常类
- **异常中的 F-strings**: 可以使用 f-strings 创建动态错误消息

#### 7. 列表数据结构
```python
messages = [
    {"role": "user", "content": "你好，今天杭州的天气怎么样"}
]
```
- **类型**: `list` - 有序的元素集合
- **语法**: `[元素1, 元素2, ...]`
- **嵌套结构**: 列表可以包含字典、其他列表等
- **可变性**: 可以添加、修改或删除元素

#### 8. 嵌套数据访问
```python
result['choices'][0]['message']['content']
```
- **链式访问**: 访问嵌套的字典和列表
- **解析**:
  - `result['choices']` - 从字典中获取 'choices' 键
  - `[0]` - 从列表中获取第一个元素（零索引）
  - `['message']` - 从字典中获取 'message' 键
  - `['content']` - 从字典中获取 'content' 键
- **索引**: 列表使用从零开始的索引（第一个元素是 `[0]`）

#### 9. JSON 处理
```python
response.json()  # 将 JSON 响应解析为 Python 字典
```
- **方法**: `.json()` 将 JSON 字符串转换为 Python 字典
- **内置 `json` 模块**: 也可以使用 `json.loads()` 和 `json.dumps()`

#### 10. 注释
```python
# 使用示例
```
- **语法**: `#` 用于单行注释
- **作用**: 文档化代码、解释逻辑或临时禁用代码

---

## 核心概念总结

### 涉及的数据类型
- **int**: 整数（101.py）
- **str**: 字符串（102.py）
- **dict**: 字典（gim.py）
- **list**: 列表（gim.py）

### 控制流
- **条件语句**: `if/else` 语句（gim.py）

### 函数
- **定义**: `def` 关键字（gim.py）
- **参数**: 必需参数和默认参数（gim.py）
- **返回值**: `return` 语句（gim.py）

### 模块和库
- **内置模块**: `json` 模块
- **第三方库**: `requests` 库

### 字符串格式化
- **F-strings**: 现代推荐方法（102.py, gim.py）

### 错误处理
- **异常**: `raise Exception()`（gim.py）

---

## 最佳实践示例

1. **函数命名**: 使用描述性名称加下划线（`call_zhipu_api`）
2. **默认参数**: 为可选参数提供合理的默认值
3. **错误处理**: 检查响应状态并为失败情况抛出异常
4. **F-strings**: 使用 f-strings 进行字符串格式化（Python 3.6+）
5. **代码组织**: 将逻辑分离到函数中以提高可重用性

---

## 安装要求

运行 `gim.py` 需要安装以下包：
```bash
pip install requests
```

---

## 学习路径

1. **从 101.py 开始**: 学习基础变量和运算
2. **进阶到 102.py**: 理解字符串格式化
3. **深入学习 gim.py**: 探索函数、API 和数据结构

---

*最后更新：基于 101.py、102.py 和 gim.py 的代码分析*

