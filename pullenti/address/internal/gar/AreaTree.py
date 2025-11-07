# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

import threading
import io
import typing
import gc
from pullenti.unisharp.Utils import Utils
from pullenti.unisharp.Misc import RefOutArgWrapper
from pullenti.unisharp.Streams import FileStream
from pullenti.unisharp.Streams import Stream

from pullenti.address.internal.FiasHelper import FiasHelper
from pullenti.util.FileHelper import FileHelper
from pullenti.address.internal.gar.AreaTreeNode import AreaTreeNode
from pullenti.address.GarLevel import GarLevel
from pullenti.address.internal.gar.AreaTreeObject import AreaTreeObject

class AreaTree:
    
    def __init__(self) -> None:
        self.__m_obj_pos = list()
        self.__m_objs = list()
        self.__m_strings = list()
        self.children = dict()
        self.m_lock = threading.Lock()
        self.__m_data = None;
    
    def get_string_id(self, str0_ : str) -> int:
        if (str0_ is None): 
            return 0
        i = Utils.indexOfList(self.__m_strings, str0_, 0)
        if (i < 0): 
            self.__m_strings.append(str0_)
            i = len(self.__m_strings)
        else: 
            i += 1
        return i
    
    def get_string(self, id0_ : int) -> str:
        if (id0_ > 0 and id0_ <= len(self.__m_strings)): 
            return self.__m_strings[id0_ - 1]
        return None
    
    def close0_(self) -> None:
        self.children.clear()
        self.__m_obj_pos.clear()
        self.__m_objs.clear()
        self.__m_strings.clear()
    
    def collect(self) -> None:
        for ch in self.children.items(): 
            ch[1].children.clear()
            ch[1].loaded = False
    
    def load_all_objects(self) -> None:
        id0_ = 1
        while id0_ <= len(self.__m_objs): 
            self.get_obj(id0_)
            id0_ += 1
    
    def load_all_data(self) -> None:
        self.load_all_objects()
        for ch in self.children.items(): 
            self.__load_all_nodes(ch[1])
    
    def __load_all_nodes(self, node : 'AreaTreeNode') -> None:
        if (not node.loaded): 
            self.__load_node(node)
        if (node.children is not None): 
            for ch in node.children.items(): 
                self.__load_all_nodes(ch[1])
    
    def get_obj(self, id0_ : int) -> 'AreaTreeObject':
        if ((id0_ < 1) or id0_ >= len(self.__m_objs)): 
            return None
        if (self.__m_objs[id0_] is not None): 
            return self.__m_objs[id0_]
        if (self.__m_obj_pos[id0_] == 0): 
            return None
        ao = AreaTreeObject()
        ao._deserialize(self.__m_data, self.__m_obj_pos[id0_], self)
        self.__m_objs[id0_] = ao
        return ao
    
    def add(self, path : str, ao : 'AreaObject', na : 'NameAnalyzer') -> 'AreaTreeNode':
        if (Utils.isNullOrEmpty(path)): 
            return None
        while len(self.__m_obj_pos) <= ao.id0_:
            self.__m_obj_pos.append(0)
            self.__m_objs.append(None)
        if (ao.id0_ == 49599): 
            pass
        o = self.__m_objs[ao.id0_]
        if (o is None): 
            o = AreaTreeObject._new1(ao.id0_)
            self.__m_objs[ao.id0_] = o
        o.region = ao.region
        o.parent_ids = ao.parent_ids
        o.parent_parent_ids = ao.parent_parent_ids
        o.level = na.level
        o.expired = not ao.actual
        o.status = ao.status
        o.glevel = (Utils.valToEnum(ao.level, GarLevel))
        o.ch_count = (((0 if ao.children_ids is None else len(ao.children_ids))))
        o.typ_id = (ao.typ.id0_)
        if (ao.old_typ is not None): 
            o.alt_typ_id = (ao.old_typ.id0_)
        if (na.miscs is not None and len(na.miscs) > 0): 
            o.miscs = na.miscs
        if (na.types is not None): 
            o.typs = na.types
        res = None
        wrapres5 = RefOutArgWrapper(None)
        inoutres6 = Utils.tryGetValue(self.children, path[0], wrapres5)
        res = wrapres5.value
        if (not inoutres6): 
            res = AreaTreeNode()
            self.children[path[0]] = res
        i = 1
        while i < len(path): 
            rr = None
            if (res.children is None): 
                res.children = dict()
            wraprr3 = RefOutArgWrapper(None)
            inoutres4 = Utils.tryGetValue(res.children, path[i], wraprr3)
            rr = wraprr3.value
            if (not inoutres4): 
                rr = AreaTreeNode._new2(res)
                res.children[path[i]] = rr
            res = rr
            i += 1
        if (res.obj_ids is None): 
            res.obj_ids = list()
        if (not ao.id0_ in res.obj_ids): 
            res.obj_ids.append(ao.id0_)
        return res
    
    def find(self, path : str, correct : bool=False, for_search : bool=False, ignore_non_correct : bool=False) -> 'AreaTreeNode':
        if (Utils.isNullOrEmpty(path)): 
            return None
        res = None
        if (not ignore_non_correct): 
            res = self.__find(None, path, 0)
            if (res is not None): 
                if (((res.obj_ids is not None and len(res.obj_ids) > 0)) or for_search): 
                    return res
            if (not correct or (len(path) < 4)): 
                return None
        wrapres9 = RefOutArgWrapper(None)
        inoutres10 = Utils.tryGetValue(self.children, path[0], wrapres9)
        res = wrapres9.value
        if (not inoutres10): 
            return None
        j = 1
        res1 = None
        while j < len(path): 
            rr = None
            if (not res.loaded): 
                self.__load_node(res)
            if (res.children is None): 
                break
            if (str.isalpha(path[j]) and not str.islower(path[j]) and ((j + 1) < len(path))): 
                for ch in res.children.items(): 
                    if (not str.isalpha(ch[0])): 
                        continue
                    if (str.islower(ch[0])): 
                        continue
                    rr = self.__find(ch[1], path, j)
                    if (rr is None or rr.obj_ids is None or len(rr.obj_ids) == 0): 
                        if (j >= 2): 
                            rr = self.__find(ch[1], path, j - 1)
                    if (rr is None or rr.obj_ids is None or len(rr.obj_ids) == 0): 
                        continue
                    if (res1 is None): 
                        res1 = rr
                    else: 
                        res2 = AreaTreeNode()
                        res2.obj_ids = list(res1.obj_ids)
                        for id0_ in rr.obj_ids: 
                            if (not id0_ in res1.obj_ids): 
                                res2.obj_ids.append(id0_)
                        res1 = res2
            if (path[j] == '$' and path[j - 1] != '@'): 
                if ('@' in res.children): 
                    rr = self.__find(res.children['@'], path, j - 1)
                    if (rr is not None and rr.obj_ids is not None and len(rr.obj_ids) > 0): 
                        if (res1 is None): 
                            res1 = rr
                        else: 
                            res2 = AreaTreeNode()
                            res2.obj_ids = list(res1.obj_ids)
                            for id0_ in rr.obj_ids: 
                                if (not id0_ in res1.obj_ids): 
                                    res2.obj_ids.append(id0_)
                            res1 = res2
            wraprr7 = RefOutArgWrapper(None)
            inoutres8 = Utils.tryGetValue(res.children, path[j], wraprr7)
            rr = wraprr7.value
            if (not inoutres8): 
                break
            res = rr
            j += 1
        if (res1 is not None): 
            return res1
        tmp = io.StringIO()
        i = 0
        first_pass3247 = True
        while True:
            if first_pass3247: first_pass3247 = False
            else: i += 1
            if (not (i < len(path))): break
            if (not str.isalpha(path[i])): 
                continue
            if (str.islower(path[i])): 
                continue
            if (i == 0 or (i + 1) == len(path)): 
                continue
            Utils.setLengthStringIO(tmp, 0)
            print(path, end="", file=tmp)
            Utils.removeStringIO(tmp, i, 1)
            res = self.__find(None, Utils.toStringStringIO(tmp), 0)
            if (res is not None and res.obj_ids is not None and len(res.obj_ids) > 0): 
                return res
        return None
    
    def __find(self, tn : 'AreaTreeNode', path : str, i : int) -> 'AreaTreeNode':
        res = None
        if (tn is None): 
            wrapres11 = RefOutArgWrapper(None)
            inoutres12 = Utils.tryGetValue(self.children, path[i], wrapres11)
            res = wrapres11.value
            if (not inoutres12): 
                return None
        else: 
            res = tn
        j = i + 1
        while j < len(path): 
            rr = None
            if (not res.loaded): 
                self.__load_node(res)
            if (res.children is None): 
                return None
            wraprr13 = RefOutArgWrapper(None)
            inoutres14 = Utils.tryGetValue(res.children, path[j], wraprr13)
            rr = wraprr13.value
            if (not inoutres14): 
                return None
            res = rr
            j += 1
        if (not res.loaded): 
            self.__load_node(res)
        return res
    
    def _get_all_obj_ids_total(self, n : 'AreaTreeNode', res : typing.List[int]) -> None:
        if (not n.loaded): 
            self.__load_node(n)
        if (n.obj_ids is not None): 
            res.extend(n.obj_ids)
        if (n.children is not None): 
            for kp in n.children.items(): 
                self._get_all_obj_ids_total(kp[1], res)
    
    def get_all_obj_ids(self, n : 'AreaTreeNode', suffix : str, street : bool, res : typing.List[int]) -> None:
        if (not n.loaded): 
            self.__load_node(n)
        if (n.children is None): 
            if (n.obj_ids is not None): 
                res.extend(n.obj_ids)
        else: 
            for kp in n.children.items(): 
                if (suffix is not None): 
                    if (kp[0] == '$'): 
                        continue
                    if (kp[0] == '_'): 
                        if (not str.isdigit(suffix[0])): 
                            self.__get_all_obj_ids_after_suffix(kp[1], suffix, street, res)
                        continue
                    if (str.isdigit(kp[0]) and str.isdigit(suffix[0])): 
                        if (kp[0] == suffix[0]): 
                            self.__get_all_obj_ids_after_suffix(kp[1], suffix[1:], street, res)
                        continue
                elif (kp[0] == '$'): 
                    self._get_all_obj_ids_total(kp[1], res)
                    continue
                elif (kp[0] == '@'): 
                    if (not kp[1].loaded): 
                        self.__load_node(kp[1])
                    if (kp[1].obj_ids is not None): 
                        res.extend(kp[1].obj_ids)
                self.get_all_obj_ids(kp[1], suffix, street, res)
    
    def __get_all_obj_ids_after_suffix(self, n : 'AreaTreeNode', suffix : str, street : bool, res : typing.List[int]) -> None:
        i = 0
        while i < len(suffix): 
            if (not n.loaded): 
                self.__load_node(n)
            tn = None
            if (n.children is None): 
                return
            wraptn15 = RefOutArgWrapper(None)
            inoutres16 = Utils.tryGetValue(n.children, suffix[i], wraptn15)
            tn = wraptn15.value
            if (not inoutres16): 
                return
            n = tn
            i += 1
        if (n is not None): 
            self.get_all_obj_ids(n, None, street, res)
    
    def __load_node(self, res : 'AreaTreeNode') -> None:
        if (not res.loaded and res.lazy_pos > 0): 
            res.deserialize(self.__m_data, res.lazy_pos)
        res.loaded = True
    
    def save(self, fname : str) -> None:
        if (self.__m_data is not None): 
            self.__m_data = (None)
        self.__m_strings.clear()
        for o in self.__m_objs: 
            if (o is not None): 
                if (o.typs is not None): 
                    for ty in o.typs: 
                        self.get_string_id(ty)
                if (o.miscs is not None): 
                    for mi in o.miscs: 
                        self.get_string_id(mi)
        with FileStream(fname, "wb") as f: 
            FiasHelper.serialize_int(f, 0)
            FiasHelper.serialize_int(f, 0)
            FiasHelper.serialize_int(f, len(self.__m_strings))
            for s in self.__m_strings: 
                FiasHelper.serialize_string(f, s, False)
            FiasHelper.serialize_int(f, len(self.__m_objs))
            pos0 = f.position
            i = 0
            while i < len(self.__m_objs): 
                FiasHelper.serialize_int(f, 0)
                i += 1
            i = 0
            while i < len(self.__m_objs): 
                if (self.__m_objs[i] is not None): 
                    self.__m_obj_pos[i] = (f.position)
                    self.__m_objs[i]._serialize(f, self)
                i += 1
            f.position = pos0
            i = 0
            while i < len(self.__m_obj_pos): 
                FiasHelper.serialize_int(f, self.__m_obj_pos[i])
                i += 1
            f.position = 4
            FiasHelper.serialize_int(f, f.length)
            f.position = f.length
            FiasHelper.serialize_int(f, len(self.children))
            for kp in self.children.items(): 
                FiasHelper.serialize_short(f, ord(kp[0]))
                kp[1].serialize(f)
        self.close0_()
        gc.collect()
    
    def load(self, fname : str) -> None:
        self.__m_data = FileHelper.load_data_from_file(fname, 0)
        pos = 0
        a0 = int.from_bytes(self.__m_data[pos:pos+4], byteorder="little")
        pos += 4
        pos0 = int.from_bytes(self.__m_data[pos:pos+4], byteorder="little")
        pos += 4
        cou = int.from_bytes(self.__m_data[pos:pos+4], byteorder="little")
        pos += 4
        self.__m_strings.clear()
        while cou > 0: 
            wrappos17 = RefOutArgWrapper(pos)
            s = FiasHelper.deserialize_string_from_bytes(self.__m_data, wrappos17, False)
            pos = wrappos17.value
            self.__m_strings.append(s)
            cou -= 1
        cou = int.from_bytes(self.__m_data[pos:pos+4], byteorder="little")
        pos += 4
        if (cou > 0): 
            self.__m_objs = list()
            self.__m_obj_pos = list()
            while cou > 0: 
                self.__m_obj_pos.append(int.from_bytes(self.__m_data[pos:pos+4], byteorder="little"))
                self.__m_objs.append(None)
                cou -= 1; pos += 4
        pos = pos0
        cou = int.from_bytes(self.__m_data[pos:pos+4], byteorder="little")
        pos += 4
        if (cou == 0): 
            return
        i = 0
        while i < cou: 
            ch = chr(int.from_bytes(self.__m_data[pos:pos+2], byteorder="little"))
            pos += 2
            tn = AreaTreeNode()
            pos = tn.deserialize(self.__m_data, pos)
            self.children[ch] = tn
            i += 1