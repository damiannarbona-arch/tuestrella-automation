"""Ajusta las esquinas de la foto interior de cada polaroid del diseño buscando el borde crema del marco."""
import numpy as np
from PIL import Image
rgb=np.asarray(Image.open('diseno-chatgpt.webp').convert('RGB')).astype(float)
def isborder(x,y):
    r,g,b=rgb[int(round(y)),int(round(x))]
    return (r+g+b)/3>225 and 3<=r-b<=30
# esquinas aproximadas de la foto interior (TL, TR, BR, BL) medidas a ojo sobre el diseño
quads={'p1':[(67.5,119),(265,97.5),(286,306),(90,327.5)],
       'p2':[(46,380),(252.5,355),(276,546),(72.5,572.5)],
       'p3':[(112.5,582.5),(300,614),(272.5,805),(80,775)]}
def refine(q):
    q=np.array(q,float); c=q.mean(0); lines=[]
    for i in range(4):
        a,b=q[i],q[(i+1)%4]; d=(b-a)/np.linalg.norm(b-a); n=np.array([-d[1],d[0]])
        if np.dot(n,c-(a+b)/2)>0: n=-n
        offs=[]
        for t in np.linspace(0.12,0.88,30):
            p=a+(b-a)*t
            ss=np.arange(-14,14.5,0.5)
            flags=[isborder(*(p+n*s)) for s in ss]
            for j in range(len(ss)-5):
                if all(flags[j:j+5]): offs.append(ss[j]);break
        off=np.median(offs) if offs else 0
        lines.append((a+n*off,d,len(offs)))
    corners=[]
    for i in range(4):
        (p1,d1,_),(p2,d2,_)=lines[i-1],lines[i]
        t=np.linalg.solve(np.array([d1,-d2]).T,p2-p1); corners.append([round(float(v),1) for v in p1+d1*t[0]])
    return corners,[l[2] for l in lines]
def params(c):
    """centro, ángulo (grados, coordenadas de imagen), ancho y alto a partir de las 4 esquinas"""
    c=np.array(c); tl,tr,br,bl=c
    cx,cy=c.mean(0)
    ang=np.degrees(np.arctan2(((tr-tl)+(br-bl))[1],((tr-tl)+(br-bl))[0]))
    w=(np.linalg.norm(tr-tl)+np.linalg.norm(br-bl))/2; h=(np.linalg.norm(bl-tl)+np.linalg.norm(br-tr))/2
    return round(cx,1),round(cy,1),round(ang,2),round(w,1),round(h,1)
if __name__=='__main__':
    for k,q in quads.items():
        c,n=refine(q); print(k,c,n,params(c))
