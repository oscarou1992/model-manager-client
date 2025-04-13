from pydantic import BaseModel
from typing import List, Union, Optional

from model_manager_client.enums import ProviderType, InvokeType
from model_manager_client.enums.channel import Channel


class TextInput(BaseModel):
    text: str


class FileInput(BaseModel):
    file_url: str


class UserContext(BaseModel):
    org_id: str
    user_id: str
    client_type: str


class BaseRequest(BaseModel):
    model_provider: ProviderType
    channel: Optional[Channel] = None
    invoke_type: InvokeType = InvokeType.GENERATION
    model_name: Optional[str] = None
    input: List[Union[TextInput, FileInput]]
    stream: bool = False  # 默认值
    instructions: Optional[str] = None
    max_output_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    timeout: Optional[float] = None
    custom_id: Optional[str] = None


class ModelRequest(BaseRequest):
    user_context: UserContext


class BatchModelRequestItem(BaseRequest):
    priority: Optional[int] = None


class BatchModelRequest(BaseModel):
    user_context: UserContext
    items: List[BatchModelRequestItem]
