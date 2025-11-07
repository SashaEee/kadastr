# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.address.internal.PullentiAddressInternalResourceHelper import PullentiAddressInternalResourceHelper
from pullenti.address.internal.AbbrTreeNode import AbbrTreeNode
from pullenti.ner.address.internal.StreetItemType import StreetItemType
from pullenti.address.BaseAttributes import BaseAttributes
from pullenti.morph.LanguageHelper import LanguageHelper
from pullenti.address.AddrLevel import AddrLevel
from pullenti.address.AreaAttributes import AreaAttributes
from pullenti.address.AddrObject import AddrObject
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.address.internal.StreetItemToken import StreetItemToken
from pullenti.address.internal.RegionHelper import RegionHelper
from pullenti.ner.SourceOfAnalysis import SourceOfAnalysis
from pullenti.ner.geo.internal.CityItemToken import CityItemToken
from pullenti.ner.address.internal.AddressItemToken import AddressItemToken

class CorrectionHelper:
    
    @staticmethod
    def correct(txt : str, has_def_object : bool, details : str) -> typing.List[str]:
        details.value = (None)
        res = list()
        tmp = io.StringIO()
        print(txt.strip(), end="", file=tmp)
        while tmp.tell() > 0:
            if (not str.isalnum(Utils.getCharAtStringIO(tmp, 0)) and Utils.getCharAtStringIO(tmp, 0) != '"'): 
                Utils.removeStringIO(tmp, 0, 1)
            else: 
                break
        i = 0
        while i < tmp.tell(): 
            if (LanguageHelper.is_hiphen(Utils.getCharAtStringIO(tmp, i)) or Utils.getCharAtStringIO(tmp, i) == '_' or Utils.getCharAtStringIO(tmp, i) == '*'): 
                Utils.setCharAtStringIO(tmp, i, '-')
            if (Utils.getCharAtStringIO(tmp, i) == '\t'): 
                Utils.setCharAtStringIO(tmp, i, ' ')
            if (Utils.getCharAtStringIO(tmp, i) == '\\' and ((i + 1) < tmp.tell())): 
                if (Utils.getCharAtStringIO(tmp, i + 1) == '"'): 
                    Utils.removeStringIO(tmp, i, 1)
            i += 1
        if (tmp.tell() > 1 and Utils.getCharAtStringIO(tmp, 0) == '"' and Utils.getCharAtStringIO(tmp, tmp.tell() - 1) == '"'): 
            Utils.removeStringIO(tmp, 0, 1)
            Utils.setLengthStringIO(tmp, tmp.tell() - 1)
        if (tmp.tell() > 0 and Utils.getCharAtStringIO(tmp, tmp.tell() - 1) == ';'): 
            Utils.setLengthStringIO(tmp, tmp.tell() - 1)
        i = 0
        first_pass3277 = True
        while True:
            if first_pass3277: first_pass3277 = False
            else: i += 1
            if (not (i < (tmp.tell() - 1))): break
            if (Utils.getCharAtStringIO(tmp, i) == Utils.getCharAtStringIO(tmp, i + 1) and not str.isalnum(Utils.getCharAtStringIO(tmp, i))): 
                cou1 = 1
                j = i + 2
                while j < tmp.tell(): 
                    if (Utils.getCharAtStringIO(tmp, j) != Utils.getCharAtStringIO(tmp, i)): 
                        break
                    j += 1; cou1 += 1
                if (cou1 == 1 and ((Utils.getCharAtStringIO(tmp, i) == ',' or Utils.getCharAtStringIO(tmp, i) == '.'))): 
                    continue
                Utils.removeStringIO(tmp, i + 1, cou1)
                i -= 1
        i = 0
        while i < (tmp.tell() - 3): 
            if (Utils.getCharAtStringIO(tmp, i) == ' ' and Utils.getCharAtStringIO(tmp, i + 1) == '-' and Utils.getCharAtStringIO(tmp, i + 2) == ' '): 
                Utils.removeStringIO(tmp, i + 1, 2)
                Utils.setCharAtStringIO(tmp, i, '-')
            i += 1
        txt = Utils.toStringStringIO(tmp).strip()
        if ("областьг" in txt): 
            txt = txt.replace("областьг", "область г")
        if ("снт Тверь" in txt): 
            txt = txt.replace("снт Тверь", "г.Тверь")
        if ("Санкт-Петербур " in txt): 
            txt = txt.replace("Санкт-Петербур ", "Санкт-Петербург ")
        txt = txt.replace("кл-ще", "кладбище")
        txt = txt.replace("областьасть", "область")
        txt = txt.replace("ж/д_ст", "железнодорожная станция")
        if (txt.endswith("д., , ,")): 
            txt = txt[0:0+len(txt) - 7].strip()
        if (Utils.startsWithString(txt, "НЕТ,", True)): 
            txt = txt[4:].strip()
        if (Utils.startsWithString(txt, "СУБЪЕКТ", True)): 
            txt = txt[7:].strip()
        if (Utils.startsWithString(txt, "ФЕДЕРАЦИЯ.", True)): 
            txt = "{0} {1}".format(txt[0:0+9], txt[10:])
        i0 = 0
        if (Utils.startsWithString(txt, "РОССИЯ", True)): 
            i0 = 6
        elif (Utils.startsWithString(txt, "РФ", True)): 
            i0 = 2
        elif (Utils.startsWithString(txt, "RU", True)): 
            i0 = 2
        elif (Utils.startsWithString(txt, "РСФСР", True)): 
            i0 = 5
        elif (Utils.startsWithString(txt, "СССР", True)): 
            i0 = 4
        elif (Utils.startsWithString(txt, "Р.Ф.", True)): 
            i0 = 4
        elif (Utils.startsWithString(txt, "г. Москва и Московская область", True)): 
            i0 = 30
            txt1 = txt[i0:]
            if ("Москва" in txt1 or "Москов" in txt1): 
                pass
            else: 
                i0 = 12
        elif (Utils.startsWithString(txt, "г. Санкт-Петербург и Ленинградская область", True)): 
            i0 = 42
        if (i0 > 0 and ((i0 + 1) < len(txt)) and ((not str.isalpha(txt[i0]) or ((ord(txt[i0 - 1])) < 0x80)))): 
            while i0 < len(txt): 
                if (str.isalpha(txt[i0])): 
                    if (txt[i0] == 'О' and str.isdigit(txt[i0 - 1])): 
                        for k in range(i0 - 1, 0, -1):
                            if (str.isdigit(txt[k])): 
                                i0 = k
                            else: 
                                break
                    txt = txt[i0:]
                    break
                i0 += 1
        if (Utils.startsWithString(txt, "МО", True) and len(txt) > 3): 
            if (txt[2] == ' ' or txt[2] == ','): 
                txt = ("Московская область" + txt[2:])
        if (((Utils.startsWithString(txt, "М\\О", True) or ((Utils.startsWithString(txt, "М/О", True))))) and len(txt) > 3): 
            txt = ("Московская область " + txt[3:])
        i = 0
        while i < len(txt): 
            if (CorrectionHelper.__is_start_of(txt, i, "УССР", False) and ((i == 0 or not str.isalpha(txt[i - 1])))): 
                txt = "{0}, Украина {1}".format(("" if i == 0 else txt[0:0+i]), (txt[i + 4:] if (i + 4) < len(txt) else ""))
                break
            elif (i >= 2 and CorrectionHelper.__is_start_of(txt, i, "ССР", False)): 
                for kk in range(2):
                    del0_ = (',' if kk == 0 else ' ')
                    j = i - 1
                    while j > 0: 
                        if (txt[j] != ' ' and txt[j] != '.'): 
                            break
                        j -= 1
                    while j >= 0: 
                        if (txt[j] == del0_ or txt[j] == '.'): 
                            break
                        j -= 1
                    if (j < 0): 
                        reg = CorrectionHelper.__calc_su_reg(txt[0:0+i].upper(), i)
                        if (reg is not None): 
                            if (Utils.isNullOrEmpty(reg) and kk > 0): 
                                continue
                            jjj = reg.find('+')
                            if (jjj < 0): 
                                txt = "{0}, {1}".format(reg, txt[i + 3:])
                            else: 
                                res.append("{0}, {1}".format(reg[jjj + 1:], txt[i + 3:]))
                                txt = "{0}, {1}".format(reg[jjj:], txt[i + 3:])
                            i = 0
                            break
                    else: 
                        j += 1
                        reg = CorrectionHelper.__calc_su_reg(txt[j:j+i - j].upper().strip(), i)
                        if (reg is not None): 
                            if (Utils.isNullOrEmpty(reg) and kk > 0): 
                                continue
                            jjj = reg.find('+')
                            if (jjj < 0): 
                                txt = "{0}, {1}, {2}".format(txt[0:0+j], reg, txt[i + 3:])
                            else: 
                                res.append("{0} {1}, {2}".format(txt[0:0+j], reg[jjj + 1:], txt[i + 3:]))
                                txt = "{0}, {1}, {2}".format(txt[0:0+j], reg[0:0+jjj], txt[i + 3:])
                            i = 0
                            break
            i += 1
        if (not has_def_object): 
            i = 0
            while i < len(txt): 
                if (txt[i] == ' ' or txt[i] == ','): 
                    if (i < 4): 
                        break
                    ppp = txt[0:0+i].upper()
                    countr = None
                    wrapcountr127 = RefOutArgWrapper(None)
                    inoutres128 = Utils.tryGetValue(CorrectionHelper.__m_cities, ppp, wrapcountr127)
                    countr = wrapcountr127.value
                    if (inoutres128): 
                        if (str(countr).upper() in txt.upper()): 
                            txt = ("г." + txt)
                        else: 
                            txt = "{0}, город {1}".format(str(countr), txt)
                    else: 
                        wrapcountr125 = RefOutArgWrapper(None)
                        inoutres126 = Utils.tryGetValue(CorrectionHelper.__m_regions, ppp, wrapcountr125)
                        countr = wrapcountr125.value
                        if (inoutres126): 
                            txt = "{0}, {1}".format(str(countr), txt)
                    break
                i += 1
        i = 0
        first_pass3278 = True
        while True:
            if first_pass3278: first_pass3278 = False
            else: i += 1
            if (not (i < len(txt))): break
            if (txt[i] == 'O' or txt[i] == 'О'): 
                ok = False
                if (i == 0 or not str.isdigit(txt[i - 1])): 
                    continue
                if ((i + 1) == len(txt)): 
                    ok = True
                elif (not str.isalpha(txt[i + 1])): 
                    ok = True
                elif (txt[i + 1] == txt[i]): 
                    if ((i + 2) == len(txt)): 
                        ok = True
                    elif (not str.isalpha(txt[i + 2])): 
                        ok = True
                    elif (txt[i + 2] == txt[i] or txt[i + 2] == 'А'): 
                        ok = True
                elif (txt[i + 1] == 'А'): 
                    ok = True
                if (ok): 
                    txt = "{0}0{1}".format(txt[0:0+i], txt[i + 1:])
        i = 1
        while i < (len(txt) - 1): 
            if (txt[i] == '%'): 
                txt = "{0}/{1}".format(txt[0:0+i], txt[i + 1:])
            i += 1
        i = 0
        while i < (len(txt) - 5): 
            if (txt[i] == 'у' and txt[i + 1] == 'л' and str.isupper(txt[i + 2])): 
                txt = "{0}.{1}".format(txt[0:0+i + 2], txt[i + 2:])
                break
            i += 1
        i = 0
        while i < (len(txt) - 5): 
            if ((str.isdigit(txt[i]) and str.isalpha(txt[i + 1]) and txt[i + 2] == 'к') and txt[i + 3] == 'в'): 
                txt = "{0} {1}".format(txt[0:0+i + 2], txt[i + 2:])
                break
            i += 1
        i = 10
        first_pass3279 = True
        while True:
            if first_pass3279: first_pass3279 = False
            else: i += 1
            if (not (i < (len(txt) - 3))): break
            if (txt[i - 1] == ' ' or txt[i - 1] == ','): 
                if (((CorrectionHelper.__is_start_of(txt, i, "паспорт", False) or CorrectionHelper.__is_start_of(txt, i, "выдан", False) or CorrectionHelper.__is_start_of(txt, i, "Выдан", False)) or CorrectionHelper.__is_start_of(txt, i, "серия", False) or CorrectionHelper.__is_start_of(txt, i, "док:", False)) or CorrectionHelper.__is_start_of(txt, i, "док.:", False)): 
                    txt = Utils.trimEndString(txt[0:0+i])
                    break
                elif (CorrectionHelper.__is_start_of(txt, i, "ОКАТО", False) and i >= (len(txt) - 20) and not str.isalpha(txt[i - 1])): 
                    if ((i + 5) == len(txt) or not str.isalpha(txt[i + 5])): 
                        txt = Utils.trimEndString(txt[0:0+i])
                        break
                elif (CorrectionHelper.__is_start_of(txt, i, "адрес ориентира:", False)): 
                    details.value = txt[0:0+i]
                    txt = txt[i + 16:].strip()
                    i = 0
                elif ((CorrectionHelper.__is_start_of(txt, i, "ОВД", False) or CorrectionHelper.__is_start_of(txt, i, "УВД", False) or CorrectionHelper.__is_start_of(txt, i, "РОВД", False)) or CorrectionHelper.__is_start_of(txt, i, "ГОВД", False)): 
                    if (i > 0 and str.isalpha(txt[i])): 
                        continue
                    jj = i + 3
                    if (((jj + 1) < len(txt)) and txt[jj] == 'Д'): 
                        jj += 1
                    if ((jj + 1) < len(txt)): 
                        if (str.isalpha(txt[jj])): 
                            continue
                    kk = 0
                    br = False
                    kk = 10
                    while kk < (i - 2): 
                        if (CorrectionHelper.__is_start_of(txt, kk, "кв", False) or CorrectionHelper.__is_start_of(txt, kk, "Кв", False)): 
                            if (txt[kk + 2] == '.' or txt[kk + 2] == ' '): 
                                kk += 2
                                while kk < (i - 2): 
                                    if (txt[kk] != ' ' and txt[kk] != '.'): 
                                        break
                                    kk += 1
                                if (str.isdigit(txt[kk])): 
                                    while kk < i: 
                                        if (not str.isdigit(txt[kk])): 
                                            break
                                        kk += 1
                                    txt = txt[0:0+kk]
                                    br = True
                                break
                        kk += 1
                    if (br): 
                        break
                    j = i - 2
                    sp = 0
                    while j > 0: 
                        if (txt[j] == ' ' and txt[j - 1] != ' '): 
                            sp += 1
                            if (sp >= 4): 
                                break
                        j -= 1
                    if (j > 10 and sp == 4): 
                        txt = Utils.trimEndString(txt[0:0+j])
                        break
        txt0 = txt.upper()
        i = 0
        first_pass3280 = True
        while True:
            if first_pass3280: first_pass3280 = False
            else: i += 1
            if (not (i < len(txt0))): break
            if (txt0[i] == '\\' and (i + 20) > len(txt0)): 
                if (CorrectionHelper.__is_start_of(txt0, i, "\\РЕГИСТРАЦИ", False) or CorrectionHelper.__is_start_of(txt0, i, "\\ДОСТАВК", False) or CorrectionHelper.__is_start_of(txt0, i, "\\ПОЧТОВ", False)): 
                    txt = txt[0:0+i].strip()
                    txt0 = txt.upper()
                    break
            if (not str.isalpha(txt0[i])): 
                continue
            if (((i > 10 and str.isdigit(txt[i - 1]) and str.isupper(txt[i])) and ((i + 2) < len(txt)) and txt[i + 1] == 'к') and str.isdigit(txt[i + 2])): 
                txt = "{0} {1}".format(txt[0:0+i + 1], txt[i + 1:])
                txt0 = txt.upper()
                continue
            if (CorrectionHelper.__is_start_of(txt0, i, "ИЙР-Н", False)): 
                txt = "{0} {1}".format(txt[0:0+i + 2], txt[i + 2:])
                txt0 = txt.upper()
                continue
            if (CorrectionHelper.__is_start_of(txt0, i, "РНД", True)): 
                txt = "{0}Ростов-на-Дону {1}".format(txt[0:0+i], txt[i + 3:])
                txt0 = txt.upper()
                continue
            if (CorrectionHelper.__is_start_of(txt0, i, "АМЕТ-ХАН", True)): 
                txt = "{0} {1}".format(txt[0:0+i + 4], txt[i + 5:])
                txt0 = txt.upper()
                continue
            if (CorrectionHelper.__is_start_of(txt0, i, "РСО", True)): 
                n = 3
                if ((i + n + 2) <= len(txt) and ((txt[i + n] == '-' or txt[i + n] == '/')) and txt0[i + n + 1] == 'А'): 
                    n += 2
                txt = "{0}республика Северная Осетия {1}".format(txt[0:0+i], txt[i + n:])
                txt0 = txt.upper()
                continue
            if (CorrectionHelper.__is_start_of(txt0, i, "РС(Я)", False)): 
                txt = "{0}республика Саха (Якутия){1}".format(txt[0:0+i], txt[i + 5:])
                txt0 = txt.upper()
                continue
            if ((i < 20) and CorrectionHelper.__is_start_of(txt0, i, "ЧАО", False)): 
                txt = "{0}Чукотский автономный округ{1}".format(txt[0:0+i], txt[i + 3:])
                txt0 = txt.upper()
                continue
            if ((i < 20) and CorrectionHelper.__is_start_of(txt0, i, "ЕАО", False)): 
                txt = "{0}Еврейская автономная область{1}".format(txt[0:0+i], txt[i + 3:])
                txt0 = txt.upper()
                continue
            if ((i < 20) and CorrectionHelper.__is_start_of(txt0, i, "КЧР", False)): 
                txt = "{0}Карачаево-Черкессия{1}".format(txt[0:0+i], txt[i + 3:])
                txt0 = txt.upper()
                continue
            if (CorrectionHelper.__is_start_of(txt0, i, "КЧАО", False)): 
                txt = "{0}Карачаево-Черкессия{1}".format(txt[0:0+i], txt[i + 4:])
                txt0 = txt.upper()
                continue
            if ((i == 0 and CorrectionHelper.__is_start_of(txt0, i, "РУЗ", False) and ((i + 3) < len(txt))) and not str.isalpha(txt[i + 3])): 
                txt = "Узбекистан {0}".format(txt[i + 3:])
                txt0 = txt.upper()
                continue
            if (CorrectionHelper.__is_start_of(txt0, i, "РС (Я)", False)): 
                txt = "{0}республика Саха (Якутия){1}".format(txt[0:0+i], txt[i + 6:])
                txt0 = txt.upper()
                continue
            if (CorrectionHelper.__is_start_of(txt0, i, "СПБ", True)): 
                txt = "{0}Санкт-Петербург {1}".format(txt[0:0+i], txt[i + 3:])
                txt0 = txt.upper()
                continue
            if (CorrectionHelper.__is_start_of(txt0, i, "MOSCOW", True)): 
                txt = "{0}МОСКВА {1}".format(txt[0:0+i], txt[i + 6:])
                txt0 = txt.upper()
                continue
            if (CorrectionHelper.__is_start_of(txt0, i, "РОСТОВ", False) and ((i + 11) < len(txt))): 
                jj = i + 6
                if (txt[jj] == ' '): 
                    jj += 1
                if (txt0[jj] == 'Н' and ((txt0[jj + 1] == '/' or txt0[jj + 1] == '\\')) and txt[jj + 2] == 'Д'): 
                    txt = "{0}Ростов-на-Дону {1}".format(txt[0:0+i], txt[jj + 3:])
                    txt0 = txt.upper()
                    continue
            if (i > 5 and CorrectionHelper.__is_start_of(txt0, i, "УРАЛЬСК", False)): 
                jj = i - 1
                if (txt[jj] == ' '): 
                    jj -= 1
                if (txt[jj] == '-'): 
                    jj -= 1
                if (txt[jj] == ' '): 
                    jj -= 1
                if (jj > 3 and CorrectionHelper.__is_start_of(txt0, jj - 2, "КАМ", False)): 
                    jj -= 2
                elif (jj >= 0 and txt0[jj] == 'К' and ((jj == 0 or not str.isalpha(txt0[jj - 1])))): 
                    pass
                else: 
                    continue
                if (((i + 7) < len(txt)) and not str.isalpha(txt[i + 7])): 
                    txt = "{0}ИЙ{1}".format(txt[0:0+i + 7], txt[i + 7:])
                txt = "{0}Каменск-{1}".format(txt[0:0+jj], txt[i:])
                txt0 = txt.upper()
                continue
            if (CorrectionHelper.__is_start_of(txt0, i, "ВОРОШИЛОВГРАДСКАЯ О", False)): 
                txt = "{0}, Луганская {1}".format(txt[0:0+i], txt[i + 17:])
                txt0 = txt.upper()
                continue
            if (CorrectionHelper.__is_start_of(txt0, i, "СТАЛИНГРАДСКАЯ О", False)): 
                txt = "{0}, Волгоградская {1}".format(txt[0:0+i], txt[i + 14:])
                txt0 = txt.upper()
                continue
            if (CorrectionHelper.__is_start_of(txt0, i, "ДО ВОСТРЕБ", False) or CorrectionHelper.__is_start_of(txt0, i, "ЗАКЛЮЧЕННЫЙ", False)): 
                txt = txt[0:0+i].strip()
                txt0 = txt.upper()
                break
            if ((i < 30) and CorrectionHelper.__is_start_of(txt0, i, "ССР", False)): 
                reg = CorrectionHelper.__calc_su_reg(txt0[0:0+i], i)
                if (not Utils.isNullOrEmpty(reg)): 
                    jjj = reg.find('+')
                    if (jjj < 0): 
                        txt = "{0}, {1}".format(reg, txt[i + 3:])
                        txt0 = txt.upper()
                        i = 0
                        continue
                    else: 
                        res.append("{0}, {1}".format(reg[jjj + 1:], txt[i + 3:]))
                        txt = "{0}, {1}".format(reg[0:0+jjj], txt[i + 3:])
                        txt0 = txt.upper()
                        i = 0
                        continue
            if (i == 0 or txt[i - 1] == ',' or txt[i - 1] == ' '): 
                pass
            else: 
                continue
            if (CorrectionHelper.__is_start_of(txt0, i, "ХХХ", False) or CorrectionHelper.__is_start_of(txt0, i, "XXX", False)): 
                txt = (txt[0:0+i] + txt[i + 3:])
                txt0 = txt.upper()
                continue
            if (CorrectionHelper.__m_root is None): 
                continue
            tn = CorrectionHelper.__m_root.find(txt0, i)
            if (tn is None): 
                continue
            j = i + tn.len0_
            ok = False
            if (tn.len0_ == 2 and txt0[i] == 'У' and txt0[i + 1] == 'Л'): 
                continue
            if (tn.len0_ == 2 and txt0[i] == 'С' and txt0[i + 1] == 'Т'): 
                continue
            if ((tn.len0_ == 3 and txt0[i] == 'П' and txt0[i + 1] == 'Е') and txt0[i + 2] == 'Р'): 
                continue
            while j < len(txt0): 
                if (txt0[j] == '.' or txt0[j] == ' '): 
                    ok = True
                else: 
                    break
                j += 1
            if (j >= len(txt0) or not ok or tn.corrs is None): 
                continue
            for kp in tn.corrs.items(): 
                if (not CorrectionHelper.__is_start_of(txt0, j, kp[0], False)): 
                    continue
                if (tn.len0_ == 8 and CorrectionHelper.__is_start_of(txt0, i, "НОВГОРОД", False)): 
                    continue
                if (tn.len0_ == 2 and CorrectionHelper.__is_start_of(txt0, i, "ПР", False)): 
                    continue
                if (tn.len0_ == 2 and CorrectionHelper.__is_start_of(txt0, i, "КР", False)): 
                    continue
                tmp1 = Utils.newStringIO(txt)
                Utils.removeStringIO(tmp1, i, tn.len0_)
                if (Utils.getCharAtStringIO(tmp1, i) == '.'): 
                    Utils.removeStringIO(tmp1, i, 1)
                Utils.insertStringIO(tmp1, i, kp[1] + " ")
                txt = Utils.toStringStringIO(tmp1)
                txt0 = txt.upper()
                break
        i = 0
        first_pass3281 = True
        while True:
            if first_pass3281: first_pass3281 = False
            else: i += 1
            if (not ((i < len(txt)) and (i < 20))): break
            if (not str.isalpha(txt[i]) and txt[i] != '-'): 
                city = txt[0:0+i]
                if (RegionHelper.is_big_city(city) is None): 
                    continue
                if (city.endswith("Й")): 
                    continue
                ok = False
                j = 0
                j = i
                first_pass3282 = True
                while True:
                    if first_pass3282: first_pass3282 = False
                    else: j += 1
                    if (not (j < len(txt))): break
                    if (Utils.isWhitespace(txt[j])): 
                        continue
                    if (txt[j] == 'г' or txt[j] == 'Г'): 
                        ok = True
                    break
                if (ok): 
                    break
                if ((j < len(txt)) and txt[j] == ','): 
                    j += 1
                if (j < len(txt)): 
                    ar0 = ProcessorService.get_empty_processor().process(SourceOfAnalysis._new129(txt[j:], "ADDRESS"), None, None)
                    cits = CityItemToken.try_parse_list(ar0.first_token, 2, None)
                    if (cits is not None and len(cits) == 1 and cits[0].typ == CityItemToken.ItemType.NOUN): 
                        break
                    if (AddressItemToken.check_house_after(ar0.first_token, True, False)): 
                        break
                    if (has_def_object): 
                        st = StreetItemToken.try_parse(ar0.first_token, None, False, None)
                        if (st is not None and st.typ == StreetItemType.NOUN): 
                            break
                txt = "г.{0},{1}".format(txt[0:0+i], txt[i:])
                break
        i = 0
        first_pass3283 = True
        while True:
            if first_pass3283: first_pass3283 = False
            else: i += 1
            if (not (i < len(txt))): break
            if (txt[i] == ' '): 
                if (CorrectionHelper.__is_start_of(txt, i + 1, "филиал", False) or CorrectionHelper.__is_start_of(txt, i + 1, "ФИЛИАЛ", False)): 
                    reg = txt[0:0+i]
                    city = None
                    if (CorrectionHelper.__m_root is None): 
                        continue
                    tn = CorrectionHelper.__m_root.find(reg.upper(), 0)
                    if (tn is not None and tn.corrs is not None): 
                        for kp in tn.corrs.items(): 
                            if (kp[0] == "ОБ"): 
                                nam = kp[1]
                                reg = (nam + " область")
                                r = RegionHelper.find_region_by_adj(nam)
                                if (r is not None and r.capital is not None): 
                                    city = r.capital
                                break
                    if (city is not None): 
                        res.append("г.{0}, {1}".format(city, txt[i + 7:]))
                    txt1 = "{0}, {1}".format(reg, txt[i + 7:])
                    txt = txt1
                break
        txt0 = txt.upper()
        if (CorrectionHelper.__is_start_of(txt0, 0, "ФИЛИАЛ ", False)): 
            txt = txt[7:]
        if (len(txt) > 10 and txt[0] == 'г' and txt[1] == ','): 
            txt = ("г." + txt[2:])
        if (len(txt) < 1): 
            return None
        if (str.isalpha(txt[len(txt) - 1])): 
            for i in range(len(txt) - 7, 10, -1):
                if (str.isalpha(txt[i])): 
                    if (txt[i - 1] == '.' and str.isupper(txt[i]) and (ord(txt[i])) > 0x80): 
                        if (txt[i + 1] == '.'): 
                            continue
                        if (str.isupper(txt[i - 2])): 
                            continue
                        has_cap = False
                        for j in range(i - 3, 10, -1):
                            if (txt[j] == ','): 
                                p0 = txt[0:0+j + 1]
                                p1 = txt[i:]
                                p2 = txt[j + 1:j + 1+i - j - 2]
                                if (len(p2) > 4): 
                                    txt = "{0}{1},{2}".format(p0, p1, p2)
                                break
                            elif (not has_cap and not str.isalpha(txt[j]) and str.isalpha(txt[j + 1])): 
                                if (not str.isupper(txt[j + 1])): 
                                    break
                                has_cap = True
                        break
                else: 
                    break
        i = 1
        first_pass3284 = True
        while True:
            if first_pass3284: first_pass3284 = False
            else: i += 1
            if (not (i < (len(txt) - 1))): break
            if (((txt[i] == 'г' or txt[i] == 'Г')) and str.isalpha(txt[i - 1]) and ((txt[i + 1] == ' ' or txt[i + 1] == '.'))): 
                if (txt[i - 1] == 'У' or txt[i - 1] == 'у'): 
                    continue
                res.append("{0} г,{1}".format(txt[0:0+i], txt[i + 1:]))
                res.append("{0}, г {1}".format(txt[0:0+i], txt[i + 1:]))
                break
        i = 1
        first_pass3285 = True
        while True:
            if first_pass3285: first_pass3285 = False
            else: i += 1
            if (not (i < (len(txt) - 2))): break
            if ((((txt[i] == 'y' or txt[i] == 'У')) and ((txt[i + 1] == 'л' or txt[i + 1] == 'Л')) and str.isalpha(txt[i - 1])) and ((txt[i + 2] == ' ' or txt[i + 2] == '.' or txt[i + 2] == ','))): 
                if (txt[i - 1] == 'А' or txt[i - 1] == 'а'): 
                    continue
                res.append("{0} {1}".format(txt[0:0+i], txt[i:]))
                break
        i = 1
        first_pass3286 = True
        while True:
            if first_pass3286: first_pass3286 = False
            else: i += 1
            if (not (i < (len(txt) - 2))): break
            if (((((txt[i] == 'y' or txt[i] == 'У')) and ((txt[i + 1] == 'л' or txt[i + 1] == 'Л')) and not str.isalpha(txt[i - 1])) and str.isalpha(txt[i + 2]) and txt[i + 2] != 'Ь') and txt[i + 2] != 'ь'): 
                if (str.islower(txt[i + 2])): 
                    continue
                res.append("{0}. {1}".format(txt[0:0+i + 2], txt[i + 2:]))
                break
        cou = 0
        i = len(txt) - 2
        first_pass3287 = True
        while True:
            if first_pass3287: first_pass3287 = False
            else: i -= 1
            if (not (i > 0 and (cou < 5))): break
            if (str.isalpha(txt[i])): 
                cou += 1
                continue
            cou = 0
            if (txt[i] != ' '): 
                continue
            if (str.isalpha(txt[i - 1]) and str.isdigit(txt[i + 1])): 
                pass
            else: 
                continue
            for j in range(i - 1, 0, -1):
                if (not str.isalpha(txt[j])): 
                    break
                else: 
                    cou += 1
            if (cou > 4): 
                res.append("{0},{1}".format(txt[0:0+i], txt[i:]))
            cou = 0
        if (len(txt) > 20 and str.isdigit(txt[0])): 
            ppp = list(Utils.splitString(txt, ',', False))
            for i in range(len(ppp) - 1, -1, -1):
                if (Utils.isNullOrEmpty(ppp[i])): 
                    del ppp[i]
            i = 0
            first_pass3288 = True
            while True:
                if first_pass3288: first_pass3288 = False
                else: i += 1
                if (not (i < (len(ppp) - 1))): break
                reg = ppp[i]
                if (not str.isdigit(reg[0])): 
                    break
                if (not str.isalpha(ppp[i + 1][0])): 
                    continue
                if (len(reg) > 2): 
                    break
                if (i == 0 or len(ppp[i - 1]) == 6): 
                    pass
                else: 
                    break
                if (reg[0] == '0'): 
                    reg = reg[1:]
                rr = 0
                wraprr132 = RefOutArgWrapper(0)
                inoutres133 = Utils.tryParseInt(reg, wraprr132)
                rr = wraprr132.value
                if (not inoutres133): 
                    break
                ri = None
                wrapri130 = RefOutArgWrapper(None)
                inoutres131 = Utils.tryGetValue(RegionHelper.REGIONS_BY_CODE, rr, wrapri130)
                ri = wrapri130.value
                if (not inoutres131): 
                    break
                Utils.setLengthStringIO(tmp, 0)
                j = 0
                while j < i: 
                    print("{0}, ".format(ppp[j]), end="", file=tmp, flush=True)
                    j += 1
                print(str(ri.attrs), end="", file=tmp)
                j = i + 1
                while j < len(ppp): 
                    print(", {0}".format(ppp[j]), end="", file=tmp, flush=True)
                    j += 1
                res.append(Utils.toStringStringIO(tmp))
                break
        res.insert(0, txt)
        return res
    
    @staticmethod
    def __is_start_of(txt : str, i : int, sub : str, check_non_let_surr : bool=False) -> bool:
        no_casesens = False
        if (i > 0 and txt[i - 1] == ' '): 
            no_casesens = True
        j = 0
        while j < len(sub): 
            if ((i + j) >= len(txt)): 
                return False
            elif (sub[j] == txt[i + j]): 
                pass
            elif (no_casesens and str.upper(sub[j]) == str.upper(txt[i + j])): 
                pass
            else: 
                return False
            j += 1
        if (check_non_let_surr): 
            if (i > 0 and str.isalpha(txt[i - 1])): 
                return False
            if (((i + len(sub)) < len(txt)) and str.isalpha(txt[i + len(sub)])): 
                return False
        return True
    
    @staticmethod
    def __calc_su_reg(str0_ : str, i : int) -> str:
        hasa = False
        if (str0_.endswith("А") or str0_.endswith("A")): 
            hasa = True
            str0_ = str0_[0:0+len(str0_) - 1]
        if (str0_.endswith(".")): 
            str0_ = str0_[0:0+len(str0_) - 1]
        str0_ = str0_.strip()
        has_sp = str0_.find(' ') > 0 or str0_.find(',') > 0
        if (str0_ == "М" or str0_.startswith("МОЛ")): 
            return "Молдавия"
        if (str0_.startswith("МАР")): 
            return "Марий Эл"
        if (str0_ == "Б" and hasa): 
            return "Башкортостан"
        if (((str0_ == "Т" and hasa)) or str0_.startswith("ТАТ")): 
            return "Татарстан"
        if (str0_.startswith("КАРАКАЛ")): 
            return ("республика Каракалпакстан, Узбекистан" if i > 30 else "Узбекистан, республика Каракалпакстан")
        if (((str0_.startswith("КАР") and not has_sp)) or ((str0_ == "К" and hasa))): 
            return "Карелия"
        if (str0_.startswith("КАЛ") and not has_sp): 
            return "Калмыкия"
        if (str0_.startswith("БАШ") and not has_sp): 
            return "Башкирия"
        if (str0_.startswith("БУР") and not has_sp): 
            return "Бурятия"
        if (str0_.startswith("КАЗ") and not has_sp): 
            return "Казахстан"
        if (str0_ == "КБ"): 
            return "Кабардино-Балкария"
        if (str0_ == "ЧИ" or str0_.startswith("ЧЕЧЕНО-ИНГ")): 
            return "Чечня+Ингушетия"
        if (str0_.startswith("ЯК") and not has_sp): 
            return "Якутия"
        if (str0_.startswith("ЧУВ") and not has_sp): 
            return "Чувашия"
        if (str0_ == "Ч"): 
            return "Чувашия+Чехия"
        if (str0_.startswith("АРМ") and not has_sp): 
            return "Армения"
        if (str0_.startswith("АЗ") and not has_sp): 
            return "Азербайджан"
        if (str0_ == "Г" or ((str0_.startswith("ГР") and not has_sp))): 
            return "Грузия"
        if (str0_.startswith("УЗ") and not has_sp): 
            return "Узбекистан"
        if (has_sp): 
            return None
        if (str0_.startswith("Э")): 
            return "Эстония"
        if (str0_.startswith("ЛАТ")): 
            return "Латвия"
        if (str0_.startswith("ЛИТ")): 
            return "Литва"
        if (str0_.startswith("БЕЛ") or str0_ == "Б"): 
            return "Белоруссия"
        if (str0_.startswith("УК")): 
            return "Украина"
        if (str0_ == "У"): 
            return ("Удмуртия+Украина" if hasa else "Украина")
        if (str0_.startswith("ТУР")): 
            return "Туркмения"
        if (str0_.startswith("ТАДЖ")): 
            return "Таджикистан"
        if (str0_.startswith("МОР")): 
            return "Мордовия"
        if (str0_.startswith("КИР")): 
            return "Киргизия"
        if (str0_.startswith("УД")): 
            return "Удмуртия"
        if (str0_.startswith("ЧЕХ")): 
            return "Чехословакия"
        if (str0_.startswith("АБХ")): 
            return "Грузия, Абхазская область"
        if (str0_.startswith("АДЖАР")): 
            return "Грузия, Аджарская область"
        if (str0_.startswith("ДАГ") or ((str0_ == "Д" and hasa))): 
            return "Дагестан"
        if (str0_ == "КОМИ"): 
            return "республика Коми"
        if (str0_ == "СО"): 
            return "Северная Осетия"
        if (str0_ == "С"): 
            return ""
        return None
    
    @staticmethod
    def initialize() -> None:
        CorrectionHelper.__m_root = AbbrTreeNode()
        for r in RegionHelper.REGIONS: 
            a = Utils.asObjectOrNull(r.attrs, AreaAttributes)
            if (a is None): 
                continue
            if (len(a.types) == 0 or "город" in a.types): 
                continue
            if (len(a.names) == 0): 
                continue
            if (a.types[0] == "республика"): 
                CorrectionHelper.__add(a.names[0], "респ")
            elif (a.types[0] == "край"): 
                CorrectionHelper.__add(a.names[0], "кр")
                if (a.names[0].endswith("ий")): 
                    CorrectionHelper.__add(a.names[0][0:0+len(a.names[0]) - 2] + "ая", "об")
            elif (a.types[0] == "область"): 
                CorrectionHelper.__add(a.names[0], "об")
                if (a.names[0].endswith("ая")): 
                    CorrectionHelper.__add(a.names[0][0:0+len(a.names[0]) - 2] + "ий", "р")
            elif (a.types[0] == "автономная область"): 
                CorrectionHelper.__add(a.names[0], "об")
                CorrectionHelper.__add(a.names[0], "ао")
            elif (a.types[0] == "автономный округ"): 
                CorrectionHelper.__add(a.names[0], "ок")
                CorrectionHelper.__add(a.names[0], "ао")
            elif (a.types[0] == "город"): 
                CorrectionHelper.__add(a.names[0], "г")
            else: 
                pass
    
    @staticmethod
    def initialize0() -> None:
        dat = PullentiAddressInternalResourceHelper.get_string("CitiesNonRus.txt")
        country = None
        for line in Utils.splitString(dat, '\n', False): 
            if (line.startswith("//")): 
                continue
            if (line.startswith("*")): 
                aa = AreaAttributes()
                country = AddrObject._new120(aa, AddrLevel.COUNTRY)
                nam = line[1:].strip()
                ii = nam.find(';')
                if (ii > 0): 
                    country.tag = (nam[ii + 1:].strip())
                    nam = nam[0:0+ii].strip()
                aa.names.append(nam)
                continue
            if (country is None): 
                continue
            is_city = True
            if (line.find("область") >= 0 or line.find("район") >= 0 or line.find(" край") > 0): 
                is_city = False
            line1 = line.replace(',', ';')
            for v in Utils.splitString(line1, ';', False): 
                city = v.upper().strip().replace('Ё', 'Е')
                if (Utils.isNullOrEmpty(city)): 
                    continue
                if (is_city): 
                    if (not city in CorrectionHelper.__m_cities): 
                        CorrectionHelper.__m_cities[city] = country
                    continue
                ii = city.find("ОБЛАСТЬ")
                if (ii < 0): 
                    ii = city.find("РАЙОН")
                if (ii < 0): 
                    ii = city.find(" КРАЙ")
                if (ii > 0): 
                    city = city[0:0+ii].strip()
                if (not city in CorrectionHelper.__m_regions): 
                    CorrectionHelper.__m_regions[city] = country
    
    __m_root = None
    
    __m_cities = None
    
    __m_regions = None
    
    @staticmethod
    def find_country(obj : 'AddrObject') -> 'AddrObject':
        aa = Utils.asObjectOrNull(obj.attrs, AreaAttributes)
        if (aa is None): 
            return None
        res = None
        for nam in aa.names: 
            wrapres137 = RefOutArgWrapper(None)
            inoutres138 = Utils.tryGetValue(CorrectionHelper.__m_cities, nam.upper(), wrapres137)
            res = wrapres137.value
            if (inoutres138): 
                return res
            wrapres135 = RefOutArgWrapper(None)
            inoutres136 = Utils.tryGetValue(CorrectionHelper.__m_regions, nam.upper(), wrapres135)
            res = wrapres135.value
            if (inoutres136): 
                return res
        return None
    
    @staticmethod
    def __add(corr : str, typ : str) -> None:
        typ = typ.upper()
        corr = corr.upper()
        i = 1
        while i < (len(corr) - 2): 
            if (not LanguageHelper.is_cyrillic_vowel(corr[i])): 
                str0_ = corr[0:0+i + 1]
                if (RegionHelper.is_big_city(str0_) is not None): 
                    pass
                else: 
                    CorrectionHelper.__m_root.add(str0_, 0, corr, typ)
            i += 1
    
    @staticmethod
    def correct_country(addr : 'TextAddress') -> None:
        if (len(addr.items) == 0): 
            return
        if (addr.items[0].level == AddrLevel.COUNTRY): 
            return
        for it in addr.items: 
            if (len(it.gars) > 0): 
                reg = it.gars[0].region_number
                if ((reg == 90 or reg == 93 or reg == 94) or reg == 95): 
                    addr.items.insert(0, CorrectionHelper.create_country("UA", None))
                    addr.alpha2 = "UA"
                else: 
                    addr.items.insert(0, CorrectionHelper.create_country("RU", None))
                    addr.alpha2 = "RU"
                return
    
    @staticmethod
    def create_country(alpha : str, geo : 'GeoReferent') -> 'AddrObject':
        aa = AreaAttributes()
        if (alpha == "RU"): 
            aa.names.append("Россия")
        elif (alpha == "UA"): 
            aa.names.append("Украина")
        elif (alpha == "BY"): 
            aa.names.append("Белоруссия")
        elif (alpha == "KZ"): 
            aa.names.append("Казахстан")
        elif (alpha == "KG"): 
            aa.names.append("Киргизия")
        elif (alpha == "MD"): 
            aa.names.append("Молдавия")
        elif (alpha == "GE"): 
            aa.names.append("Грузия")
        elif (alpha == "AZ"): 
            aa.names.append("Азербайджан")
        elif (alpha == "AM"): 
            aa.names.append("Армения")
        elif (alpha == "EE"): 
            aa.names.append("Эстония")
        elif (alpha == "LT"): 
            aa.names.append("Литва")
        elif (alpha == "LV"): 
            aa.names.append("Латвия")
        elif (alpha == "TM"): 
            aa.names.append("Туркменистан")
        elif (alpha == "TJ"): 
            aa.names.append("Таджикистан")
        elif (alpha == "TM"): 
            aa.names.append("Туркменистан")
        elif (alpha == "UZ"): 
            aa.names.append("Узбекистан")
        elif (geo is not None): 
            aa.names.append(str(geo))
        else: 
            return None
        res = AddrObject(aa)
        res.level = AddrLevel.COUNTRY
        return res
    
    # static constructor for class CorrectionHelper
    @staticmethod
    def _static_ctor():
        CorrectionHelper.__m_cities = dict()
        CorrectionHelper.__m_regions = dict()

CorrectionHelper._static_ctor()