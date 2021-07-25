import rsa


def encryptBookKey(pubkey, key):
    if(len(key) <= 117):
        crypto = rsa.encrypt(key.encode(), pubkey)
        return crypto
    else:
        key1 = key[0:117]
        key2 = key[117:]
        crypto1 = rsa.encrypt(key1.encode(), pubkey)
        crypto2 = rsa.encrypt(key2.encode(), pubkey)
        crypto = crypto1 + crypto2
        return crypto

# (pubkey, privkey) = rsa.newkeys(1024)
# encrypt1 = encrypt(pubkey, privkey, 'hello'.encode())
# (pubkey, privkey) = rsa.newkeys(1024)

# encryptBookKey('00001111')
