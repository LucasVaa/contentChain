import rsa


class DeviceKey:

   def __init__(self):
       (self.pubkey, self.privkey) = rsa.newkeys(1024)
       self.pubkey = self.pubkey.save_pkcs1().decode()
       self.privkey = self.privkey.save_pkcs1().decode()


class InvalidClient(Exception):  # 异常处理类

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


if __name__ == '__main__':

    try:
        newKey = DeviceKey()
        pubkey = newKey.pubkey
        privkey = newKey.privkey
        print(pubkey)
        print(privkey)

    except InvalidClient as e:
        print(e)

