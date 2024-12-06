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
    "name" : "Blender Colors",
    "author" : "Jeran Poehls", 
    "description" : "Import Curated or custom colormaps into Blender",
    "blender" : (4, 0, 0),
    "version" : (1, 5, 0),
    "location" : "",
    "warning" : "",
    "doc_url": "https://github.com/TheJeran/Blender-Colormaps", 
    "tracker_url": "", 
    "category" : "Node" 
}


import bpy
import bpy.utils.previews
import os
from matplotlib.colors import LinearSegmentedColormap
from bpy.app.handlers import persistent
import subprocess


addon_keymaps = {}
_icons = None
blender_colormaps = {'sna_cmaps': [], 'sna_libraries': [], }
dependencies = {'sna_deps_installed': False, }


def property_exists(prop_path, glob, loc):
    try:
        eval(prop_path, glob, loc)
        return True
    except:
        return False


def sna_update_sna_libraries_C21AD(self, context):
    sna_updated_prop = self.sna_libraries
    library = sna_updated_prop
    cmap_path = os.path.join(os.path.dirname(__file__), 'assets', 'colormaps')
    cmaps = None
    if library != 'matplotlib':
        files = os.listdir(f"{cmap_path}/{library}")
        cmaps = [i.split('.')[0] for i in files if i.endswith('.rgb')]
    else:
        cmaps = sorted(matplotlib.colormaps(), key = lambda x: x.lower())
    blender_colormaps['sna_cmaps'] = []
    for i_CE42B in range(len(cmaps)):
        blender_colormaps['sna_cmaps'].append([cmaps[i_CE42B], cmaps[i_CE42B], '', 0])


_item_map = dict()


def make_enum_item(_id, name, descr, preview_id, uid):
    lookup = str(_id)+"\0"+str(name)+"\0"+str(descr)+"\0"+str(preview_id)+"\0"+str(uid)
    if not lookup in _item_map:
        _item_map[lookup] = (_id, name, descr, preview_id, uid)
    return _item_map[lookup]


class SNA_PT_COLORMAPS_4CB30(bpy.types.Panel):
    bl_label = 'Colormaps'
    bl_idname = 'SNA_PT_COLORMAPS_4CB30'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'Tool'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        col_D76F1 = layout.column(heading='', align=False)
        col_D76F1.alert = False
        col_D76F1.enabled = True
        col_D76F1.active = True
        col_D76F1.use_property_split = False
        col_D76F1.use_property_decorate = False
        col_D76F1.scale_x = 1.0
        col_D76F1.scale_y = 1.0
        col_D76F1.alignment = 'Expand'.upper()
        col_D76F1.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        split_74CE5 = col_D76F1.split(factor=0.5, align=False)
        split_74CE5.alert = False
        split_74CE5.enabled = True
        split_74CE5.active = True
        split_74CE5.use_property_split = False
        split_74CE5.use_property_decorate = False
        split_74CE5.scale_x = 1.0
        split_74CE5.scale_y = 1.0
        split_74CE5.alignment = 'Expand'.upper()
        if not True: split_74CE5.operator_context = "EXEC_DEFAULT"
        split_74CE5.label(text='Library', icon_value=0)
        split_74CE5.prop(bpy.context.scene, 'sna_libraries', text='', icon_value=0, emboss=True)
        split_0C2BA = col_D76F1.split(factor=0.5, align=False)
        split_0C2BA.alert = False
        split_0C2BA.enabled = True
        split_0C2BA.active = True
        split_0C2BA.use_property_split = False
        split_0C2BA.use_property_decorate = False
        split_0C2BA.scale_x = 1.0
        split_0C2BA.scale_y = 1.0
        split_0C2BA.alignment = 'Expand'.upper()
        if not True: split_0C2BA.operator_context = "EXEC_DEFAULT"
        split_0C2BA.label(text='Color Map', icon_value=0)
        split_0C2BA.prop(bpy.context.scene, 'sna_cmaps', text='', icon_value=0, emboss=True)
        split_1D120 = col_D76F1.split(factor=0.5, align=False)
        split_1D120.alert = False
        split_1D120.enabled = True
        split_1D120.active = True
        split_1D120.use_property_split = False
        split_1D120.use_property_decorate = False
        split_1D120.scale_x = 1.0
        split_1D120.scale_y = 1.0
        split_1D120.alignment = 'Expand'.upper()
        if not True: split_1D120.operator_context = "EXEC_DEFAULT"
        split_1D120.label(text='Steps', icon_value=0)
        split_1D120.prop(bpy.context.scene, 'sna_steps', text='', icon_value=0, emboss=True)
        op = col_D76F1.operator('sna.create_node_86a6a', text='Create Color Ramp', icon_value=0, emboss=True, depress=False)
        if property_exists("bpy.context.active_node.select", globals(), locals()):
            if ((bpy.context.active_node.type == 'VALTORGB') and bpy.context.active_node.select):
                op = col_D76F1.operator('sna.update_node_026a5', text='Update Selected', icon_value=0, emboss=True, depress=False)


def sna_cmaps_enum_items(self, context):
    enum_items = blender_colormaps['sna_cmaps']
    return [make_enum_item(item[0], item[1], item[2], item[3], i) for i, item in enumerate(enum_items)]


def sna_update_node_CE1D2():
    steps = bpy.context.scene.sna_steps
    cmap_name = bpy.context.scene.sna_cmaps
    library = bpy.context.scene.sna_libraries
    cmap_path = os.path.join(os.path.dirname(__file__), 'assets', 'colormaps')
    if library == 'matplotlib':
        cmap = matplotlib.cm.get_cmap(cmap_name)
    else:
        cmap = parse_rgb_to_colormap(f'{cmap_path}/{library}/{cmap_name}.rgb')
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


def sna_create_node_BF021():
    steps = bpy.context.scene.sna_steps
    cmap_name = bpy.context.scene.sna_cmaps
    library = bpy.context.scene.sna_libraries
    cmap_path = os.path.join(os.path.dirname(__file__), 'assets', 'colormaps')
    material = bpy.context.active_object.active_material
    modifier = bpy.context.object.modifiers.active
    if material is not None and bpy.context.area.ui_type == 'ShaderNodeTree':
        nodes = material.node_tree.nodes
        cramp = nodes.new(type='ShaderNodeValToRGB')
    elif modifier is not None and bpy.context.area.ui_type == 'GeometryNodeTree':
        if modifier.type == 'NODES':
            nodes = modifier.node_group.nodes
            cramp = nodes.new(type='ShaderNodeValToRGB')
    if library == 'matplotlib':
        cmap = matplotlib.cm.get_cmap(cmap_name)
    else:
        cmap = parse_rgb_to_colormap(f'{cmap_path}/{library}/{cmap_name}.rgb')
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


class SNA_OT_Create_Node_86A6A(bpy.types.Operator):
    bl_idname = "sna.create_node_86a6a"
    bl_label = "Create Node"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_create_node_BF021()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Update_Node_026A5(bpy.types.Operator):
    bl_idname = "sna.update_node_026a5"
    bl_label = "Update Node"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_update_node_CE1D2()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


import matplotlib


def parse_rgb_to_colormap(file_path):
    """
    Parses an .RGB file and returns a continuous Matplotlib colormap.
    Parameters:
        file_path (str): Path to the .RGB file.
    Returns:
        matplotlib.colors.LinearSegmentedColormap: Continuous colormap object.
    """
    # Read the RGB file
    with open(file_path, 'r') as file:
        lines = file.readlines()
    # Parse the RGB values (assume values are space-separated integers)
    colors = []
    for line in lines:
        parts = line.split()
        if len(parts) == 3:
            r, g, b = map(int, parts)
            colors.append((r / 255.0, g / 255.0, b / 255.0))  # Normalize to [0, 1]
    if not colors:
        raise ValueError("No valid RGB values found in the file.")
    # Create the colormap
    colormap = LinearSegmentedColormap.from_list(file_path.split('/')[-1].split('.')[0], colors)
    return colormap


@persistent
def load_pre_handler_CFC23(dummy):
    cmaps_path = os.path.join(os.path.dirname(__file__), 'assets', 'colormaps')
    libraries = None
    files = os.listdir(cmaps_path)
    libraries = [i for i in files if os.path.isdir(f'{cmaps_path}/{i}')]
    libraries = ['matplotlib']+libraries
    blender_colormaps['sna_libraries'] = []
    for i_1D664 in range(len(libraries)):
        blender_colormaps['sna_libraries'].append([libraries[i_1D664], libraries[i_1D664], '', 0])
    bpy.context.scene.sna_libraries = 'matplotlib'


def sna_libraries_enum_items(self, context):
    enum_items = blender_colormaps['sna_libraries']
    return [make_enum_item(item[0], item[1], item[2], item[3], i) for i, item in enumerate(enum_items)]


class SNA_AddonPreferences_94E08(bpy.types.AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        if not (False):
            layout = self.layout 
            if dependencies['sna_deps_installed']:
                pass
            else:
                col_34AA7 = layout.column(heading='', align=False)
                col_34AA7.alert = False
                col_34AA7.enabled = True
                col_34AA7.active = True
                col_34AA7.use_property_split = False
                col_34AA7.use_property_decorate = False
                col_34AA7.scale_x = 1.0
                col_34AA7.scale_y = 1.0
                col_34AA7.alignment = 'Expand'.upper()
                col_34AA7.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                col_34AA7.label(text='Matplotlib MISSING!', icon_value=619)
                op = col_34AA7.operator('sna.install_deps_a414d', text='Install Matplotlib', icon_value=0, emboss=True, depress=False)


class SNA_OT_Install_Deps_A414D(bpy.types.Operator):
    bl_idname = "sna.install_deps_a414d"
    bl_label = "Install Deps"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        py_path = sys.executable
        subprocess.call([py_path, '-m', 'pip', 'install', 'matplotlib'])
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


good = None
good = True
try:
    import matplotlib


except:
    good = False


dependencies['sna_deps_installed'] = good


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.types.Scene.sna_steps = bpy.props.IntProperty(name='Steps', description='', default=10, subtype='NONE', min=1, max=50)
    bpy.types.Scene.sna_libraries = bpy.props.EnumProperty(name='Libraries', description='', items=sna_libraries_enum_items, update=sna_update_sna_libraries_C21AD)
    bpy.types.Scene.sna_cmaps = bpy.props.EnumProperty(name='cmaps', description='', items=sna_cmaps_enum_items)
    bpy.utils.register_class(SNA_PT_COLORMAPS_4CB30)
    bpy.utils.register_class(SNA_OT_Create_Node_86A6A)
    bpy.utils.register_class(SNA_OT_Update_Node_026A5)
    bpy.app.handlers.load_pre.append(load_pre_handler_CFC23)
    bpy.utils.register_class(SNA_AddonPreferences_94E08)
    bpy.utils.register_class(SNA_OT_Install_Deps_A414D)


def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    del bpy.types.Scene.sna_cmaps
    del bpy.types.Scene.sna_libraries
    del bpy.types.Scene.sna_steps
    bpy.utils.unregister_class(SNA_PT_COLORMAPS_4CB30)
    bpy.utils.unregister_class(SNA_OT_Create_Node_86A6A)
    bpy.utils.unregister_class(SNA_OT_Update_Node_026A5)
    bpy.app.handlers.load_pre.remove(load_pre_handler_CFC23)
    bpy.utils.unregister_class(SNA_AddonPreferences_94E08)
    bpy.utils.unregister_class(SNA_OT_Install_Deps_A414D)
