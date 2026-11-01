import re
def boxes(s):
    out=[]; i=0
    while True:
        i=s.find('<div class="box example">',i)
        if i<0: return out
        d=0; j=i
        for m in re.finditer(r'<div\b|</div>', s[i:]):
            d += 1 if m.group(0)=='<div' else -1
            if d==0: j=i+m.end(); break
        # section id
        h=s.rfind('<h2 id="',0,i); sid=s[h+8:s.find('"',h+8)] if h>=0 else ''
        out.append((i,j,sid,s[i:j])); i=j
