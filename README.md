# Blender-Colormaps

![colormaps](https://user-images.githubusercontent.com/76405582/182592080-b02c832b-cc95-4c06-812c-8621240ce2d3.png)

This is an addon to quickly and efficiently load colormaps into the colorramp node in Blender

## Installation
Simply install the .zip from this repository in Blender. 
This addon uses matplotlib which needs to be installed to the blender python environment. After activating the addon you will be notified if you need to install matplotlib.

![image](https://github.com/user-attachments/assets/10ddee0f-860d-496f-8c3b-d9077beaa714)

### _Matplotlib not installing?_
On windows there can be permission errors that prevent you from writing to the site-packages folder. If that happens you need to manaully install matplotlib there


## Usage
Find it in the tools section of node menus

After install, everything will be blank. Click the search button to scan the librarys folder. It will rescan automatically each time you start blender

![image](https://github.com/user-attachments/assets/2ea02348-ddec-4f14-9386-4ec6962d0247)

Currently there are **six** built-in color libraries: [Matplotlib](https://matplotlib.org/stable/tutorials/colors/colormaps.html), [MetBrewer](https://github.com/BlakeRMills/MetBrewer), [Cmocean](https://matplotlib.org/cmocean/), [scientific](https://pratiman-91.github.io/colormaps/docs/collections/scientific), [carbonplan](https://pratiman-91.github.io/colormaps/docs/collections/carbonplan), and [tableau](https://pratiman-91.github.io/colormaps/docs/collections/tableau)

![image](https://github.com/user-attachments/assets/6a70a41f-79da-4e3e-9c14-e0d92230a540)

You can update ColorRamp nodes when one is selected

![image](https://github.com/user-attachments/assets/2358f8fd-0dae-459e-a7b9-f6530de26a32)

Gamma-correction ensures that colors in Blender are perceived the same way as in matplotlib

![image](https://github.com/user-attachments/assets/af2f75ef-a9af-4a6c-b301-f01632dfc5b8)

## Custom ColorMaps
You can add additional and custom libraries by creating folders in the colormaps folder (`blender_colormaps/assets/colormaps`) in the install folder of the addon.

![image](https://github.com/user-attachments/assets/1cb49c38-47f3-4352-999b-cbb4ab44931a)

![image](https://github.com/user-attachments/assets/88dc607f-3d48-4624-bfc5-5686ae9fc7f3)

Colormaps are `.rgb` format. 

## Examples
![german_tree_ages_credits](https://github.com/TheJeran/Blender-Colormaps/assets/76405582/e043d7d0-66ac-444e-8b4a-60a599b2f1ef)
![hairs](https://github.com/TheJeran/Blender-Colormaps/assets/76405582/62ebb1e6-7389-41f4-9457-88355e84cc61)
![pole_year0022](https://github.com/TheJeran/Blender-Colormaps/assets/76405582/6251b49e-1c4e-4697-b843-97862a45d811)




