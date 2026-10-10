"""Versión "Kira viva" del diseño: quita la fecha (2014 — 2026 y su corazón) y cambia la frase en pasado
"Corriste a mi lado cada día" por "Corres a mi lado cada día". Para los vídeos en los que Kira va a ver su cuadro."""
import os, cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
FUENTE=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','fuentes','Caveat.ttf')  # OFL
FRASE='Corres a mi lado cada día'
im=cv2.imread('diseno-chatgpt.webp')
gris=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY); sat=cv2.cvtColor(im,cv2.COLOR_BGR2HSV)[...,1]
tinta=(gris<200)&(sat<70)  # trazos negros; deja fuera el capullo de rosa, que es rosa
m=np.zeros(gris.shape,np.uint8)
# cajas en coordenadas del diseño (1024×1536): fecha · frase · pie de la "C"
for x0,y0,x1,y1 in [(665,40,920,145),(295,1312,760,1376),(295,1376,400,1390)]:
    m[y0:y1,x0:x1]=tinta[y0:y1,x0:x1].astype(np.uint8)*255
m=cv2.dilate(m,np.ones((5,5),np.uint8),iterations=2)
limpio=Image.fromarray(cv2.cvtColor(cv2.inpaint(im,m,9,cv2.INPAINT_TELEA),cv2.COLOR_BGR2RGB))
# frase nueva: manuscrita, a 4× para que los bordes salgan suaves, ligeramente inclinada como la original
K=4; f=ImageFont.truetype(FUENTE,84*K); f.set_variation_by_axes([700])
d=ImageDraw.Draw(Image.new('L',(1,1))); bb=d.textbbox((0,0),FRASE,font=f)
capa=Image.new('L',(bb[2]-bb[0]+40*K,bb[3]-bb[1]+40*K),0)
ImageDraw.Draw(capa).text((20*K-bb[0],20*K-bb[1]),FRASE,font=f,fill=255)
capa=capa.rotate(2.5,Image.BICUBIC,expand=True)
ancho=440; capa=capa.resize((ancho,round(capa.height*ancho/capa.width)),Image.LANCZOS)
cx,cy=527,1348
limpio.paste((22,20,18),(cx-capa.width//2,cy-capa.height//2),capa)
limpio.save('diseno-sin-fecha.png')
