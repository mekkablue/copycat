import sys, os
import importlib

class BaseResultParser:

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