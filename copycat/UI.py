#MenuTitle: CopyCat UI
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
A tool for comparing two fonts. UI version.
"""
import sys, os, inspect
import copycat
import vanilla as vl

def getParserDict():
	parserNameToClass = {}
	for name, obj in inspect.getmembers(sys.modules["copycat"]):
		if inspect.isclass(obj):
			if obj.__name__.endswith("ResultParser") and obj.__name__ != "ResultParser":
				parserNameToClass[obj.__name__.replace("ResultParser","")] = obj
	return parserNameToClass

def getProfileNames():
	profilePath = "./profiles"
	return [p[:-3] for p in os.listdir(profilePath) if p.endswith(".py")]




class CopyCatUI:

	def __init__(self):
		self.font1 = None
		self.font2 = None
		x, y, p, btnH, txtH = (10, 10, 10, 20, 17)
		self.fontsDict = {os.path.basename(font.filepath):font for font in Glyphs.fonts}
		self.parserDict = getParserDict()
		profileNames = getProfileNames()


		self.w = vl.Window((200,200,430,240))
		self.w.parserTitle = vl.TextBox((x,y,200,txtH), "select parser:")
		y += txtH + p
		self.w.parser = vl.PopUpButton((x,y,200,btnH), list(self.parserDict.keys()))

		y += txtH + p
		self.w.profileTitle = vl.TextBox((x,y,200,txtH), "select profile:")
		y += txtH + p
		self.w.profile = vl.PopUpButton((x,y,200,btnH), profileNames)

		splitHeight = btnH + p + y
		
		y = splitHeight
		self.w.font1Title = vl.TextBox((x,y,-10,txtH), "select font 1:")
		y += txtH + p
		self.w.font1PopUp = vl.PopUpButton((x,y,200,btnH), list(self.fontsDict.keys()), callback=self.fontChanged)
		self.w.font1PopUp.set(0)
		self.w.font1PopUp.number = 1
		y += btnH + p
		self.w.master1PopUp = vl.PopUpButton((x,y,200,btnH),[])
		
		y = splitHeight
		x = 220
		self.w.font2Title = vl.TextBox((x,y,-10,txtH), "select font 2:")
		y += txtH + p
		self.w.font2PopUp = vl.PopUpButton((x,y,200,btnH), list(self.fontsDict.keys()), callback=self.fontChanged)
		self.w.font2PopUp.set(1)
		self.w.font2PopUp.number = 2
		y += btnH + p
		self.w.master2PopUp = vl.PopUpButton((x,y,200,btnH),[])

		y += btnH + p
		x = 10
		self.w.applyButton = vl.Button((x,y,100,btnH),"parse", callback=self.apply)

		self.w.open()
		self.fontChanged(self.w.font1PopUp)
		self.fontChanged(self.w.font2PopUp)

	def apply(self, sender):
		Glyphs.clearLog()
		Glyphs.showMacroWindow()
		ResultParser = self.parserDict[self.w.parser.getItem()]
		profileName = self.w.profile.getItem()
		resultParser = ResultParser(profileName=profileName)

		masterName1 = self.w.master1PopUp.getItem()
		masterName2 = self.w.master2PopUp.getItem()
		
		resultParser.make_font_to_font_test(self.font1, self.font2, masterName1, masterName2, collectDescriptions=True, collectDocumentation=True)

	def fontChanged(self, sender):
		fontBaseName = self.w.font1PopUp.getItem()
		fontObj = self.fontsDict[fontBaseName]
		masterNames = [master.name for master in fontObj.masters]
		if sender.number == 1:
			self.font1 = fontObj
			masterPopUp = self.w.master1PopUp
		if sender.number == 2:
			self.font2 = fontObj
			masterPopUp = self.w.master2PopUp
		masterPopUp.setItems(masterNames)
def main():
	CopyCatUI()

if __name__ == '__main__':
	main()