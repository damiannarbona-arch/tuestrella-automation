"""Reel v4: como la v3, con rótulos estilo TikTok, gancho A/B y el cierre de Kivoa.
Uso: python3 video4.py A|B [--sin-fecha] [--sin-audio]
  --sin-fecha: usa kira-final-sin-fecha.jpg (Kira viva: sin años en el cuadro)
  --sin-audio: sin el audio de Dola, para poner la música desde TikTok
Reel v3 (≈10 s, cortes rápidos): playa → césped (Kira sale corriendo) → sus fotos caen como recuerdos sobre el césped
→ la foto principal se convierte en el retrato y las polaroids vuelan a su hueco → zoom hacia atrás: el cuadro en la pared."""
import math, os, subprocess, sys, numpy as np
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from marca import rotulo, cierre
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from video import W,H,FPS,F_WEB,ease,fade,texto,frames
from detect import quads, refine
K=2; W2,H2=W*K,H*K  # la pared se dibuja al doble para que el zoom hacia atrás salga nítido
BORDE=(254,250,242)
def ease_out_back(t):
    t=min(max(t,0),1); c=1.7; return 1+(c+1)*(t-1)**3+c*(t-1)**2
# ---------- retrato y pared en alta ----------
SIN_FECHA='--sin-fecha' in sys.argv; SIN_AUDIO='--sin-audio' in sys.argv
final=Image.open('kira-final-sin-fecha.jpg' if SIN_FECHA else 'kira-final.jpg').convert('RGB')           # 2048×3072, diseño ×2
S=final.width/1024
slots={k:np.array(refine(q)[0])*S for k,q in quads.items()}  # esquinas de cada hueco en coordenadas de kira-final
vacio=final.copy(); d=ImageDraw.Draw(vacio)
for q in slots.values(): d.polygon([tuple(p) for p in q],fill=BORDE)  # huecos vacíos, a la espera de sus fotos
IW=1320; IH=round(IW*final.height/final.width); PP,MK=112,52
CW,CH=IW+2*(PP+MK),IH+2*(PP+MK); CX,CY=(W2-CW)//2,500; RX,RY=CX+MK+PP,CY+MK+PP  # RX,RY: esquina del retrato
HH=H2+700
def pared(retrato):
    yy,xx=np.mgrid[0:HH,0:W2]
    luz=1-0.18*np.hypot((xx-W2*0.35)/W2,(yy-HH*0.22)/HH)
    px=np.stack([c*luz for c in (236,226,212)],-1)
    img=Image.fromarray(px.clip(0,255).astype('uint8'))
    sh=Image.new('L',(W2,HH),0); ImageDraw.Draw(sh).rectangle((CX+28,CY+60,CX+CW+28,CY+CH+60),fill=120)
    img.paste((60,45,30),(0,0),sh.filter(ImageFilter.GaussianBlur(56)))
    cu=Image.new('RGB',(CW,CH),(28,26,24)); dd=ImageDraw.Draw(cu)
    dd.rectangle((MK,MK,CW-MK-1,CH-MK-1),fill=(250,248,243))
    cu.paste(retrato.resize((IW,IH),Image.LANCZOS),(MK+PP,MK+PP))
    dd.rectangle((MK+PP-4,MK+PP-4,MK+PP+IW+3,MK+PP+IH+3),outline=(220,214,204),width=4)
    img.paste(cu,(CX,CY)); return img
pared_vacia,pared_llena=pared(vacio),pared(final)
# encuadre inicial: el retrato ocupa todo el ancho de la pantalla
BW=IW; BH=BW*H/W; B0=(RX,RY+IH/2-BH/2,RX+BW,RY+IH/2+BH/2); B1=(0,300,W2,H2+300)  # al final el cuadro queda arriba y deja sitio al cierre
def vista(img,box): return img.resize((W,H),Image.LANCZOS,box=tuple(box))
def a_pantalla(p):
    """coordenadas de kira-final → pantalla, con el encuadre inicial"""
    p=np.asarray(p,float); return (p*IW/final.width+[RX-B0[0],RY-B0[1]])*W/BW
def geo(q):
    q=a_pantalla(q); tl,tr,br,bl=q
    v=(tr-tl)+(br-bl); ang=math.degrees(math.atan2(v[1],v[0]))
    return q.mean(0),ang,(np.linalg.norm(tr-tl)+np.linalg.norm(br-bl))/2,(np.linalg.norm(bl-tl)+np.linalg.norm(br-tr))/2
# ---------- polaroids ----------
# (foto, hueco o None si es la principal, foco vertical, posición en el montón, ángulo en el montón)
# la principal cae la última, encima del montón y en el centro
FOTOS=[('orig-sofa.webp','p1',0.25,(330,640),-9),
       ('orig-pelota.webp','p2',0.35,(760,720),7),
       ('orig-playa.webp','p3',0.30,(380,1290),5),
       ('orig-jardin.webp',None,0.30,(620,1080),-3)]
PW=470  # ancho de la foto en el montón
pol=[]
for f,k,fy,pos,ang in FOTOS:
    if k: c,a,w,h=geo(slots[k]); asp=w/h
    else:
        asp=0.8; h=900; w=h*asp; c=a_pantalla([final.width*0.52,final.height*0.33]); a=0  # cara del retrato
    foto=ImageOps.fit(Image.open(f).convert('RGB'),(round(PW*2),round(PW*2/asp)),Image.LANCZOS,centering=(0.5,fy))
    pol.append(dict(foto=foto,pile=(np.array(pos,float),ang,PW,PW/asp),slot=(np.asarray(c),a,w,h),principal=k is None))
def dibuja(fr,foto,c,ang,w,h,alpha=1.0,b=None):
    """polaroid: foto w×h con marco crema, girada ang grados (sentido de las agujas), con sombra"""
    if alpha<=0.01 or w<4: return
    b=max(2,round(w*0.045)) if b is None else b
    p=Image.new('RGBA',(round(w)+2*b,round(h)+2*b),BORDE+(255,))
    p.paste(foto.resize((round(w),round(h)),Image.LANCZOS),(b,b))
    sh=Image.new('RGBA',(p.width+80,p.height+80),(0,0,0,0)); sh.paste((40,30,20,90),(40,40,40+p.width,40+p.height))
    sh=sh.filter(ImageFilter.GaussianBlur(14)).rotate(-ang,Image.BICUBIC,expand=True)
    p=p.rotate(-ang,Image.BICUBIC,expand=True)
    if alpha<1:
        for im in (p,sh): im.putalpha(im.getchannel('A').point(lambda v:int(v*alpha)))
    fr.alpha_composite(sh,(round(c[0]-sh.width/2+8),round(c[1]-sh.height/2+16)))
    fr.alpha_composite(p,(round(c[0]-p.width/2),round(c[1]-p.height/2)))
def lerp(a,b,t): return a+(b-a)*t
# ---------- clips ----------
PLAYA=('dola-playa.mp4',1.0,1.9); CESPED=('dola-cesped.mp4',6.4,3.05,1.5)  # el césped va a 1,5×
playa=frames(*PLAYA); cesped=frames(*CESPED)
fondo=Image.blend(cesped[-1].filter(ImageFilter.GaussianBlur(14)),Image.new('RGB',(W,H),(30,25,15)),0.25)  # césped vacío, desenfocado
T1=len(playa)/FPS; T2=len(cesped)/FPS
DROP=0.32; T3=DROP*len(pol)+0.45   # caen las 4 fotos
T4=1.9                              # la foto principal se vuelve retrato y las polaroids vuelan a su hueco
T5=1.4; T6=2.6                      # zoom hacia atrás · cierre de Kivoa
total=T1+T2+T3+T4+T5+T6
VAR=([a for a in sys.argv[1:] if not a.startswith('--')] or ['A'])[0].upper()
SALIDA=f'kira-reel-v4{VAR}'+('-sin-fecha' if SIN_FECHA else '')+('-sin-audio' if SIN_AUDIO else '')+'.mp4'
TXT={'A':dict(h1=['¿A dónde va Kira','con tanta prisa? 👀'],h2=['Alguien le ha preparado','una sorpresa…'],fin=['¡A ver su cuadro! 🖼️']),
     'B':dict(h1=['Mándanos 4 fotos','de tu perro…'],h2=['…y mira lo que','hacemos con ellas 👀'],fin=['Su cuadro, listo','para colgar 🖼️'])}[VAR]
def pop(t): return 0.75+0.25*ease_out_back(t/0.25)
def sacudida(t):
    """pequeño golpe de cámara cada vez que cae una foto"""
    dx=dy=0.0
    for i in range(len(pol)):
        u=t-(i*DROP+0.2)
        if 0<=u<0.25: e=math.exp(-u*14)*math.sin(u*70); dx+=9*e; dy+=14*e
    return round(dx),round(dy)
def escena(t):
    if t<T1: return rotulo(playa[min(int(t*FPS),len(playa)-1)],TXT['h1'],230,70,pop=pop(t))
    t-=T1
    if t<T2: return rotulo(cesped[min(int(t*FPS),len(cesped)-1)],TXT['h2'],230,70,pop=pop(t))
    t-=T2
    if t<T3:  # caen los recuerdos
        fr=fondo.convert('RGBA')
        for i,p in enumerate(pol):
            u=(t-i*DROP)/0.22
            if u<=0: continue
            c,a,w,h=p['pile']; s=lerp(1.6,1.0,ease_out_back(u))
            dibuja(fr,p['foto'],c,a+(1-min(u,1))*12,w*s,h*s,min(u*2,1))
        dx,dy=sacudida(t); fr=fr.convert('RGB')
        if dx or dy: fr=fr.transform(fr.size,Image.AFFINE,(1,0,-dx,0,1,-dy),Image.BICUBIC)
        return rotulo(fr,['Sus mejores momentos…'],230,66,pop=pop(t))
    t-=T3
    if t<T4:  # se montan en el cuadro
        a=ease(t/0.7)
        fr=Image.blend(fondo,vista(pared_vacia,B0),a).convert('RGBA')
        orden=[p for p in pol if not p['principal']]+[p for p in pol if p['principal']]
        for p in orden:
            if p['principal']:   # crece hacia la cara del retrato y se funde con él
                u=ease(t/0.7); c0,a0,w0,h0=p['pile']; c1,a1,w1,h1=p['slot']
                dibuja(fr,p['foto'],lerp(c0,c1,u),lerp(a0,a1,u),lerp(w0,w1,u),lerp(h0,h1,u),1-ease((t-0.45)/0.45))
            else:
                i=orden.index(p); u=ease((t-0.55-i*0.15)/0.45)
                c0,a0,w0,h0=p['pile']; c1,a1,w1,h1=p['slot']
                b0=round(w0*0.045); b1=max(2,round(w1*0.06))  # al aterrizar el marco coincide con el del diseño
                dibuja(fr,p['foto'],lerp(c0,c1,u),lerp(a0,a1,u),lerp(w0,w1,u),lerp(h0,h1,u),1-ease((t-1.45)/0.2),round(lerp(b0,b1,u)))
        fr=fr.convert('RGB')
        if t>1.4: fr=Image.blend(fr,vista(pared_llena,B0),ease((t-1.4)/0.2))
        return rotulo(fr,['…en un solo cuadro'],150,66,pop=pop(t))
    t-=T4
    u=ease(min(t/T5,1))
    fr=vista(pared_llena,[lerp(x0,x1,u) for x0,x1 in zip(B0,B1)])
    fr=rotulo(fr,TXT['fin'],1420,70,alpha=1-ease((t-T5-0.1)/0.3),pop=pop(t-0.5) if t>0.5 else 0.01)
    return cierre(fr,t-T5-0.35)  # entra cuando ya se ha ido el rótulo
ff=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
    '-c:v','libx264','-preset','slow','-crf','18','-pix_fmt','yuv420p',f'video-tmp-{VAR}.mp4'],stdin=subprocess.PIPE)
for n in range(round(total*FPS)): ff.stdin.write(escena(n/FPS).tobytes())
ff.stdin.close(); ff.wait()
fc=(f"[1:a]atrim={PLAYA[1]}:{PLAYA[1]+T1},asetpts=PTS-STARTPTS[a];"
    f"[2:a]atrim={CESPED[1]}:{CESPED[1]+CESPED[2]},asetpts=PTS-STARTPTS,atempo={CESPED[3]}[b];"
    f"[a][b]concat=n=2:v=0:a=1,apad,atrim=0:{total},afade=t=out:st={T1+T2-0.2}:d=1.2[out]")
if SIN_AUDIO:
    subprocess.run(['ffmpeg','-y','-v','error','-i',f'video-tmp-{VAR}.mp4','-c:v','copy','-an','-movflags','+faststart',SALIDA],check=True)
else:
    subprocess.run(['ffmpeg','-y','-v','error','-i',f'video-tmp-{VAR}.mp4','-i',PLAYA[0],'-i',CESPED[0],'-filter_complex',fc,
        '-map','0:v','-map','[out]','-c:v','copy','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',SALIDA],check=True)
import os; os.remove(f'video-tmp-{VAR}.mp4')
print('ok',round(total,2),'s',[round(x,2) for x in (T1,T2,T3,T4,T5)])
