from baseResultParser import BaseResultParser

class PrintOneLinerResultParser(BaseResultParser):
	def __init__(self, profileName="default"):
		super().__init__(profileName)
	
	def presentResults(self, results):
		for testResult in results:
			method_name = testResult.get('method_name')
			method_name = self.getNiceMethodName(method_name)
			
			name1 = testResult.get("name1")
			name2 = testResult.get("name2")
			boolResult = testResult.get('boolResult')
			
			txt = f"> Test {method_name}"
			if name1 is not None:
				txt += f", name1: {name1}"
			if name2 is not None:
				txt += f", name2: {name2}"
			txt += f", returns: {boolResult}"

			print(txt)
