#MenuTitle: CopyCat
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
A tool for comparing two fonts.
"""
import sys, os, traceback
import importlib
from collections import OrderedDict


class BaseTestClass:
	def setFonts(self, font1, font2):
		self.font1 = font1
		self.font2 = font2

	def make_font_to_font_test(self, masterName1, masterName2, returnDetails=True, returnDocString=True, excludeGlyphs=[]):
		
		results = self._parseTestMethods("font__", returnDetails, returnDocString, **dict(font1=self.font1, font2=self.font2))
		master_id_1 = None
		for master in self.font1.masters:
			if master.name == masterName1:
				master_id_1 = master.id
		assert master_id_1 is not None, str(master_id_1)

		master_id_2 = None
		for master in self.font2.masters:
			if master.name == masterName2:
				master_id_2 = master.id
		
		assert master_id_2 is not None, str(master_id_2)
		
		for glyph1 in self.font1.glyphs:
			if glyph1 is None: continue
			glyph2 = self.font2.glyphForUnicode_(glyph1.unicode)
			if glyph2 is None: continue

			if glyph1.name in excludeGlyphs: continue
			if glyph2.name in excludeGlyphs: continue

			layer1 = glyph1.layers[master_id_1]
			if layer1 is None: continue
			layer2 = glyph2.layers[master_id_2]
			if layer2 is None: continue

			results += self._parseTestMethods("layer__", returnDetails, returnDocString, **dict(layer1=layer1, layer2=layer2))
				
				
		return results


	def parseLayerTestMethodsOnSpecificLayers(self, returnDetails, returnDocString, layer1, layer2):
		self._parseTestMethods("layer__", returnDetails, returnDocString, **dict(layer1=layer1, layer2=layer2))
		

	def parseFontTestMethods(self, returnDetails, returnDocString, font1, font2):
		self._parseTestMethods("font__", returnDetails, returnDocString, **dict(font1=font1, font2=font2))

	def _parseTestMethods(self, prefix, returnDetails, returnDocString, **kwargs):
		method_list = [func for func in dir(self) if callable(getattr(self, func))]

		resultList = []

		for method_name in method_list:
			if method_name.startswith(prefix):
				abortTest = False
				method = getattr(self, method_name)
				try:
					resultData = method(kwargs)
				except:
					print(traceback.format_exc())
					print(f"\n\nErr: <{prefix[:-1]}> test <{method_name[len(prefix):]}>: \n\tcouldn't parse test with parameters:")
					for k, v in kwargs.items():
						print(f"\t\t {k} = {v}")
					print("\t\tTest will be skipped.")

					returnData = {}
					abortTest = True

				# I'm not sure about worning implementation, maybe I should introduce some logger object
				try:
					assert isinstance(resultData, dict)
				except:
					print(f"\n\nErr: <{prefix[:-1]}> test <{method_name[len(prefix):]}>:\n\t test doesn't return dict type.\n\t\tTest will be skipped.")
					abortTest = True
				try:
					boolResult = resultData.get("boolResult")
					assert isinstance(boolResult, bool)
				except:	
					print(f"\n\nErr: <{prefix[:-1]}> test <{method_name[len(prefix):]}>:\n\t return dict doesn't contain proper \"boolResult\" key\n\t (key returns {boolResult}).\n\t\tTest will be skipped.")
					abortTest = True

				if abortTest: continue

				testResult = OrderedDict([("method_name", method_name),("boolResult", boolResult)])	

				if returnDetails:
					for k in sorted(list(resultData.keys())):
						if k == "boolResult": continue
						testResult[k] = resultData[k]
				if returnDocString:
					testResult["__doc__"] = method.__doc__

				resultList.append(testResult)
		return resultList

class ResultParser:

	def __init__(self, profileName="default"):
		profileMod = self.getProfileMod(profileName)
		self.testCase = profileMod.TestCase()
	
	def make_font_to_font_test(self, font1, font2, masterName1, masterName2, returnDetails=True, returnDocString=True, excludeGlyphs=[]):
		self.testCase.setFonts(font1, font2)
		results = self.testCase.make_font_to_font_test(masterName1, masterName2, returnDetails, returnDocString, excludeGlyphs)
		self.presentResults(results)

	def presentResults(self, results):
		"""results – list with the results dicts of comparison tests"""
		NotImplemented()

	def getProfileMod(self, profileName):
		profilePath = "./profiles"
		assert os.path.exists(os.path.abspath(os.path.join(profilePath, profileName + ".py"))), \
																	f"profile file for {profileName} doesn't exists"
		absProfilePath = os.path.abspath(profilePath)
		if absProfilePath not in sys.path:
			sys.path.append(absProfilePath)
		return importlib.import_module(profileName)
	
	@staticmethod
	def getNiceMethodName(txt):
		splitMethodName = txt.split("__")
		testType, method_name = splitMethodName[0], "_".join(splitMethodName[1:])
		method_name = method_name.replace("_", " ")
		method_name = method_name.title()
		testType = testType.title()
		return f"{testType}: {method_name}"

class PrintResultParser(ResultParser):
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

class PrintOneLinerResultParser(ResultParser):
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



			

def main():
	# testCase
	resultParser = PrintOneLinerResultParser(profileName="simple")
	fonts = Glyphs.fonts
	masterName = "Medium"
	
	resultParser.make_font_to_font_test(fonts[0], fonts[1], masterName, masterName, returnDetails=True, returnDocString=True, excludeGlyphs=[])


if __name__ == '__main__':
	main()