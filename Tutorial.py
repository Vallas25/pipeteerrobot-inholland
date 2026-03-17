from opentrons import protocol_api

# metadata
metadata = {
	"apiLevel": "2.16",
    "protocolName": "Serial Dilution Tutorial – OT-2 single-channel, blow_out",
	"description": """This protocol is the outcome of following the
        Python Protocol API Tutorial located at
        https://docs.opentrons.com/v2/tutorial.html. It takes a solution
        and progressively dilutes it by transferring it stepwise across a plate. script contains blow_out arg""",
       "author": "Maurits Jansens"
}

# requirements
requirements = {"robotType": "OT-2"}

def run(protocol: protocol_api.ProtocolContext):
	# Labware
	tips = protocol.load_labware("opentrons_96_tiprack_300ul", "A1")
	reservoir = protocol.load_labware("opentrons_6_tuberack_falcon_50ml_conical", "A2")
	plate = protocol.load_labware("nest_96_wellplate_200ul_flat", "B3")
	# using OT-2, no trash nessicary
	right_pipette = protocol.load_instrument("p300_single", "right", tip_racks=[tips])

	# program
	right_pipette.transfer(100, reservoir["A1"], plate.wells(),
		blow_out=True, blowout_location = "destination well")

	for i in range(8):
		row = plate.rows()[i]
		right_pipette.transfer(100, reservoir["A2"], row[0],
			blow_out = True, blowout_location = "destination well", 
			mix_after=(3, 50), )
		right_pipette.transfer(100, row[:11], row[1:], 
			blow_out = True, blowout_location = "destination well",
			 mix_after=(3,50))

