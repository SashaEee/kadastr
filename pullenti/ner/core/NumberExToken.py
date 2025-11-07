# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.NumberToken import NumberToken
from pullenti.ner.core.NumberExType import NumberExType

class NumberExToken(NumberToken):
    # Число с стандартный постфиксом (мерой длины, вес, деньги и т.п.)
    # Устарело, вместо этого лучше использовать MeasureReferent или NumbersWithUnitToken
    
    def __init__(self, begin : 'Token', end : 'Token', val : str, typ_ : 'NumberSpellingType', ex_typ_ : 'NumberExType'=NumberExType.UNDEFINED) -> None:
        super().__init__(begin, end, val, typ_, None)
        self.alt_real_value = 0
        self.alt_rest_money = 0
        self.ex_typ = NumberExType.UNDEFINED
        self.ex_typ2 = NumberExType.UNDEFINED
        self.ex_typ_param = None;
        self.mult_after = False
        self.ex_typ = ex_typ_
    
    def normalize_value(self, ty : 'NumberExType') -> float:
        val = self.real_value
        ety = self.ex_typ
        if (ty.value == ety): 
            return val
        if (self.ex_typ2 != NumberExType.UNDEFINED): 
            return val
        if (ty.value == NumberExType.GRAMM): 
            if (self.ex_typ == NumberExType.KILOGRAM): 
                val *= (1000)
                ety = ty.value
            elif (self.ex_typ == NumberExType.MILLIGRAM): 
                val /= (1000)
                ety = ty.value
            elif (self.ex_typ == NumberExType.TONNA): 
                val *= (1000000)
                ety = ty.value
        elif (ty.value == NumberExType.KILOGRAM): 
            if (self.ex_typ == NumberExType.GRAMM): 
                val /= (1000)
                ety = ty.value
            elif (self.ex_typ == NumberExType.TONNA): 
                val *= (1000)
                ety = ty.value
        elif (ty.value == NumberExType.TONNA): 
            if (self.ex_typ == NumberExType.KILOGRAM): 
                val /= (1000)
                ety = ty.value
            elif (self.ex_typ == NumberExType.GRAMM): 
                val /= (1000000)
                ety = ty.value
        elif (ty.value == NumberExType.MILLIMETER): 
            if (self.ex_typ == NumberExType.SANTIMETER): 
                val *= (10)
                ety = ty.value
            elif (self.ex_typ == NumberExType.METER): 
                val *= (1000)
                ety = ty.value
        elif (ty.value == NumberExType.SANTIMETER): 
            if (self.ex_typ == NumberExType.MILLIMETER): 
                val *= (10)
                ety = ty.value
            elif (self.ex_typ == NumberExType.METER): 
                val *= (100)
                ety = ty.value
        elif (ty.value == NumberExType.METER): 
            if (self.ex_typ == NumberExType.KILOMETER): 
                val *= (1000)
                ety = ty.value
        elif (ty.value == NumberExType.LITR): 
            if (self.ex_typ == NumberExType.MILLILITR): 
                val /= (1000)
                ety = ty.value
        elif (ty.value == NumberExType.MILLILITR): 
            if (self.ex_typ == NumberExType.LITR): 
                val *= (1000)
                ety = ty.value
        elif (ty.value == NumberExType.GEKTAR): 
            if (self.ex_typ == NumberExType.METER2): 
                val /= (10000)
                ety = ty.value
            elif (self.ex_typ == NumberExType.AR): 
                val /= (100)
                ety = ty.value
            elif (self.ex_typ == NumberExType.KILOMETER2): 
                val *= (100)
                ety = ty.value
        elif (ty.value == NumberExType.KILOMETER2): 
            if (self.ex_typ == NumberExType.GEKTAR): 
                val /= (100)
                ety = ty.value
            elif (self.ex_typ == NumberExType.AR): 
                val /= (10000)
                ety = ty.value
            elif (self.ex_typ == NumberExType.METER2): 
                val /= (1000000)
                ety = ty.value
        elif (ty.value == NumberExType.METER2): 
            if (self.ex_typ == NumberExType.AR): 
                val *= (100)
                ety = ty.value
            elif (self.ex_typ == NumberExType.GEKTAR): 
                val *= (10000)
                ety = ty.value
            elif (self.ex_typ == NumberExType.KILOMETER2): 
                val *= (1000000)
                ety = ty.value
        elif (ty.value == NumberExType.DAY): 
            if (self.ex_typ == NumberExType.YEAR): 
                val *= (365)
                ety = ty.value
            elif (self.ex_typ == NumberExType.MONTH): 
                val *= (30)
                ety = ty.value
            elif (self.ex_typ == NumberExType.WEEK): 
                val *= (7)
                ety = ty.value
        ty.value = ety
        return val
    
    @staticmethod
    def ex_typ_to_string(ty : 'NumberExType', ty2 : 'NumberExType'=NumberExType.UNDEFINED) -> str:
        from pullenti.ner.core.internal.NumberExHelper import NumberExHelper
        if (ty2 != NumberExType.UNDEFINED): 
            return "{0}/{1}".format(NumberExToken.ex_typ_to_string(ty, NumberExType.UNDEFINED), NumberExToken.ex_typ_to_string(ty2, NumberExType.UNDEFINED))
        res = None
        wrapres938 = RefOutArgWrapper(None)
        inoutres939 = Utils.tryGetValue(NumberExHelper._m_normals_typs, ty, wrapres938)
        res = wrapres938.value
        if (inoutres939): 
            return res
        return "?"
    
    def __str__(self) -> str:
        return "{0}{1}".format(self.real_value, Utils.ifNotNull(self.ex_typ_param, NumberExToken.ex_typ_to_string(self.ex_typ, self.ex_typ2)))
    
    @staticmethod
    def _new834(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : float, _arg7 : 'MorphCollection') -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.alt_real_value = _arg6
        res.morph = _arg7
        return res
    
    @staticmethod
    def _new835(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : 'MorphCollection') -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.morph = _arg6
        return res
    
    @staticmethod
    def _new836(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : float, _arg7 : bool, _arg8 : float, _arg9 : 'MorphCollection') -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.real_value = _arg6
        res.is_real = _arg7
        res.alt_real_value = _arg8
        res.morph = _arg9
        return res
    
    @staticmethod
    def _new837(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : float, _arg7 : float, _arg8 : bool, _arg9 : str) -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.real_value = _arg6
        res.alt_real_value = _arg7
        res.is_real = _arg8
        res.ex_typ_param = _arg9
        return res
    
    @staticmethod
    def _new839(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : float, _arg7 : float, _arg8 : bool, _arg9 : 'MorphCollection', _arg10 : str) -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.real_value = _arg6
        res.alt_real_value = _arg7
        res.is_real = _arg8
        res.morph = _arg9
        res.ex_typ_param = _arg10
        return res
    
    @staticmethod
    def _new840(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : float, _arg7 : float, _arg8 : bool, _arg9 : 'MorphCollection') -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.real_value = _arg6
        res.alt_real_value = _arg7
        res.is_real = _arg8
        res.morph = _arg9
        return res
    
    @staticmethod
    def _new841(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : float, _arg7 : float, _arg8 : str) -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.real_value = _arg6
        res.alt_real_value = _arg7
        res.ex_typ_param = _arg8
        return res
    
    @staticmethod
    def _new842(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : float, _arg7 : float, _arg8 : 'NumberExType', _arg9 : str) -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.real_value = _arg6
        res.alt_real_value = _arg7
        res.ex_typ2 = _arg8
        res.ex_typ_param = _arg9
        return res
    
    @staticmethod
    def _new843(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : float, _arg7 : float, _arg8 : bool) -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.real_value = _arg6
        res.alt_real_value = _arg7
        res.mult_after = _arg8
        return res
    
    @staticmethod
    def _new844(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : object) -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.tag = _arg6
        return res
    
    @staticmethod
    def _new845(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : str) -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.ex_typ_param = _arg6
        return res
    
    @staticmethod
    def _new961(_arg1 : 'Token', _arg2 : 'Token', _arg3 : str, _arg4 : 'NumberSpellingType', _arg5 : 'NumberExType', _arg6 : float, _arg7 : bool) -> 'NumberExToken':
        res = NumberExToken(_arg1, _arg2, _arg3, _arg4, _arg5)
        res.real_value = _arg6
        res.is_real = _arg7
        return res