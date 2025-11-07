# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import io
import datetime
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper

from pullenti.ner.core.GetTextAttr import GetTextAttr
from pullenti.ner.MetaToken import MetaToken
from pullenti.ner.core.TerminParseAttr import TerminParseAttr
from pullenti.morph.MorphGender import MorphGender
from pullenti.morph.MorphNumber import MorphNumber
from pullenti.ner.core.NounPhraseParseAttr import NounPhraseParseAttr
from pullenti.ner.TextToken import TextToken
from pullenti.ner.chat.VerbType import VerbType
from pullenti.ner.chat.ChatType import ChatType
from pullenti.ner.core.MiscHelper import MiscHelper
from pullenti.ner.date.DateRangeReferent import DateRangeReferent
from pullenti.ner.ProcessorService import ProcessorService
from pullenti.ner.core.TerminCollection import TerminCollection
from pullenti.ner.core.NounPhraseHelper import NounPhraseHelper
from pullenti.ner.core.Termin import Termin
from pullenti.ner.date.DateReferent import DateReferent

class ChatItemToken(MetaToken):
    
    def __init__(self, b : 'Token', e0_ : 'Token') -> None:
        super().__init__(b, e0_, None)
        self.not0_ = False
        self.typ = ChatType.UNDEFINED
        self.vtyp = VerbType.UNDEFINED
        self.value = None;
    
    def __str__(self) -> str:
        tmp = io.StringIO()
        print(Utils.enumToString(self.typ), end="", file=tmp)
        if (self.not0_): 
            print(" not", end="", file=tmp)
        if (self.value is not None): 
            print(" {0}".format(self.value), end="", file=tmp, flush=True)
        if (self.vtyp != VerbType.UNDEFINED): 
            print(" [{0}]".format(Utils.enumToString(self.vtyp)), end="", file=tmp, flush=True)
        return Utils.toStringStringIO(tmp)
    
    @staticmethod
    def __is_empty_token(t : 'Token') -> bool:
        if (not (isinstance(t, TextToken))): 
            return False
        if (t.length_char == 1): 
            return True
        mc = t.get_morph_class_in_dictionary()
        if ((((mc.is_misc or mc.is_adverb or mc.is_conjunction) or mc.is_preposition or mc.is_personal_pronoun) or mc.is_pronoun or mc.is_conjunction) or mc.is_preposition): 
            return True
        return False
    
    @staticmethod
    def try_parse(t : 'Token') -> 'ChatItemToken':
        tok = None
        not0__ = False
        tt = None
        t0 = None
        t1 = None
        has_modal = False
        dt0 = datetime.datetime.min
        dt1 = datetime.datetime.min
        tt = t
        first_pass3390 = True
        while True:
            if first_pass3390: first_pass3390 = False
            else: tt = tt.next0_
            if (not (tt is not None)): break
            if (tt != t and tt.is_newline_before): 
                break
            if (tt.is_char_of(".?!")): 
                break
            if (tt.length_char == 1): 
                continue
            ok = False
            if (isinstance(tt.get_referent(), DateReferent)): 
                dr = Utils.asObjectOrNull(tt.get_referent(), DateReferent)
                wrapdt0786 = RefOutArgWrapper(None)
                wrapdt1787 = RefOutArgWrapper(None)
                ok = dr.calculate_date_range((datetime.datetime.now() if ProcessorService.DEBUG_CURRENT_DATE_TIME is None else ProcessorService.DEBUG_CURRENT_DATE_TIME), wrapdt0786, wrapdt1787, 0)
                dt0 = wrapdt0786.value
                dt1 = wrapdt1787.value
            elif (isinstance(tt.get_referent(), DateRangeReferent)): 
                dr = Utils.asObjectOrNull(tt.get_referent(), DateRangeReferent)
                wrapdt0788 = RefOutArgWrapper(None)
                wrapdt1789 = RefOutArgWrapper(None)
                ok = dr.calculate_date_range((datetime.datetime.now() if ProcessorService.DEBUG_CURRENT_DATE_TIME is None else ProcessorService.DEBUG_CURRENT_DATE_TIME), wrapdt0788, wrapdt1789, 0)
                dt0 = wrapdt0788.value
                dt1 = wrapdt1789.value
            if (ok): 
                if (dt0 != dt1): 
                    res = ChatItemToken._new790(tt, tt, ChatType.DATERANGE)
                    res.value = "{0}.{1}.{2}".format(dt0.year, "{:02d}".format(dt0.month), "{:02d}".format(dt0.day))
                    if (dt0.hour > 0 or dt0.minute > 0): 
                        res.value = "{0} {1}:{2}".format(res.value, "{:02d}".format(dt0.hour), "{:02d}".format(dt0.minute))
                    res.value = "{0} - {1}.{2}.{3}".format(res.value, dt1.year, "{:02d}".format(dt1.month), "{:02d}".format(dt1.day))
                    if (dt1.hour > 0 or dt1.minute > 0): 
                        res.value = "{0} {1}:{2}".format(res.value, "{:02d}".format(dt1.hour), "{:02d}".format(dt1.minute))
                    return res
                else: 
                    res = ChatItemToken._new790(tt, tt, ChatType.DATE)
                    res.value = "{0}.{1}.{2}".format(dt0.year, "{:02d}".format(dt0.month), "{:02d}".format(dt0.day))
                    if (dt0.hour > 0 or dt0.minute > 0): 
                        res.value = "{0} {1}:{2}".format(res.value, "{:02d}".format(dt0.hour), "{:02d}".format(dt0.minute))
                    return res
            if (not (isinstance(tt, TextToken))): 
                break
            tok = ChatItemToken.__m_ontology.try_parse(tt, TerminParseAttr.NO)
            if (tok is not None): 
                break
            mc = tt.get_morph_class_in_dictionary()
            term = tt.term
            if (term == "НЕ"): 
                not0__ = True
                if (t0 is None): 
                    t0 = tt
                continue
            if ((mc.is_personal_pronoun or mc.is_pronoun or mc.is_conjunction) or mc.is_preposition): 
                continue
            if (tt.is_value("ХОТЕТЬ", None) or tt.is_value("ЖЕЛАТЬ", None) or tt.is_value("МОЧЬ", None)): 
                has_modal = True
                if (t0 is None): 
                    t0 = tt
                t1 = tt
                continue
            if (mc.is_adverb or mc.is_misc): 
                continue
            if (mc.is_verb): 
                res = ChatItemToken(tt, tt)
                res.typ = ChatType.VERB
                res.value = tt.lemma
                if (not0__): 
                    res.not0_ = True
                if (t0 is not None): 
                    res.begin_token = t0
                return res
        if (tok is not None): 
            res = ChatItemToken(tok.begin_token, tok.end_token)
            res.typ = (Utils.valToEnum(tok.termin.tag, ChatType))
            if (isinstance(tok.termin.tag2, VerbType)): 
                res.vtyp = (Utils.valToEnum(tok.termin.tag2, VerbType))
            if (res.typ == ChatType.VERB and tok.begin_token == tok.end_token and (isinstance(tok.begin_token, TextToken))): 
                res.value = tok.begin_token.lemma
            else: 
                res.value = MiscHelper.get_text_value_of_meta_token(res, GetTextAttr.NO)
            if (not0__): 
                res.not0_ = True
            if (t0 is not None): 
                res.begin_token = t0
            if (res.typ == ChatType.REPEAT): 
                tt = tok.end_token.next0_
                first_pass3391 = True
                while True:
                    if first_pass3391: first_pass3391 = False
                    else: tt = tt.next0_
                    if (not (tt is not None)): break
                    if (not (isinstance(tt, TextToken))): 
                        break
                    if (ChatItemToken.__is_empty_token(tt)): 
                        continue
                    tok1 = ChatItemToken.__m_ontology.try_parse(tt, TerminParseAttr.NO)
                    if (tok1 is not None): 
                        if ((Utils.valToEnum(tok1.termin.tag, ChatType)) == ChatType.ACCEPT or (Utils.valToEnum(tok1.termin.tag, ChatType)) == ChatType.MISC): 
                            tt = tok1.end_token
                            continue
                        if ((Utils.valToEnum(tok1.termin.tag, ChatType)) == ChatType.REPEAT): 
                            res.end_token = tok1.end_token
                            tt = res.end_token
                            continue
                        break
                    npt = NounPhraseHelper.try_parse(tt, NounPhraseParseAttr.NO, 0, None)
                    if (npt is not None): 
                        if (npt.end_token.is_value("ВОПРОС", None) or npt.end_token.is_value("ФРАЗА", None) or npt.end_token.is_value("ПРЕДЛОЖЕНИЕ", None)): 
                            res.end_token = npt.end_token
                            tt = res.end_token
                            res.value = npt.get_normal_case_text(None, MorphNumber.UNDEFINED, MorphGender.UNDEFINED, False)
                            continue
                    break
            return res
        if (not0__ and has_modal): 
            res = ChatItemToken(t0, t1)
            res.typ = ChatType.CANCEL
            return res
        return None
    
    __m_ontology = None
    
    @staticmethod
    def initialize() -> None:
        if (ChatItemToken.__m_ontology is not None): 
            return
        ChatItemToken.__m_ontology = TerminCollection()
        t = None
        t = Termin._new124("ДА", ChatType.ACCEPT)
        t.add_variant("КОНЕЧНО", False)
        t.add_variant("РАЗУМЕЕТСЯ", False)
        t.add_variant("ПОЖАЛУЙСТА", False)
        t.add_variant("ПОЖАЛУЙ", False)
        t.add_variant("ПЛИЗ", False)
        t.add_variant("НЕПРЕМЕННО", False)
        t.add_variant("ЕСТЬ", False)
        t.add_variant("АГА", False)
        t.add_variant("УГУ", False)
        ChatItemToken.__m_ontology.add(t)
        t = Termin._new124("НЕТ", ChatType.CANCEL)
        t.add_variant("ДА НЕТ", False)
        t.add_variant("НИ ЗА ЧТО", False)
        t.add_variant("НЕ ХОТЕТЬ", False)
        t.add_variant("ОТСТАТЬ", False)
        t.add_variant("НИКТО", False)
        t.add_variant("НИЧТО", False)
        t.add_variant("НИЧЕГО", False)
        t.add_variant("НИГДЕ", False)
        t.add_variant("НИКОГДА", False)
        ChatItemToken.__m_ontology.add(t)
        t = Termin._new124("СПАСИБО", ChatType.THANKS)
        t.add_variant("БЛАГОДАРИТЬ", False)
        t.add_variant("БЛАГОДАРСТВОВАТЬ", False)
        ChatItemToken.__m_ontology.add(t)
        t = Termin._new124("НУ", ChatType.MISC)
        ChatItemToken.__m_ontology.add(t)
        t = Termin._new124("ПРИВЕТ", ChatType.HELLO)
        for s in ["ЗДРАВСТВУЙ", "ЗДРАВСТВУЙТЕ", "ПРИВЕТИК", "ЗДРАВИЯ ЖЕЛАЮ", "ХЭЛЛОУ", "АЛЛЕ", "ХЭЛО", "АЛЛО", "САЛЮТ", "ДОБРЫЙ ДЕНЬ", "ДОБРЫЙ ВЕЧЕР", "ДОБРОЕ УТРО", "ДОБРАЯ НОЧЬ", "ЗДОРОВО"]: 
            t.add_variant(s, False)
        ChatItemToken.__m_ontology.add(t)
        t = Termin._new124("ПОКА", ChatType.BYE)
        for s in ["ДО СВИДАНИЯ", "ДОСВИДАНИЯ", "ПРОЩАЙ", "ПРОЩАЙТЕ", "ПРОЩЕВАЙ", "ХОРОШЕГО ДНЯ", "ХОРОШЕГО ВЕЧЕРА", "ВСЕГО ХОРОШЕГО", "ВСЕГО ДОБРОГО", "ВСЕХ БЛАГ", "СЧАСТЛИВО", "ДО СКОРОЙ ВСТРЕЧИ", "ДО ЗАВТРА", "ДО ВСТРЕЧИ", "СКОРО УВИДИМСЯ", "ПОКЕДА", "ПОКЕДОВА", "ПРОЩАЙ", "ПРОЩАЙТЕ", "ЧАО", "ГУД БАЙ", "ГУДБАЙ", "ЧАО"]: 
            t.add_variant(s, False)
        ChatItemToken.__m_ontology.add(t)
        t = Termin._new360("ГОВОРИТЬ", ChatType.VERB, VerbType.SAY)
        for s in ["СКАЗАТЬ", "РАЗГОВАРИВАТЬ", "ПРОИЗНЕСТИ", "ПРОИЗНОСИТЬ", "ОТВЕТИТЬ", "ОТВЕЧАТЬ", "СПРАШИВАТЬ", "СПРОСИТЬ", "ПОТОВОРИТЬ", "ОБЩАТЬСЯ", "ПООБЩАТЬСЯ"]: 
            t.add_variant(s, False)
        ChatItemToken.__m_ontology.add(t)
        t = Termin._new360("ЗВОНИТЬ", ChatType.VERB, VerbType.CALL)
        for s in ["ПЕРЕЗВОНИТЬ", "ПОЗВОНИТЬ", "СДЕЛАТЬ ЗВОНОК", "НАБРАТЬ"]: 
            t.add_variant(s, False)
        ChatItemToken.__m_ontology.add(t)
        t = Termin._new360("БЫТЬ", ChatType.VERB, VerbType.BE)
        for s in ["ЯВЛЯТЬСЯ"]: 
            t.add_variant(s, False)
        ChatItemToken.__m_ontology.add(t)
        t = Termin._new360("ИМЕТЬ", ChatType.VERB, VerbType.HAVE)
        for s in ["ОБЛАДАТЬ", "ВЛАДЕТЬ"]: 
            t.add_variant(s, False)
        ChatItemToken.__m_ontology.add(t)
        t = Termin._new124("ПОЗЖЕ", ChatType.LATER)
        for s in ["ПОПОЗЖЕ", "ПОЗДНЕЕ", "ПОТОМ", "НЕКОГДА"]: 
            t.add_variant(s, False)
        ChatItemToken.__m_ontology.add(t)
        t = Termin._new124("ЗАНЯТ", ChatType.BUSY)
        for s in ["НЕУДОБНО", "НЕ УДОБНО", "НЕТ ВРЕМЕНИ", "ПАРАЛЛЕЛЬНЫЙ ЗВОНОК", "СОВЕЩАНИЕ", "ОБЕД", "ТРАНСПОРТ", "МЕТРО"]: 
            t.add_variant(s, False)
        ChatItemToken.__m_ontology.add(t)
        t = Termin._new124("ПОВТОРИТЬ", ChatType.REPEAT)
        t.add_variant("НЕ РАССЛЫШАТЬ", False)
        t.add_variant("НЕ УСЛЫШАТЬ", False)
        t.add_variant("ПЛОХО СЛЫШНО", False)
        t.add_variant("ПЛОХАЯ СВЯЗЬ", False)
        ChatItemToken.__m_ontology.add(t)
    
    @staticmethod
    def _new790(_arg1 : 'Token', _arg2 : 'Token', _arg3 : 'ChatType') -> 'ChatItemToken':
        res = ChatItemToken(_arg1, _arg2)
        res.typ = _arg3
        return res