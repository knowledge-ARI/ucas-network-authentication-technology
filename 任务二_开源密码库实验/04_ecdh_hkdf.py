"""实验四：ECDH 密钥交换及 HKDF 会话密钥派生。"""
import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

# 1. Alice、Bob 在相同 P-256 曲线上各自生成临时私钥。
alice = ec.generate_private_key(ec.SECP256R1())
bob = ec.generate_private_key(ec.SECP256R1())


# 2. 将公钥点编码为未压缩格式，供对方解析；私钥从不传送。
def public_bytes(private):
    return private.public_key().public_bytes(
        serialization.Encoding.X962,
        serialization.PublicFormat.UncompressedPoint)


# 用公钥的编码与解码模拟传递；不传递私钥。
ap, bp = public_bytes(alice), public_bytes(bob)
bob_public = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), bp)
alice_public = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), ap)
# 3. Alice 用自己的私钥和 Bob 公钥计算共享秘密；Bob 反向计算。
sa = alice.exchange(ec.ECDH(), bob_public)
sb = bob.exchange(ec.ECDH(), alice_public)
# 4. 为 HKDF 准备同一份 salt 与 info；info 绑定用途和双方公钥。
salt = os.urandom(16)
info = b"course/04/Alice-to-Bob/" + ap + bp


# 5. HKDF-SHA256 把共享秘密材料派生为 32 字节 AES 会话密钥。
def derive(secret):
    # 双方使用相同 salt、info 和输出长度。
    return HKDF(algorithm=hashes.SHA256(), length=32,
                salt=salt, info=info).derive(secret)


# 6. 双方分别派生并比较结果；一致说明本次协商材料相同。
ka, kb = derive(sa), derive(sb)
print("实验四  ECDH P-256 + HKDF-SHA256")
print("双方临时密钥生成完成，公钥编码长度:", len(ap), "字节")
print("共享秘密长度:", len(sa), "字节")
print("共享秘密一致:", sa == sb)
print("派生会话密钥一致:", ka == kb)
if sa != sb or ka != kb:
    raise RuntimeError("密钥协商结果不一致")
print("[PASS] 双方独立计算得到相同会话密钥")
# 7. Alice 用派生密钥加密“Hello Bob”，Bob 用自己的派生密钥解密。
nonce = os.urandom(12)
packet = AESGCM(ka).encrypt(nonce, b"Hello Bob", info)
recovered = AESGCM(kb).decrypt(nonce, packet, info)
print("Bob解密结果:", recovered.decode())
if recovered != b"Hello Bob":
    raise RuntimeError("会话密钥通信测试失败")
print("[PASS] 派生密钥可以用于AES通信")
print("说明：本实验未实现对端身份认证")
print("实验四完成")

