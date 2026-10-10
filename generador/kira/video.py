"""Reel vertical 1080x1920 (≈12 s): Kira corre por la playa → "¿Sabes a dónde?" → su cuadro en la pared.
Si existe clip-dola.mp4 (vídeo de Kira corriendo generado con IA), sustituye a la foto de la playa en la escena 1."""
import os, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
W,H,FPS=1080,1920,30
F_TXT='/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
F_WEB='/usr/share/fonts/opentype/inter/Inter-Medium.otf'
def ease(t): t=min(max(t,0),1); return t*t*(3-2*t)
def kenburns(img,t,z0,z1,fy=0.5):
    """recorte 9:16 con zoom suave de z0 a z1"""
    base=ImageOps.fit(img,(W,H),Image.LANCZOS,centering=(0.5,fy))
    z=z0+(z1-z0)*ease(t); w,h=W/z,H/z
    x=(W-w)/2; y=(H-h)*fy
    return base.transform((W,H),Image.EXTENT,(x,y,x+w,y+h),Image.BICUBIC)
def texto(fr,s,y,size,alpha=1.0,font=F_TXT):
    """texto blanco centrado con sombra suave, estilo subtítulo de reel"""
    if alpha<=0: return fr
    f=ImageFont.truetype(font,size)
    capa=Image.new('RGBA',fr.size,(0,0,0,0)); d=ImageDraw.Draw(capa)
    x=(W-d.textlength(s,font=f))/2
    sh=Image.new('RGBA',fr.size,(0,0,0,0)); ImageDraw.Draw(sh).text((x,y+4),s,font=f,fill=(0,0,0,int(170*alpha)))
    sh=sh.filter(ImageFilter.GaussianBlur(8))
    d.text((x,y),s,font=f,fill=(255,255,255,int(255*alpha)))
    out=fr.convert('RGBA'); out.alpha_composite(sh); out.alpha_composite(capa)
    return out.convert('RGB')
def fade(t,a,b,d=0.35): return ease((t-a)/d)*(1-ease((t-(b-d))/d))
# --- mockup del cuadro en la pared ---
def mockup():
    pared=Image.new('RGB',(W,H)); px=np.zeros((H,W,3),float)
    yy,xx=np.mgrid[0:H,0:W]
    luz=1-0.18*np.hypot((xx-W*0.35)/W,(yy-H*0.25)/H)  # luz cálida desde arriba a la izquierda
    for i,c in enumerate((236,226,212)): px[...,i]=c*luz
    pared=Image.fromarray(px.clip(0,255).astype('uint8'))
    retrato=Image.open('kira-final.jpg').convert('RGB')
    iw=660; ih=round(iw*retrato.height/retrato.width)
    retrato=retrato.resize((iw,ih),Image.LANCZOS)
    pp,mk=56,26  # paspartú y moldura
    cw,ch=iw+2*(pp+mk),ih+2*(pp+mk)
    cuadro=Image.new('RGB',(cw,ch),(28,26,24))
    ImageDraw.Draw(cuadro).rectangle((mk,mk,cw-mk-1,ch-mk-1),fill=(250,248,243))
    cuadro.paste(retrato,(mk+pp,mk+pp))
    ImageDraw.Draw(cuadro).rectangle((mk+pp-2,mk+pp-2,mk+pp+iw+1,mk+pp+ih+1),outline=(220,214,204),width=2)  # bisel
    x,y=(W-cw)//2,250
    sh=Image.new('L',(W,H),0); ImageDraw.Draw(sh).rectangle((x+14,y+30,x+cw+14,y+ch+30),fill=120)
    sh=sh.filter(ImageFilter.GaussianBlur(28))
    pared.paste((60,45,30),(0,0),sh); pared.paste(cuadro,(x,y))
    return pared
if __name__=='__main__':
    playa=Image.open('orig-playa.webp').convert('RGB')
    pelota=Image.open('orig-pelota.webp').convert('RGB')
    pared=mockup()
    clip=None
    if os.path.exists('clip-dola.mp4'):
        raw=subprocess.run(['ffmpeg','-v','error','-i','clip-dola.mp4','-t','4','-vf',f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}',
                            '-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True,check=True).stdout
        clip=[Image.frombytes('RGB',(W,H),raw[i:i+W*H*3]) for i in range(0,len(raw),W*H*3)]
    T1,T2,T3=4.0,2.5,5.5; X=0.5  # duración de escenas y del fundido
    def escena(t):
        if t<T1:
            fr=clip[min(int(t*FPS),len(clip)-1)] if clip else kenburns(playa,t/T1,1.0,1.18,0.45)
            return texto(fr,'Kira va corriendo…',260,78,fade(t,0.3,T1+1))
        t-=T1
        if t<T2:
            fr=kenburns(pelota,t/T2,1.05,1.15,0.35)
            return texto(fr,'¿Sabes a dónde?',260,78,fade(t,0.2,T2+1))
        t-=T2
        fr=kenburns(pared,t/T3,1.12,1.0,0.35)
        fr=texto(fr,'A ver su cuadro',1600,78,fade(t,0.6,T3+1))
        return texto(fr,'kivoa.es',1710,46,fade(t,1.6,T3+1),F_WEB)
    total=T1+T2+T3
    ff=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
        '-c:v','libx264','-preset','slow','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart','kira-reel.mp4'],stdin=subprocess.PIPE)
    cortes=[T1,T1+T2]
    for n in range(int(total*FPS)):
        t=n/FPS; fr=escena(t)
        for c in cortes:  # fundido cruzado de X segundos en cada corte
            if c-X/2<=t<c:
                a=ease((t-(c-X/2))/X); fr=Image.blend(fr,escena(c+0.001),a)
            elif c<=t<c+X/2:
                a=ease((t-(c-X/2))/X); fr=Image.blend(escena(c-0.001),fr,a)
        ff.stdin.write(fr.tobytes())
    ff.stdin.close(); ff.wait()
    pared.save('kira-mockup-pared.jpg',quality=92)
    print('ok',total,'s')
