import os
from grpc_tools import protoc


def generate_grpc_code():
    proto_file = "model_manager_client/generated/model_service.proto"
    output_dir = "model_manager_client/generated"

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 运行 protoc 命令生成 Python 文件
    protoc.main([
        "",
        f"-I={os.path.dirname(proto_file)}",
        f"--python_out={output_dir}",
        f"--grpc_python_out={output_dir}",
        proto_file,
    ])


if __name__ == "__main__":
    generate_grpc_code()
