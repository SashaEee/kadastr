# SDK Pullenti Address, version 4.31, august 2025. Copyright (c) 2013-2025, Pullenti. All rights reserved.
# Non-Commercial Freeware and Commercial Software.
# This class is generated using the converter Unisharping (www.unisharping.ru) from Pullenti C# project.
# The latest version of the code is available on the site www.pullenti.ru

from pullenti.unisharp.Streams import Stream

from pullenti.address.internal.FiasHelper import FiasHelper

class AreaTreeNode:
    
    def __init__(self) -> None:
        self.obj_ids = None
        self.parent = None;
        self.children = None
        self.lazy_pos = 0
        self.loaded = False
    
    def __str__(self) -> str:
        return "Objs={0}, Chils={1}{2}".format((0 if self.obj_ids is None else len(self.obj_ids)), (0 if self.children is None else len(self.children)), (" (loaded)" if self.loaded else ""))
    
    def serialize(self, f : Stream) -> None:
        FiasHelper.serialize_int(f, (0 if self.obj_ids is None else len(self.obj_ids)))
        if (self.obj_ids is not None): 
            for v in self.obj_ids: 
                FiasHelper.serialize_int(f, v)
        FiasHelper.serialize_short(f, ((0 if self.children is None else len(self.children))))
        if (self.children is not None): 
            for kp in self.children.items(): 
                FiasHelper.serialize_short(f, ord(kp[0]))
                p0 = f.position
                FiasHelper.serialize_int(f, 0)
                kp[1].serialize(f)
                p1 = f.position
                f.position = p0
                FiasHelper.serialize_int(f, p1)
                f.position = p1
    
    def deserialize(self, dat : bytearray, pos : int) -> int:
        cou = int.from_bytes(dat[pos:pos+4], byteorder="little")
        pos += 4
        if (cou > 0x7000 or (cou < 0)): 
            pass
        if (cou > 0): 
            self.obj_ids = list()
            i = 0
            while i < cou: 
                self.obj_ids.append(int.from_bytes(dat[pos:pos+4], byteorder="little"))
                i += 1; pos += 4
        cou = (int.from_bytes(dat[pos:pos+2], byteorder="little"))
        pos += 2
        if (cou == 0): 
            return pos
        if (cou > 0x1000 or (cou < 0)): 
            pass
        i = 0
        while i < cou: 
            ch = chr(int.from_bytes(dat[pos:pos+2], byteorder="little"))
            pos += 2
            p1 = int.from_bytes(dat[pos:pos+4], byteorder="little")
            pos += 4
            tn = AreaTreeNode()
            tn.lazy_pos = pos
            tn.loaded = False
            if (self.children is None): 
                self.children = dict()
            self.children[ch] = tn
            tn.parent = self
            pos = p1
            i += 1
        self.loaded = True
        return pos
    
    @staticmethod
    def _new2(_arg1 : 'AreaTreeNode') -> 'AreaTreeNode':
        res = AreaTreeNode()
        res.parent = _arg1
        return res