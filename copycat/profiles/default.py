#############################
# Please, don't code below:
#############################
import platform, os
def importFileAsAModule(path):
	import importlib.util
	spec = importlib.util.spec_from_file_location(os.path.splitext(os.path.basename(path))[0], path)
	foo = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(foo)
	return foo
path = os.path.abspath(os.path.abspath(os.path.join(__file__, os.pardir,os.pardir,"copycat.py")))
copycat = importFileAsAModule(path)

#############################
#############################
#############################

# ██    ██  ██████  ██    ██ ██████      ████████ ███████ ███████ ████████         
#  ██  ██  ██    ██ ██    ██ ██   ██        ██    ██      ██         ██            
#   ████   ██    ██ ██    ██ ██████         ██    █████   ███████    ██            
#    ██    ██    ██ ██    ██ ██   ██        ██    ██           ██    ██            
#    ██     ██████   ██████  ██   ██        ██    ███████ ███████    ██            
#
#
#  ██████   ██████  ███████ ███████     ██████  ███████ ██       ██████  ██     ██ 
# ██       ██    ██ ██      ██          ██   ██ ██      ██      ██    ██ ██     ██ 
# ██   ███ ██    ██ █████   ███████     ██████  █████   ██      ██    ██ ██  █  ██ 
# ██    ██ ██    ██ ██           ██     ██   ██ ██      ██      ██    ██ ██ ███ ██ 
#  ██████   ██████  ███████ ███████     ██████  ███████ ███████  ██████   ███ ███  
                                                                                 
                                                                                 
#############################
# Define your test cases as
# the methods of this class:
#############################


class TestCase(copycat.BaseTestClass):

	def layer__point_count(self, data):
		"""
This test compares point count 
of two layers, result is True 
when those layer have the same
number"""
		def _get_layer_point_count(layer):
			count = 0
			for path in layer.paths:
				for point in path.nodes:
					count += 1
			return count

		layer1, layer2 = data["layer1"], data["layer2"]
		layer_point_count_layer1 = _get_layer_point_count(layer1)
		layer_point_count_layer2 = _get_layer_point_count(layer2)
		
		boolResult = layer_point_count_layer1 == layer_point_count_layer2
		
		result_dictionary = {
					"boolResult":boolResult, 
					"name1":layer1.parent.name, 
					"name2":layer2.parent.name, 
					"difference_in_point_count":abs(layer_point_count_layer1-layer_point_count_layer2)	
				}
		
		return result_dictionary

	def layer__normalized_point_comparison(self, data):
		"""
This test compares point positions 
of normalized two layers with the threshold 
of error 2 units per em.

Result is True if point count is the same and 
all the layers' points have the same position 
within threshold"""
		def _get_layer_point_positions(layer):
			# normalization:
			shift_x, shift_y = (layer.bounds.origin.x * -1, layer.bounds.origin.y * -1)
			positions = []
			for path in layer.paths:
				for point in path.nodes:
					point_position = (point.x + shift_x, point.y + shift_y)
					positions.append(point_position)
			return positions

		layer1, layer2 = data["layer1"], data["layer2"]
		layer1_point_positions = _get_layer_point_positions(layer1)
		layer2_point_positions = _get_layer_point_positions(layer2)
		difference_in_point_count = True if len(layer1_point_positions) != len(layer2_point_positions) else False
		
		base_points = layer1_point_positions
		reference_points = layer2_point_positions
		
		if len(layer2_point_positions) > len(layer1_point_positions):	
			base_points = layer2_point_positions
			reference_points = layer1_point_positions
		

		matched = []
		for point in base_points:
			thisPointMatched = False
			x, y = point
			for ref_point in reference_points:
				rx, ry = ref_point
				if rx-2 < x < rx+2 and ry-2 < y < ry+2:
					matched.append(True)
					thisPointMatched = True
					break
			if not thisPointMatched:
				matched.append(False)

		boolResult = all(matched)
		
		result_dictionary = {
					"boolResult":boolResult, 
					"name1":layer1.parent.name, 
					"name2":layer2.parent.name, 
					"difference in point count":difference_in_point_count	
				}
		if difference_in_point_count:
			result_dictionary["count difference"] = len(base_points) - len(reference_points)
		if len(matched) != 0:
			result_dictionary["similarly positioned points (%)"] = matched.count(True)/len(matched)*100
		else:
			result_dictionary["similarly positioned points (%)"] = 0
		return result_dictionary
	
	def font__glyphs_count(self, data):
		font1, font2 = data["font1"], data["font2"]

		font1_glyphs_count = len([g for g in font1.glyphs if g is not None])
		font2_glyphs_count = len([g for g in font2.glyphs if g is not None])

		return {"boolResult":font1_glyphs_count==font2_glyphs_count, 
				"name1":os.path.basename(font1.filepath),
				"name2":os.path.basename(font2.filepath),
				"font1 glyphs count":font1_glyphs_count,
				"font2 glyphs count":font2_glyphs_count,
				"glyphs count difference":abs(font1_glyphs_count-font2_glyphs_count),
		}
