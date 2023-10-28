#!/usr/bin/env python3
# -*- coding:utf-8 -*-


def rotation_left(x, num):
    # 循环左移。
    num %= 32
    left = (x << num) % (2 ** 32)
    right = (x >> (32 - num)) % (2 ** 32)
    result = left ^ right
    return result


def int_to_bin(x, k):
    x = str(bin(x)[2:])
    result = "0" * (k - len(x)) + x
    return result


class SM3(object):

    def __init__(self):
        # 常量初始化。
        self.IV = [0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600, 0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E]
        self.T = [0x79cc4519, 0x7a879d8a]
        self.maxu32 = 2 ** 32
        self.w1 = [0] * 68
        self.w2 = [0] * 64

    @staticmethod
    def ff(x, y, z, j):
        # 布尔函数FF。
        result = 0
        if j < 16:
            result = x ^ y ^ z
        elif j >= 16:
            result = (x & y) | (x & z) | (y & z)
        return result

    @staticmethod
    def gg(x, y, z, j):
        # 布尔函数GG。
        result = 0
        if j < 16:
            result = x ^ y ^ z
        elif j >= 16:
            result = (x & y) | (~x & z)
        return result

    @staticmethod
    def p(x, mode):
        result = 0
        # 置换函数P。
        # 输入参数X的长度为32bit(=1个字)。
        # 输入参数mode共两种取值：0和1。
        if mode == 0:
            result = x ^ rotation_left(x, 9) ^ rotation_left(x, 17)
        elif mode == 1:
            result = x ^ rotation_left(x, 15) ^ rotation_left(x, 23)
        return result

    @staticmethod
    def sm3_fill(msg):
        # 填充消息，使其长度为512bit的整数倍。
        # 输入参数msg为bytearray类型。
        # 中间参数msg_new_bin为二进制string类型。
        # 输出参数msg_new_bytes为bytearray类型。
        length = len(msg)  # msg的长度（单位：byte）。
        ll = length * 8  # msg的长度（单位：bit）。

        num = length // 64
        remain_byte = length % 64
        msg_remain_bin = ""
        msg_new_bytes = bytearray((num + 1) * 64)  # 填充后的消息长度，单位：byte。

        # 将原数据存储至msg_new_bytes中。
        for i in range(length):
            msg_new_bytes[i] = msg[i]

        # remain部分以二进制字符串形式存储。
        remain_bit = remain_byte * 8  # 单位：bit。
        for i in range(remain_byte):
            msg_remain_bin += "{:08b}".format(msg[num * 64 + i])

        k = (448 - ll - 1) % 512
        while k < 0:
            # k为满足 ll + k + 1 = 448 % 512 的最小非负整数。
            k += 512

        msg_remain_bin += "1" + "0" * k + int_to_bin(ll, 64)

        for i in range(0, 64 - remain_byte):
            string = msg_remain_bin[i * 8 + remain_bit: (i + 1) * 8 + remain_bit]
            temp = length + i
            msg_new_bytes[temp] = int(string, 2)  # 将2进制字符串按byte为组转换为整数。
        return msg_new_bytes

    def sm3_msg_extend(self, msg):
        # 扩展函数: 将512bit的数据msg扩展为132个字（w1共68个字，w2共64个字）。
        # 输入参数msg为bytearray类型,长度为512bit=64byte。
        for i in range(0, 16):
            self.w1[i] = int.from_bytes(msg[i * 4:(i + 1) * 4], byteorder="big")

        for i in range(16, 68):
            self.w1[i] = self.p(self.w1[i - 16] ^ self.w1[i - 9] ^ rotation_left(self.w1[i - 3], 15),
                                1) ^ rotation_left(self.w1[i - 13], 7) ^ self.w1[i - 6]

        for i in range(64):
            self.w2[i] = self.w1[i] ^ self.w1[i + 4]

        # 测试扩展数据w1和w2。
        # print("w1:")
        # for i in range(0, len(self.w1), 8):
        #     print(hex(self.w1[i]))
        # print("w2:")
        # for i in range(0, len(self.w2), 8):
        #     print(hex(self.w2[i]))

    def sm3_compress(self, msg):
        # 压缩函数。
        # 输入参数v为初始化参数，类型为bytes/bytearray，大小为256bit。
        # 输入参数msg为512bit的待压缩数据。

        self.sm3_msg_extend(msg)
        ss1 = 0

        a = self.IV[0]
        b = self.IV[1]
        c = self.IV[2]
        d = self.IV[3]
        e = self.IV[4]
        f = self.IV[5]
        g = self.IV[6]
        h = self.IV[7]

        for j in range(64):
            if j < 16:
                ss1 = rotation_left((rotation_left(a, 12) + e + rotation_left(self.T[0], j)) % self.maxu32, 7)
            elif j >= 16:
                ss1 = rotation_left((rotation_left(a, 12) + e + rotation_left(self.T[1], j)) % self.maxu32, 7)
            ss2 = ss1 ^ rotation_left(a, 12)
            tt1 = (self.ff(a, b, c, j) + d + ss2 + self.w2[j]) % self.maxu32
            tt2 = (self.gg(e, f, g, j) + h + ss1 + self.w1[j]) % self.maxu32
            d = c
            c = rotation_left(b, 9)
            b = a
            a = tt1
            h = g
            g = rotation_left(f, 19)
            f = e
            e = self.p(tt2, 0)

            # 测试IV的压缩中间值。
            # print("j= %d：" % j, hex(A)[2:], hex(B)[2:], hex(C)[2:], hex(D)[2:],
            #       hex(E)[2:], hex(F)[2:], hex(G)[2:], hex(H)[2:])

        self.IV[0] ^= a
        self.IV[1] ^= b
        self.IV[2] ^= c
        self.IV[3] ^= d
        self.IV[4] ^= e
        self.IV[5] ^= f
        self.IV[6] ^= g
        self.IV[7] ^= h

    def sm3_update(self, msg):
        # 迭代函数。
        # 输入参数msg为bytearray类型。
        # msg_new为bytearray类型。
        msg_new = self.sm3_fill(msg)  # msg_new经过填充后一定是512的整数倍。
        n = len(msg_new) // 64  # n是整数，n>=1。

        for i in range(0, n):
            self.sm3_compress(msg_new[i * 64:(i + 1) * 64])

    def sm3_final(self):
        digest_str = ""
        for i in range(len(self.IV)):
            tmp_str = hex(self.IV[i])[2:]
            print(tmp_str)
            if len(tmp_str) < 8:
                tmp_str = "0" * (8 - len(tmp_str)) + tmp_str
            digest_str += tmp_str

        return digest_str.lower()

    def hash_file(self, filename):
        with open(filename, 'rb') as fp:
            contents = fp.read()
            self.sm3_update(bytearray(contents))
        return self.sm3_final()


if __name__ == "__main__":

    # msg1 = bytearray(b"abc")
    # print("msg1:", msg1.hex(), len(msg1))
    #
    # test1 = SM3()
    # test1.sm3_update(msg1)
    # digest1 = test1.sm3_final()
    # print("digest1:", digest1)
    #
    # msg2 = bytearray(b'abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd')
    # msg2 = bytes(msg2)
    # print("msg2:", msg2.hex(), len(msg2))
    #
    # test2 = SM3()
    # test2.sm3_update(msg2)
    # digest2 = test2.sm3_final()
    # print("digest2:", digest2)

    # 求大小为48M的文件的摘要，大约需要7分钟。
    test3 = SM3()
    file_digest = test3.hash_file("../resources/我的逻辑小键盘.mp4")
    file_digest = file_digest.lower()
    print('file_digest', file_digest)
