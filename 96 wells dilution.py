from opentrons import protocol_api
import csv
import io

# csv data 
csv_data = """0.32,0.4379,0.4055,0.5493,0.5978,0.1661,0.2031,0.086,0.3254,0.6225,0.6054,0.3904,
0.4457,0.3845,0.5748,0.5535,0.4692,0.1634,0.1189,0.3602,0.347,0.073,0.144,0.4726,
0.6143,0.5497,0.1118,0.6458,0.0481,0.5471,0.0465,0.454,0.0788,0.0602,0.652,0.178,
0.4633,0.0579,0.3311,0.0589,0.498,0.1422,0.6548,0.6127,0.0453,0.3388,0.6228,0.454,
0.5033,0.2232,0.1456,0.0692,0.3819,0.5778,0.3329,0.5365,0.5725,0.4228,0.105,0.6442,
0.6505,0.4801,0.6142,0.0442,0.1527,0.1867,0.3031,0.6037,0.1972,0.0487,0.068,0.5162,
0.0984,0.4441,0.6673,0.0636,0.5516,0.6054,0.2104,0.3815,0.3706,0.5107,0.1521,0.6354,
0.2843,0.4394,0.6361,0.0922,0.1689,0.4857,0.304,0.2038,0.2918,0.0526,0.4489,0.0504,"""

# metadata
metadata = {
	"apiLevel": "2.22",
    "protocolName": "96 wells dilution",
	"description": """This protocol dilutes samples to a target OD of 0.5.""",
       "author": "Maurits Jansens"
}

# settings for targed OD/volume 
max_OD = 1
target_OD = 0.2
volume = 100

# requirements
requirements = {"robotType": "OT-2"}

# run protocol (carried out by robot)
def run(protocol: protocol_api.ProtocolContext):
	# Labware
	tips1 = protocol.load_labware("opentrons_96_tiprack_300ul", "10")
	tips2 = protocol.load_labware("opentrons_96_tiprack_300ul", "7")
	tubes = protocol.load_labware("opentrons_6_tuberack_falcon_50ml_conical", "11")
	plate = protocol.load_labware("nest_96_wellplate_200ul_flat", "9")
	sample_plate = protocol.load_labware("nest_96_wellplate_200ul_flat", "8")
	# using OT-2, no trash slot nessicary
	right_pipette = protocol.load_instrument("p300_single", "right", tip_racks=[tips1,tips2])

	# Liquids
	dOH2 = protocol.define_liquid(
		name = "demi water",
		description = "demi water for dilution",
		display_color = "#4bbae3",)

	stock = protocol.define_liquid(
		name = "stock",
		description = "stock in sample plate",
		display_color = "#b37700")

	tubes.load_liquid(
		wells = ["A1"],
		volume = 10000,
		liquid = dOH2)

	sample_plate.load_liquid(
		wells = sample_plate.wells(),
		volume = 100,
		liquid = stock)

	demi = tubes["A1"]

	#csv logic
	f = io.StringIO(csv_data)
	csv_reader = csv.reader(f)

	for i, row in enumerate(csv_reader):

		sample_volumes = []
		dilutant_volumes = []

		for col in range(12):

			raw_value = row[col]

			try:
				value = float(raw_value)

				if target_OD <= value <= max_OD:
					sample = round(target_OD * volume / value)
					sample_volumes.append(sample)
					dilutant_volumes.append(volume - sample)

				else:
					sample_volumes.append(0)
					dilutant_volumes.append(0)

			except ValueError:
				sample_volumes.append(0)
				dilutant_volumes.append(0)

		dest_row = plate.rows()[i]
		source_row = sample_plate.rows()[i]

		# Pipetting logic

		right_pipette.transfer(dilutant_volumes, demi, dest_row,
            blow_out=True, blowout_location="destination well",
            touch_tip = True)
            
		right_pipette.transfer(sample_volumes, source_row, dest_row,
            blow_out=True, blowout_location="destination well",
            mix_after=(3, 50),
            new_tip="always",
            touch_tip = True)
