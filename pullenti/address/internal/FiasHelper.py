# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import Stream

class FiasHelper:
    
    @staticmethod
    def serialize_byte(res : Stream, val : int) -> None:
        res.writebyte(val)
    
    @staticmethod
    def serialize_short(res : Stream, val : int) -> None:
        res.writebyte(val)
        res.writebyte((val >> 8))
    
    @staticmethod
    def serialize_int(res : Stream, val : int) -> None:
        res.writebyte(val)
        res.writebyte((val >> 8))
        res.writebyte((val >> 16))
        res.writebyte((val >> 24))
    
    @staticmethod
    def deserialize_byte(str0_ : Stream) -> int:
        return str0_.readbyte()
    
    @staticmethod
    def deserialize_short(str0_ : Stream) -> int:
        b0 = str0_.readbyte()
        b1 = str0_.readbyte()
        res = b1
        res <<= 8
        return (res | b0)
    
    @staticmethod
    def deserialize_int(str0_ : Stream) -> int:
        b0 = str0_.readbyte()
        b1 = str0_.readbyte()
        b2 = str0_.readbyte()
        b3 = str0_.readbyte()
        res = b3
        res <<= 8
        res |= b2
        res <<= 8
        res |= b1
        res <<= 8
        return (res | b0)
    
    @staticmethod
    def serialize_string(res : Stream, s : str, utf8 : bool=False) -> None:
        if (s is None): 
            res.writebyte(0xFF)
        elif (len(s) == 0): 
            res.writebyte(0)
        else: 
            data = (s.encode("UTF-8", 'ignore') if utf8 else FiasHelper.encode_string1251(s))
            res.writebyte(len(data))
            res.write(data, 0, len(data))
    
    @staticmethod
    def deserialize_string_from_bytes(dat : bytearray, ind : int, utf8 : bool=False) -> str:
        len0_ = dat[ind.value]
        ind.value += 1
        if (len0_ == (0xFF)): 
            return None
        if (len0_ == (0)): 
            return ""
        res = (dat[ind.value:ind.value+len0_].decode("UTF-8", 'ignore') if utf8 else FiasHelper.decode_string1251(dat, ind.value, len0_, False))
        ind.value += (len0_)
        return res
    
    @staticmethod
    def deserialize_string(str0_ : Stream) -> str:
        len0_ = str0_.readbyte()
        if (len0_ == (0xFF)): 
            return None
        if (len0_ == (0)): 
            return ""
        buf = Utils.newArrayOfBytes(len0_, 0)
        str0_.read(buf, 0, len0_)
        return FiasHelper.decode_string1251(buf, 0, -1, False)
    
    __m_1251_utf = None
    
    __m_utf_1251 = None
    
    @staticmethod
    def encode_string1251(str0_ : str) -> bytearray:
        if (str0_ is None): 
            return Utils.newArrayOfBytes(0, 0)
        res = Utils.newArrayOfBytes(len(str0_), 0)
        j = 0
        while j < len(str0_): 
            i = ord(str0_[j])
            if (i < 0x80): 
                res[j] = (i)
            else: 
                b = 0
                wrapb139 = RefOutArgWrapper(0)
                inoutres140 = Utils.tryGetValue(FiasHelper.__m_utf_1251, i, wrapb139)
                b = wrapb139.value
                if (inoutres140): 
                    res[j] = b
                else: 
                    res[j] = (ord('?'))
            j += 1
        return res
    
    @staticmethod
    def decode_string1251(dat : bytearray, pos : int=0, len0_ : int=-1, zero_term : bool=False) -> str:
        if (dat is None): 
            return None
        if (len(dat) == 0): 
            return ""
        if (len0_ < 0): 
            len0_ = (len(dat) - pos)
            if (zero_term and len0_ > 300): 
                len0_ = 300
        tmp = io.StringIO()
        j = pos
        while (j < (pos + len0_)) and (j < len(dat)): 
            i = dat[j]
            if (zero_term and i == 0): 
                break
            if (i < 0x80): 
                print(chr(i), end="", file=tmp)
            elif (FiasHelper.__m_1251_utf[i] == 0): 
                print('?', end="", file=tmp)
            else: 
                print(chr(FiasHelper.__m_1251_utf[i]), end="", file=tmp)
            j += 1
        return Utils.toStringStringIO(tmp)
    
    # static constructor for class FiasHelper
    @staticmethod
    def _static_ctor():
        FiasHelper.__m_1251_utf = Utils.newArray(256, 0)
        FiasHelper.__m_utf_1251 = dict()
        for i in range(0x80):
            FiasHelper.__m_1251_utf[i] = i
        m_1251_80_bf = [0x0402, 0x0403, 0x201A, 0x0453, 0x201E, 0x2026, 0x2020, 0x2021, 0x20AC, 0x2030, 0x0409, 0x2039, 0x040A, 0x040C, 0x040B, 0x040F, 0x0452, 0x2018, 0x2019, 0x201C, 0x201D, 0x2022, 0x2013, 0x2014, 0x0000, 0x2122, 0x0459, 0x203A, 0x045A, 0x045C, 0x045B, 0x045F, 0x00A0, 0x040E, 0x045E, 0x0408, 0x00A4, 0x0490, 0x00A6, 0x00A7, 0x0401, 0x00A9, 0x0404, 0x00AB, 0x00AC, 0x00AD, 0x00AE, 0x0407, 0x00B0, 0x00B1, 0x0406, 0x0456, 0x0491, 0x00B5, 0x00B6, 0x00B7, 0x0451, 0x2116, 0x0454, 0x00BB, 0x0458, 0x0405, 0x0455, 0x0457]
        for i in range(0x40):
            FiasHelper.__m_1251_utf[i + 0x80] = m_1251_80_bf[i]
            FiasHelper.__m_utf_1251[m_1251_80_bf[i]] = (i + 0x80)
        for i in range(0x20):
            FiasHelper.__m_1251_utf[i + 0xC0] = ((ord('А')) + i)
            FiasHelper.__m_utf_1251[(ord('А')) + i] = (i + 0xC0)
        for i in range(0x20):
            FiasHelper.__m_1251_utf[i + 0xE0] = ((ord('а')) + i)
            FiasHelper.__m_utf_1251[(ord('а')) + i] = (i + 0xE0)

FiasHelper._static_ctor()