from enum import Enum


class ProviderType(str, Enum):
    """模型提供商类型枚举"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    DEEPSEEK = "deepseek"
    PERPLEXITY = "perplexity"
