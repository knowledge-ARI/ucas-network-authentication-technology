"""实验五：SHA-256 摘要计算。"""
from cryptography.hazmat.primitives import hashes


# 1. 定义摘要函数：把输入字节送入 SHA-256，返回固定 32 字节结果。
def sha256(data):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(data)
    return digest.finalize()


# 2. 选定输入 abc，并与公开的 SHA-256 已知摘要比对。
message = b"abc"
result = sha256(message)
expected = ("ba7816bf8f01cfea414140de5dae2223"
            "b00361a396177a9cb410ff61f20015ad")
print("实验五  SHA-256")
print("输入:", message.decode())
print("摘要:", result.hex())
print("摘要长度:", len(result) * 8, "bit")
if result.hex() != expected:
    raise RuntimeError("与已知摘要不一致")
print("[PASS] 与abc已知摘要一致")

# 3. 分两次输入 a 与 bc；拼接后的字节序列仍然是 abc。
stream = hashes.Hash(hashes.SHA256())
stream.update(b"a")
stream.update(b"bc")
if stream.finalize() != result:
    raise RuntimeError("分块摘要不一致")
print("[PASS] 分块a+bc与一次输入abc的摘要一致")
# 4. 只把最后一个字节 c 改成 d，观察输出摘要是否变化。
changed = sha256(b"abd")
print("修改后的输入: abd")
print("修改后的摘要:", changed.hex())
if changed == result:
    raise RuntimeError("两组测试输入摘要意外相同")
print("[PASS] 这两组不同输入的摘要不同")
print("实验五完成")

