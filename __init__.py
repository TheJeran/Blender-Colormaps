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
    "version" : (1, 4, 0),
    "location" : "",
    "warning" : "",
    "doc_url": "https://github.com/TheJeran/Blender-Colormaps", 
    "tracker_url": "", 
    "category" : "Node" 
}


import bpy
import bpy.utils.previews
import os
from collections.abc import Sized
from bpy.app.handlers import persistent




def string_to_int(value):
    if value.isdigit():
        return int(value)
    return 0


def string_to_icon(value):
    if value in bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items.keys():
        return bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items[value].value
    return string_to_int(value)


addon_keymaps = {}
_icons = None
visual_scripting_editor = {'sna_cmaps': [], 'sna_libraries': [], 'sna_preview': 0, }


def property_exists(prop_path, glob, loc):
    try:
        eval(prop_path, glob, loc)
        return True
    except:
        return False


_item_map = dict()


def make_enum_item(_id, name, descr, preview_id, uid):
    lookup = str(_id)+"\0"+str(name)+"\0"+str(descr)+"\0"+str(preview_id)+"\0"+str(uid)
    if not lookup in _item_map:
        _item_map[lookup] = (_id, name, descr, preview_id, uid)
    return _item_map[lookup]


def sna_update_sna_libraries_96FE5(self, context):
    sna_updated_prop = self.sna_libraries
    library = sna_updated_prop
    cmap_path = os.path.join(os.path.dirname(__file__), 'assets', 'colormaps')
    cmaps = None
    files = os.listdir(f"{cmap_path}/{library}")
    cmaps = [i.split('.')[0] for i in files if i.endswith('.rgb')]
    visual_scripting_editor['sna_cmaps'] = []
    for i_EEE6A in range(len(cmaps)):
        visual_scripting_editor['sna_cmaps'].append([cmaps[i_EEE6A], cmaps[i_EEE6A], '', 0])
    cmap_name = bpy.context.scene.sna_cmaps
    library = bpy.context.scene.sna_libraries
    cmaps = os.path.join(os.path.dirname(__file__), 'assets', 'colormaps')
    file_path = ''
    img_id = None

    def colors_2_img(colors, file_path):
        color_array = np.array(colors, dtype=np.float32)
        height = 256
        img_array = np.tile(color_array, (height, 1, 1)).reshape(-1)
        image_name = "ColorPalette"
        if image_name in bpy.data.images:
            bpy.data.images.remove(bpy.data.images[image_name])
        img = bpy.data.images.new(name=image_name, width=256, height=height, alpha=True, float_buffer=False)
        # 4. Fast-copy the numpy array directly into Blender's pixel buffer
        img.pixels.foreach_set(img_array)
        # 5. Save to disk
    #    img.filepath_raw = file_path
    #    img.file_format = 'PNG'
    #    img.save()
        img.pack()
        if img.preview is None:
            img.asset_generate_preview()  # Generates the preview object
            # Alternative fallback if needed: img.preview_ensure()
        return img.preview.icon_id
    cmap_path = f"{cmaps}/{library}/{cmap_name}.rgb"
    cm = parse_rgb_to_colormap(cmap_path,discrete=True)
    colors = np.array([cm(i/256) for i in range(256)])
    img_id = colors_2_img(colors, file_path)
    visual_scripting_editor['sna_preview'] = img_id


def sna_update_sna_cmaps_A6B7E(self, context):
    sna_updated_prop = self.sna_cmaps
    cmap_name = sna_updated_prop
    library = bpy.context.scene.sna_libraries
    cmaps = os.path.join(os.path.dirname(__file__), 'assets', 'colormaps')
    file_path = ''
    img_id = None

    def colors_2_img(colors, file_path):
        color_array = np.array(colors, dtype=np.float32)
        height = 256
        img_array = np.tile(color_array, (height, 1, 1)).reshape(-1)
        image_name = "ColorPalette"
        if image_name in bpy.data.images:
            bpy.data.images.remove(bpy.data.images[image_name])
        img = bpy.data.images.new(name=image_name, width=256, height=height, alpha=True, float_buffer=False)
        # 4. Fast-copy the numpy array directly into Blender's pixel buffer
        img.pixels.foreach_set(img_array)
        # 5. Save to disk
    #    img.filepath_raw = file_path
    #    img.file_format = 'PNG'
    #    img.save()
        img.pack()
        if img.preview is None:
            img.asset_generate_preview()  # Generates the preview object
            # Alternative fallback if needed: img.preview_ensure()
        return img.preview.icon_id
    cmap_path = f"{cmaps}/{library}/{cmap_name}.rgb"
    cm = parse_rgb_to_colormap(cmap_path,discrete=True)
    colors = np.array([cm(i/256) for i in range(256)])
    img_id = colors_2_img(colors, file_path)
    visual_scripting_editor['sna_preview'] = img_id


class SNA_PT_COLORMAPS_4B498(bpy.types.Panel):
    bl_label = 'Colormaps'
    bl_idname = 'SNA_PT_COLORMAPS_4B498'
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
        col_4D304 = layout.column(heading='', align=False)
        col_4D304.alert = False
        col_4D304.enabled = True
        col_4D304.active = True
        col_4D304.use_property_split = False
        col_4D304.use_property_decorate = False
        col_4D304.scale_x = 1.0
        col_4D304.scale_y = 1.0
        col_4D304.alignment = 'Expand'.upper()
        col_4D304.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        split_3409E = col_4D304.split(factor=0.4000000059604645, align=False)
        split_3409E.alert = False
        split_3409E.enabled = True
        split_3409E.active = True
        split_3409E.use_property_split = False
        split_3409E.use_property_decorate = False
        split_3409E.scale_x = 1.0
        split_3409E.scale_y = 1.0
        split_3409E.alignment = 'Expand'.upper()
        if not True: split_3409E.operator_context = "EXEC_DEFAULT"
        split_CC9B1 = split_3409E.split(factor=0.7599999904632568, align=False)
        split_CC9B1.alert = False
        split_CC9B1.enabled = True
        split_CC9B1.active = True
        split_CC9B1.use_property_split = False
        split_CC9B1.use_property_decorate = False
        split_CC9B1.scale_x = 1.0
        split_CC9B1.scale_y = 1.0
        split_CC9B1.alignment = 'Expand'.upper()
        if not True: split_CC9B1.operator_context = "EXEC_DEFAULT"
        split_CC9B1.label(text='Library', icon_value=0)
        op = split_CC9B1.operator('sna.rescan_666e2', text='', icon_value=string_to_icon('VIEWZOOM'), emboss=True, depress=False)
        split_3409E.prop(bpy.context.scene, 'sna_libraries', text='', icon_value=0, emboss=True)
        split_5B2A9 = col_4D304.split(factor=0.4000000059604645, align=False)
        split_5B2A9.alert = False
        split_5B2A9.enabled = True
        split_5B2A9.active = True
        split_5B2A9.use_property_split = False
        split_5B2A9.use_property_decorate = False
        split_5B2A9.scale_x = 1.0
        split_5B2A9.scale_y = 1.0
        split_5B2A9.alignment = 'Expand'.upper()
        if not True: split_5B2A9.operator_context = "EXEC_DEFAULT"
        split_5B2A9.label(text='Color Map', icon_value=0)
        split_5B2A9.prop(bpy.context.scene, 'sna_cmaps', text='', icon_value=0, emboss=True)
        split_2459A = col_4D304.split(factor=0.5, align=False)
        split_2459A.alert = False
        split_2459A.enabled = True
        split_2459A.active = True
        split_2459A.use_property_split = False
        split_2459A.use_property_decorate = False
        split_2459A.scale_x = 1.0
        split_2459A.scale_y = 1.0
        split_2459A.alignment = 'Expand'.upper()
        if not True: split_2459A.operator_context = "EXEC_DEFAULT"
        split_2459A.label(text='Steps', icon_value=0)
        split_2459A.prop(bpy.context.scene, 'sna_steps', text='', icon_value=0, emboss=True)
        op = col_4D304.operator('sna.create_node_30af9', text='Create Color Ramp', icon_value=string_to_icon('COLORSET_04_VEC'), emboss=True, depress=False)
        if property_exists("bpy.context.active_node.select", globals(), locals()):
            if ((bpy.context.active_node.type == 'VALTORGB') and bpy.context.active_node.select):
                op = col_4D304.operator('sna.update_node_48605', text='Update Selected', icon_value=string_to_icon('COLORSET_01_VEC'), emboss=True, depress=False)
        col_670EA = col_4D304.column(heading='', align=False)
        col_670EA.alert = False
        col_670EA.enabled = True
        col_670EA.active = True
        col_670EA.use_property_split = False
        col_670EA.use_property_decorate = False
        col_670EA.scale_x = 3.0
        col_670EA.scale_y = 1.0
        col_670EA.alignment = 'Center'.upper()
        col_670EA.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_670EA.label(text='Preview', icon_value=0)
        col_670EA.template_icon(icon_value=visual_scripting_editor['sna_preview'], scale=6.0)


class SNA_OT_Rescan_666E2(bpy.types.Operator):
    bl_idname = "sna.rescan_666e2"
    bl_label = "Rescan"
    bl_description = "Scan for color Libraries"
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
        visual_scripting_editor['sna_libraries'] = []
        for i_8F4D6 in range(len(libraries)):
            visual_scripting_editor['sna_libraries'].append([libraries[i_8F4D6], libraries[i_8F4D6], '', 0])
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


def sna_libraries_enum_items(self, context):
    enum_items = visual_scripting_editor['sna_libraries']
    return [make_enum_item(item[0], item[1], item[2], item[3], i) for i, item in enumerate(enum_items)]


@persistent
def load_post_handler_D80C7(dummy):
    cmaps_path = os.path.join(os.path.dirname(__file__), 'assets', 'colormaps')
    libraries = None
    files = os.listdir(cmaps_path)
    libraries = [i for i in files if os.path.isdir(f'{cmaps_path}/{i}')]
    print(libraries)
    visual_scripting_editor['sna_libraries'] = []
    for i_B2993 in range(len(libraries)):
        visual_scripting_editor['sna_libraries'].append([libraries[i_B2993], libraries[i_B2993], '', 0])
    bpy.context.scene.sna_libraries = 'matplotlib'


class SNA_OT_Update_Node_48605(bpy.types.Operator):
    bl_idname = "sna.update_node_48605"
    bl_label = "Update Node"
    bl_description = "Update the selected color ramp"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
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
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Create_Node_30Af9(bpy.types.Operator):
    bl_idname = "sna.create_node_30af9"
    bl_label = "Create Node"
    bl_description = "Create a color ramp from the selected Colormap"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
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
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_cmaps_enum_items(self, context):
    enum_items = visual_scripting_editor['sna_cmaps']
    return [make_enum_item(item[0], item[1], item[2], item[3], i) for i, item in enumerate(enum_items)]


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.types.Scene.sna_steps = bpy.props.IntProperty(name='steps', description='', default=10, subtype='NONE')
    bpy.types.Scene.sna_libraries = bpy.props.EnumProperty(name='Libraries', description='', items=sna_libraries_enum_items, update=sna_update_sna_libraries_96FE5)
    bpy.types.Scene.sna_cmaps = bpy.props.EnumProperty(name='cmaps', description='', items=sna_cmaps_enum_items, update=sna_update_sna_cmaps_A6B7E)
    bpy.utils.register_class(SNA_PT_COLORMAPS_4B498)
    bpy.utils.register_class(SNA_OT_Rescan_666E2)
    bpy.app.handlers.load_post.append(load_post_handler_D80C7)
    bpy.utils.register_class(SNA_OT_Update_Node_48605)
    bpy.utils.register_class(SNA_OT_Create_Node_30Af9)


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
    bpy.utils.unregister_class(SNA_PT_COLORMAPS_4B498)
    bpy.utils.unregister_class(SNA_OT_Rescan_666E2)
    bpy.app.handlers.load_post.remove(load_post_handler_D80C7)
    bpy.utils.unregister_class(SNA_OT_Update_Node_48605)
    bpy.utils.unregister_class(SNA_OT_Create_Node_30Af9)
