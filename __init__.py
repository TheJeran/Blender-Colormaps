# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Blender Colormaps",
    "author" : "Jeran Poehls", 
    "description" : "Import Matplotlib color maps into Shader ",
    "blender" : (3, 0, 0),
    "version" : (1, 0, 5),
    "location" : "Shader Editor > Tool > Colormaps",
    "waring" : "",
    "doc_url": "https://github.com/TheJeran/Blender-Colormaps", 
    "tracker_url": "", 
    "category" : "Node" 
}


import bpy
import bpy.utils.previews
import matplotlib.pyplot as plt
import numpy as np


addon_keymaps = {}
_icons = None
nodetree = {'sna_cmaps': [], }
_item_map = dict()

def srgb2lin(s):
    if s <= 0.0404482362771082:
        lin = s / 12.92
    else:
        lin = pow(((s + 0.055) / 1.055), 2.4)
    return lin


def to_blender_color(rgba):
    return np.array([
        srgb2lin(rgba[0]),
        srgb2lin(rgba[1]),
        srgb2lin(rgba[2]),
        rgba[3]])


def make_enum_item(_id, name, descr, preview_id, uid):
    lookup = str(_id)+"\0"+str(name)+"\0"+str(descr)+"\0"+str(preview_id)+"\0"+str(uid)
    if not lookup in _item_map:
        _item_map[lookup] = (_id, name, descr, preview_id, uid)
    return _item_map[lookup]


def sna_colormaps_E002E():
    cmaps = None
    import cmocean
    cmaps = sorted(plt.colormaps(), key = lambda x: x.lower())
    nodetree['sna_cmaps'] = []
    for i_FAA08 in range(len(cmaps)):
        nodetree['sna_cmaps'].append([cmaps[i_FAA08], cmaps[i_FAA08], '', 0])
    return nodetree['sna_cmaps']


def sna_cmaps_enum_items(self, context):
    enum_items = sna_colormaps_E002E()
    return [make_enum_item(item[0], item[1], item[2], item[3], i) for i, item in enumerate(enum_items)]


def sna_create_colorramp_0B482():
    steps = bpy.data.scenes['Scene'].sna_colormap_steps
    cmap_name = bpy.data.scenes['Scene'].sna_cmaps

    material = bpy.context.active_object.active_material
    modifier = bpy.context.object.modifiers.active
    if material is not None and bpy.context.area.ui_type == 'ShaderNodeTree':
        nodes = material.node_tree.nodes
        cramp = nodes.new(type='ShaderNodeValToRGB')
    elif modifier is not None and bpy.context.area.ui_type == 'GeometryNodeTree':
        if modifier.type == 'NODES':
            nodes = modifier.node_group.nodes
            cramp = nodes.new(type='ShaderNodeValToRGB')

    cmap = plt.get_cmap(cmap_name)
    el = cramp.color_ramp.elements
    dis = 1/(steps-1)
    x   = dis
    for r in range(steps-2):
        el.new(x)
        x += dis
    for e in el:
        pos = e.position
        e.color = to_blender_color(cmap(pos))
    cramp.label = cmap_name


def sna_update_color_map_5D6A6():
    steps = bpy.data.scenes['Scene'].sna_colormap_steps
    cmap_name = bpy.data.scenes['Scene'].sna_cmaps

    cramp = bpy.context.active_node
    cmap = plt.get_cmap(cmap_name)
    el = cramp.color_ramp.elements
    count=0
    for idx in range(len(el.values())-1):
        el.remove(el[idx-count])
        count +=1 
    dis = 1/(steps-1)
    x  = 0
    for r in range(steps-1):
        el.new(x)
        x += dis
    for e in el:
        pos = e.position
        e.color = to_blender_color(cmap(pos))
    cramp.label = cmap_name


class SNA_OT_Update_Colorramp_8Fdfb(bpy.types.Operator):
    bl_idname = "sna.update_colorramp_8fdfb"
    bl_label = "Update Colorramp"
    bl_description = "Update Selected Colorramp"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        sna_update_color_map_5D6A6()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Create_Color_Ramp_0Dbb6(bpy.types.Operator):
    bl_idname = "sna.create_color_ramp_0dbb6"
    bl_label = "Create Color Ramp"
    bl_description = "Create a Color Ramp of the specified Color Map"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        sna_create_colorramp_0B482()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_PT_COLORMAPS_C3E26(bpy.types.Panel):
    bl_label = 'Colormaps'
    bl_idname = 'SNA_PT_COLORMAPS_C3E26'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'Tool'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        mat = context.object.active_material
        if mat is not None:
            if mat.use_nodes and bpy.context.area.ui_type == 'ShaderNodeTree':
                return True
        modifier = context.object.modifiers.active
        if modifier is not None:
            if modifier.type == 'NODES' and bpy.context.area.ui_type == 'GeometryNodeTree':
                return True
        return False

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        col_E8864 = layout.column(heading='', align=False)
        col_E8864.alert = False
        col_E8864.enabled = True
        col_E8864.active = True
        col_E8864.use_property_split = False
        col_E8864.use_property_decorate = False
        col_E8864.scale_x = 1.0
        col_E8864.scale_y = 1.0
        col_E8864.alignment = 'Expand'.upper()
        col_A4FA5 = col_E8864.column(heading='', align=False)
        col_A4FA5.alert = False
        col_A4FA5.enabled = True
        col_A4FA5.active = True
        col_A4FA5.use_property_split = False
        col_A4FA5.use_property_decorate = False
        col_A4FA5.scale_x = 1.0
        col_A4FA5.scale_y = 1.0
        col_A4FA5.alignment = 'Expand'.upper()
        col_A4FA5.label(text='Color Map', icon_value=0)
        col_A4FA5.prop(bpy.context.scene, 'sna_cmaps', text='', icon_value=0, emboss=True)
        split_20DBF = col_E8864.split(factor=0.23333331942558289, align=False)
        split_20DBF.alert = False
        split_20DBF.enabled = True
        split_20DBF.active = True
        split_20DBF.use_property_split = False
        split_20DBF.use_property_decorate = False
        split_20DBF.scale_x = 1.0
        split_20DBF.scale_y = 1.0
        split_20DBF.alignment = 'Expand'.upper()
        split_20DBF.label(text='Steps', icon_value=0)
        split_20DBF.prop(bpy.context.scene, 'sna_colormap_steps', text='', icon_value=0, emboss=True)
        col_E8864.operator('sna.create_color_ramp_0dbb6', text='Create Color Ramp', icon_value=0, emboss=True, depress=False)
        if bpy.context.active_node is not None:
            if bpy.context.active_node.type == 'VALTORGB' and bpy.context.active_node.select:
                col_E8864.operator('sna.update_colorramp_8fdfb', text='Update Selected', icon_value=0, emboss=True, depress=False)


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.types.Scene.sna_cmaps = bpy.props.EnumProperty(name='Cmaps', description='', items=sna_cmaps_enum_items)
    bpy.types.Scene.sna_colormap_steps = bpy.props.IntProperty(name='Colormap Steps', description='', default=10, subtype='NONE')
    bpy.utils.register_class(SNA_OT_Update_Colorramp_8Fdfb)
    bpy.utils.register_class(SNA_OT_Create_Color_Ramp_0Dbb6)
    bpy.utils.register_class(SNA_PT_COLORMAPS_C3E26)


def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    del bpy.types.Scene.sna_colormap_steps
    del bpy.types.Scene.sna_cmaps
    bpy.utils.unregister_class(SNA_OT_Update_Colorramp_8Fdfb)
    bpy.utils.unregister_class(SNA_OT_Create_Color_Ramp_0Dbb6)
    bpy.utils.unregister_class(SNA_PT_COLORMAPS_C3E26)
