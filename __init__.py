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
    "description" : "Import curated or custom colormaps into Blender",
    "blender" : (4, 2, 0),
    "version" : (1, 3, 0),
    "location" : "",
    "warning" : "",
    "doc_url": "https://github.com/TheJeran/Blender-Colormaps", 
    "tracker_url": "", 
    "category" : "3D View" 
}


import bpy
import bpy.utils.previews
import os
from bpy.app.handlers import persistent


addon_keymaps = {}
_icons = None
colormaps = {'sna_cmaps': [], 'sna_libraries': [], }


def sna_update_sna_libraries_BA574(self, context):
    sna_updated_prop = self.sna_libraries
    library = sna_updated_prop
    cmap_path = os.path.join(os.path.dirname(__file__), 'assets', 'colormaps')
    cmaps = None
    files = os.listdir(f"{cmap_path}/{library}")
    cmaps = [i.split('.')[0] for i in files if i.endswith('.rgb')]
    colormaps['sna_cmaps'] = []
    for i_DFA7F in range(len(cmaps)):
        colormaps['sna_cmaps'].append([cmaps[i_DFA7F], cmaps[i_DFA7F], '', 0])


_item_map = dict()


def make_enum_item(_id, name, descr, preview_id, uid):
    lookup = str(_id)+"\0"+str(name)+"\0"+str(descr)+"\0"+str(preview_id)+"\0"+str(uid)
    if not lookup in _item_map:
        _item_map[lookup] = (_id, name, descr, preview_id, uid)
    return _item_map[lookup]


def property_exists(prop_path, glob, loc):
    try:
        eval(prop_path, glob, loc)
        return True
    except:
        return False


class SNA_OT_Rescan_1472F(bpy.types.Operator):
    bl_idname = "sna.rescan_1472f"
    bl_label = "Rescan"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        cmaps_path = os.path.join(os.path.dirname(__file__), 'assets', 'colormaps')
        libraries = None
        files = os.listdir(cmaps_path)
        libraries = [i for i in files if os.path.isdir(f'{cmaps_path}/{i}')]
        print(libraries)
        colormaps['sna_libraries'] = []
        for i_78D83 in range(len(libraries)):
            colormaps['sna_libraries'].append([libraries[i_78D83], libraries[i_78D83], '', 0])
        bpy.context.scene.sna_libraries = 'matplotlib'
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


import numpy as np


def parse_rgb_to_colormap(file_path,discrete=False):
    """
    Parses an .RGB file and returns a continuous/discrete Matplotlib colormap.
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
    colormap = SimpleColormap(colors)
    return colormap


class SimpleColormap:
    """
    Simplified colormap for RGB tuple lists.
    Assumes colors are always provided as (r, g, b) tuples with values in [0, 1].
    """

    def __init__(self, colors, name='simple_cmap'):
        """
        Parameters
        ----------
        colors : list of tuples
            List of (r, g, b) tuples with values in [0, 1].
        name : str, optional
            The name of the colormap.
        """
        self.name = name
        self.colors = colors
        self.N = len(colors)
        self._lut = None
        self._init()

    def _init(self):
        """Generate the lookup table from RGB tuples."""
        # Convert list of RGB tuples to RGBA array (add alpha=1.0)
        self._lut = np.zeros((self.N, 4), float)
        for i, (r, g, b) in enumerate(self.colors):
            self._lut[i] = [r, g, b, 1.0]

    def __call__(self, X, alpha=None, bytes=False):
        """
        Map values to colors.
        Parameters
        ----------
        X : float or array-like
            Values in [0.0, 1.0] to map to colors.
        alpha : float, optional
            Override alpha value.
        bytes : bool
            If True, return uint8 values [0, 255], else float [0, 1].
        Returns
        -------
        RGBA color(s) corresponding to X.
        """
        xa = np.array(X, copy=True)
        # Map [0, 1] to indices [0, N-1]
        xa = np.clip(xa * self.N, 0, self.N - 1).astype(int)
        # Get colors from lookup table
        rgba = self._lut[xa]
        # Override alpha if provided
        if alpha is not None:
            rgba[..., -1] = np.clip(alpha, 0, 1)
        # Convert to bytes if requested
        if bytes:
            rgba = (rgba * 255).astype(np.uint8)
        # Return as tuple if input was scalar
        if not np.iterable(X):
            return tuple(rgba)
        return rgba

    def reversed(self, name=None):
        """Return a reversed version of the colormap."""
        if name is None:
            name = self.name + "_r"
        return SimpleColormap(list(reversed(self.colors)), name=name)


def sna_create_node_8D210():
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
    cmap = parse_rgb_to_colormap(f'{cmap_path}\\{library}\\{cmap_name}.rgb')
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


class SNA_OT_Create_Node_Df11C(bpy.types.Operator):
    bl_idname = "sna.create_node_df11c"
    bl_label = "Create Node"
    bl_description = "Create a color ramp from the selected Colormap"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_create_node_8D210()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_update_node_AFB3D():
    steps = bpy.context.scene.sna_steps
    cmap_name = bpy.context.scene.sna_cmaps
    library = bpy.context.scene.sna_libraries
    cmap_path = os.path.join(os.path.dirname(__file__), 'assets', 'colormaps')
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


class SNA_OT_Update_Node_17224(bpy.types.Operator):
    bl_idname = "sna.update_node_17224"
    bl_label = "Update Node"
    bl_description = "Update the selected color ramp"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        sna_update_node_AFB3D()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_cmaps_enum_items(self, context):
    enum_items = colormaps['sna_cmaps']
    return [make_enum_item(item[0], item[1], item[2], item[3], i) for i, item in enumerate(enum_items)]


@persistent
def load_post_handler_18205(dummy):
    cmaps_path = os.path.join(os.path.dirname(__file__), 'assets', 'colormaps')
    libraries = None
    files = os.listdir(cmaps_path)
    libraries = [i for i in files if os.path.isdir(f'{cmaps_path}/{i}')]
    print(libraries)
    colormaps['sna_libraries'] = []
    for i_E2B55 in range(len(libraries)):
        colormaps['sna_libraries'].append([libraries[i_E2B55], libraries[i_E2B55], '', 0])
    bpy.context.scene.sna_libraries = 'matplotlib'


def sna_libraries_enum_items(self, context):
    enum_items = colormaps['sna_libraries']
    return [make_enum_item(item[0], item[1], item[2], item[3], i) for i, item in enumerate(enum_items)]


class SNA_PT_COLORMAPS_879CE(bpy.types.Panel):
    bl_label = 'Colormaps'
    bl_idname = 'SNA_PT_COLORMAPS_879CE'
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 0
    bl_parent_id = 'NODE_PT_active_tool'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        col_A7E4B = layout.column(heading='', align=False)
        col_A7E4B.alert = False
        col_A7E4B.enabled = True
        col_A7E4B.active = True
        col_A7E4B.use_property_split = False
        col_A7E4B.use_property_decorate = False
        col_A7E4B.scale_x = 1.0
        col_A7E4B.scale_y = 1.0
        col_A7E4B.alignment = 'Expand'.upper()
        col_A7E4B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        split_6AEA7 = col_A7E4B.split(factor=0.4000000059604645, align=False)
        split_6AEA7.alert = False
        split_6AEA7.enabled = True
        split_6AEA7.active = True
        split_6AEA7.use_property_split = False
        split_6AEA7.use_property_decorate = False
        split_6AEA7.scale_x = 1.0
        split_6AEA7.scale_y = 1.0
        split_6AEA7.alignment = 'Expand'.upper()
        if not True: split_6AEA7.operator_context = "EXEC_DEFAULT"
        split_84EC1 = split_6AEA7.split(factor=0.7599999904632568, align=False)
        split_84EC1.alert = False
        split_84EC1.enabled = True
        split_84EC1.active = True
        split_84EC1.use_property_split = False
        split_84EC1.use_property_decorate = False
        split_84EC1.scale_x = 1.0
        split_84EC1.scale_y = 1.0
        split_84EC1.alignment = 'Expand'.upper()
        if not True: split_84EC1.operator_context = "EXEC_DEFAULT"
        split_84EC1.label(text='Library', icon_value=0)
        op = split_84EC1.operator('sna.rescan_1472f', text='', icon_value=111, emboss=True, depress=False)
        split_6AEA7.prop(bpy.context.scene, 'sna_libraries', text='', icon_value=0, emboss=True)
        split_8B78A = col_A7E4B.split(factor=0.4000000059604645, align=False)
        split_8B78A.alert = False
        split_8B78A.enabled = True
        split_8B78A.active = True
        split_8B78A.use_property_split = False
        split_8B78A.use_property_decorate = False
        split_8B78A.scale_x = 1.0
        split_8B78A.scale_y = 1.0
        split_8B78A.alignment = 'Expand'.upper()
        if not True: split_8B78A.operator_context = "EXEC_DEFAULT"
        split_8B78A.label(text='Color Map', icon_value=0)
        split_8B78A.prop(bpy.context.scene, 'sna_cmaps', text='', icon_value=0, emboss=True)
        split_6F791 = col_A7E4B.split(factor=0.4000000059604645, align=False)
        split_6F791.alert = False
        split_6F791.enabled = True
        split_6F791.active = True
        split_6F791.use_property_split = False
        split_6F791.use_property_decorate = False
        split_6F791.scale_x = 1.0
        split_6F791.scale_y = 1.0
        split_6F791.alignment = 'Expand'.upper()
        if not True: split_6F791.operator_context = "EXEC_DEFAULT"
        split_6F791.label(text='Steps', icon_value=0)
        split_6F791.prop(bpy.context.scene, 'sna_steps', text='', icon_value=0, emboss=True)
        op = col_A7E4B.operator('sna.create_node_df11c', text='Create Color Ramp', icon_value=791, emboss=True, depress=False)
        if property_exists("bpy.context.active_node.select", globals(), locals()):
            if (bpy.context.active_node.select and (bpy.context.active_node.type == 'VALTORGB')):
                op = col_A7E4B.operator('sna.update_node_17224', text='Update Selected', icon_value=0, emboss=True, depress=False)


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.types.Scene.sna_steps = bpy.props.IntProperty(name='Steps', description='', default=10, subtype='NONE')
    bpy.types.Scene.sna_libraries = bpy.props.EnumProperty(name='Libraries', description='', items=sna_libraries_enum_items, update=sna_update_sna_libraries_BA574)
    bpy.types.Scene.sna_cmaps = bpy.props.EnumProperty(name='cmaps', description='', items=sna_cmaps_enum_items)
    bpy.utils.register_class(SNA_OT_Rescan_1472F)
    bpy.utils.register_class(SNA_OT_Create_Node_Df11C)
    bpy.utils.register_class(SNA_OT_Update_Node_17224)
    bpy.app.handlers.load_post.append(load_post_handler_18205)
    bpy.utils.register_class(SNA_PT_COLORMAPS_879CE)


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
    bpy.utils.unregister_class(SNA_OT_Rescan_1472F)
    bpy.utils.unregister_class(SNA_OT_Create_Node_Df11C)
    bpy.utils.unregister_class(SNA_OT_Update_Node_17224)
    bpy.app.handlers.load_post.remove(load_post_handler_18205)
    bpy.utils.unregister_class(SNA_PT_COLORMAPS_879CE)
