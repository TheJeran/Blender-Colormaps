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
    "version" : (1, 1, 1),
    "location" : "Shader Editor > Tool > Colormaps",
    "warning" : "",
    "doc_url": "https://github.com/TheJeran/Blender-Colormaps", 
    "tracker_url": "", 
    "category" : "Node" 
}


import bpy
import bpy.utils.previews
import sys
import subprocess
import numpy as np
from bpy.app.handlers import persistent

good = True

try:
    import matplotlib
    import cmocean
    import colorcet


except:
    good = False

addon_keymaps = {}
_icons = None
dependencies = {'sna_deps_installed': False, }
dependencies['sna_deps_installed'] = good
nodetree = {'sna_color_libraries': [], 'sna_cmaps': [], }
_item_map = dict()

def make_enum_item(_id, name, descr, preview_id, uid):
    lookup = str(_id)+"\0"+str(name)+"\0"+str(descr)+"\0"+str(preview_id)+"\0"+str(uid)
    if not lookup in _item_map:
        _item_map[lookup] = (_id, name, descr, preview_id, uid)
    return _item_map[lookup]


def sna_update_sna_color_libraries_22719(self, context):
    sna_updated_prop = self.sna_color_libraries
    library = sna_updated_prop
    cmaps = None
    cmaps = sorted(matplotlib.colormaps(), key = lambda x: x.lower())
    options = ['matplotlib','colorcet','cmocean']
    cmos = [i for i in cmaps if 'cmo.' in i]
    cets = [i for i in cmaps if 'cet_' in i and not i.endswith('_r')]
    matplot = [i for i in cmaps if not i.startswith('cmo.') and not i.startswith('cet_')]
    libraries = {'matplotlib':matplot,'colorcet':cets,'cmocean':cmos}
    cmaps = libraries[library]
    nodetree['sna_cmaps'] = []
    for i_FAA08 in range(len(cmaps)):
        nodetree['sna_cmaps'].append([cmaps[i_FAA08], cmaps[i_FAA08], '', 0])


class SNA_OT_Install_Dependencies_E7270(bpy.types.Operator):
    bl_idname = "sna.install_dependencies_e7270"
    bl_label = "Install Dependencies"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        import subprocess
        pyth_path = sys.executable
        for lib in ["matplotlib", "cmocean", "colorcet"]:
            subprocess.call([pyth_path, "-m","pip","install",lib])
        bpy.ops.script.reload()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_AddonPreferences_58A3E(bpy.types.AddonPreferences):
    bl_idname = 'blender_colormaps'

    def draw(self, context):
        if not (False):
            layout = self.layout 
            if dependencies['sna_deps_installed']:
                pass
            else:
                col_720D4 = layout.column(heading='', align=False)
                col_720D4.alert = False
                col_720D4.enabled = True
                col_720D4.active = True
                col_720D4.use_property_split = False
                col_720D4.use_property_decorate = False
                col_720D4.scale_x = 1.0
                col_720D4.scale_y = 1.0
                col_720D4.alignment = 'Expand'.upper()
                if not True: col_720D4.operator_context = "EXEC_DEFAULT"
                col_720D4.label(text='DEPENDENCIES MISSING', icon_value=778)
                op = col_720D4.operator('sna.install_dependencies_e7270', text='Install Dependencies', icon_value=0, emboss=True, depress=False)


def sna_create_colorramp_0B482():
    steps = bpy.data.scenes['Scene'].sna_colormap_steps
    cmap_name = bpy.context.scene.sna_cmaps
    import sys
    import numpy as np
    material = bpy.context.active_object.active_material
    modifier = bpy.context.object.modifiers.active
    if material is not None and bpy.context.area.ui_type == 'ShaderNodeTree':
        nodes = material.node_tree.nodes
        cramp = nodes.new(type='ShaderNodeValToRGB')
    elif modifier is not None and bpy.context.area.ui_type == 'GeometryNodeTree':
        if modifier.type == 'NODES':
            nodes = modifier.node_group.nodes
            cramp = nodes.new(type='ShaderNodeValToRGB')
    cmap = matplotlib.cm.get_cmap(cmap_name)
    el = cramp.color_ramp.elements
    dis = 1/(steps-1)
    x   = dis
    for r in range(steps-2):
        el.new(x)
        x += dis
    for e in el:
        pos = e.position
        e.color = [i**2.2 for i in cmap(pos)]
    cramp.label = cmap_name
    return


def sna_update_color_map_5D6A6():
    steps = bpy.data.scenes['Scene'].sna_colormap_steps
    cmap_name = bpy.context.scene.sna_cmaps
    node_name = bpy.context.active_node.name
    import matplotlib
    import numpy as np
    cmap = matplotlib.cm.get_cmap(cmap_name)
    cramp = bpy.context.active_node
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
        e.color = [i**2.2 for i in cmap(pos)]
    cramp.label = cmap_name
    return


class SNA_OT_Update_Colorramp_8Fdfb(bpy.types.Operator):
    bl_idname = "sna.update_colorramp_8fdfb"
    bl_label = "Update Colorramp"
    bl_description = "Update Selected Colorramp"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
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
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        sna_create_colorramp_0B482()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_color_libraries_enum_items(self, context):
    enum_items = [['matplotlib', 'matplotlib', '', 0], ['colorcet', 'colorcet', '', 0], ['cmocean', 'cmocean', '', 0]]
    return [make_enum_item(item[0], item[1], item[2], item[3], i) for i, item in enumerate(enum_items)]


def sna_cmaps_enum_items(self, context):
    enum_items = nodetree['sna_cmaps']
    return [make_enum_item(item[0], item[1], item[2], item[3], i) for i, item in enumerate(enum_items)]


@persistent
def load_post_handler_197C2(dummy):
    bpy.context.scene.sna_color_libraries = 'matplotlib'


class SNA_PT_COLORMAPS_321D4(bpy.types.Panel):
    bl_label = 'Colormaps'
    bl_idname = 'SNA_PT_COLORMAPS_321D4'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'Tool'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        mat = context.object.active_material
        if mat is not None and (mat.use_nodes and bpy.context.area.ui_type == 'ShaderNodeTree'):
            return True
        modifier = context.object.modifiers.active
        return modifier is not None and (
            modifier.type == 'NODES'
            and bpy.context.area.ui_type == 'GeometryNodeTree'
            and modifier.node_group is not None
        )

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        col_F7EAC = layout.column(heading='', align=False)
        col_F7EAC.alert = False
        col_F7EAC.enabled = True
        col_F7EAC.active = True
        col_F7EAC.use_property_split = False
        col_F7EAC.use_property_decorate = False
        col_F7EAC.scale_x = 1.0
        col_F7EAC.scale_y = 1.0
        col_F7EAC.alignment = 'Expand'.upper()
        if not True: col_F7EAC.operator_context = "EXEC_DEFAULT"
        split_FF844 = col_F7EAC.split(factor=0.5, align=False)
        split_FF844.alert = False
        split_FF844.enabled = True
        split_FF844.active = True
        split_FF844.use_property_split = False
        split_FF844.use_property_decorate = False
        split_FF844.scale_x = 1.0
        split_FF844.scale_y = 1.0
        split_FF844.alignment = 'Expand'.upper()
        if not True: split_FF844.operator_context = "EXEC_DEFAULT"
        split_FF844.label(text='Library', icon_value=0)
        split_FF844.prop(bpy.context.scene, 'sna_color_libraries', text='', icon_value=0, emboss=True)
        split_47029 = col_F7EAC.split(factor=0.5, align=False)
        split_47029.alert = False
        split_47029.enabled = True
        split_47029.active = True
        split_47029.use_property_split = False
        split_47029.use_property_decorate = False
        split_47029.scale_x = 1.0
        split_47029.scale_y = 1.0
        split_47029.alignment = 'Expand'.upper()
        if not True: split_47029.operator_context = "EXEC_DEFAULT"
        split_47029.label(text='Color Maps', icon_value=0)
        split_47029.prop(bpy.context.scene, 'sna_cmaps', text='', icon_value=0, emboss=True)
        split_20DBF = col_F7EAC.split(factor=0.23333331942558289, align=False)
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
        op = col_F7EAC.operator('sna.create_color_ramp_0dbb6', text='Create Color Ramp', icon_value=0, emboss=True, depress=False)
        if bpy.context.active_node is not None and ((bpy.context.active_node.type == 'VALTORGB') and bpy.context.active_node.select):
            op = col_F7EAC.operator('sna.update_colorramp_8fdfb', text='Update Selected', icon_value=0, emboss=True, depress=False)


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.types.Scene.sna_cmaps = bpy.props.EnumProperty(name='cmaps', description='', items=sna_cmaps_enum_items)
    bpy.types.Scene.sna_color_libraries = bpy.props.EnumProperty(name='Color Libraries', description='', items=sna_color_libraries_enum_items, update=sna_update_sna_color_libraries_22719)
    bpy.types.Scene.sna_colormap_steps = bpy.props.IntProperty(name='Colormap Steps', description='', default=10, subtype='NONE')
    bpy.utils.register_class(SNA_OT_Install_Dependencies_E7270)
    bpy.utils.register_class(SNA_AddonPreferences_58A3E)
    bpy.utils.register_class(SNA_OT_Update_Colorramp_8Fdfb)
    bpy.utils.register_class(SNA_OT_Create_Color_Ramp_0Dbb6)
    bpy.app.handlers.load_post.append(load_post_handler_197C2)
    bpy.utils.register_class(SNA_PT_COLORMAPS_321D4)


def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    del bpy.types.Scene.sna_colormap_steps
    del bpy.types.Scene.sna_color_libraries
    del bpy.types.Scene.sna_cmaps
    bpy.utils.unregister_class(SNA_OT_Install_Dependencies_E7270)
    bpy.utils.unregister_class(SNA_AddonPreferences_58A3E)
    bpy.utils.unregister_class(SNA_OT_Update_Colorramp_8Fdfb)
    bpy.utils.unregister_class(SNA_OT_Create_Color_Ramp_0Dbb6)
    bpy.app.handlers.load_post.remove(load_post_handler_197C2)
    bpy.utils.unregister_class(SNA_PT_COLORMAPS_321D4)
