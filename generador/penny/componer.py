"""Sustituye las fotos de las polaroids del diseño de ChatGPT por las fotos originales, sin alterarlas."""
from PIL import Image, ImageFilter, ImageOps
S=2  # trabajamos al doble de resolución para que las fotos originales queden nítidas
BORDE=(250,246,239)
base=Image.open('diseno-chatgpt.webp').convert('RGB')
base=base.resize((base.width*S,base.height*S),Image.LANCZOS).convert('RGBA')
# (foto original, centro x,y, ángulo, ancho, alto, foco vertical del recorte 0-1) en coordenadas del diseño original
POLAROIDS=[
 ('orig-tumbada.jpg',  179.5,459.8,-4.6, 256.3,265.7,0.50,None),
 ('orig-piscina.jpg',  209.6,203.4,-4.74,297.1,229.2,0.30,(330,0,1224,690)),
 ('orig-hombre-bn.jpg',207.8,751.8, 6.56,267.2,268.1,0.50,None),
]
B=19  # grosor del marco blanco
for f,cx,cy,ang,w,h,fy,caja in POLAROIDS:
    foto=Image.open(f).convert('RGB')
    if caja: foto=foto.crop(caja)
    foto=ImageOps.fit(foto,(round(w*S),round(h*S)),Image.LANCZOS,centering=(0.5,fy))
    pol=Image.new('RGBA',(foto.width+2*B*S,foto.height+2*B*S),BORDE+(255,))
    pol.paste(foto,(B*S,B*S))
    # sombra suave
    sh=Image.new('RGBA',(pol.width+60*S,pol.height+60*S),(0,0,0,0))
    sh.paste((60,40,30,70),(30*S,30*S,30*S+pol.width,30*S+pol.height))
    sh=sh.filter(ImageFilter.GaussianBlur(6*S))
    # el ángulo medido es en coordenadas de imagen (y hacia abajo): PIL rota en sentido antihorario
    sh=sh.rotate(-ang,resample=Image.BICUBIC,expand=True)
    pr=pol.rotate(-ang,resample=Image.BICUBIC,expand=True)
    base.alpha_composite(sh,(round(cx*S-sh.width/2+3*S),round(cy*S-sh.height/2+5*S)))
    base.alpha_composite(pr,(round(cx*S-pr.width/2),round(cy*S-pr.height/2)))
base.convert('RGB').save('penny-final.jpg',quality=95)
print(base.size)
