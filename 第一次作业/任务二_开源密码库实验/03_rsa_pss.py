"""实验三：RSA-PSS 数字签名与验证。"""
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

# 1. 单独生成 2048 位签名密钥对，不复用加密实验中的私钥。
# 签名独立生成密钥，不复用加密实验的密钥。
private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public = private.public_key()


# 2. 设置 PSS 编码：MGF1 使用 SHA-256，随机盐固定为 32 字节。
def pss():
    return padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()), salt_length=32)


# 3. 把待签消息编码为字节；sign 内部计算 SHA-256 摘要并用私钥签名。
message = "本消息用于网络认证签名实验".encode("utf-8")
signature = private.sign(message, pss(), hashes.SHA256())
print("实验三  RSA-PSS / SHA-256")
print("签名密钥模数:", public.key_size, "bit")
print("原始消息:", message.decode())
print("签名长度:", len(signature), "字节")
print("签名前32字节（节选）:", signature[:32].hex())
# 4. 用对应公钥验证原消息；成功时正常返回，不返回布尔值。
public.verify(signature, message, pss(), hashes.SHA256())
print("[PASS] 原消息与对应公钥验签成功")

# 5. 修改消息末尾一个字节；摘要变化，原签名应验证失败。
try:
    public.verify(signature, message + b"!", pss(), hashes.SHA256())
except InvalidSignature:
    print("[PASS] 篡改消息验签失败 InvalidSignature")
else:
    raise RuntimeError("错误：篡改消息通过验签")

# 6. 新建另一组密钥；用错误公钥检查签名和密钥的绑定。
other = rsa.generate_private_key(public_exponent=65537, key_size=2048)
try:
    other.public_key().verify(
        signature, message, pss(), hashes.SHA256())
except InvalidSignature:
    print("[PASS] 错误公钥验签失败 InvalidSignature")
else:
    raise RuntimeError("错误：错误公钥通过验签")
print("实验三完成")

