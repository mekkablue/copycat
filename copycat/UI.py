#MenuTitle: CopyCat UI
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
A tool for comparing two fonts. UI version.
"""

import copycat
import vanilla as vl
import sys, inspect, os, importlib

def getParsersMod():
    parserPath = "./parsers"
    parserDict = {}
    for parserName in os.listdir(parserPath):
        
        if not parserName.endswith("ResultParser.py"): continue
        parserName = parserName[:-3]
        assert os.path.exists(os.path.abspath(os.path.join(parserPath, parserName + ".py"))), \
                                                                    f"parser file for {parserName} doesn't exists"
        absParserPath = os.path.abspath(parserPath)
        if absParserPath not in sys.path:
            sys.path.append(absParserPath)
        parserDict[parserName] = importlib.import_module(parserName)
    return parserDict

def getParserDict():
    parserNameToClass = {}
    for k, v in getParsersMod().items():
        for name, obj in inspect.getmembers(sys.modules[k]):
            if name == "BaseResultParser":continue
            if inspect.isclass(obj):
                if obj.__name__.endswith("ResultParser") and obj.__name__ != "ResultParser":
                    parserNameToClass[obj.__name__.replace("ResultParser","")] = obj
    return parserNameToClass

def getProfileNames():
	profilePath = "./profiles"
	return [p[:-3] for p in os.listdir(profilePath) if p.endswith(".py")]

def characterToGlyphName(c, cmap):
	v = ord(c)
	v = cmap.get(v)
	if isinstance(v, list):
		v = v[0]
	return v


def splitText(text, cmap, fallback=".notdef"):
	# method from defconAppKit
	text = text.replace("//", "/slash ")
	#
	glyphNames = []
	compileStack = None
	for c in text:
		# start a glyph name compile.
		if c == "/":
			# finishing a previous compile.
			if compileStack is not None:
				# only add the compile if something has been added to the stack.
				if compileStack:
					glyphNames.append("".join(compileStack))
			# reset the stack.
			compileStack = []
		# adding to or ending a glyph name compile.
		elif compileStack is not None:
			# space. conclude the glyph name compile.
			if c == " ":
				# only add the compile if something has been added to the stack.
				if compileStack:
					glyphNames.append("".join(compileStack))
				compileStack = None
			# add the character to the stack.
			else:
				compileStack.append(c)
		# adding a character that needs to be converted to a glyph name.
		else:
			glyphName = characterToGlyphName(c, cmap)
			if glyphName is None:
				glyphName = fallback
			glyphNames.append(glyphName)
	# catch remaining compile.
	if compileStack is not None and compileStack:
		glyphNames.append("".join(compileStack))
	return glyphNames


class CopyCatUI:

	def __init__(self):
		self.font1 = None
		self.font2 = None
		x, y, p, btnH, txtH = (10, 10, 10, 20, 17)
		self.fontsDict = {os.path.basename(font.filepath):font for font in Glyphs.fonts}
		self.parserDict = getParserDict()
		profileNames = getProfileNames()


		self.w = vl.Window((200,200,430,240))
		self.w.parserTitle = vl.TextBox((x,y,200,txtH), "Select parser:")
		y += txtH + p
		self.w.parser = vl.PopUpButton((x,y,200,btnH), list(self.parserDict.keys()))

		y += txtH + p
		self.w.profileTitle = vl.TextBox((x,y,200,txtH), "Select profile:")
		y += txtH + p
		self.w.profile = vl.PopUpButton((x,y,200,btnH), profileNames)

		splitHeight = btnH + p + y
		
		y = splitHeight
		self.w.font1Title = vl.TextBox((x,y,-10,txtH), "Select font 1:")
		y += txtH + p
		self.w.font1PopUp = vl.PopUpButton((x,y,200,btnH), list(self.fontsDict.keys()), callback=self.font1Changed)
		self.w.font1PopUp.set(0)
		y += btnH + p
		self.w.master1PopUp = vl.PopUpButton((x,y,200,btnH),[])
		
		y = splitHeight
		x = 220
		self.w.font2Title = vl.TextBox((x,y,-10,txtH), "Select font 2:")
		y += txtH + p
		self.w.font2PopUp = vl.PopUpButton((x,y,200,btnH), list(self.fontsDict.keys()), callback=self.font2Changed)
		self.w.font2PopUp.set(1)
		y += btnH + p
		self.w.master2PopUp = vl.PopUpButton((x,y,200,btnH),[])

		y += btnH + p
		x = 10
		self.w.showDocString = vl.CheckBox((x,y,-p,txtH),"Show method description")
		y += txtH + p
		self.w.showDetails = vl.CheckBox((x,y,-p,txtH),"Show detailed output")
		y += btnH + p

		self.w.excludeGlyphsTitle = vl.TextBox((x,y,-p,txtH),"Exclude glyphs:")
		y += txtH + p

		self.w.excludeGlyphs = vl.EditText((x,y,200,btnH*5),"I l /bar /brokenbar /space")
		y += btnH*5 + p

		self.w.applyButton = vl.Button((-x-100,y,100,txtH),"Parse", callback=self.apply)
		y += btnH + p
		h = y
		x,y,w,_ = self.w.getPosSize()
		self.w.setPosSize((x,y,w,h))
		self.w.open()
		self.font1Changed(self.w.font1PopUp)
		self.font2Changed(self.w.font2PopUp)

	def apply(self, sender):
		Glyphs.clearLog()
		Glyphs.showMacroWindow()
		returnDetails = True if self.w.showDetails.get() == 1 else False
		returnDocString = True if self.w.showDocString.get() == 1 else False
		parserName = self.w.parser.getItem()
		ResultParser = self.parserDict[parserName]
		profileName = self.w.profile.getItem()
		resultParser = ResultParser(profileName=profileName)
		print()
		print("*"*20)
		print("*"*20)
		print(f"\tParser: {parserName}ResultParser, \n\tprofile: {profileName}, \n\t\tfont1: {self.font1},\n\t\tfont2: {self.font2}")
		print("*"*20)
		print("*"*20)
		print()
		masterName1 = self.w.master1PopUp.getItem()
		masterName2 = self.w.master2PopUp.getItem()
		
		cmap = {int("0x"+glyph.unicode, 0):glyph.name for glyph in self.font1.glyphs if glyph.unicode is not None}
		excludeGlyphs = splitText(self.w.excludeGlyphs.get(), cmap)
		resultParser.make_font_to_font_test(self.font1, self.font2, masterName1, masterName2, returnDetails=returnDetails, returnDocString=returnDocString, excludeGlyphs=excludeGlyphs)

	def font1Changed(self, sender):
		self.fontChanged(sender, 1)

	def font2Changed(self, sender):
		self.fontChanged(sender, 2)

	def fontChanged(self, sender, fontNo):
		fontBaseName = self.w.font1PopUp.getItem()
		masterPopUp = self.w.master1PopUp
		if fontNo == 2:
			fontBaseName = self.w.font2PopUp.getItem()
			masterPopUp = self.w.master2PopUp

		fontObj = self.fontsDict[fontBaseName]
		masterNames = [master.name for master in fontObj.masters]
		masterPopUp.setItems(masterNames)

		if fontNo == 1:
			self.font1 = fontObj
		if fontNo == 2:
			self.font2 = fontObj

def main():
	CopyCatUI()

if __name__ == '__main__':
	main()