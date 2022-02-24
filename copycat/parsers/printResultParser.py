from baseResultParser import BaseResultParser

class PrintResultParser(BaseResultParser):
	def __init__(self, profileName="default"):
		super().__init__(profileName)
	
	def presentResults(self, results):
		for testResult in results:
			print("#"*20)
			print("#"*20)
			print("#"*20)
			method_name = testResult.get('method_name')
			method_name = self.getNiceMethodName(method_name)
			print(f"Test \n\t{method_name}")
			
			doc = testResult.get('__doc__')
			if doc is not None:
				doc = doc.replace("\n","\n#\t")
				print(f"description:\n\n{doc}")
			
			print("#"*20)
			print()
			boolResult = testResult.get('boolResult')
			print(f"\t - is there a copycat?: {boolResult}\n")

			for key, value in testResult.items():
				if key in ["method_name", '__doc__', 'boolResult']: continue
				print(f"\t - {key}: {value}")
			print()