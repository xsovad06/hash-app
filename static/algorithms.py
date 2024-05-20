import math
import hashlib
from typing import List
from struct import pack, unpack

def isTrue(x): return x == 1    # truth condition is integer 1
def if_(i, y, z): return y if isTrue(i) else z  # simple if
def and_(i, j): return if_(i, j, 0) # and - both arguments need to be true
def AND(i, j): return [and_(ia, ja) for ia, ja in zip(i,j)] 
def not_(i): return if_(i, 0, 1)    # simply negates argument
def NOT(i): return [not_(x) for x in i]
def xor(i, j): return if_(i, not_(j), j)    # retrun true if either i or j is true but not both at the same time
def XOR(i, j): return [xor(ia, ja) for ia, ja in zip(i, j)]
def xorxor(i, j, l): return xor(i, xor(j, l))   # if number of truth values is odd then return true
def XORXOR(i, j, l): return [xorxor(ia, ja, la) for ia, ja, la, in zip(i, j, l)]
def maj(i,j,k): return max([i,j,], key=[i,j,k].count)   # get the majority of results, i.e., if 2 or more of three values are the same


class Algorithm:
    """A class applying the hash algorithms."""

    algorithms = ['md5', 'sha1', 'sha1-custom', 'sha256']

    def __init__(self, message: str, type: str) -> None:
        self.message = message
        self._type = type
        if self._type not in self.algorithms:
            raise ValueError(f'Invalid algorithm: {self._type}')

    @property
    def type(self):
        return self._type

    def hash(self):
        """Hash the message using the given algorithm."""

        if self._type =='md5':
            hash = MD5()
        elif self._type =='sha1':
            hash = SHA1()
        elif self._type =='sha256':
            hash = SHA256()

        hash.update(self.message)
        return hash.hexdigest()

class MD5:
    """Class implementing a MD5 hash algorithm."""
    rotate_by = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
                4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]
    # This list maintains the additive constant to be added in each processing step.
    constants = [int(abs(math.sin(i+1)) * 4294967296) & 0xFFFFFFFF for i in range(64)]
    init_MDBuffer = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]

    def __pad(self, message):
        msg_len_in_bits = (8*len(message)) & 0xffffffffffffffff
        message.append(0x80)

        while len(message)%64 != 56:
            message.append(0)


        # sys.byteorder -> 'little'
        message += msg_len_in_bits.to_bytes(8, byteorder='little') # little endian convention
        # to_bytes(8...) will return the lower order 64 bits(8 bytes) of the length.
        return message

    def __leftRotate(self, x, amount):
        x &= 0xFFFFFFFF
        return (x << amount | x >> (32-amount)) & 0xFFFFFFFF

    def __processMessage(self, message: str):
        init_temp = self.init_MDBuffer[:] # create copy of the buffer init constants to preserve them for when message has multiple 512-bit blocks

        # message length is a multiple of 512bits, but the processing is to be done separately for every 512-bit block.
        for offset in range(0, len(message), 64):
            A, B, C, D = init_temp # have to initialise MD Buffer for every block
            block = message[offset : offset+64] # create block to be processed
            # msg is processed as chunks of 16-words, hence, 16 such 32-bit chunks
            for i in range(64): # 1 pass through the loop processes some 32 bits out of the 512-bit block.
                if i < 16:
                    # Round 1
                    func = lambda b, c, d: (b & c) | (~b & d)
                    # if b is true then ans is c, else d.
                    index_func = lambda i: i

                elif i >= 16 and i < 32:
                    # Round 2
                    func = lambda b, c, d: (d & b) | (~d & c)
                    # if d is true then ans is b, else c.
                    index_func = lambda i: (5*i + 1)%16

                elif i >= 32 and i < 48:
                    # Round 3
                    func = lambda b, c, d: b ^ c ^ d
                    # Parity of b, c, d
                    index_func = lambda i: (3*i + 5)%16

                elif i >= 48 and i < 64:
                    # Round 4
                    func = lambda b, c, d: c ^ (b | ~d)
                    index_func = lambda i: (7*i)%16

                F = func(B, C, D) # operate on MD Buffers B, C, D
                G = index_func(i) # select one of the 32-bit words from the 512-bit block of the original message to operate on.

                to_rotate = A + F + self.constants[i] + int.from_bytes(block[4*G : 4*G + 4], byteorder='little')
                newB = (B + self.__leftRotate(to_rotate, self.rotate_by[i])) & 0xFFFFFFFF

                A, B, C, D = D, newB, B, C
                # rotate the contents of the 4 MD buffers by one every pass through the loop

            # Add the final output of the above stage to initial buffer states
            for i, val in enumerate([A, B, C, D]):
                init_temp[i] += val
                init_temp[i] &= 0xFFFFFFFF
            # The init_temp list now holds the MD(in the form of the 4 buffers A, B, C, D) of the 512-bit block of the message fed.

        # The same process is to be performed for every 512-bit block to get the final MD(message digest).

        # Construct the final message from the final states of the MD Buffers
        return sum(buffer_content<<(32*i) for i, buffer_content in enumerate(init_temp))

    def __MD_to_hex(self, digest):
        # takes MD from the processing stage, change its endian-ness and return it as 128-bit hex hash
        raw = digest.to_bytes(16, byteorder='little')
        return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))

    def update(self, message: str) -> str:
        """Prepares the given message."""

        message = bytearray(message, 'ascii') # create a copy of the original message in form of a sequence of integers [0, 256)
        message = self.__pad(message)
        self.processed_msg = self.__processMessage(message)

    def hexdigest(self) -> str:
        """Calculates the MD5 hash of the processed message."""

        # processed_msg contains the integer value of the hash
        return self.__MD_to_hex(self.processed_msg)

class SHA1:
    """Class implementing a SHA1 hash algorithm."""

    def __init__(self):
        self.__H = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]

    def __str__(self):
        return ''.join((hex(h)[2:]).rjust(8, '0') for h in self.__H)

    # Private static methods used for internal operations.
    @staticmethod
    def __ROTL(n, x, w=32):
        return ((x << n) | (x >> w - n))

    @staticmethod
    def __padding(stream):
        l = len(stream)  # Bytes
        hl = [int((hex(l*8)[2:]).rjust(16, '0')[i:i+2], 16)
              for i in range(0, 16, 2)]

        l0 = (56 - l) % 64
        if not l0:
            l0 = 64

        if isinstance(stream, str):
            stream += chr(0b10000000)
            stream += chr(0)*(l0-1)
            for a in hl:
                stream += chr(a)
        elif isinstance(stream, bytes):
            stream += bytes([0b10000000])
            stream += bytes(l0-1)
            stream += bytes(hl)

        return stream

    @staticmethod
    def __prepare(stream):
        M = []
        n_blocks = len(stream) // 64

        stream = bytearray(stream)

        for i in range(n_blocks):  # 64 Bytes per Block
            m = []

            for j in range(16):  # 16 Words per Block
                n = 0
                for k in range(4):  # 4 Bytes per Word
                    n <<= 8
                    n += stream[i*64 + j*4 + k]

                m.append(n)

            M.append(m[:])

        return M

    def __process_block(self, block):
        MASK = 2**32-1

        W = block[:]
        for t in range(16, 80):
            W.append(SHA1.__ROTL(1, (W[t-3] ^ W[t-8] ^ W[t-14] ^ W[t-16]))
                     & MASK)

        a, b, c, d, e = self.__H[:]

        for t in range(80):
            if t <= 19:
                K = 0x5a827999
                f = (b & c) ^ (~b & d)
            elif t <= 39:
                K = 0x6ed9eba1
                f = b ^ c ^ d
            elif t <= 59:
                K = 0x8f1bbcdc
                f = (b & c) ^ (b & d) ^ (c & d)
            else:
                K = 0xca62c1d6
                f = b ^ c ^ d

            T = ((SHA1.__ROTL(5, a) + f + e + K + W[t]) & MASK)
            e = d
            d = c
            c = SHA1.__ROTL(30, b) & MASK
            b = a
            a = T

        self.__H[0] = (a + self.__H[0]) & MASK
        self.__H[1] = (b + self.__H[1]) & MASK
        self.__H[2] = (c + self.__H[2]) & MASK
        self.__H[3] = (d + self.__H[3]) & MASK
        self.__H[4] = (e + self.__H[4]) & MASK

    # Public methods for class use.
    def update(self, stream: str):
        stream = stream.encode('utf-8')
        stream = SHA1.__padding(stream)
        stream = SHA1.__prepare(stream)

        for block in stream:
            self.__process_block(block)

    def digest(self):
        pass

    def hexdigest(self):
        s = ''
        for h in self.__H:
            s += (hex(h)[2:]).rjust(8, '0')
        return s

class SHA256:
    """Class implementing a SHA256 hash algorithm."""

    K = ['0x428a2f98', '0x71374491', '0xb5c0fbcf', '0xe9b5dba5', '0x3956c25b', '0x59f111f1', '0x923f82a4','0xab1c5ed5', '0xd807aa98', '0x12835b01', '0x243185be', '0x550c7dc3', '0x72be5d74', '0x80deb1fe','0x9bdc06a7', '0xc19bf174', '0xe49b69c1', '0xefbe4786', '0x0fc19dc6', '0x240ca1cc', '0x2de92c6f','0x4a7484aa', '0x5cb0a9dc', '0x76f988da', '0x983e5152', '0xa831c66d', '0xb00327c8', '0xbf597fc7','0xc6e00bf3', '0xd5a79147', '0x06ca6351', '0x14292967', '0x27b70a85', '0x2e1b2138', '0x4d2c6dfc','0x53380d13', '0x650a7354', '0x766a0abb', '0x81c2c92e', '0x92722c85', '0xa2bfe8a1', '0xa81a664b','0xc24b8b70', '0xc76c51a3', '0xd192e819', '0xd6990624', '0xf40e3585', '0x106aa070', '0x19a4c116','0x1e376c08', '0x2748774c', '0x34b0bcb5', '0x391c0cb3', '0x4ed8aa4a', '0x5b9cca4f', '0x682e6ff3','0x748f82ee', '0x78a5636f', '0x84c87814', '0x8cc70208', '0x90befffa', '0xa4506ceb', '0xbef9a3f7','0xc67178f2']
    h_hex = ['0x6a09e667', '0xbb67ae85', '0x3c6ef372', '0xa54ff53a', '0x510e527f', '0x9b05688c', '0x1f83d9ab', '0x5be0cd19']

    def __translate(self, message: str) -> List[int]:
        """Takes a string and converts it to a list of 32-bit integers."""

        # string characters to unicode values
        charcodes = [ord(c) for c in message]
        # unicode values to 8-bit strings (removed binary indicator)
        bytes = []
        for char in charcodes:
            bytes.append(bin(char)[2:].zfill(8))
        # 8-bit strings to list of bits as integers
        bits = []
        for byte in bytes:
            for bit in byte:
                bits.append(int(bit))
        return bits

    def __b2Tob16(self, value: List[int]) -> str:
        """Takes list of 32 bits and converts them to a HEX string."""

        # convert to string
        value = ''.join([str(x) for x in value])
        # creat 4 bit chunks, and add bin-indicator
        binaries = []
        for d in range(0, len(value), 4):
            binaries.append('0b' + value[d:d+4])
        # transform to hexadecimal and remove hex-indicator
        hexes = ''
        for b in binaries:
            hexes += hex(int(b ,2))[2:]
        return hexes

    def __fillZeros(self, bits: List[int], length=8, endian='LE'):
        """Takes a list of bits and fills it with zeros to the given length."""

        l = len(bits)
        if endian == 'LE':
            for i in range(l, length):
                bits.append(0)
        else: 
            while l < length:
                bits.insert(0, 0)
                l = len(bits)
        return bits

    def __chunker(self, bits: List[int], chunk_length=8):
        """Divides list of bits into desired byte/word chunks, starting at LSB."""

        chunked = []
        for b in range(0, len(bits), chunk_length):
            chunked.append(bits[b:b+chunk_length])
        return chunked

    def __initializer(self, values):
        """Initializes a new instance of the chunker class."""

        # convert from hex to python binary string (with cut bin indicator ('0b'))."""
        binaries = [bin(int(v, 16))[2:] for v in values]
        # convert from python string representation to a list of 32 bit lists
        words = []
        for binary in binaries:
            word = []
            for b in binary:
                word.append(int(b))
            words.append(self.__fillZeros(word, 32, 'BE'))
        return words

    def __preprocessMessage(self, message: str):
        """Takes the message converts it into a chunks of bits."""

        # translate message into bits
        bits = self.__translate(message)
        # message length 
        length = len(bits)
        #  get length in bits  of message (64 bit block)
        message_len = [int(b) for b in bin(length)[2:].zfill(64)]
        # if length smaller than 448 handle block individually otherwise
        # if exactly 448 then add single 1 and add up to 1024 and if longer than 448
        # create multiple of 512 - 64 bits for the length at the end of the message (big endian)
        if length < 448:
            # append single 1
            bits.append(1)
            # fill zeros little endian wise
            bits = self.__fillZeros(bits, 448, 'LE')
            # add the 64 bits representing the length of the message
            bits = bits + message_len
            # return as list
            return [bits]
        elif 448 <= length <= 512:
            bits.append(1)
            # moves to next message block - total length = 1024
            bits = self.__fillZeros(bits, 1024, 'LE')
            # replace the last 64 bits of the multiple of 512 with the original message length
            bits[-64:] = message_len
            # returns it in 512 bit chunks
            return self.__chunker(bits, 512)
        else:
            bits.append(1)
            # loop until multiple of 512 + 64 bit message_len if message length exceeds 448 bits
            while (len(bits)+64) % 512 != 0:
                bits.append(0)
            # add the 64 bits representing the length of the message    
            bits = bits + message_len
            # returns it in 512 bit chunks
            return self.__chunker(bits, 512)

    def __rotr(self, x, n):
        """Rotates the list of bites to the right."""

        return x[-n:] + x[:-n]

    def __shr(self, x, n):
        """Shifts the list of bites to the right."""

        return n * [0] + x[:-n]

    def __add(self, i: List[int], j: List[int]) -> List[int]:
        """Takes to lists of binaries and adds them."""

        length = len(i)
        sums = list(range(length))
        # initial input needs an carry over bit as 0
        c = 0
        for x in range(length-1,-1,-1):
            # add the inout bits with a double xor gate
            sums[x] = xorxor(i[x], j[x], c)
            # carry over bit is equal the most represented, e.g., output = 0,1,0 
            # then 0 is the carry over bit
            c = maj(i[x], j[x], c)
        return sums

    def update(self, message: str) -> None:
        """Calculates the the SHA-256 hash of a message."""

        self.chunks = self.__preprocessMessage(message)

    def hexdigest(self) -> str:
        """Calculates the the SHA-256 hash of a message."""

        k = self.__initializer(self.K)
        h0, h1, h2, h3, h4, h5, h6, h7 = self.__initializer(self.h_hex)
        for chunk in self.chunks:
            w = self.__chunker(chunk, 32)
            for _ in range(48):
                w.append(32 * [0])
            for i in range(16, 64):
                s0 = XORXOR(self.__rotr(w[i-15], 7), self.__rotr(w[i-15], 18), self.__shr(w[i-15], 3) ) 
                s1 = XORXOR(self.__rotr(w[i-2], 17), self.__rotr(w[i-2], 19), self.__shr(w[i-2], 10))
                w[i] = self.__add(self.__add(self.__add(w[i-16], s0), w[i-7]), s1)
            a = h0
            b = h1
            c = h2
            d = h3
            e = h4
            f = h5
            g = h6
            h = h7
            for j in range(64):
                S1 = XORXOR(self.__rotr(e, 6), self.__rotr(e, 11), self.__rotr(e, 25) )
                ch = XOR(AND(e, f), AND(NOT(e), g))
                temp1 = self.__add(self.__add(self.__add(self.__add(h, S1), ch), k[j]), w[j])
                S0 = XORXOR(self.__rotr(a, 2), self.__rotr(a, 13), self.__rotr(a, 22))
                m = XORXOR(AND(a, b), AND(a, c), AND(b, c))
                temp2 = self.__add(S0, m)
                h = g
                g = f
                f = e
                e = self.__add(d, temp1)
                d = c
                c = b
                b = a
                a = self.__add(temp1, temp2)
            h0 = self.__add(h0, a)
            h1 = self.__add(h1, b)
            h2 = self.__add(h2, c)
            h3 = self.__add(h3, d)
            h4 = self.__add(h4, e)
            h5 = self.__add(h5, f)
            h6 = self.__add(h6, g)
            h7 = self.__add(h7, h)
        digest = ''
        for val in [h0, h1, h2, h3, h4, h5, h6, h7]:
            digest += self.__b2Tob16(val)
        return digest