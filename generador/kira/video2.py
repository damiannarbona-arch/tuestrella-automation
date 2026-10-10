"""Reel v2 con los clips de Dola: playa ("¿Dónde va Kira?") → césped (salta y sale corriendo por la derecha)
→ la pared con su cuadro entra empujando desde la derecha, en la dirección en la que se va Kira."""
import subprocess
from PIL import Image
from video import W,H,FPS,F_WEB,ease,fade,kenburns,texto,mockup
def frames(f,ss,t):
    """decodifica un tramo; el recorte de 1234 px de alto deja fuera la marca de agua de abajo a la derecha"""
    raw=subprocess.run(['ffmpeg','-v','error','-ss',str(ss),'-t',str(t),'-i',f,'-vf',
        f'crop=694:1234:13:0,scale={W}:{H}:flags=lanczos,fps={FPS}','-f','rawvideo','-pix_fmt','rgb24','-'],
        capture_output=True,check=True).stdout
    n=W*H*3; return [Image.frombytes('RGB',(W,H),raw[i:i+n]) for i in range(0,len(raw)-n+1,n)]
# (clip, inicio, duración) — el césped arranca justo antes del salto y acaba cuando Kira ya ha salido del plano
PLAYA=('dola-playa.mp4',1.0,3.5); CESPED=('dola-cesped.mp4',6.0,3.4); T3=4.5; X=0.4; P=0.5
playa=frames(*PLAYA); cesped=frames(*CESPED); pared=mockup()
T1,T2=len(playa)/FPS,len(cesped)/FPS; total=T1+T2+T3
def pared_fr(t):
    fr=kenburns(pared,t/T3,1.06,1.0,0.35)
    fr=texto(fr,'A ver su cuadro',1600,78,fade(t,0.5,T3+1))
    return texto(fr,'kivoa.es',1710,46,fade(t,1.4,T3+1),F_WEB)
def escena(t):
    if t<T1: return texto(playa[min(int(t*FPS),len(playa)-1)],'¿Dónde va Kira?',250,92,1.0 if t<T1-0.5 else 1-ease((t-T1+0.5)/0.5))
    t-=T1
    if t<T2-P: return cesped[int(t*FPS)]
    # empuje lateral: el césped sale por la izquierda y la pared entra por la derecha
    a=ease((t-(T2-P))/P); dx=round(W*a); fr=Image.new('RGB',(W,H))
    fr.paste(cesped[min(int(t*FPS),len(cesped)-1)],(-dx,0)); fr.paste(pared_fr(0),(W-dx,0))
    return fr
ff=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
    '-c:v','libx264','-preset','slow','-crf','18','-pix_fmt','yuv420p','video-tmp.mp4'],stdin=subprocess.PIPE)
for n in range(int(total*FPS)):
    t=n/FPS
    if t>=T1+T2: fr=pared_fr(t-T1-T2)
    else:
        fr=escena(t)
        if T1-X/2<=t<T1+X/2:  # fundido cruzado playa → césped
            a=ease((t-(T1-X/2))/X)
            fr=Image.blend(escena(min(t,T1-0.001)),escena(max(t,T1+0.001)),a)
    ff.stdin.write(fr.tobytes())
ff.stdin.close(); ff.wait()
# audio de Dola: olas de la playa → césped, y se apaga sobre el cuadro
fc=(f"[1:a]atrim={PLAYA[1]}:{PLAYA[1]+T1},asetpts=PTS-STARTPTS[a];"
    f"[2:a]atrim={CESPED[1]}:{CESPED[1]+T2},asetpts=PTS-STARTPTS[b];"
    f"[a][b]acrossfade=d={X}[ab];[ab]apad,atrim=0:{total},afade=t=out:st={T1+T2-0.3}:d=1.5[out]")
subprocess.run(['ffmpeg','-y','-v','error','-i','video-tmp.mp4','-i',PLAYA[0],'-i',CESPED[0],'-filter_complex',fc,
    '-map','0:v','-map','[out]','-c:v','copy','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart','kira-reel-v2.mp4'],check=True)
import os; os.remove('video-tmp.mp4')
print('ok',round(total,2),'s')
