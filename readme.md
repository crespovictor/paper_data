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