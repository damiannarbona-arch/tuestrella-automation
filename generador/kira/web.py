"""Imágenes 2000×2000 de Kira para la ficha de Estilo Recuerdo: el cuadro en la pared y sus fotos → su retrato."""
import os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from marca import fuente
N=2000; FONDO=(246,241,233); TINTA=(40,36,32)
final=Image.open('kira-final.jpg').convert('RGB')
def sombra(base,box,r=40,o=(16,30),a=110):
    sh=Image.new('L',base.size,0); ImageDraw.Draw(sh).rectangle((box[0]+o[0],box[1]+o[1],box[2]+o[0],box[3]+o[1]),fill=a)
    base.paste((60,45,30),(0,0),sh.filter(ImageFilter.GaussianBlur(r)))
# 1) cuadro en la pared, marco negro con paspartú
def pared():
    im=Image.new('RGB',(N,N),(236,228,216)); px=im.load()
    g=Image.linear_gradient('L').resize((N,N)).filter(ImageFilter.GaussianBlur(40))
    im=Image.composite(Image.new('RGB',(N,N),(226,216,202)),im,g.point(lambda v:int(v*0.6)))
    ih=1500; iw=round(ih*final.width/final.height); pp,mk=70,34
    cw,ch=iw+2*(pp+mk),ih+2*(pp+mk); x,y=(N-cw)//2,(N-ch)//2-20
    sombra(im,(x,y,x+cw,y+ch))
    cu=Image.new('RGB',(cw,ch),(28,26,24)); d=ImageDraw.Draw(cu)
    d.rectangle((mk,mk,cw-mk-1,ch-mk-1),fill=(250,248,243)); cu.paste(final.resize((iw,ih),Image.LANCZOS),(mk+pp,mk+pp))
    d.rectangle((mk+pp-3,mk+pp-3,mk+pp+iw+2,mk+pp+ih+2),outline=(220,214,204),width=3)
    im.paste(cu,(x,y)); return im
# 2) sus fotos → su retrato
def sus_fotos():
    im=Image.new('RGB',(N,N),FONDO); d=ImageDraw.Draw(im)
    t='Sus fotos'; f=fuente(84,b'Bold'); d.text((470-d.textlength(t,font=f)/2,150),t,font=f,fill=TINTA)
    t='Su retrato'; d.text((1475-d.textlength(t,font=f)/2,150),t,font=f,fill=TINTA)
    fotos=['orig-jardin.webp','orig-sofa.webp','orig-pelota.webp','orig-playa.webp']
    s=370; pos=[(70,330),(470,330),(70,800),(470,800)]; rot=[-3,2.5,2,-2.5]
    for f_,(px,py),a in zip(fotos,pos,rot):
        ph=ImageOps.fit(Image.open(f_).convert('RGB'),(s,s),Image.LANCZOS,centering=(0.5,0.3))
        p=Image.new('RGBA',(s+36,s+36),(255,253,248,255)); p.paste(ph,(18,18))
        sh=Image.new('RGBA',(p.width+60,p.height+60),(0,0,0,0)); sh.paste((40,30,20,80),(30,30,30+p.width,30+p.height))
        sh=sh.filter(ImageFilter.GaussianBlur(12)).rotate(-a,Image.BICUBIC,expand=True); p=p.rotate(-a,Image.BICUBIC,expand=True)
        im.paste(sh,(px-20,py-10),sh); im.paste(p,(px,py),p)
    # flecha
    d.line((905,880,965,880),fill=TINTA,width=12); d.polygon([(995,880),(955,850),(955,910)],fill=TINTA)
    ih=1380; iw=round(ih*final.width/final.height); x,y=1475-iw//2,310
    sombra(im,(x,y,x+iw,y+ih),r=30,o=(10,20),a=90)
    im.paste(final.resize((iw,ih),Image.LANCZOS),(x,y))
    f3=fuente(44,b'Medium')
    d.text((470-d.textlength('Foto principal + 3 secundarias',font=f3)/2,1290),'Foto principal + 3 secundarias',font=f3,fill=(95,90,84))
    f4=fuente(38,b'Medium'); t='Diseño de ejemplo'
    d.text((N-60-d.textlength(t,font=f4),N-80),t,font=f4,fill=(150,144,136))
    return im
pared().save('kira-web-1-pared.jpg',quality=90)
sus_fotos().save('kira-web-2-sus-fotos.jpg',quality=90)
