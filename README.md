# Model Manager Client

这是一个用于与 Model Manager gRPC 服务进行交互的 Python SDK。该客户端库提供了简单易用的接口来管理和操作模型，支持同步/异步调用、流式/静态请求。

## 功能特点

- 🌟 支持 同步和异步 client
- ✅ 基于 gRPC 的高性能通信，支持流式和静态响应
- 🔒 JWT 鉴权支持，自动生成并附加认证令牌
-  ⚡ 支持 重试机制，最大重试次数可配置
- 📈 类型安全的数据模型（使用 Pydantic）
- 🛡 完整的异常处理

## 系统要求

- Python 3.8 或更高版本
- 支持的操作系统：跨平台（Windows / Linux / macOS）

## 安装

你可以通过 pip 安装此包：

```bash
pip install model-manager-client
```

## 项目结构

```
model_manager_client/
├── generated/             # gRPC 生成的代码
├── schemas/               # 数据模型定义
├── enums/                 # 枚举类型定义
├── async_client.py        # 异步客户端实现
├── sync_client.py         # 同步客户端实现
├── exceptions.py          # 自定义异常
├── auth.py                # JWT认证处理器
└── __init__.py            # 包初始化
```

## 使用方法

### 基本设置

```python
from model_manager_client import ModelManagerClient, AsyncModelManagerClient

# 创建同步客户端实例
sync_client = ModelManagerClient(
    server_address="localhost:50051",  # 服务器地址
    jwt_token="your-jwt-token"  # JWT 认证令牌
)

# 或者固定key，然后存在加密逻辑
sync_client_secret_key = ModelManagerClient(
    server_address="localhost:50051",  # 服务器地址
    jwt_secret_key="your-jwt-secret-key"  # JWT 秘钥
)


# 创建异步客户端实例
async_client = AsyncModelManagerClient(
    server_address="localhost:50051",  # 服务器地址
    jwt_token="your-jwt-token"  # 可选的 JWT 认证令牌
)

# 或者固定key，然后存在加密逻辑
async_client_secret_key = AsyncModelManagerClient(
    server_address="localhost:50051",  # 服务器地址
    jwt_secret_key="your-jwt-secret-key"  # JWT 秘钥
)
```

> 需要注意，这里的JWT存在2个字段jwt_secret_key和jwt_secret_key，两者是不一样的，一个是固定key进行加密后，另外一个是加密后传过去的token。
> 因此这里推荐使用环境变量

### 同步调用示例

```python
from model_manager_client import ModelManagerClient
from model_manager_client.schemas import ModelRequest, TextInput, UserContext
from model_manager_client.enums.providers import ProviderType
from model_manager_client.enums.invoke import InvokeType

# 创建同步客户端
client = ModelManagerClient()

# 组装请求参数
request_data = ModelRequest(
    model_provider=ProviderType.OPENAI,  # 选择模型提供商
    model_name="gpt-4",  # 指定具体模型
    invoke_type=InvokeType.GENERATION,  # 调用类型
    input=[
        TextInput(text="你好，请介绍一下你自己。")
    ],
    user_context=UserContext(
        user_id="test_user",
        org_id="test_org",
        client_type="python-sdk"
    ),
    stream=False,  # 非流式调用
    temperature=0.7,  # 可选参数
    max_output_tokens=1000,  # 可选参数
)

# 发送请求并获取响应
response = client.invoke(request_data)
if response.error:
    print(f"错误: {response.error}")
else:
    print(f"响应: {response.content}")
    if response.usage:
        print(f"Token 使用情况: {response.usage}")
```

### 异步调用示例

```python
import asyncio
from model_manager_client import AsyncModelManagerClient
from model_manager_client.schemas import ModelRequest, TextInput, UserContext
from model_manager_client.enums.providers import ProviderType
from model_manager_client.enums.invoke import InvokeType

async def main():
    # 创建异步客户端
    client = AsyncModelManagerClient()

    # 组装请求参数
    request_data = ModelRequest(
        model_provider=ProviderType.OPENAI,
        model_name="gpt-4",
        invoke_type=InvokeType.GENERATION,
        input=[
            TextInput(text="你好，请介绍一下你自己。")
        ],
        user_context=UserContext(
            user_id="test_user",
            org_id="test_org",
            client_type="python-sdk"
        ),
        stream=False,
        temperature=0.7,
        max_output_tokens=1000,
    )

    # 发送请求并获取响应
    response = await client.invoke(request_data)
    if response.error:
        print(f"错误: {response.error}")
    else:
        print(f"响应: {response.content}")
        if response.usage:
            print(f"Token 使用情况: {response.usage}")

# 运行异步示例
asyncio.run(main())
```

### 流式调用示例

```python
import asyncio
from model_manager_client import AsyncModelManagerClient
from model_manager_client.schemas import ModelRequest, TextInput, UserContext
from model_manager_client.enums.providers import ProviderType
from model_manager_client.enums.invoke import InvokeType

async def stream_example():
    # 创建异步客户端
    client = AsyncModelManagerClient()

    # 组装请求参数
    request_data = ModelRequest(
        model_provider=ProviderType.OPENAI,
        model_name="gpt-4",
        invoke_type=InvokeType.GENERATION,
        input=[
            TextInput(text="你好，请介绍一下你自己。")
        ],
        user_context=UserContext(
            user_id="test_user",
            org_id="test_org",
            client_type="python-sdk"
        ),
        stream=True,  # 启用流式输出
        temperature=0.7,
    )

    # 发送请求并获取流式响应
    async for response in client.invoke(request_data):
        if response.error:
            print(f"错误: {response.error}")
        else:
            print(f"响应片段: {response.content}", end="", flush=True)
            if response.usage:
                print(f"\nToken 使用情况: {response.usage}")

# 运行流式示例
asyncio.run(stream_example())
```

### 批量调用示例

```python
import asyncio
from model_manager_client import AsyncModelManagerClient
from model_manager_client.schemas import (
    BatchModelRequest, BatchModelRequestItem,
    TextInput, UserContext
)
from model_manager_client.enums.providers import ProviderType
from model_manager_client.enums.invoke import InvokeType

async def batch_example():
    # 创建异步客户端
    client = AsyncModelManagerClient()

    # 组装批量请求参数
    batch_request = BatchModelRequest(
        user_context=UserContext(
            user_id="test_user",
            org_id="test_org",
            client_type="python-sdk"
        ),
        items=[
            BatchModelRequestItem(
                model_provider=ProviderType.OPENAI,
                model_name="gpt-4",
                invoke_type=InvokeType.GENERATION,
                input=[TextInput(text="第一个问题：什么是人工智能？")],
                priority=1,
                custom_id="q1"
            ),
            BatchModelRequestItem(
                model_provider=ProviderType.OPENAI,
                model_name="gpt-4",
                invoke_type=InvokeType.GENERATION,
                input=[TextInput(text="第二个问题：什么是机器学习？")],
                priority=2,
                custom_id="q2"
            )
        ]
    )

    # 发送批量请求并获取响应
    response = await client.invoke_batch(batch_request)
    if response.responses:
        for resp in response.responses:
            print(f"\n问题 {resp.custom_id} 的响应:")
            if resp.error:
                print(f"错误: {resp.error}")
            else:
                print(f"内容: {resp.content}")
                if resp.usage:
                    print(f"Token 使用情况: {resp.usage}")

# 运行批量调用示例
asyncio.run(batch_example())
```

### 文件输入示例

```python
import asyncio
from model_manager_client import AsyncModelManagerClient
from model_manager_client.schemas import ModelRequest, TextInput, FileInput, UserContext
from model_manager_client.enums.providers import ProviderType
from model_manager_client.enums.invoke import InvokeType

async def file_input_example():
    # 创建异步客户端
    client = AsyncModelManagerClient()

    # 组装请求参数（包含文件输入）
    request_data = ModelRequest(
        model_provider=ProviderType.OPENAI,
        model_name="gpt-4-vision-preview",  # 使用支持图像的模型
        invoke_type=InvokeType.GENERATION,
        input=[
            FileInput(file_url="https://example.com/image.jpg"),  # 图片URL
            TextInput(text="请描述这张图片。")  # 文本提示
        ],
        user_context=UserContext(
            user_id="test_user",
            org_id="test_org",
            client_type="python-sdk"
        ),
        stream=False
    )

    # 发送请求并获取响应
    response = await client.invoke(request_data)
    if response.error:
        print(f"错误: {response.error}")
    else:
        print(f"响应: {response.content}")
        if response.usage:
            print(f"Token 使用情况: {response.usage}")

# 运行文件输入示例
asyncio.run(file_input_example())
```

> ⚠注意：由于 gRPC 使用 HTTP/2 长连接，建议将 client 实例作为 单例实 (singleton) 保持使用。若要不同场景创建多个 client，请确保使用 `close()`手动关闭，以防此往处处使用造成连接重复和泄露。


### 环境变量配置

你也可以通过环境变量来配置客户端：

```bash
export MODEL_MANAGER_SERVER_ADDRESS="localhost:50051"
export MODEL_MANAGER_SERVER_JWT_TOKEN="your-jwt-secret"
export MODEL_MANAGER_SERVER_GRPC_USE_TLS="false"
export MODEL_MANAGER_SERVER_GRPC_DEFAULT_AUTHORITY="localhost"
export MODEL_MANAGER_SERVER_GRPC_MAX_RETRIES="5"
export MODEL_MANAGER_SERVER_GRPC_RETRY_DELAY="1.5"
```

或者本地 `.env` 文件
```
# ========================
# 🔌 gRPC 通信配置
# ========================

# gRPC 服务端地址（必填）
MODEL_MANAGER_SERVER_ADDRESS=localhost:50051

# 是否启用 TLS 加密通道（true/false，默认 true）
MODEL_MANAGER_SERVER_GRPC_USE_TLS=true

# 当使用 TLS 时指定 authority（域名必须和证书匹配才需要）
MODEL_MANAGER_SERVER_GRPC_DEFAULT_AUTHORITY=localhost


# ========================
# 🔐 鉴权配置（JWT）
# ========================

# JWT 签名密钥（用于生成 Token）
MODEL_MANAGER_SERVER_JWT_SECRET_KEY=your_jwt_secret_key


# ========================
# 🔁 重试配置（可选）
# ========================

# 最大重试次数（默认 3）
MODEL_MANAGER_SERVER_GRPC_MAX_RETRIES=3

# 初始重试延迟（秒，默认 1.0），指数退避
MODEL_MANAGER_SERVER_GRPC_RETRY_DELAY=1.0
```

然后创建客户端时可以不传参数：

```python
from model_manager_client import ModelManagerClient

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