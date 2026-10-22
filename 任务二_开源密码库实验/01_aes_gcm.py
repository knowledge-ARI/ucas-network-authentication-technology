"""实验一：AES-256-GCM 对称加解密。"""
import os
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# 1. 生成 256 位 AES 密钥和 12 字节随机 Nonce。
#    GCM 在同一密钥下不能重复使用 Nonce；本程序每次仅加密一次。
key = AESGCM.generate_key(bit_length=256)
nonce = os.urandom(12)  # 此密钥只加密一次，避免重复 nonce。
# 2. 准备 UTF-8 明文与只认证、不加密的附加数据 AAD。
message = "网络认证技术 AES 实验".encode("utf-8")
aad = b"course=network-auth;experiment=01"
# 3. 用密钥建立 AES-GCM 对象；encrypt 输出“密文 + 16 字节标签”。
cipher = AESGCM(key)
packet = cipher.encrypt(nonce, message, aad)
# 4. 使用相同密钥、Nonce、AAD 验证标签并解密。
recovered = cipher.decrypt(nonce, packet, aad)

# 5. 分别展示明文、密文、标签和解密结果，便于和截图核对。
print("实验一  AES-256-GCM")
print("密钥长度:", len(key) * 8, "bit")
print("原始明文:", message.decode())
print("Nonce:", nonce.hex())
print("密文:", packet[:-16].hex())
print("认证标签:", packet[-16:].hex())
print("解密明文:", recovered.decode())
if recovered != message:
    raise RuntimeError("加解密结果不一致")
print("[PASS] 加解密一致")

# 6. 翻转密文第一字节的一个比特；原标签不变，认证必须失败。
altered = bytes([packet[0] ^ 1]) + packet[1:]
try:
    cipher.decrypt(nonce, altered, aad)
except InvalidTag:
    print("[PASS] 篡改密文被拒绝 InvalidTag")
else:
    raise RuntimeError("错误：接受了篡改密文")
# 7. 仅替换 AAD；即使密文不变，标签核验仍应拒绝。
try:
    cipher.decrypt(nonce, packet, b"wrong-aad")
except InvalidTag:
    print("[PASS] 错误AAD被拒绝 InvalidTag")
else:
    raise RuntimeError("错误：接受了错误AAD")
print("实验一完成")

