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
		"""layer comperison
documentation text"""
		layer1, layer2 = data["layer1"], data["layer2"]

		return {
					"boolResult":True, 
					"glyph 1 name/layer1 name":(layer1.parent.name, layer1.name), 
					"glyph 2 name/layer2 name":(layer2.parent.name, layer2.name), 
				}

	
	def font__glyphs_count(self, data):
		"""font comperison
documentation text"""
		font1, font2 = data["font1"], data["font2"]

		return {
					"boolResult":True, 
					"font1 file name":os.path.basename(font1.filepath),
					"font2 file name":os.path.basename(font2.filepath),
				}
