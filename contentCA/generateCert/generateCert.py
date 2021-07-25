import base64
import time

from M2Crypto import X509, EVP, RSA, ASN1


def issuer_name():

    """

    证书发行人名称(专有名称)。

    Parameters:

        none

    Return:

        X509标准的发行人obj.

    """

    issuer = X509.X509_Name()

    issuer.C = "CN"     # 国家名称

    issuer.CN = "*.jb51.net"    # 普通名字

    issuer.ST = "Hunan Changsha"

    issuer.L = "Hunan Changsha"

    issuer.O = "Geekso Company Ltd"

    issuer.OU = "Geekso Company Ltd"

    issuer.Email = "123456@qq.com"

    return issuer


def make_request(bits, cn):

    """

    创建一个X509标准的请求。

    Parameters:

        bits = 证书位数

        cn = 证书名称

    Return:

        返回 X509 request 与 private key (EVP).

    """

    rsa = RSA.gen_key(bits, 65537)

    pk = EVP.PKey()

    pk.assign_rsa(rsa)

    req = X509.Request()

    req.set_pubkey(pk)

    name = req.get_subject()

    name.C = "US"

    name.CN = cn

    req.sign(pk, 'sha256')

    return req, pk


def make_certificate_valid_time(cert, days):

    """

    从当前时间算起证书有效期几天。

    Parameters:

        cert = 证书obj

        days = 证书过期的天数

    Return:

        none

    """

    t = int(time.time()) # 获取当前时间

    time_now = ASN1.ASN1_UTCTIME()

    time_now.set_time(t)

    time_exp = ASN1.ASN1_UTCTIME()

    time_exp.set_time(t + days * 24 * 60 * 60)

    cert.set_not_before(time_now)

    cert.set_not_after(time_exp)


def make_certificate(bits):

    """

    创建证书

    Parameters:

        bits = 证快的位数

    Return:

        证书, 私钥 key (EVP) 与 公钥 key (EVP).

    """

    req, pk = make_request(bits, "localhost")

    puk = req.get_pubkey()

    cert = X509.X509()

    cert.set_serial_number(1) # 证书的序例号

    cert.set_version(1) # 证书的版本

    cert.set_issuer(issuer_name()) # 发行人信息

    cert.set_subject(issuer_name()) # 主题信息

    cert.set_pubkey(puk)

    make_certificate_valid_time(cert, 365) # 证书的过期时间

    cert.sign(pk, 'sha256')

    return cert, pk, puk


def geekso_encrypt_with_certificate(message, cert_loc):

    """

    cert证书加密，可以用私钥文件解密.

    Parameters:

        message = 要加密的串

        cert_loc = cert证书路径

    Return:

        加密串 or 异常串

    """

    cert = X509.load_cert(cert_loc)

    puk = cert.get_pubkey().get_rsa() # get RSA for encryption

    message = base64.b64encode(message.encode())

    try:

        encrypted = puk.public_encrypt(message, RSA.pkcs1_padding)

    except RSA.RSAError as e:

        return "ERROR encrypting " + e.message

    return encrypted


def geekso_decrypt_with_private_key(message, pk_loc):

    """

    私钥解密证书生成的加密串

    Parameters:

        message = 加密的串

        pk_loc = 私钥路径

    Return:

        解密串 or 异常串

    """

    pk = RSA.load_key(pk_loc) # load RSA for decryption

    try:

        decrypted = pk.private_decrypt(message, RSA.pkcs1_padding)

        decrypted = base64.b64decode(decrypted)

    except RSA.RSAError as e:

        return "ERROR decrypting " + e.message

    return decrypted


# 开始创建

cert, pk, puk = make_certificate(1024)

cert.save_pem('./key/cret.pem')

pk.save_key('./key/private.pem', cipher=None, callback=lambda: None)

puk.get_rsa().save_pub_key('./key/public.pem')
# print(time.time())

encrypted = geekso_encrypt_with_certificate('cid,uid,did,private_key', './key/cret.pem')

print('加密串', encrypted)

print('解密串', geekso_decrypt_with_private_key(encrypted, './key/private.pem'))
