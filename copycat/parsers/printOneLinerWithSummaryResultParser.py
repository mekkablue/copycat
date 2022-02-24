from printOneLinerResultParser import PrintOneLinerResultParser

class PrintOneLinerWithSummaryResultParser(PrintOneLinerResultParser):
	def __init__(self, profileName="default"):
		super().__init__(profileName)
	
	def presentResults(self, results):
		super().presentResults(results)
		line = "\n" + "*"*20 + "\n"
		print(f"\n\n{line}SUMMARY{line}\n\n")


		summaryDict = OrderedDict()
		for testResult in results:
			method_name = testResult.get('method_name')
			method_name = self.getNiceMethodName(method_name)
			title = f"# {method_name}"
			doc = testResult.get('__doc__')
			boolResult = testResult.get('boolResult')
			if doc is not None:
				doc = doc.replace("\n","\n#\t")
				title += f"\ndescription:\n\n{doc}\n"
			
			if title not in summaryDict.keys():
				summaryDict[title] = []
			summaryDict[title] += [boolResult]
		for title, boolResults in summaryDict.items():
			print(title)
			print(f">> same-positive count: {boolResults.count(True)}")
			print(f">> same-negative count: {boolResults.count(False)}")
			proc = 0
			if len(boolResults) != 0:
				proc = boolResults.count(True)/len(boolResults)
			# percentage is rounded to 100th floating point
			print(f">> percentage of same-positives: {round(proc*100,2)}%")