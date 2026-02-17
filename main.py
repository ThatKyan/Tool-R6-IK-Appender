import bpy

                
                
blender_file_with_tool = r"BLENDER FILE WITH EXPORTED TOOL RIG.blend"



tool_collection_name = r"Tool"
tool_armature_name = r"ToolArmature"

def set_collection_visible(layer_collection, collection_name, is_Visible):

    if layer_collection.name == collection_name:
        layer_collection.hide_viewport = is_Visible
        layer_collection.exclude = is_Visible
        layer_collection.collection.hide_select = is_Visible

        for anObject in layer_collection.collection.objects:
            anObject.hide_select  = is_Visible
            anObject.hide_viewport = is_Visible
        
        return True
    

    for child in layer_collection.children:
        if set_collection_visible(child, collection_name, is_Visible):
            return True
    return False


set_collection_visible(bpy.context.view_layer.layer_collection, "Rig1", False)




meta_rig = bpy.data.objects.get("Rig")
primary_armature = bpy.data.objects.get("__PrimaryArmature")

meta_rig.hide_select = False
meta_rig.hide_viewport = False


with bpy.data.libraries.load(blender_file_with_tool, link=False) as (data_from, data_to):
    if tool_collection_name in data_from.collections:
        data_to.collections = [tool_collection_name]

for col in data_to.collections:
    if col:
        bpy.context.scene.collection.children.link(col)
        

get_tool_armature = bpy.data.objects.get(tool_armature_name)
tool_object = bpy.data.objects.get("Handle")

##### Duplicate armature and join with meta rig
meta_rig_tool_armature = get_tool_armature.copy()
meta_rig_tool_armature.data = get_tool_armature.data.copy()
bpy.context.scene.collection.objects.link(meta_rig_tool_armature)



for obj in bpy.context.selected_objects:
    obj.select_set(False)  # clear selection

for obj in [meta_rig, meta_rig_tool_armature]:
    obj.select_set(True)   # select the ones to join

bpy.context.view_layer.objects.active =  meta_rig

bpy.ops.object.join()


#####



##### the spare armature and join with PRIMARY ARMATURE
primary_armature = bpy.data.objects.get("__PrimaryArmature")
get_tool_armature = bpy.data.objects.get(tool_armature_name)
for obj in bpy.context.selected_objects:
    obj.select_set(False)  # clear selection

for obj in [primary_armature, get_tool_armature]:
    obj.select_set(True)   # select the ones to join
    

bpy.context.view_layer.objects.active =  primary_armature

bpy.ops.object.join()

#####



##### in meta rig, parent bone to right arm
for obj in bpy.context.selected_objects:
    obj.select_set(False)  # clear selection
    
bpy.context.view_layer.objects.active = meta_rig
bpy.ops.object.mode_set(mode='EDIT')

edit_bones = meta_rig.data.edit_bones

edit_bones["Handle"].parent = edit_bones["Right Arm"]
edit_bones["Handle"].use_connect = False



#####

##### add bone constraints to meta rig handle
bpy.ops.object.mode_set(mode='POSE')

pose_bones = meta_rig.pose.bones
handleBone = pose_bones.get("Handle")


# copy location constraint
copy_location_constraint = handleBone.constraints.new(type='COPY_LOCATION')

copy_location_constraint.target = primary_armature        
copy_location_constraint.subtarget = "Handle"


# Child of constraint
child_of_constraint = handleBone.constraints.new(type='CHILD_OF')

child_of_constraint.target = primary_armature        
child_of_constraint.subtarget = "Handle"

child_of_constraint.use_location_x = False
child_of_constraint.use_location_y = False
child_of_constraint.use_location_z = False


bpy.context.active_object.data.bones.active = handleBone.bone
with bpy.context.temp_override(active_object=handleBone):
    bpy.ops.constraint.childof_set_inverse(constraint="Child Of", owner='BONE')

handleBone.bone.use_inherit_rotation = False
    


##### child of constraint on primary armature handle to primary armature right hand

for obj in bpy.context.selected_objects:
    obj.select_set(False)  # clear selection
    
primary_armature.select_set(True)
bpy.context.view_layer.objects.active = primary_armature
bpy.ops.object.mode_set(mode='POSE')

pose_bones = primary_armature.pose.bones
handleBone = pose_bones.get("Handle")

child_of_constraint = handleBone.constraints.new(type='CHILD_OF')

child_of_constraint.target = primary_armature        
child_of_constraint.subtarget = "RightHand"


bpy.context.active_object.data.bones.active = handleBone.bone
with bpy.context.temp_override(active_object=handleBone):
    bpy.ops.constraint.childof_set_inverse(constraint="Child Of", owner='BONE')
    
    

######

meta_rig.hide_set(True)
