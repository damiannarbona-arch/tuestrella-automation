"""Elementos de marca para los reels: rótulos con el estilo de TikTok (TikTok Sans en caja blanca redondeada)
y el cierre de Kivoa, que va SIEMPRE al final de cada vídeo."""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont
AQUI=os.path.dirname(os.path.abspath(__file__))
TT=os.path.join(AQUI,'fuentes','TikTokSans.ttf')  # OFL, de github.com/google/fonts
EMOJI='/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf'
_cache={}
def fuente(size,peso=b'Bold'):
    k=(size,peso)
    if k not in _cache:
        f=ImageFont.truetype(TT,size); f.set_variation_by_name(peso); _cache[k]=f
    return _cache[k]
def _emoji(ch,alto):
    f=ImageFont.truetype(EMOJI,109)
    im=Image.new('RGBA',(160,160),(0,0,0,0)); ImageDraw.Draw(im).text((10,10),ch,font=f,embedded_color=True)
    im=im.crop(im.getbbox()); return im.resize((round(im.width*alto/im.height),alto),Image.LANCZOS)
def _es_emoji(c): return ord(c)>0x2100
def rotulo(fr,lineas,y,size=64,alpha=1.0,pop=1.0,caja=(255,255,255),tinta=(18,18,18)):
    """rótulo estilo TikTok: cada línea en su caja redondeada, centrada; pop escala el bloque (0-1 → aparece)"""
    if alpha<=0.01: return fr
    f=fuente(size); pad_x,pad_y,r=round(size*0.42),round(size*0.22),round(size*0.32)
    capas=[]
    for ln in lineas:
        ln=ln.replace('\ufe0f',''); txt=''.join(c for c in ln if not _es_emoji(c)).rstrip(); ems=[c for c in ln if _es_emoji(c)]
        w=ImageDraw.Draw(Image.new('L',(1,1))).textlength(txt,font=f)
        eh=round(size*1.0); ew=sum(_emoji(e,eh).width+8 for e in ems)
        a,d=f.getmetrics(); h=a+d
        im=Image.new('RGBA',(round(w+ew+2*pad_x),h+2*pad_y),(0,0,0,0)); dr=ImageDraw.Draw(im)
        dr.rounded_rectangle((0,0,im.width-1,im.height-1),r,fill=caja+(255,))
        dr.text((pad_x,pad_y),txt,font=f,fill=tinta+(255,))
        x=pad_x+w+8
        for e in ems:
            ei=_emoji(e,eh); im.alpha_composite(ei,(round(x),pad_y+(h-eh)//2+2)); x+=ei.width+8
        capas.append(im)
    gap=-round(size*0.06)  # las cajas se tocan, como en TikTok
    W=max(c.width for c in capas); H=sum(c.height for c in capas)+gap*(len(capas)-1)
    bloque=Image.new('RGBA',(W,H),(0,0,0,0)); yy=0
    for c in capas: bloque.alpha_composite(c,((W-c.width)//2,yy)); yy+=c.height+gap
    if pop<1:
        s=max(pop,0.05); bloque=bloque.resize((max(1,round(W*s)),max(1,round(H*s))),Image.LANCZOS)
    if alpha<1: bloque.putalpha(bloque.getchannel('A').point(lambda v:int(v*alpha)))
    out=fr.convert('RGBA')
    sh=Image.new('RGBA',out.size,(0,0,0,0)); sh.alpha_composite(bloque,((out.width-bloque.width)//2,round(y+(H-bloque.height)/2)+6))
    sh=Image.eval(sh.getchannel('A'),lambda v:int(v*0.35)).filter(ImageFilter.GaussianBlur(10))
    out.paste((0,0,0),(0,0),sh)
    out.alpha_composite(bloque,((out.width-bloque.width)//2,round(y+(H-bloque.height)/2)))
    return out.convert('RGB')
def cierre(fr,t,dur=0.5):
    """franja final de Kivoa: marca, qué hacemos, garantías y dónde comprar. t = segundos desde que empieza"""
    a=min(max(t/dur,0),1); a=a*a*(3-2*a)
    if a<=0: return fr
    W,H=fr.size; ph=560; y0=H-ph+round((1-a)*120)
    out=fr.convert('RGBA'); p=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(p)
    d.rounded_rectangle((40,y0,W-40,y0+ph+60),48,fill=(255,253,248,int(245*a)))
    def c(txt,y,size,peso,col):
        f=fuente(size,peso); d.text(((W-d.textlength(txt,font=f))/2,y0+y),txt,font=f,fill=col+(int(255*a),))
    c('KIVOA',40,96,b'Black',(24,22,20))
    c('Retratos personalizados de tu mascota',160,42,b'SemiBold',(60,56,52))
    c('Vista previa en 48 h · nada se imprime sin tu OK',236,34,b'Medium',(95,90,84))
    c('Enmarcado y listo para colgar · Envío gratis',284,34,b'Medium',(95,90,84))
    f=fuente(52,b'Bold'); txt='kivoa.es'; bw=d.textlength(txt,font=f)+90
    d.rounded_rectangle(((W-bw)/2,y0+360,(W+bw)/2,y0+446),43,fill=(24,22,20,int(255*a)))
    d.text(((W-d.textlength(txt,font=f))/2,y0+372),txt,font=f,fill=(255,255,255,int(255*a)))
    c('También en Etsy: ByKivoa',470,32,b'Medium',(95,90,84))
    out.alpha_composite(p); return out.convert('RGB')
