# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils

from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.address.internal.NumberItemClass import NumberItemClass

class NumberItem:
    
    def __init__(self) -> None:
        self.cla = NumberItemClass.UNDEFINED
        self.value = None;
        self.typ = None;
        self.slash = False
        self.can_be_flat = False
        self.can_absent = False
        self.twix = None;
    
    def __str__(self) -> str:
        return "{0} ({1}): {2}{3}{4}{5}".format(Utils.ifNotNull(self.typ, "?"), Utils.enumToString(self.cla), Utils.ifNotNull(self.value, ""), (" (after slash)" if self.slash else ""), (" (flat?)" if self.can_be_flat else ""), ("(?)" if self.can_absent else ""))
    
    def equal_coef(self, it : 'NumberItem') -> float:
        if (self.cla != it.cla and self.cla != NumberItemClass.UNDEFINED): 
            if (self.cla == NumberItemClass.FLAT and it.cla == NumberItemClass.SPACE): 
                pass
            elif (self.cla == NumberItemClass.SPACE and it.cla == NumberItemClass.FLAT): 
                pass
            else: 
                return 0
        res = 0
        if (self.value != it.value): 
            if (self.value == "1" and it.value == "А"): 
                res += 0.1
            elif (self.value == "А" and it.value == "1"): 
                res += 0.1
            else: 
                return 0
        else: 
            res += (1)
        if (self.typ != it.typ or self.typ is None): 
            res /= (2)
            if (it.can_absent or self.can_absent): 
                pass
            elif (self.cla == NumberItemClass.UNDEFINED): 
                if (it.cla == NumberItemClass.PLOT): 
                    res *= 0.3
                elif (it.cla != NumberItemClass.HOUSE): 
                    return 0
        return res
    
    @staticmethod
    def parse(val : str, typ_ : str, cla_ : 'NumberItemClass') -> typing.List['NumberItem']:
        if (Utils.isNullOrEmpty(val)): 
            val = "0"
        if (Utils.compareStrings(val, "Б/Н", True) == 0): 
            val = "0"
        res = list()
        i = 0
        first_pass3297 = True
        while True:
            if first_pass3297: first_pass3297 = False
            else: i += 1
            if (not (i < len(val))): break
            ch = val[i]
            if (not str.isalnum(ch)): 
                continue
            dig = str.isdigit(ch)
            j = 0
            j = (i + 1)
            while j < len(val): 
                if (dig != str.isdigit(val[j])): 
                    break
                j += 1
            num = NumberItem()
            if (i == 0 and j == len(val)): 
                num.value = val
            else: 
                num.value = val[i:i+j - i]
                while len(num.value) > 1 and num.value[0] == '0':
                    num.value = num.value[1:]
            if (not dig): 
                num.value = num.value.upper()
                if ((ord(num.value[0])) < 0x80): 
                    tmp = io.StringIO()
                    print(num.value, end="", file=tmp)
                    k = 0
                    while k < tmp.tell(): 
                        ch = LanguageHelper.get_cyr_for_lat(Utils.getCharAtStringIO(tmp, k))
                        if (ch != (chr(0))): 
                            Utils.setCharAtStringIO(tmp, k, ch)
                        k += 1
                    num.value = Utils.toStringStringIO(tmp)
            if (i > 0 and ((val[i - 1] == '/' or val[i - 1] == '\\'))): 
                num.slash = True
            res.append(num)
            i = (j - 1)
        if (typ_ is not None and len(res) > 0 and res[0].typ is None): 
            res[0].typ = typ_
        for r in res: 
            r.cla = cla_
        return res