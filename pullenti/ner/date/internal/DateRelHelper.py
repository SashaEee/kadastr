# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import typing
import operator
import datetime
import io
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.Token import Token
from pullenti.ner.date.DatePointerType import DatePointerType
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.ReferentToken import ReferentToken
from pullenti.ner.Referent import Referent
from pullenti.ner.date.DateReferent import DateReferent
from pullenti.ner.date.DateRangeReferent import DateRangeReferent
from pullenti.ner.date.internal.DateExToken import DateExToken

class DateRelHelper:
    
    @staticmethod
    def create_referents(et : 'DateExToken') -> typing.List['ReferentToken']:
        if (not et.is_diap or len(et.items_to) == 0): 
            li = DateRelHelper.__create_refs(et.items_from)
            if (li is None or len(li) == 0): 
                return None
            return li
        li_fr = DateRelHelper.__create_refs(et.items_from)
        li_to = DateRelHelper.__create_refs(et.items_to)
        ra = DateRangeReferent()
        if (len(li_fr) > 0): 
            ra.date_from = Utils.asObjectOrNull(li_fr[0].tag, DateReferent)
        if (len(li_to) > 0): 
            ra.date_to = Utils.asObjectOrNull(li_to[0].tag, DateReferent)
        res = list()
        res.extend(li_fr)
        res.extend(li_to)
        res.append(ReferentToken(ra, et.begin_token, et.end_token))
        if (len(res) == 0): 
            return None
        res[0].tag = (ra)
        return res
    
    @staticmethod
    def __create_refs(its : typing.List['DateExItemToken']) -> typing.List['ReferentToken']:
        res = list()
        own = None
        i = 0
        first_pass3450 = True
        while True:
            if first_pass3450: first_pass3450 = False
            else: i += 1
            if (not (i < len(its))): break
            it = its[i]
            d = DateReferent()
            if (it.is_value_relate): 
                d.is_relative = True
            if (own is not None): 
                d.higher = own
            if (it.typ == DateExToken.DateExItemTokenType.DAY): 
                d.day = it.value
                if (it.is_last and ((it.value == 0 or it.value == -1)) and i > 0): 
                    it0 = its[i - 1]
                    day = 0
                    if (it0.typ == DateExToken.DateExItemTokenType.MONTH and not it0.is_value_relate): 
                        m = d.month
                        if (((m == 1 or m == 3 or m == 5) or m == 7 or m == 8) or m == 10 or m == 12): 
                            day = 31
                        elif (m == 2): 
                            day = 28
                        elif (m > 0): 
                            day = 30
                    elif (it0.typ == DateExToken.DateExItemTokenType.QUARTAL and not it0.is_value_relate): 
                        m = 1 + (((it0.value - 1)) * 4)
                        dm = DateReferent()
                        dm.month = m
                        if (own is not None): 
                            dm.higher = own
                        res.append(ReferentToken(dm, it.begin_token, it.end_token))
                        d.higher = dm
                        own = d.higher
                        if (((m == 1 or m == 3 or m == 5) or m == 7 or m == 8) or m == 10 or m == 12): 
                            day = 31
                        elif (m == 2): 
                            day = 28
                        elif (m > 0): 
                            day = 30
                    elif (it0.typ == DateExToken.DateExItemTokenType.YEAR): 
                        dm = DateReferent()
                        dm.month = 12
                        if (own is not None): 
                            dm.higher = own
                        res.append(ReferentToken(dm, it.begin_token, it.end_token))
                        d.higher = dm
                        own = d.higher
                        day = 31
                    elif (it0.typ == DateExToken.DateExItemTokenType.CENTURY): 
                        dy = DateReferent()
                        dy.year = 99
                        dy.is_relative = True
                        if (own is not None): 
                            dy.higher = own
                        res.append(ReferentToken(dy, it.begin_token, it.end_token))
                        own = dy
                        dm = DateReferent()
                        dm.month = 12
                        dm.higher = own
                        res.append(ReferentToken(dm, it.begin_token, it.end_token))
                        d.higher = dm
                        own = d.higher
                        day = 31
                    if ((day + it.value) > 0): 
                        d.is_relative = False
                        d.day = day + it.value
            elif (it.typ == DateExToken.DateExItemTokenType.DAYOFWEEK): 
                d.day_of_week = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.HOUR): 
                d.hour = it.value
                if (((i + 1) < len(its)) and its[i + 1].typ == DateExToken.DateExItemTokenType.MINUTE and not its[i + 1].is_value_relate): 
                    d.minute = its[i + 1].value
                    i += 1
            elif (it.typ == DateExToken.DateExItemTokenType.MINUTE): 
                d.minute = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.MONTH): 
                d.month = it.value
                if (it.is_last and ((it.value == 0 or it.value == -1)) and i > 0): 
                    it0 = its[i - 1]
                    m = 0
                    if (it0.typ == DateExToken.DateExItemTokenType.QUARTAL and not it0.is_value_relate): 
                        m = (1 + (((it0.value - 1)) * 4) + it.value)
                    elif (it0.typ == DateExToken.DateExItemTokenType.YEAR or it0.typ == DateExToken.DateExItemTokenType.DECADE or it0.typ == DateExToken.DateExItemTokenType.CENTURY): 
                        m = (12 + it.value)
                    if (m > 0): 
                        d.is_relative = False
                        d.month = m
            elif (it.typ == DateExToken.DateExItemTokenType.QUARTAL): 
                d.quartal = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.SEASON): 
                d.season = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.WEEK): 
                d.week = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.HALFYEAR): 
                d.halfyear = (2 if it.is_last else it.value)
            elif (it.typ == DateExToken.DateExItemTokenType.YEAR): 
                d.year = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.CENTURY): 
                d.century = it.value
            elif (it.typ == DateExToken.DateExItemTokenType.DECADE): 
                d.decade = it.value
            else: 
                continue
            res.append(ReferentToken(d, it.begin_token, it.end_token))
            own = d
            it.src = d
        if (len(res) > 0): 
            res[0].tag = (own)
        return res
    
    @staticmethod
    def __create_date_ex(dr : 'DateReferent') -> typing.List['DateExItemToken']:
        res = list()
        while dr is not None: 
            n = 0
            for s in dr.slots: 
                tt = Token(None, 0, 1)
                it = DateExToken.DateExItemToken._new1159(tt, tt, DateExToken.DateExItemTokenType.UNDEFINED)
                if (dr.get_string_value(DateReferent.ATTR_ISRELATIVE) == "true"): 
                    it.is_value_relate = True
                if (s.type_name == DateReferent.ATTR_YEAR): 
                    it.typ = DateExToken.DateExItemTokenType.YEAR
                    wrapn1160 = RefOutArgWrapper(0)
                    inoutres1161 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn1160)
                    n = wrapn1160.value
                    if (inoutres1161): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_DECADE): 
                    it.typ = DateExToken.DateExItemTokenType.DECADE
                    wrapn1162 = RefOutArgWrapper(0)
                    inoutres1163 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn1162)
                    n = wrapn1162.value
                    if (inoutres1163): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_CENTURY): 
                    it.typ = DateExToken.DateExItemTokenType.CENTURY
                    wrapn1164 = RefOutArgWrapper(0)
                    inoutres1165 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn1164)
                    n = wrapn1164.value
                    if (inoutres1165): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_HALFYEAR): 
                    it.typ = DateExToken.DateExItemTokenType.HALFYEAR
                    wrapn1166 = RefOutArgWrapper(0)
                    inoutres1167 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn1166)
                    n = wrapn1166.value
                    if (inoutres1167): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_QUARTAL): 
                    it.typ = DateExToken.DateExItemTokenType.QUARTAL
                    wrapn1168 = RefOutArgWrapper(0)
                    inoutres1169 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn1168)
                    n = wrapn1168.value
                    if (inoutres1169): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_SEASON): 
                    it.typ = DateExToken.DateExItemTokenType.SEASON
                    wrapn1170 = RefOutArgWrapper(0)
                    inoutres1171 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn1170)
                    n = wrapn1170.value
                    if (inoutres1171): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_MONTH): 
                    it.typ = DateExToken.DateExItemTokenType.MONTH
                    wrapn1172 = RefOutArgWrapper(0)
                    inoutres1173 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn1172)
                    n = wrapn1172.value
                    if (inoutres1173): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_WEEK): 
                    it.typ = DateExToken.DateExItemTokenType.WEEK
                    wrapn1174 = RefOutArgWrapper(0)
                    inoutres1175 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn1174)
                    n = wrapn1174.value
                    if (inoutres1175): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_DAYOFWEEK): 
                    it.typ = DateExToken.DateExItemTokenType.DAYOFWEEK
                    wrapn1176 = RefOutArgWrapper(0)
                    inoutres1177 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn1176)
                    n = wrapn1176.value
                    if (inoutres1177): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_DAY): 
                    it.typ = DateExToken.DateExItemTokenType.DAY
                    wrapn1178 = RefOutArgWrapper(0)
                    inoutres1179 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn1178)
                    n = wrapn1178.value
                    if (inoutres1179): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_HOUR): 
                    it.typ = DateExToken.DateExItemTokenType.HOUR
                    wrapn1180 = RefOutArgWrapper(0)
                    inoutres1181 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn1180)
                    n = wrapn1180.value
                    if (inoutres1181): 
                        it.value = n
                elif (s.type_name == DateReferent.ATTR_MINUTE): 
                    it.typ = DateExToken.DateExItemTokenType.MINUTE
                    wrapn1182 = RefOutArgWrapper(0)
                    inoutres1183 = Utils.tryParseInt(Utils.asObjectOrNull(s.value, str), wrapn1182)
                    n = wrapn1182.value
                    if (inoutres1183): 
                        it.value = n
                if (it.typ != DateExToken.DateExItemTokenType.UNDEFINED): 
                    res.insert(0, it)
            dr = dr.higher
        # PYTHON: sort(key=attrgetter('typ'))
        res.sort(key=operator.attrgetter('typ'))
        return res
    
    @staticmethod
    def calculate_date(dr : 'DateReferent', now : datetime.datetime, tense : int) -> datetime.datetime:
        if (dr.pointer == DatePointerType.TODAY): 
            return now
        if (not dr.is_relative and dr.dt is not None): 
            return dr.dt
        det = DateExToken(None, None)
        det.items_from = DateRelHelper.__create_date_ex(dr)
        return det.get_date(now, tense)
    
    @staticmethod
    def calculate_date_range(dr : 'DateReferent', now : datetime.datetime, from0_ : datetime.datetime, to : datetime.datetime, tense : int) -> bool:
        if (dr.pointer == DatePointerType.TODAY): 
            from0_.value = now
            to.value = now
            return True
        if (not dr.is_relative and dr.dt is not None): 
            to.value = dr.dt
            from0_.value = to.value
            return True
        t = Token(None, 0, 1)
        det = DateExToken(t, t)
        det.items_from = DateRelHelper.__create_date_ex(dr)
        inoutres1184 = det.get_dates(now, from0_, to, tense)
        return inoutres1184
    
    @staticmethod
    def calculate_date_range2(dr : 'DateRangeReferent', now : datetime.datetime, from0_ : datetime.datetime, to : datetime.datetime, tense : int) -> bool:
        from0_.value = datetime.datetime.min
        to.value = datetime.datetime.max
        dt0 = None
        dt1 = None
        if (dr.date_from is None): 
            if (dr.date_to is None): 
                return False
            wrapdt01185 = RefOutArgWrapper(None)
            wrapdt11186 = RefOutArgWrapper(None)
            inoutres1187 = DateRelHelper.calculate_date_range(dr.date_to, now, wrapdt01185, wrapdt11186, tense)
            dt0 = wrapdt01185.value
            dt1 = wrapdt11186.value
            if (not inoutres1187): 
                return False
            to.value = dt1
            return True
        elif (dr.date_to is None): 
            wrapdt01188 = RefOutArgWrapper(None)
            wrapdt11189 = RefOutArgWrapper(None)
            inoutres1190 = DateRelHelper.calculate_date_range(dr.date_from, now, wrapdt01188, wrapdt11189, tense)
            dt0 = wrapdt01188.value
            dt1 = wrapdt11189.value
            if (not inoutres1190): 
                return False
            from0_.value = dt0
            return True
        wrapdt01194 = RefOutArgWrapper(None)
        wrapdt11195 = RefOutArgWrapper(None)
        inoutres1196 = DateRelHelper.calculate_date_range(dr.date_from, now, wrapdt01194, wrapdt11195, tense)
        dt0 = wrapdt01194.value
        dt1 = wrapdt11195.value
        if (not inoutres1196): 
            return False
        from0_.value = dt0
        dt2 = None
        dt3 = None
        wrapdt21191 = RefOutArgWrapper(None)
        wrapdt31192 = RefOutArgWrapper(None)
        inoutres1193 = DateRelHelper.calculate_date_range(dr.date_to, now, wrapdt21191, wrapdt31192, tense)
        dt2 = wrapdt21191.value
        dt3 = wrapdt31192.value
        if (not inoutres1193): 
            return False
        to.value = dt3
        return True
    
    @staticmethod
    def append_to_string(dr : 'DateReferent', res : io.StringIO) -> None:
        dt0 = None
        dt1 = None
        cur = (datetime.datetime.now() if ProcessorService.DEBUG_CURRENT_DATE_TIME is None else ProcessorService.DEBUG_CURRENT_DATE_TIME)
        wrapdt01197 = RefOutArgWrapper(None)
        wrapdt11198 = RefOutArgWrapper(None)
        inoutres1199 = DateRelHelper.calculate_date_range(dr, cur, wrapdt01197, wrapdt11198, 0)
        dt0 = wrapdt01197.value
        dt1 = wrapdt11198.value
        if (not inoutres1199): 
            return
        DateRelHelper.__append_dates(cur, dt0, dt1, res)
    
    @staticmethod
    def append_to_string2(dr : 'DateRangeReferent', res : io.StringIO) -> None:
        dt0 = None
        dt1 = None
        cur = (datetime.datetime.now() if ProcessorService.DEBUG_CURRENT_DATE_TIME is None else ProcessorService.DEBUG_CURRENT_DATE_TIME)
        wrapdt01200 = RefOutArgWrapper(None)
        wrapdt11201 = RefOutArgWrapper(None)
        inoutres1202 = DateRelHelper.calculate_date_range2(dr, cur, wrapdt01200, wrapdt11201, 0)
        dt0 = wrapdt01200.value
        dt1 = wrapdt11201.value
        if (not inoutres1202): 
            return
        DateRelHelper.__append_dates(cur, dt0, dt1, res)
    
    @staticmethod
    def __append_dates(cur : datetime.datetime, dt0 : datetime.datetime, dt1 : datetime.datetime, res : io.StringIO) -> None:
        mon0 = dt0.month
        print(" ({0}.{1}.{2}".format(dt0.year, "{:02d}".format(mon0), "{:02d}".format(dt0.day)), end="", file=res, flush=True)
        if (dt0.hour > 0 or dt0.minute > 0): 
            print(" {0}:{1}".format("{:02d}".format(dt0.hour), "{:02d}".format(dt0.minute)), end="", file=res, flush=True)
        if (dt0 != dt1): 
            mon1 = dt1.month
            print("-{0}.{1}.{2}".format(dt1.year, "{:02d}".format(mon1), "{:02d}".format(dt1.day)), end="", file=res, flush=True)
            if (dt1.hour > 0 or dt1.minute > 0): 
                print(" {0}:{1}".format("{:02d}".format(dt1.hour), "{:02d}".format(dt1.minute)), end="", file=res, flush=True)
        monc = cur.month
        print(" отн. {0}.{1}.{2}".format(cur.year, "{:02d}".format(monc), "{:02d}".format(cur.day)), end="", file=res, flush=True)
        if (cur.hour > 0 or cur.minute > 0): 
            print(" {0}:{1}".format("{:02d}".format(cur.hour), "{:02d}".format(cur.minute)), end="", file=res, flush=True)
        print(")", end="", file=res)