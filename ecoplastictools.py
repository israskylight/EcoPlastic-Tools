bl_info = {
    "name":        "Eco Plastic Tools",
    "author":      "Israel Navarro Fernandez. Materiales y Tecnología: Diseño. Escuela de Arte y Superior de Diseño de Sevilla",
    "version":     (1, 0, 0),
    "blender":     (3, 0, 0),
    "location":    "Sidebar > Plástico (N) | Object Properties > Plástico",
    "description": "Selector de Plásticos, Huella de Carbono, Biodegradabilidad y Recomendación unificados",
    "category":    "Object",
}

import re
import numpy as np
import bpy
from bpy.types import Panel, PropertyGroup, UIList, Operator
from bpy.props import (
    EnumProperty, FloatProperty, PointerProperty,
    IntProperty, CollectionProperty, StringProperty
)

# ---------------------------------------------------------------------------
# Datos compartidos
PLASTICS_DATA = {
    "PET": ("PET", 1.38, 3.0, "Vertedero", "No • >450 a", "Felt acústico reciclado, panel translúcido, tejidos de display"),
    "r-PET": ("PET⟳", 1.35, 0.8, "Reciclaje", "Reciclable", "Láminas y tableros reciclados, impresión UV"),
    "PET-G": ("—", 1.27, 3.0, "Vertedero", "No • >400 a", "Placas termoformables para stands, expositores back-lit"),
    "HDPE": ("2", 0.95, 1.9, "Vertedero", "No • >500 a", "Tableros reciclados de mobiliario, tarimas modulares"),
    "LDPE": ("4", 0.92, 1.85, "Vertedero", "No • >500 a", "Films protectores, envolventes tensadas"),
    "EVA": ("—", 0.94, 2.2, "Vertedero", "No • >300 a", "Suelos blandos, juntas expansivas, soft-graphics"),
    "PP": ("5", 0.90, 1.65, "Vertedero", "No • >400 a", "Panel alveolar, impresión 3D, ferias"),
    "r-PP": ("5⟳", 0.89, 0.7, "Reciclaje", "Reciclable", "Colmenas modulares, carcasas de luminaria"),
    "PVC rig.": ("3", 1.42, 3.25, "Vertedero", "No • >1000 a", "Paneles espumados Forex®, perfilería temporal"),
    "PVC flex": ("3", 1.32, 3.45, "Vertedero", "No • >1000 a", "Lonas back-lit, suelos vinílicos clic"),
    "PS": ("6", 1.05, 2.85, "Vertedero", "No • >500 a", "Maquetas, núcleos XPS, rótulos corpóreos"),
    "ABS": ("7", 1.05, 4.0, "Vertedero", "No • >500 a", "Piezas impresas FDM, carcasas expo"),
    "PMMA": ("—", 1.18, 4.5, "Vertedero", "No • >400 a", "Paneles LED edge-lit, letras corpóreas traslúcidas"),
    "PC": ("7", 1.20, 5.0, "Vertedero", "No • >1000 a", "Placas alveolares de cubierta ligera, viseras transparentes"),
    "PCL": ("—", 1.14, 2.25, "Compost dom.", "Sí • <12 m", "Adhesivo termofusible low-temp, moldeables DIY"),
    "TPS": ("—", 1.20, 1.6, "Compost dom.", "Sí • 1-6 m", "Vajilla desechable, recubrimientos hidrosolubles"),
    "Starch-blend": ("—", 1.20, 1.85, "Compost dom.", "Sí • 3-6 m", "Lonas compostables, cubre-alfombras"),
    "Cellophane": ("—", 1.45, 2.0, "Suelo", "Sí • 10-30 d", "Ventanas de packaging, láminas envolventrio"),
    "CA": ("—", 1.30, 2.25, "Compost dom.", "Sí • 2-4 m", "Láminas semitransp. para back-light"),
    "PGA": ("—", 1.50, 2.8, "Compost dom.", "Sí • <60 d", "Hilos fijación temporal, piezas solubles"),
}

# ---------------------------------------------------------------------------
# Función de parseo de biodegradabilidad (panel)
_UNIT2D = {'d': 1, 'm': 30, 'a': 365}

def parse_biodeg(cadena: str):
    if not cadena:
        return None, None, "Sin datos"
    cadena = cadena.replace('•', '').replace('Sí', '').strip()
    if 'Reciclable' in cadena or cadena.startswith('No'):
        return None, None, 'No biodegradable'
    m = re.search(r'([<>]?)([\d\.]+)(?:-([\d\.]+))?\s*([adm])', cadena)
    if not m:
        return None, None, cadena
    signo, v1, v2, unidad = m.groups()
    mult = _UNIT2D[unidad]
    d1 = float(v1) * mult
    d2 = float(v2) * mult if v2 else d1
    if signo == '>': texto = f"> {int(d1)} días"
    elif signo == '<': texto = f"< {int(d1)} días"
    elif v2: texto = f"{int(d1)}–{int(d2)} días"
    else: texto = f"{int(d1)} días"
    return d1, d2, texto

# ---------------------------------------------------------------------------
# Función auxiliar para recomendador
_UNIT = {'d': 1, 'm': 30, 'a': 365}
FLEXIBLES = {"LDPE","EVA","PVC flex","TPU","Starch_blend",
             "PBSA","PBAT","Cellophane","TPS","PCL"}

def dias_biodeg(txt: str) -> float:
    if not txt or "Reciclable" in txt or txt.startswith("No"):
        return 9e4
    clean = txt.replace("•", "").replace("Sí", "").strip()
    m = re.search(r'([<>]?)([\d\.]+)(?:-([\d\.]+))?\s*([adm])', clean)
    if not m:
        return 9e4
    s, v1, v2, u = m.groups()
    d1 = float(v1) * _UNIT[u]
    d2 = float(v2) * _UNIT[u] if v2 else d1
    if s == "<": return d1 * 0.5
    if s == ">": return d1
    return (d1 + d2) / 2

# ---------------------------------------------------------------------------
# Property Groups
class ECO_Props(PropertyGroup):
    plastic: EnumProperty(
        name="Plástico",
        items=[(k, k, "") for k in PLASTICS_DATA.keys()],
        default=next(iter(PLASTICS_DATA))
    )

class ECO_Leg(PropertyGroup):
    mode: EnumProperty(name="Modo", items=[
        ("TRUCK","Camión",""),
        ("TRAIN","Tren",""),
        ("SHIP","Barco",""),
        ("AIR","Avión",""),
    ], default="TRUCK")
    km: FloatProperty(name="km", default=100.0, min=0.0)

class ECO_FootprintProps(PropertyGroup):
    process: EnumProperty(name="Proceso", items=[
        ("EXTRUSION","Extrusión",""),
        ("INJECTION","Inyección",""),
        ("FDM","Impresión 3D (FDM)",""),
    ], default="EXTRUSION")
    eol: EnumProperty(name="Fin de vida", items=[
        ("LANDFILL","Vertedero",""),
        ("RECYCLE","Reciclaje",""),
        ("INCINERATION","Incineración",""),
    ], default="LANDFILL")
    legs: CollectionProperty(type=ECO_Leg)
    legs_index: IntProperty(default=-1)
    kwh_use: FloatProperty(name="Consumo eléctrico (kWh)", default=0.0, min=0.0)
    units: IntProperty(name="Unidades", default=1, min=1)
    co2_mat:    FloatProperty(default=0.0, options={'HIDDEN'})
    co2_proc:   FloatProperty(default=0.0, options={'HIDDEN'})
    co2_transp: FloatProperty(default=0.0, options={'HIDDEN'})
    co2_use:    FloatProperty(default=0.0, options={'HIDDEN'})
    co2_eol:    FloatProperty(default=0.0, options={'HIDDEN'})
    co2_total:  FloatProperty(default=0.0, options={'HIDDEN'})

class ECO_RecomProps(PropertyGroup):
    need: EnumProperty(
        name="Tipo requerido",
        items=[("ANY","Cualquiera",""),("RIGID","Rígido",""),("FLEX","Flexible","")],
        default="RIGID"
    )
    top_n: IntProperty(name="Top N", default=5, min=1, max=20)
    w_bio: FloatProperty(default=0.7, subtype='FACTOR')
    w_co2: FloatProperty(default=0.3, subtype='FACTOR')

class ECO_RecomItem(PropertyGroup):
    display: StringProperty()

# ---------------------------------------------------------------------------
# UIList Classes
class ECO_UL_Transport(UIList):
    bl_idname = "ECO_UL_transport"
    def draw_item(self, _ctx, layout, _data, item, _icon, _active_data, _active_propname, _index):
        row = layout.row(align=True)
        row.prop(item, "mode", text="", emboss=False)
        row.prop(item, "km", text="km")

class ECO_UL_Recs(UIList):
    bl_idname = "ECO_UL_recs"
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        plast, score, co2, tipo, dbio, rec = item.display.split("|")
        row = layout.row(align=True)
        row.label(text=plast)
        row.label(text=f"{float(score):.2f}")
        row.label(text=f"{float(co2):.2f}")
        row.label(text="Rígido" if tipo=="R" else "Flexible")
        row.label(text="—" if float(dbio)>=9e4 else f"{int(float(dbio))}d")
        row.label(text=rec)

# ---------------------------------------------------------------------------
# Operators
class ECO_OT_AddLeg(Operator):
    bl_idname = "eco.add_leg"
    bl_label = "Añadir tramo"
    def execute(self, ctx):
        fp = ctx.object.eco_footprint
        leg = fp.legs.add(); fp.legs_index = len(fp.legs)-1
        return {'FINISHED'}

class ECO_OT_RemoveLeg(Operator):
    bl_idname = "eco.remove_leg"
    bl_label = "Quitar tramo"
    def execute(self, ctx):
        fp = ctx.object.eco_footprint
        if 0 <= fp.legs_index < len(fp.legs): fp.legs.remove(fp.legs_index); fp.legs_index = max(fp.legs_index-1,0)
        return {'FINISHED'}

class ECO_OT_CalcFootprint(Operator):
    bl_idname = "eco.calc_huella"
    bl_label = "Calcular huella"
    @classmethod
    def poll(cls, ctx):
        return ctx.object and hasattr(ctx.object, "eco_props")
    def execute(self, ctx):
        obj = ctx.object; fp = obj.eco_footprint; key = obj.eco_props.plastic
        symbol, rho, fact_resin, *_ = PLASTICS_DATA.get(key,(None,0,0,))
        rho_kg = rho*1000; volumen = getattr(obj,"volume", obj.dimensions.x*obj.dimensions.y*obj.dimensions.z)
        masa = rho_kg*volumen*fp.units
        PROCESS_FACTORS = {"EXTRUSION":0.20,"INJECTION":0.25,"FDM":0.50}
        TRANSPORT_FACTORS = {"TRUCK":0.090,"TRAIN":0.040,"SHIP":0.010,"AIR":0.580}
        ELEC_FACTOR = 0.20
        EOL_FACTORS = {"LANDFILL":0.00,"RECYCLE":-0.30,"INCINERATION":0.60}
        fp.co2_mat = masa*fact_resin
        fp.co2_proc = masa*PROCESS_FACTORS[fp.process]
        fp.co2_transp = sum((masa/1000)*leg.km*TRANSPORT_FACTORS[leg.mode] for leg in fp.legs)
        fp.co2_use = fp.kwh_use*ELEC_FACTOR
        fp.co2_eol = masa*EOL_FACTORS[fp.eol]
        fp.co2_total = sum((fp.co2_mat,fp.co2_proc,fp.co2_transp,fp.co2_use,fp.co2_eol))
        self.report({'INFO'}, f"Huella total: {fp.co2_total:.2f} kg CO₂")
        return {'FINISHED'}

class ECO_OT_AHP_Quiz(Operator):
    bl_idname = "eco.ahp_quiz"
    bl_label = "Cuestionario AHP (15 preguntas)"
    bl_options = {'REGISTER'}

    q1:  IntProperty(name="1) Biodegradación vs CO₂", default=5, min=1, max=9)
    q2:  IntProperty(name="2) Rigidez vs CO₂", default=5, min=1, max=9)
    q3:  IntProperty(name="3) Rigidez vs Biodegradación", default=5, min=1, max=9)
    q4:  IntProperty(name="4) Estética vs CO₂", default=5, min=1, max=9)
    q5:  IntProperty(name="5) Estética vs Biodegradación", default=5, min=1, max=9)
    q6:  IntProperty(name="6) Estética vs Rigidez", default=5, min=1, max=9)
    q7:  IntProperty(name="7) Procesado vs CO₂", default=5, min=1, max=9)
    q8:  IntProperty(name="8) Procesado vs Biodegradación", default=5, min=1, max=9)
    q9:  IntProperty(name="9) Procesado vs Rigidez", default=5, min=1, max=9)
    q10: IntProperty(name="10) Procesado vs Estética", default=5, min=1, max=9)
    q11: IntProperty(name="11) Coste vs CO₂", default=5, min=1, max=9)
    q12: IntProperty(name="12) Coste vs Biodegradación", default=5, min=1, max=9)
    q13: IntProperty(name="13) Coste vs Rigidez", default=5, min=1, max=9)
    q14: IntProperty(name="14) Coste vs Estética", default=5, min=1, max=9)
    q15: IntProperty(name="15) Coste vs Procesado", default=5, min=1, max=9)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        for i in range(1, 16):
            layout.prop(self, f"q{i}")

    def execute(self, context):
        sc = context.scene; fp = sc.recom_props
        A = np.ones((6,6))
        def set_pair(i, j, v):
            A[i, j] = float(v)
            A[j, i] = 1.0 / float(v)
        pairs = [
            (0,1),(2,1),(2,0),(3,1),(3,0),(3,2),
            (4,1),(4,0),(4,2),(4,3),(5,1),(5,0),
            (5,2),(5,3),(5,4)
        ]
        qs = [getattr(self, f"q{i}") for i in range(1, 16)]
        for (i, j), v in zip(pairs, qs):
            set_pair(i, j, v)
        eigvals, eigvecs = np.linalg.eig(A)
        w = eigvecs[:, eigvals.argmax()].real
        w /= w.sum()
        fp.w_bio, fp.w_co2 = float(w[0]), float(w[1])
        self.report({'INFO'}, f"Pesos → Bio: {fp.w_bio:.2f} / CO₂: {fp.w_co2:.2f}")
        return {'FINISHED'}

class ECO_OT_GenRecs(Operator):
    bl_idname = "eco.gen_recs"
    bl_label = "Generar recomendaciones"
    def execute(self, context):
        sc = context.scene; fp = sc.recom_props; sc.recom_items.clear()
        cand = []
        for k,(_,_,co2,env,bio,_) in PLASTICS_DATA.items():
            tipo = "R" if k not in FLEXIBLES else "F"
            if fp.need == "RIGID" and tipo == "F": continue
            if fp.need == "FLEX" and tipo == "R": continue
            rec = "Sí" if "Recicl" in env or "Compost" in env else "No"
            d = dias_biodeg(bio)
            cand.append((k,co2,tipo,d,rec))
        if not cand:
            self.report({'WARNING'}, "Sin candidatos disponibles")
            return {'CANCELLED'}
        max_d = max(x[3] for x in cand); max_c = max(x[1] for x in cand)
        scored = [(fp.w_bio*(d/max_d)+fp.w_co2*(c/max_c),k,c,tipo,d,rec) for k,c,tipo,d,rec in cand]
        scored.sort(key=lambda x: x[0])
        for score,k,c,tipo,d,rec in scored[:fp.top_n]:
            item = sc.recom_items.add()
            item.display = f"{k}|{score:.3f}|{c}|{tipo}|{int(d)}|{rec}"
        return {'FINISHED'}

# ---------------------------------------------------------------------------
# Panels
class ECO_PT_ObjectPanel(Panel):
    bl_label = "Plástico"
    bl_space_type = "PROPERTIES"; bl_region_type = "WINDOW"; bl_context = "object"
    def draw(self, context):
        obj = context.object; props = obj.eco_props; key = props.plastic
        layout = self.layout; layout.prop(props, "plastic")
        if key in PLASTICS_DATA:
            sym,rho,co2,env,bio,uses = PLASTICS_DATA[key]
            box = layout.box()
            box.label(text=f"Símbolo: {sym}")
            box.label(text=f"Densidad: {rho:.3f} g/cm³")
            box.label(text=f"CO₂: {co2:.1f} kg/kg")
            box.label(text=f"Fin de vida: {env}")
            box.label(text=f"Biodegrad.: {bio}")
            box.label(text=f"Usos: {uses}")

class ECO_PT_SidebarPanel(Panel):
    bl_label = "Plástico"
    bl_space_type = "VIEW_3D"; bl_region_type = "UI"; bl_category = "Plástico"
    def draw(self, context):
        ECO_PT_ObjectPanel.draw(self, context)

class ECO_PT_Footprint(Panel):
    bl_label = "Huella de Carbono"
    bl_space_type = "VIEW_3D"; bl_region_type = "UI"; bl_category = "Plástico"
    @classmethod
    def poll(cls, context):
        return context.object and hasattr(context.object, "eco_props")
    def draw(self, context):
        fp = context.object.eco_footprint
        lay = self.layout
        lay.prop(fp, "process")
        lay.label(text="Transporte:")
        row = lay.row()
        row.template_list("ECO_UL_transport", "", fp, "legs", fp, "legs_index", rows=2)
        col = row.column(align=True)
        col.operator("eco.add_leg", icon='ADD', text="")
        col.operator("eco.remove_leg", icon='REMOVE', text="")
        lay.prop(fp, "kwh_use")
        lay.prop(fp, "eol")
        lay.prop(fp, "units")
        lay.operator("eco.calc_huella", icon='PLAY')
        if fp.co2_total > 0:
            box = lay.box()
            box.label(text=f"Material: {fp.co2_mat:.2f} kg")
            box.label(text=f"Procesado: {fp.co2_proc:.2f} kg")
            box.label(text=f"Transporte: {fp.co2_transp:.2f} kg")
            box.label(text=f"Uso: {fp.co2_use:.2f} kg")
            box.separator()
            box.label(text=f"Fin de vida: {fp.co2_eol:.2f} kg")
            box.label(text=f"TOTAL: {fp.co2_total:.2f} kg CO₂", icon='INFO')

class ECO_PT_Biodeg(Panel):
    bl_label = "Biodegradabilidad"
    bl_space_type = "VIEW_3D"; bl_region_type = "UI"; bl_category = "Plástico"
    @classmethod
    def poll(cls, context):
        return context.object and hasattr(context.object, "eco_props")
    def draw(self, context):
        key = context.object.eco_props.plastic
        _,_,txt = parse_biodeg(PLASTICS_DATA[key][4])
        self.layout.label(text=txt)

class ECO_PT_Recom(Panel):
    bl_label = "Recomendación de Plástico"
    bl_space_type = "VIEW_3D"; bl_region_type = "UI"; bl_category = "Plástico"
    bl_options = {'DEFAULT_CLOSED'}
    @classmethod
    def poll(cls, context):
        return context.object and hasattr(context.object, "eco_props")
    def draw(self, context):
        layout = self.layout; sc = context.scene; fp = sc.recom_props
        layout.row(align=True).prop(fp, "need", text="")
        layout.prop(fp, "top_n")
        layout.operator("eco.ahp_quiz", icon='QUESTION')
        layout.operator("eco.gen_recs", icon='CHECKMARK')
        hdr = layout.row(align=True)
        for h in ("Plástico","Score","CO₂","Tipo","Bio d","Rec"): hdr.label(text=h)
        layout.template_list("ECO_UL_recs", "", sc, "recom_items", sc, "recom_index", rows=fp.top_n)
        layout.label(text=f"Pesos → Bio: {fp.w_bio:.2f} / CO₂: {fp.w_co2:.2f}", icon='INFO')

# ---------------------------------------------------------------------------
# Registro
classes = (
    ECO_Props, ECO_Leg, ECO_FootprintProps, ECO_RecomProps, ECO_RecomItem,
    ECO_UL_Transport, ECO_UL_Recs,
    ECO_OT_AddLeg, ECO_OT_RemoveLeg, ECO_OT_CalcFootprint,
    ECO_OT_AHP_Quiz, ECO_OT_GenRecs,
    ECO_PT_ObjectPanel, ECO_PT_SidebarPanel,
    ECO_PT_Footprint, ECO_PT_Biodeg, ECO_PT_Recom,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Object.eco_props = PointerProperty(type=ECO_Props)
    bpy.types.Object.eco_footprint = PointerProperty(type=ECO_FootprintProps)
    bpy.types.Scene.recom_props = PointerProperty(type=ECO_RecomProps)
    bpy.types.Scene.recom_items = CollectionProperty(type=ECO_RecomItem)
    bpy.types.Scene.recom_index = IntProperty(default=0)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Object.eco_props
    del bpy.types.Object.eco_footprint
    del bpy.types.Scene.recom_props
    del bpy.types.Scene.recom_items
    del bpy.types.Scene.recom_index

if __name__ == "__main__":
    register()