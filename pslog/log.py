import os
from datetime import date
import sys

from .utils import page, figure

__all__ = ['LOG']

cm2pt = 1./2.54 * 72.
paper_size = {
    'a4': {
        'width': 595,
        'height': 842,
    }
}


class stdout_duplicator(object):
    def __init__(self, log):
        self.terminal = sys.stdout
        self.log = log
        
    def write(self, message):
        self.terminal.write(message)
        self.log(message.rstrip())

    def flush(self):
        self.terminal.flush()


class LOG:
    def __init__(self, fmt='a4', fontsize=10):
        self.left = int(2*cm2pt)
        self.top = int(2*cm2pt)
        self.fontsize = fontsize
        self.format = fmt
        self.height = paper_size[fmt]['height']
        self.width = paper_size[fmt]['width']

        self.stack = []
        self.page = page()
        self.set_page()
        
        self.stdout_cache = None

    def set_page(self):
        self.page.h = self.height - 2*self.top
        self.page.w = self.width - 2*self.left
        self.page.vpos = 0
        
    def set_margin_left_cm(self, m):
        self.left = int(m * cm2pt)
        self.set_page()
        
    def set_margin_top_cm(self, m):
        self.top = int(m * cm2pt)
        self.set_page()
        
    def set_fontsize(self, fs):
        self.fontsize = int(fs)
        
    def get_vpos(self):
        return self.height - self.top - self.page.vpos
    
    def new_page(self):
        self.stack.append("showpage")
        self.page.vpos = 0
        
    def push_font(self, fs):
        self.stack.append(f"/Courier findfont")
        self.stack.append(f"{fs} scalefont")
        self.stack.append(f"setfont")
        self.page.fontsize = fs
        
    def push_line(self, line, ofs=0):
        if not self.page.next_line():
            self.new_page()
        self.stack.append(f"{self.left + ofs} {self.get_vpos()} moveto")
        self.stack.append(f"({line}) show")
        
    def message(self, text, mode='text', fontsize=None, align='left'):
        if (self.page.mode != mode):
            self.push_font(self.fontsize if fontsize is None else fontsize)
            self.page.mode = mode
        n = 0
        nchars = self.page.chars_per_line()
        while (n < len(text)):
            ofs = 0
            if align=='right':
                ofs = self.page.w - self.page.str_width(len(text[n:n+nchars]))
            elif align=='center':
                ofs = (self.page.w - self.page.str_width(len(text[n:n+nchars])))/2
            self.push_line(text[n:n+nchars], ofs)
            n += nchars

            
    def start_capture(self):
        self.stdout_cache = sys.stdout
        sys.stdout = stdout_duplicator(self.message)
        
    def end_capture(self):
        sys.stdout = self.stdout_cache
        self.stdout_cache = None
        
    def make_title(self, title='Title', author='Author'):
        fs = int(self.fontsize*1.8)
        ls = self.page.line_skip
        self.page.line_skip = 6
        self.message(title, 'title', fontsize=fs, align='center')
        self.message(author, 'text', align='center')
        self.message(date.today().strftime("%B %d, %Y"), 'text', align='center')
        self.message(os.uname()[1], 'text', align='right')
        self.page.line_skip = ls
        
    def pyplot_figure(self, pyplot):
        self.page.mode = 'figure'
        pyplot.savefig('tmp.eps')
        fig = figure('tmp.eps')
        if not self.page.fits(fig.height):
            self.new_page()
        fig.set_origin(self.get_vpos())
        self.stack.extend(fig())
        self.page.move_vpos(fig.height)
        os.remove('tmp.eps')
        
    def save(self, fname, pdf=False):
        basename = os.path.splitext(fname)[0]
        with open(f"{basename}.ps", 'w') as f:
            f.write('%!PS-Adobe-3.0\n')
            f.write(f"<< /PageSize [{self.width} {self.height}] >> setpagedevice\n")
            f.write("\n".join(self.stack))
            f.write("\nshowpage\n")
            f.write("%%EOF")
            
        if pdf:
            if (os.popen('which gs').read()!=''):
                out = os.popen(f"gs -o {basename}.pdf -sDEVICE=pdfwrite {basename}.ps").read()
                print('pslog: Converting to PDF')
                print(out)
                os.remove(f"{basename}.ps")
            else:
                print('pslog: gs command not found. No PDF file generated')