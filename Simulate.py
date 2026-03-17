from opentrons import simulate

protocol_path = "96 wells dilution quick and dirty.py"


with open(protocol_path, "rb") as f:
    run_log, bundle = simulate.simulate(f)

for line in run_log:
    print(line)