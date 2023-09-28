import subprocess

process1 = subprocess.Popen(["python", "create_soldiers.py"]) # Create and launch process pop.py using python interpreter
process2 = subprocess.Popen(["python", "controller.py"])
process3 = subprocess.Popen(["python", "defense_mechanism.py"])
process4 = subprocess.Popen(["python", "missile_launcher.py"])

process1.wait() # Wait for process1 to finish (basically wait for script to finish)
process2.wait()
process3.wait()
process4.wait()