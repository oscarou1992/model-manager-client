# Model Manager Client

这是一个用于与 Model Manager gRPC 服务进行交互的 Python SDK。该客户端库提供了简单易用的接口来管理和操作模型。

## 功能特点

- 基于 gRPC 的高性能通信
- 类型安全的数据模型（使用 Pydantic）
- 完整的异常处理
- 简单易用的 API 接口

## 系统要求

- Python 3.8 或更高版本
- 支持的操作系统：跨平台（Windows、Linux、macOS）

## 安装

你可以通过 pip 安装此包：

```bash
pip install model-manager-client
```

或者从源代码安装：

```bash
git clone https://github.com/your-username/model-manager-client.git
cd model-manager-client
pip install -e .
```

## 项目结构

```
model-manager-client/
├── model_manager_client/
│   ├── generated/          # gRPC 生成的代码
│   ├── schemas/           # 数据模型定义
│   ├── enums/            # 枚举类型定义
│   ├── client.py         # 主要客户端实现
│   ├── exceptions.py     # 自定义异常
│   └── __init__.py
├── setup.py              # 包配置
└── make_grpc.py         # gRPC 代码生成脚本
```

## 使用方法

### 基本设置

```python
from model_manager_client import ModelManagerClient
from model_manager_client.schemas.inputs import ChatInput, ChatMessage
from model_manager_client.enums.providers import ProviderType

# 创建客户端实例
client = ModelManagerClient(
    server_address="localhost:50051",  # 服务器地址
    jwt_token="your-jwt-token"  # 可选的 JWT 认证令牌
)
```

### 单次对话示例

```python
import asyncio

async def chat_example():
    # 创建对话输入
    chat_input = ChatInput(
        provider=ProviderType.OPENAI,  # 选择模型提供商
        model_name="gpt-3.5-turbo",   # 可选的模型名称
        messages=[
            ChatMessage(role="user", content="你好，请介绍一下你自己。")
        ],
        temperature=0.7,              # 可选的温度参数
        stream=True                   # 是否使用流式响应
    )

    try:
        # 发送请求并获取响应
        async for response in client.chat(chat_input):
            if response.error:
                print(f"错误: {response.error}")
            else:
                print(f"响应: {response.content}")
                if response.usage:
                    print(f"Token 使用情况: {response.usage}")
    finally:
        # 关闭客户端连接
        await client.close()

# 运行示例
asyncio.run(chat_example())
```

### 批量对话示例

```python
async def batch_chat_example():
    # 创建多个对话输入
    chat_inputs = [
        ChatInput(
            provider=ProviderType.OPENAI,
            messages=[ChatMessage(role="user", content="第一个问题")],
            priority=1
        ),
        ChatInput(
            provider=ProviderType.OPENAI,
            messages=[ChatMessage(role="user", content="第二个问题")],
            priority=2
        )
    ]

    try:
        # 发送批量请求
        responses = await client.batch_chat(chat_inputs)
        
        # 处理响应
        for i, response in enumerate(responses, 1):
            if response.error:
                print(f"问题 {i} 错误: {response.error}")
            else:
                print(f"问题 {i} 响应: {response.content}")
                if response.usage:
                    print(f"问题 {i} Token 使用情况: {response.usage}")
    finally:
        await client.close()

# 运行示例
asyncio.run(batch_chat_example())
```

### 环境变量配置

你也可以通过环境变量来配置客户端：

```bash
export MODEL_MANAGER_SERVER_ADDRESS="localhost:50051"
export MODEL_MANAGER_SERVER_JWT_TOKEN="your-jwt-token"
```

然后创建客户端时可以不传参数：

```python
client = ModelManagerClient()  # 将使用环境变量中的配置
```

## 开发

### 环境设置

1. 创建虚拟环境：
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate  # Windows
```

2. 安装开发依赖：
```bash
pip install -e .
```

### 生成 gRPC 代码

运行以下命令生成 gRPC 相关代码：

```bash
python make_grpc.py
```

## 许可证

MIT License

## 作者

- Oscar Ou (oscar.ou@tamaredge.ai)

## 贡献

欢迎提交 Issue 和 Pull Request！ 