
class page:
    def __init__(self):
        self.h = 0
        self.w = 0
        self.lock = False
        self.mode = ''
        # in units of fontsize 12 pt
        self.char_width = 7.2/12.
        self.fontsize = 12
        self.line_skip = 2
        self.vpos = 0
        
    def next_line(self):
        self.vpos += self.fontsize + self.line_skip
        if self.vpos > self.h:
            return False
        return True
    
    def chars_per_line(self):
        cw = self.char_width * self.fontsize
        return int(self.w / cw)
    
    def str_width(self, n):
        return self.char_width * n * self.fontsize
    
    def fits(self, h):
        return h < self.h - self.vpos

    def move_vpos(self, h):
        self.vpos += h


class figure:
    def __init__(self, fname):
        self.ps = [s.rstrip() for s in open(fname, 'r').readlines()]
        while (self.ps[0][0:13]!='%%BoundingBox'):
            self.ps.pop(0)
        s = self.ps[0].rstrip().split(" ")
        self.box = [int(_s) for _s in s[1:]]

        self.height = self.box[3] - self.box[1]
        self.ps.remove('showpage')

        self.idx = self.ps.index('%%EndProlog')
        if (self.ps[self.idx+1]=='mpldict begin'):
            self.idx += 2
        else:
            raise
    
    def set_origin(self, vpos):
        self.ps[self.idx] = f"{self.box[0]} {vpos-self.height} translate"
        
    def __call__(self):
        return ["gsave"] + self.ps + ["grestore"]
