import math
#from pyexpat import features
import pandas as pd
import argparse
import numpy as np
import sys

# Each scenario has two components: NPC_1 and NPC_2
def get_average_speed(data):
	array = np.ndarray([len(data[0]), 1])
	speeds = []
	for i in range(len(data)):
		# sum = 0.0
		for j in range(len(data[0])):
			array[j] = data[i][j][0]
		speeds.append(array.mean())
	return speeds

def get_number_of_lane_changes(data):
	lane_changes = []
	for i in range(len(data)):
		lc = 0
		for j in range(1, len(data[0])):
			if data[i][j][1] - data[i][j-1][1] != 0:
				lc += 1
		lane_changes.append(lc)
	return lane_changes

def get_actor_data_speed(data, actor):
	sum = np.ndarray([len(data),1])
	stats = []
	for i in range(len(data)):
		sum[i] = math.sqrt(math.pow(data[i][actor].velocity.x, 2.0) + math.pow(data[i][actor].velocity.z, 2.0))
	stats.append(sum.mean())
	stats.append(sum.min())
	stats.append(sum.max())
	stats.append(np.std(sum))
	stats.append(sum.argmax()) # Get the index where speed was max
	stats.append(sum.argmin()) # Get the index where speed was min
	return stats

def get_avg_distances(data):
	dist = [[],[]]
	npcs = ['npc_0', 'npc_1']
	# npc_0 = Sedan, npc_1 = SUV
	x = 0
	for npc in npcs:
		sum = np.ndarray(len(data))
		for i in range(len(data)):
			sum[i] = math.sqrt(math.pow(data[i][npc].transform.position.x - data[i]['ego'].transform.position.x, 2.0) + math.pow(data[i][npc].transform.position.z - data[i]['ego'].transform.position.z, 2.0))
		dist[x].append(sum.mean())
		dist[x].append(sum.min())
		dist[x].append(sum.max())
		dist[x].append(np.std(sum))
		dist[x].append(sum.argmax())
		dist[x].append(sum.argmin())
		x += 1
	return dist

def get_min_max_std_control_speed(data):
	array = np.ndarray([len(data[0]), 1])
	speeds = []
	for i in range(len(data)):
		# sum = 0.0
		for j in range(len(data[0])):
			array[j] = data[i][j][0]
		speeds.append([array.min(), array.max(), np.std(array)])
	return speeds

def get_action_npc_distances(indexes, scenario):
	actions = [] # list to return
	farthest_npc_index = indexes[0][4] if indexes[0][2]>indexes[1][2] else	indexes[1][4]
	farthest_npc = 0 if indexes[0][2]>indexes[1][2] else 1
	closest_npc_index = indexes[0][5] if indexes[0][1]<indexes[1][1] else indexes[1][5]
	closest_npc = 0 if indexes[0][1]<indexes[1][1] else 1
	actions.append(scenario[farthest_npc][int(farthest_npc_index/30)] if int(farthest_npc_index/30)<10 else scenario[farthest_npc][9])
	actions.append(scenario[closest_npc][int(closest_npc_index/30)] if int(closest_npc_index/30)<10 else scenario[closest_npc][9])
	return actions

def get_speed_npc_minmax_dist(indexes,positions):
	speeds = []
	f_npc_index = indexes[0][4] if indexes[0][2]>indexes[1][2] else	indexes[1][4]
	f_npc = 'npc_0' if indexes[0][2]>indexes[1][2] else 'npc_1'
	c_npc_index = indexes[0][5] if indexes[0][1]<indexes[1][1] else indexes[1][5]
	c_npc = 'npc_0' if indexes[0][1]<indexes[1][1] else 'npc_1'
	speeds.append(math.sqrt(math.pow(positions[f_npc_index][f_npc].velocity.x, 2.0) + math.pow(positions[f_npc_index][f_npc].velocity.z, 2.0)))
	speeds.append(math.sqrt(math.pow(positions[c_npc_index][c_npc].velocity.x, 2.0) + math.pow(positions[c_npc_index][c_npc].velocity.z, 2.0)))
	return speeds

def get_actions_npc_minmax_speed(speed_0, speed_1, scenario):
	operations = []
	fastest_npc_index = speed_0[4] if speed_0[2]>speed_1[2] else speed_1[4]
	fastest_npc = 0 if speed_0[2]>speed_1[2] else 1
	slowest_npc_index = speed_0[5] if speed_0[1]<speed_1[1] else speed_1[5]
	slowest_npc = 0 if speed_0[1]<speed_1[1] else 1
	operations.append(scenario[fastest_npc][int(fastest_npc_index/30)] if int(fastest_npc_index/30)<10 else scenario[fastest_npc][9])
	operations.append(scenario[slowest_npc][int(slowest_npc_index/30)] if int(slowest_npc_index/30)<10 else scenario[slowest_npc][9])
	return operations

def get_dist_npc_minmax_speed(speed_0, speed_1, data):
	positions = []
	f_npc_index = speed_0[4] if speed_0[2]>speed_1[2] else speed_1[4] #fastest
	f_npc = 'npc_0' if speed_0[2]>speed_1[2] else 'npc_1'
	s_npc_index = speed_0[5] if speed_0[1]<speed_1[1] else speed_1[5] #slowest
	s_npc = 'npc_0' if speed_0[1]<speed_1[1] else 'npc_1'
	positions.append(math.sqrt(math.pow(data[f_npc_index][f_npc].transform.position.x - data[f_npc_index]['ego'].transform.position.x, 2.0) + math.pow(data[f_npc_index][f_npc].transform.position.z - data[f_npc_index]['ego'].transform.position.z, 2.0)))
	positions.append(math.sqrt(math.pow(data[s_npc_index][s_npc].transform.position.x - data[s_npc_index]['ego'].transform.position.x, 2.0) + math.pow(data[s_npc_index][s_npc].transform.position.z - data[s_npc_index]['ego'].transform.position.z, 2.0)))

	return positions


if __name__ == '__main__':
	print("Starting data parsing")

	# Features dict to construct final csv document
	features_data = {
		'instances': [],
		'algo_collision': [],
		'feature_npc1_avg_control_speed': [],
		# 'feature_npc1_min_control_speed': [],
		'feature_npc1_max_control_speed': [],
		# 'feature_npc1_std_control_speed': [],
		'feature_npc2_avg_control_speed': [],
		# 'feature_npc2_min_control_speed': [],
		'feature_npc2_max_control_speed': [],
		# 'feature_npc2_std_control_speed': [],
		'feature_npc1_number_lane_changes': [],
		'feature_npc2_number_lane_changes': [],
		# 'feature_ego_avg_speed': [],
		# 'feature_ego_min_speed': [],
		'feature_ego_max_speed': [],
		# 'feature_ego_std_speed': [],
		# 'feature_npc1_avg_speed': [],
		# 'feature_npc1_min_speed': [],
		'feature_npc1_max_speed': [],
		# 'feature_npc1_std_speed': [],
		# 'feature_npc2_avg_speed': [],
		# 'feature_npc2_min_speed': [],
		'feature_npc2_max_speed': [],
		# 'feature_npc2_std_speed': [],
		# 'feature_avg_dist_ego_npc1': [],
		# 'feature_min_dist_ego_npc1': [],
		# 'feature_max_dist_ego_npc1': [],
		# 'feature_std_dist_ego_npc1': [],
		# 'feature_avg_dist_ego_npc2': [],
		# 'feature_min_dist_ego_npc2': [],
		# 'feature_max_dist_ego_npc2': [],
		# 'feature_std_dist_ego_npc2': [],
		'feature_npc_avg_dist': [],
		'feature_max_npc_dist': [],
		'feature_min_npc_dist': [],
		'feature_type_npc_max_dist': [],
		'feature_type_npc_min_dist': [],
		'feature_op_npc_max_dist': [],
		'feature_op_npc_min_dist': [],
		'feature_ctrl_speed_npc_max_dist': [],
		'feature_ctrl_speed_npc_min_dist': [],
		'feature_speed_npc_min_dist': [],
		'feature_speed_npc_max_dist': [],
		'feature_avg_speed_npcs': [],
		'feature_max_npc_speed': [],
		# 'feature_min_npc_speed': [],
		'feature_type_npc_max_speed': [],
		# 'feature_type_npc_min_speed': [],
		'feature_op_npc_max_speed': [],
		# 'feature_op_npc_min_speed': [],
		'feature_ctrl_speed_npc_max_speed': [],
		# 'feature_ctrl_speed_npc_min_speed': [],
		'feature_dist_av_npc_max_speed': [],
		# 'feature_dist_av_npc_min_speed': [],
		'source': []
	}

	total_number_scenarios = 404

	for i in range(total_number_scenarios):
		print("Processing scenario " + str(i))
		scenario_file = "scenarios/scenario_" + str(i) + ".obj"
		results_file = "results/scenario_" + str(i) + ".obj"
		records_file = "records/scenario_" + str(i) + ".obj"

		# Get avg NPC speed and Number of lane changes
		scenario_data = pd.read_pickle(scenario_file)
		avg_control_speed = get_average_speed(scenario_data)
		lane_change = get_number_of_lane_changes(scenario_data)
		minmax_npcs = get_min_max_std_control_speed(scenario_data)

		# Get fitness and fault from the results object
		results_data = pd.read_pickle(results_file)
	
		# Get average ego and npc average actual speed and average distance to npc

		record_data = pd.read_pickle(records_file)
		pos_data = record_data['frames']
		ego_data_speed = get_actor_data_speed(pos_data, 'ego')
		npc1_data_speed = get_actor_data_speed(pos_data, 'npc_0')
		npc2_data_speed = get_actor_data_speed(pos_data, 'npc_1')
		avg_distances = get_avg_distances(pos_data)
		actions_npcs_minmax_dist = get_action_npc_distances(avg_distances,scenario_data)
		speed_minmax_dist = get_speed_npc_minmax_dist(avg_distances,pos_data)
		op_npc_minmax_speed = get_actions_npc_minmax_speed(npc1_data_speed, npc2_data_speed, scenario_data)
		pos_npc_minmax_speed = get_dist_npc_minmax_speed(npc1_data_speed, npc2_data_speed, pos_data)

		features_data['instances'].append("scenario"+str(i))
		features_data['algo_collision'].append(0 if results_data['fault'][0]=='normal' else 1)
		features_data['feature_npc1_avg_control_speed'].append(avg_control_speed[0])
		# features_data['feature_npc1_min_control_speed'].append(minmax_npcs[0][0])
		features_data['feature_npc1_max_control_speed'].append(minmax_npcs[0][1])
		# features_data['feature_npc1_std_control_speed'].append(minmax_npcs[0][2])
		features_data['feature_npc2_avg_control_speed'].append(avg_control_speed[1])
		# features_data['feature_npc2_min_control_speed'].append(minmax_npcs[1][0])
		features_data['feature_npc2_max_control_speed'].append(minmax_npcs[1][1])
		# features_data['feature_npc2_std_control_speed'].append(minmax_npcs[1][2])
		features_data['feature_npc1_number_lane_changes'].append(lane_change[0])
		features_data['feature_npc2_number_lane_changes'].append(lane_change[1])
		# features_data['feature_ego_avg_speed'].append(ego_data_speed[0])
		# features_data['feature_ego_min_speed'].append(ego_data_speed[1])
		features_data['feature_ego_max_speed'].append(ego_data_speed[2])
		# features_data['feature_ego_std_speed'].append(ego_data_speed[3])
		# features_data['feature_npc1_avg_speed'].append(npc1_data_speed[0])
		# features_data['feature_npc1_min_speed'].append(npc1_data_speed[1])
		features_data['feature_npc1_max_speed'].append(npc1_data_speed[2])
		# features_data['feature_npc1_std_speed'].append(npc1_data_speed[3])
		# features_data['feature_npc2_avg_speed'].append(npc2_data_speed[0])
		# features_data['feature_npc2_min_speed'].append(npc2_data_speed[1])
		features_data['feature_npc2_max_speed'].append(npc2_data_speed[2])
		# features_data['feature_npc2_std_speed'].append(npc2_data_speed[3])
		# features_data['feature_avg_dist_ego_npc1'].append(avg_distances[0][0])
		# features_data['feature_min_dist_ego_npc1'].append(avg_distances[0][1])
		# features_data['feature_max_dist_ego_npc1'].append(avg_distances[0][2])
		# features_data['feature_std_dist_ego_npc1'].append(avg_distances[0][3])
		# features_data['feature_avg_dist_ego_npc2'].append(avg_distances[1][0])
		# features_data['feature_min_dist_ego_npc2'].append(avg_distances[1][1])
		# features_data['feature_max_dist_ego_npc2'].append(avg_distances[1][2])
		# features_data['feature_std_dist_ego_npc2'].append(avg_distances[1][3])
		features_data['feature_npc_avg_dist'].append((avg_distances[0][0]+avg_distances[1][0])/2) #avg distance of both npcs
		features_data['feature_max_npc_dist'].append(avg_distances[0][2] if avg_distances[0][2]>avg_distances[1][2] else avg_distances[1][2]) #max distance of any npc
		features_data['feature_min_npc_dist'].append(avg_distances[0][1] if avg_distances[0][1]<avg_distances[1][1] else avg_distances[1][1]) #min distance of any npc
		features_data['feature_type_npc_max_dist'].append(1 if avg_distances[0][2]>avg_distances[1][2] else 2) #type of npc which had max distance 1=Sedan, 2=SUV
		features_data['feature_type_npc_min_dist'].append(1 if avg_distances[0][1]<avg_distances[1][1] else 2) #type of npc which had min distance
		features_data['feature_op_npc_max_dist'].append(actions_npcs_minmax_dist[0][1]) #op of npc that had max dist when it was at max dist
		features_data['feature_op_npc_min_dist'].append(actions_npcs_minmax_dist[1][1]) #op of npc that had min dist when it was at min dist (collision TODO: review)
		features_data['feature_ctrl_speed_npc_max_dist'].append(actions_npcs_minmax_dist[0][0]) #ctrl speed of npc which had max dist when at max dist
		features_data['feature_ctrl_speed_npc_min_dist'].append(actions_npcs_minmax_dist[1][0]) #ctrl speed of npc which had min dist when at min dist (collision)
		features_data['feature_speed_npc_min_dist'].append(speed_minmax_dist[1]) #speed of npc with min dist when it was at min dist
		features_data['feature_speed_npc_max_dist'].append(speed_minmax_dist[0]) #speed of npc with max dist when it was at max dist
		features_data['feature_avg_speed_npcs'].append((npc1_data_speed[0]+npc2_data_speed[0])/2) #average speed of both npcs
		features_data['feature_max_npc_speed'].append(npc1_data_speed[2] if npc1_data_speed[2]>npc2_data_speed[2] else npc2_data_speed[2]) #max speed of any npc
		# features_data['feature_min_npc_speed'].append(npc1_data_speed[1] if npc1_data_speed[1]<npc2_data_speed[1] else npc2_data_speed[1]) #min speed of any npc
		features_data['feature_type_npc_max_speed'].append(1 if npc1_data_speed[2]>npc2_data_speed[2] else 2) #type of npc which had max speed
		# features_data['feature_type_npc_min_speed'].append(1 if npc1_data_speed[1]<npc2_data_speed[1] else 2) #type of npc which had min speed
		features_data['feature_op_npc_max_speed'].append(op_npc_minmax_speed[0][1]) #op of npc with max speed when it was at max speed
		# features_data['feature_op_npc_min_speed'].append(op_npc_minmax_speed[1][1]) #op of npc with min speed with it was at min speed
		features_data['feature_ctrl_speed_npc_max_speed'].append(op_npc_minmax_speed[0][0]) #ctrl speed of npc which had max speed when it was at max speed
		# features_data['feature_ctrl_speed_npc_min_speed'].append(op_npc_minmax_speed[1][0]) #strl speed of npc which had min speed whtn it was at min speed
		features_data['feature_dist_av_npc_max_speed'].append(pos_npc_minmax_speed[0])
		# features_data['feature_dist_av_npc_min_speed'].append(pos_npc_minmax_speed[1])
		features_data['source'].append(sys.argv[1])



	features = pd.DataFrame.from_dict(features_data)
	features.to_csv("metadata.csv", index=False)
	print("Features file created")




