import random
from opentrons import protocol_api

# metadata
metadata = {
	"apiLevel": "2.22",
    "protocolName": "random concentrations on 96 wells plate",
	"description": """This protocol fills a 96 wells plate with different E110 concentrations.""",
       "author": "Maurits Jansens"
}

# requirements
requirements = {"robotType": "OT-2"}


total_volume = 100
min_volume = 30


def run(protocol: protocol_api.ProtocolContext):
	#labware
	tips = protocol.load_labware("opentrons_96_tiprack_300ul", "10")
	tubes = protocol.load_labware("opentrons_6_tuberack_falcon_50ml_conical", "11")
	plate = protocol.load_labware("nest_96_wellplate_200ul_flat", "9")
	# using OT-2, no trash nessicary
	right_pipette = protocol.load_instrument("p300_single", "right", tip_racks=[tips])

	# liquids
	dOH2 = protocol.define_liquid(
		name = "demi water",
		description = "demi water for dilution",
		display_color= "#4bbae3",)

	Color_liquid = protocol.define_liquid(
		name = "E110",
		description = "E110 (0.010 g/kg) for controls",
		display_color = "#e39c4b")

	tubes.load_liquid(
		wells = ["A1"],
		volume = 10000,
		liquid = dOH2)
	tubes.load_liquid(
		wells = ["A2"],
		volume = 1000,
		liquid = Color_liquid)

	demi = tubes["A1"]
	E110 = tubes["A2"]


	for i in range(8):
		water =	[]
		stock = []
		for b in range(12):
			dilutant = random.randint(min_volume, total_volume - min_volume)
			water.append(dilutant)
			stock.append(total_volume - dilutant)

		rows = plate.rows()[i]
		right_pipette.transfer(water, demi, rows[:])
		right_pipette.transfer(stock, E110, rows[:])
