import numpy as np
from PIL import Image
rgb=np.asarray(Image.open('diseno-chatgpt.webp').convert('RGB')).astype(float)
def isborder(x,y):
    r,g,b=rgb[int(round(y)),int(round(x))]
    return (r+g+b)/3>238 and 5<=r-b<=22
quads={'p1':[(50,112.5),(341.5,74),(372.5,312.5),(77.5,322.5)],
       'p2':[(40,340),(295,314),(320,580),(65,595)],
       'p3':[(100,601.5),(351.5,639),(330,891),(59,865)]}
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
            # from inside outward, first index where 5 consecutive border samples
            for j in range(len(ss)-5):
                if all(flags[j:j+5]): offs.append(ss[j]);break
        off=np.median(offs) if offs else 0
        lines.append((a+n*off,d,len(offs)))
    corners=[]
    for i in range(4):
        (p1,d1,_),(p2,d2,_)=lines[i-1],lines[i]
        t=np.linalg.solve(np.array([d1,-d2]).T,p2-p1); corners.append([round(float(v),1) for v in p1+d1*t[0]])
    return corners,[l[2] for l in lines]
if __name__=='__main__':
    for k,q in quads.items(): print(k,refine(q))
