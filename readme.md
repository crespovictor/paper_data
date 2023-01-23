# Readme
Data from two runs of AV-Fuzzer and Random Testing for Autonomous Vehicles

## Folder Structure

<pre>
root
| README.md
| 2022-09-22
| __ AV-Fuzzer
| ______ records
| ______ results
| ______ scenarios
| __ random
| ______ records
| ______ results
| ______ scenarios
| __ ISA_Files
| ______ ISA_Results
| 2023-01-19
| __ AV-Fuzzer
| ______ apollo_data
| ______ records
| ______ results
| ______ scenarios
| __ random
| ______ apollo_data
| ______ records
| ______ results
| ______ scenarios
| __ ISA_Files
| ______ ISA_Results
| combiningboth
| __ ISA_Results
</pre>

### Scenario Data
`records` folder includes the data from all actors in the simulation at each time step (~1/5th of a second), `results` include the results of each scenario: fitness function and fault type (normal - no crash, ego, and npc - crash), `scenarios` contains the different values for the control operation (keep lane, turn left, turn right) and speed for each NPC that the algoritm controls.

### Instance Space Analysis

`ISA_Files` include the `metadata.csv` file and the results folder tht was generated from running ISA in Matlab in a local environment.

`combiningboth` includes the ISA metadata file and the results from aggregating both runs into one single file and running ISA with it.

### Apollo Data
In `apollo_data` is included the data gathered from running the simulation **and** recording the real-time apollo data and operations from the Cyber bridge. This data is only included in latest runs of AV-Fuzzer and Random Testing. This data **was not** included in the ISA Analysis for these recordings.

# Features

The list of features used in the ISA analysis includes:

| Feature | Description |
| ------- | ----------- |
| npc1_avg_control_speed | Average controlling speed (from algorithm) for NPC1 |
| npc1_max_control_speed | Maximum controlling speed (from algorithm) for NPC1 |
| npc2_avg_control_speed | Average controlling speed (from algorithm) for NPC2 |
| npc2_max_control_speed | Maximum controlling speed (from algorithm) for NPC2 |
| npc1_number_lane_changes | Number of lane changes (from algorithm) for NPC1 |
| npc2_number_lane_changes | Number of lane changes (from algorithm) for NPC2 |
| ego_max_speed | Maximum Speed of the Ego Vehicle (EV)/Autonomous Vehicle (AV) |
| npc1_max_speed | Maximum Speed of NPC1 |
| npc2_max_speed | Maximum Speed of NPC2 |
| npc_avg_dist | Average distance between the EV and **any** NPC |
| max_npc_dist | Maximum distance between the EV and **any** NPC|
| min_npc_dist | Minimum distance between the EV and **any** NPC|
| type_npc_max_dist | Type of the NPC which had the maximum distance: Sedan (1) or SUV (2) |
| type_npc_min_dist | Type of the NPC which had the minimum distance: Sedan (1) or SUV (2) |
| op_npc_max_dist | Operation that the NPC which had maximum distance was performing when it was at the maximum distance: Keep Straight (0), Turn Left (1), Turn Right (2) |
| op_npc_min_dist | Operation that the NPC which had minimum distance was performing when it was at the minimum distance: Keep Straight (0), Turn Left (1), Turn Right (2) |
| ctrl_speed_npc_max_dist | Control speed (from algorithm) that was applied to the NPC with maximum distance when it was at the maximum distance |
| ctrl_speed_npc_min_dist | Control speed (from algorithm) that was applied to the NPC with minimum distance when it was at the minimum distance |
| speed_npc_min_dist | Speed of the NPC with minimum distance when it was closest to the EV|
| speed_npc_max_dist | Speed of the NPC with maximum distance when it was farthest to the EV|
| avg_speed_npcs | Average speed of both NPCs |
| max_npc_speed | Maximum speed of **any** NPC |
| type_npc_max_speed | Type of the NPC which had the maximum speed: Sedan (1) or SUV (2) |
| op_npc_max_speed | Operation perform by the NPC with maximum speed when it was at maximum speed: Keep Straight (0), Turn Left (1), Turn Right (2) |
| ctrl_speed_npc_max_speed | Control speed (from algorithm) that was applied to the NPC with maximum speed when it was at maximum speed |
| dist_av_npc_max_speed | Distance between the EV and the NPC with maximum speed when it was at maximum speed |
