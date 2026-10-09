"""Sustituye las fotos de las polaroids del diseño de ChatGPT por las fotos originales, sin alterarlas.
A diferencia de Penny, no se redibuja el marco: cada foto se proyecta dentro del hueco detectado (detect.py),
así se conservan el marco, la sombra y la textura del diseño."""
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from detect import quads, refine
S=2  # trabajamos al doble de resolución para que las fotos originales queden nítidas
# hueco -> (foto original, foco vertical del recorte 0-1)
FOTOS={'p1':('orig-sofa.webp',0.25),'p2':('orig-pelota.webp',0.35),'p3':('orig-playa.webp',0.30)}
base=Image.open('diseno-chatgpt.webp').convert('RGB')
base=base.resize((base.width*S,base.height*S),Image.LANCZOS)
def coefs(dst,src):
    """coeficientes de PIL PERSPECTIVE que llevan cada punto de salida (dst) al de entrada (src)"""
    A=[];B=[]
    for (x,y),(u,v) in zip(dst,src):
        A+=[[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]; B+=[u,v]
    return np.linalg.solve(np.array(A,float),np.array(B,float)).tolist()
for k,(f,fy) in FOTOS.items():
    q,_=refine(quads[k])
    q=np.array(q)*S
    c=q.mean(0); q=c+(q-c)*1.006  # 0,6 % de solape para tapar el antialiasing del borde
    w=round((np.linalg.norm(q[1]-q[0])+np.linalg.norm(q[2]-q[3]))/2)
    h=round((np.linalg.norm(q[3]-q[0])+np.linalg.norm(q[2]-q[1]))/2)
    foto=ImageOps.fit(Image.open(f).convert('RGB'),(w*2,h*2),Image.LANCZOS,centering=(0.5,fy))
    src=[(0,0),(foto.width,0),(foto.width,foto.height),(0,foto.height)]
    capa=foto.transform(base.size,Image.PERSPECTIVE,coefs(q.tolist(),src),Image.BICUBIC)
    # máscara con antialiasing: se dibuja a 4x y se reduce
    m=Image.new('L',(base.width*4,base.height*4),0)
    ImageDraw.Draw(m).polygon([tuple(p*4) for p in q],fill=255)
    m=m.resize(base.size,Image.LANCZOS)
    base.paste(capa,(0,0),m)
base.save('kira-final.jpg',quality=95)
print(base.size)
