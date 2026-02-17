This is a script for Blender, that automatically appends a tool rig to the R6 IK + FK Blender Rig by Aeresei
https://devforum.roblox.com/t/r6-ik-fk-blender-rig-v21/3586405.

Instead of going and creating constraints, joining armatures, parenting bones, this script will do it all for you so that animations made with the R6 IK + FK rig with a tool can be exported to Roblox through the Blender plugin.

<bold> Steps: </bold>

Using Blender plugin in Roblox Studio, export a rig of a character attached to the tool (I guess you don't really need the character rig actually).

When importing to blender, move everything into a collection "Tool".
"Handle" - Tool object
"ToolArmature" - The armature of the exported rig (If you exported with a character, delete all bones except for the Handle bone)

<img width="314" height="78" alt="image" src="https://github.com/user-attachments/assets/071fe393-a19d-42af-8341-e80d64d17015" />



Run the code in the R6 IK - FK blend file.
