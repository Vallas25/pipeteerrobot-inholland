from opentrons import protocol_api

# metadata
metadata = {
	"apiLevel": "2.22",
    "protocolName": "pipeteer oefening – OT-2 single-channel",
	"description": """This protocol preforms a modified version of the pipetting excercise preformed in p3.""",
       "author": "Maurits Jansens"
}

# requirements
requirements = {"robotType": "OT-2"}

def run(protocol: protocol_api.ProtocolContext):
	# Labware
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

	Concentrated_color = protocol.define_liquid(
		name = "E110",
		description = "E110 (0.15 g/kg) for serial dilution",
		display_color = "#d15415")

	tubes.load_liquid(
		wells = ["A1"],
		volume = 10000,
		liquid = dOH2)
	tubes.load_liquid(
		wells = ["A2"],
		volume = 1000,
		liquid = Color_liquid)
	tubes.load_liquid(
		wells = ["A3"],
		volume = 150,
		liquid = Concentrated_color)


	demi = tubes["A1"]
	E110 = tubes["A2"]
	E110_serial = tubes["A3"]
	waste = tubes["B1"]

	# program
	for i in range(2):
		row = plate.rows()[i]
		right_pipette.transfer(250, demi, row[0],
			blow_out=True, blowout_location="destination well",
			rate = 0.5,
			touch_tip=True)
		right_pipette.transfer(100, demi, row[1:],
			blow_out=True, blowout_location = "destination well",
			rate = 0.5,
			touch_tip=True)
		right_pipette.transfer(50, E110_serial, row[0],
			blow_out=True, blowout_location = "destination well",
			mix_after=(3,50),
			rate = 0.5,
			touch_tip=True)
		right_pipette.transfer(200, row[:10], row[1:11],
			blow_out=True, blowout_location = "destination well",
			mix_after=(3,50),
			rate = 0.5,
			touch_tip=True)
		right_pipette.transfer(200, row[10], waste)
	
	demi_volume = 70
	E110_volume = 30
	for b in range(2,5):
		row = plate.rows()[b]
		right_pipette.transfer(demi_volume, demi, row[:],
			blow_out=True, blowout_location = "destination well",
			rate = 0.5,
			touch_tip=True)
		right_pipette.transfer(E110_volume, E110, row[:],
			blow_out=True, blowout_location = "destination well",
			mix_after=(3,50),
			rate = 0.5,
			touch_tip = True)
		demi_volume = demi_volume - 15
		E110_volume = E110_volume + 15

