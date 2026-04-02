from nuscenes.nuscenes import NuScenes
import os
nusc = NuScenes(version='v1.0-test', dataroot='/workspaces/Prius2audioscene/dataset/output/', verbose=True)
my_scene = nusc.scene[0]
first_sample_token = my_scene['first_sample_token']
#nusc.render_scene_channel(my_scene,"CAM_FRONT")

my_sample = nusc.get('sample', first_sample_token)
sensor = 'LIDAR_TOP'
lidar_data = nusc.get('sample_data', my_sample['data'][sensor])
# my_annotation_token = my_sample['anns'][0]
# my_annotation_metadata =  nusc.get('sample_annotation', my_annotation_token)
# my_annotation_token = my_sample['anns'][0]
# my_annotation_metadata =  nusc.get('sample_annotation', my_annotation_token)
nusc.render_sample_data(my_sample['data'][sensor], with_anns=False, box_vis_level=1,underlay_map=False, verbose=True, use_flat_vehicle_coordinates=False)