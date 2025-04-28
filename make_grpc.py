import os
from grpc_tools import protoc
import pkg_resources

def generate_grpc_code():
    proto_file = "model_manager_client/generated/model_service.proto"
    output_dir = "model_manager_client/generated"

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # grpc_tools自带的标准proto文件路径
    proto_include = pkg_resources.resource_filename('grpc_tools', '_proto')

    # 运行 protoc 命令生成 Python 文件
    result = protoc.main([
        "",
        f"-I={os.path.dirname(proto_file)}",  # 你的proto文件路径
        f"-I={proto_include}",                # 加上grpc_tools自带的标准proto路径
        f"--python_out={output_dir}",
        f"--grpc_python_out={output_dir}",
        proto_file,
    ])

    print("Generating gRPC code...")
    if result == 0:
        print("✅ gRPC code generation succeeded.")
    else:
        print(f"❌ gRPC code generation failed with exit code {result}.")

if __name__ == "__main__":
    generate_grpc_code()