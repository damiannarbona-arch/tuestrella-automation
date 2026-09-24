"""Genera las variables GraphQL para corregir los 5 retratos de Kivoa:
opciones en español, descripción limpia, handle SEO (con redirección 301),
SEO title/description, tipo de producto y alt de imágenes."""
import json, sys

P = {
 "12293154996488": ("Rosa", "rosa", "Delicado y tierno, con un toque romántico de rosas al fondo. Ideal si tu mascota era esa presencia suave que lo llenaba todo de cariño.", "Porque hay huellas que dejan flores en el camino.", "Retrato ilustrado de tu mascota con rosas al fondo, personalizado con su nombre, fecha y frase. Enmarcado y listo para colgar. Envío a España y Europa."),
 "12293158928648": ("Lavanda", "lavanda", "Sereno y suave, envuelto en tonos lavanda. El estilo perfecto para los compañeros tranquilos, curiosos, que llenaban la casa de calma con solo estar cerca.", "Pequeños gestos, inmensa huella.", "Retrato ilustrado de tu mascota en tonos lavanda, personalizado con su nombre, fecha y frase. Enmarcado y listo para colgar. Envío a España y Europa."),
 "12293162926344": ("Aventurero", "aventurero", "Montañas, senderos y un compañero siempre dispuesto a la próxima aventura. Para quien recorrió contigo cada camino sin dudarlo.", "La brújula siempre señaló hacia ti.", "Retrato ilustrado de tu perro o mascota con fondo de montaña, personalizado con nombre, fecha y frase. Enmarcado y listo para colgar."),
 "12293167317256": ("Caballos", "caballo", "Campo abierto, ferias y caminos compartidos. Un homenaje pensado para esos compañeros nobles que forman parte de tu día a día en el campo, o de tus mejores recuerdos con él.", "Gracias por tantos caminos recorridos juntos.", "Retrato ilustrado personalizado de tu caballo, con su nombre, fecha y frase. Enmarcado y listo para colgar. Envío a España y Europa."),
 "12293218271496": ("Clásico", "clasico", "El retrato que nunca pasa de moda. Un estilo atemporal y cálido, pensado para quien prefiere que el protagonista sea tu mascota y nada más, sin adornos que le resten atención.", "Un recuerdo sin fecha de caducidad, para acompañarte siempre.", "Retrato ilustrado clásico de tu perro o gato, personalizado con su nombre, fecha y frase. Enmarcado y listo para colgar. Envío a España y Europa."),
}

COMUN = """<p>Un homenaje único a quien fue mucho más que una mascota. Sube sus fotos favoritas, elige su nombre, sus características y una fecha especial, y lo convertimos en un retrato ilustrado que guardará su recuerdo para siempre.</p>
<ul>
<li><strong>Totalmente personalizable:</strong> foto principal, hasta 3 fotos secundarias, nombre, hasta 6 características, una frase y una fecha.</li>
<li><strong>Marco de madera</strong> en tres acabados: blanco, negro o natural.</li>
<li><strong>Papel de alta calidad</strong> protegido con metacrilato irrompible. Papel de origen sostenible (FSC o equivalente).</li>
<li><strong>Listo para colgar:</strong> incluye kit de montaje.</li>
<li><strong>Tamaños:</strong> 20×25 cm, 30×40 cm y 50×70 cm.</li>
</ul>"""

FRAME = {"White frame": "Blanco", "Wood frame": "Madera natural", "Black frame": "Negro"}

def build(products):
    out = []
    for p in products:
        pid = p["id"].split("/")[-1]
        estilo, slug, intro, cierre, seo_desc = P[pid]
        html = f"<p>{intro}</p>\n{COMUN}\n<p><em>{cierre}</em></p>"
        size, frame = p["options"]
        out.append({
            "product": {
                "id": p["id"],
                "handle": f"retrato-mascota-personalizado-{slug}",
                "redirectNewHandle": True,
                "descriptionHtml": html,
                "productType": "Retrato personalizado",
                "seo": {"title": f"Retrato personalizado de mascota – Estilo {estilo} | Kivoa",
                        "description": seo_desc},
            },
            "sizeOpt": {"id": size["id"], "name": "Tamaño"},
            "sizeVals": [{"id": v["id"], "name": v["name"].split(" / ")[0].replace("x", "×")} for v in size["optionValues"]],
            "frameOpt": {"id": frame["id"], "name": "Marco"},
            "frameVals": [{"id": v["id"], "name": FRAME[v["name"]]} for v in frame["optionValues"]],
            "files": [{"id": m["id"], "alt": m["alt"] if not m["alt"][:8].count("-") == 0 and "Ambientación" in m["alt"]
                       else (f"Retrato personalizado de mascota estilo {estilo}" + ("" if i == 0 else f" – vista {i+1}"))}
                      for i, m in enumerate(p["media"]["nodes"])],
        })
    return out

if __name__ == "__main__":
    data = json.load(sys.stdin)["data"]["products"]["nodes"]
    json.dump(build(data), sys.stdout, ensure_ascii=False, indent=1)
