"""实验二：RSA 密钥生成与 OAEP 加解密。"""
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

# 1. 库内部生成两个大素数及 RSA 私钥，设置 2048 位模数和 e=65537。
private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
# 2. 从私钥提取公钥，编码为 PEM 再载入，模拟公钥交给发送方。
pem = private.public_key().public_bytes(
    serialization.Encoding.PEM,
    serialization.PublicFormat.SubjectPublicKeyInfo)
public = serialization.load_pem_public_key(pem)


# 3. 统一加密与解密的 OAEP 参数：消息摘要和 MGF1 都选 SHA-256。
def oaep():
    return padding.OAEP(
        mgf=padding.MGF1(hashes.SHA256()),
        algorithm=hashes.SHA256(), label=None)


# 4. 把中文明文编码为 UTF-8 字节，再用接收方公钥随机化加密。
message = "网络认证技术 RSA 实验".encode("utf-8")
ciphertext = public.encrypt(message, oaep())
# 5. 由接收方私钥解密，并检查 OAEP 编码，恢复原始字节。
recovered = private.decrypt(ciphertext, oaep())
print("实验二  RSA-2048 / OAEP-SHA256")
print("RSA密钥生成成功，模数位数:", public.key_size)
print("公钥指数:", public.public_numbers().e)
print("原始明文:", message.decode())
print("密文长度:", len(ciphertext), "字节")
print("密文前32字节（节选）:", ciphertext[:32].hex())
print("解密明文:", recovered.decode())
if recovered != message:
    raise RuntimeError("RSA解密结果错误")
print("[PASS] 公钥加密、私钥解密一致")
# 6. 同一明文重新加密；比较两份密文，观察 OAEP 的随机性。
second = public.encrypt(message, oaep())
if second == ciphertext:
    raise RuntimeError("两次随机编码密文意外相同")
print("[PASS] 同一明文两次加密的密文不同")

# 7. 检验长度边界：2048 位模数为 256 字节，SHA-256 摘要为 32 字节。
#    OAEP 明文上限是 256 - 2*32 - 2 = 190 字节。
edge = public.encrypt(b"A" * 190, oaep())
if private.decrypt(edge, oaep()) != b"A" * 190:
    raise RuntimeError("边界测试失败")
print("[PASS] 190字节明文加解密成功")
try:
    public.encrypt(b"A" * 191, oaep())
except ValueError:
    print("[PASS] 191字节超长明文被拒绝 ValueError")
else:
    raise RuntimeError("错误：接受了超长明文")
print("实验二完成")

