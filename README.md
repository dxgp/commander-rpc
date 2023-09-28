The reposi
## Assumptions
We have made the following assumptions:
1. Two soldiers can exist at the same position. We feel that this assumption is valid since if we were representing a real battlefied, the grids would capture a large area.
2. The election selects a random soldier.

Additionally, some functions names are different in our code. I'll list the equivalent function names below:

1. status has been replaced with soldier_status
2. was_hit was a function that we felt was highly unnecessary. This is because calling the status function achieves exactly the same effect. This function felt redundant to us. 
3. take_shelter was replaced with notify_soldier (the function further calls a local function in soldoer.py named can_survive).
4. The print_layout function was replaced with print_battlefield inside controller.py.

## How to Start it
First, the project's dependencies must be installed (use the following commands):
```bash
python -m pip install grpcio-tools
python -m pip install protobuf
python -m pip install termtables
```

Next, you must recompile the protobuf using the following command since proto files are highly dependent on the python version (YOU MUST BE INSIDE THE BATTLE FOLDER TO RUN THIS):

```bash
python -m grpc_tools.protoc -I ../protobufs --python_out=. --grpc_python_out=. ../protobufs/messages.proto
```

If you're running on a linux machine (preferable), use the following command (note that these must be run from INSIDE the battle folder):

```
sh run.sh
```

If you're not running on a linux based machine, kindly start up 4 separate terminals and run the following command in EACH of them (note that these commands must be run in this order ONLY):

```bash
python make_soldiers.py
```

```bash
python controller.py
```

```bash
python defense_mechanism.py
```

```bash
python missile_launcher.py
```


## Test Cases Considered
The test cases we considered were as follows:
1. Grid Size = (2,2) -> PASSED
2. Grid Size = (3,3) -> PASSED
3. Grid Size = (5,5) -> PASSED
4. Grid Size = (7,7) -> PASSED
5. Grid Size = (9,9) -> PASSED
6. Grid Size = (11,11) -> PASSED
7. Commander dead: New commander gets elected -> PASSED
8. Commander dead: No more soldiers remaining -> PASSED
9. Missile spanning the whole grid: All soldiers dead -> PASSED

