
'''
Created on 15-Dec-2016

@author: vijay
'''

import wx
import wx.stc as stc
import keyword
# from src.view.images import images
import os
# import string

# from src.SqlBeautifier.sqlbeautifier import SqlBeautifierCommand
# from src.view import SqliteKeywords
from src.view.findAndReplace.FindAndReplacePanel import CreatingFindAndReplaceFrame
from src.view.findAndReplace.GoToLinePanel import CreatingGoToLinePanel
from src.sqlite_executer.ConnectExecuteSqlite import SQLExecuter, \
    ManageSqliteDatabase
from datetime import date, datetime
import time
import logging
# from sys import exc_info
from sqlite3 import OperationalError
import sqlparse
from src.view import SqliteKeywords

logger = logging.getLogger('extensive')
# from src.format_sql.shortcuts import Beautify
# from src.format_sql.shortcuts import format_sql

#----------------------------------------------------------------------
keylist = {
    'DOWN'  :stc.STC_KEY_DOWN,
    'UP'    :stc.STC_KEY_UP,
    'LEFT'  :stc.STC_KEY_LEFT,
    'RIGHT' :stc.STC_KEY_RIGHT,
    'HOME'  :stc.STC_KEY_HOME,
    'END'   :stc.STC_KEY_END,
    
    'PGUP'  :stc.STC_KEY_PRIOR,
    'PGDN'  :stc.STC_KEY_NEXT,
    'DEL'   :stc.STC_KEY_DELETE,
    'INS'   :stc.STC_KEY_INSERT,
    'ESC'   :stc.STC_KEY_ESCAPE,
    'BACK'  :stc.STC_KEY_BACK,
    'TAB'   :stc.STC_KEY_TAB,
    'ENTER' :stc.STC_KEY_RETURN,
    'PLUS'  :stc.STC_KEY_ADD,
    '-'     :stc.STC_KEY_SUBTRACT,
    '/'     :stc.STC_KEY_DIVIDE,
}
demoText = """select * from book;
"""

#----------------------------------------------------------------------
print(wx.Platform) 

if wx.Platform == '__WXMSW__':
    faces = { 'times': 'Consolas',
              'mono' : 'Consolas',
              'helv' : 'Consolas',
              'other': 'Comic Sans MS',
              'size' : 10,
              'size2': 8,
             }
#     faces = { 'times': 'Times New Roman',
#               'mono' : 'Courier New',
#               'helv' : 'Arial',
#               'other': 'Comic Sans MS',
#               'size' : 10,
#               'size2': 8,
#              }
elif wx.Platform == '__WXMAC__':
    faces = { 'times': 'Times New Roman',
              'mono' : 'Monaco',
              'helv' : 'Arial',
              'other': 'Comic Sans MS',
              'size' : 12,
              'size2': 10,
             }
elif wx.Platform == '__WXGTK__':
    faces = { 'times': 'Times New Roman',
              'mono' : 'Courier New',
              'helv' : 'Arial',
              'other': 'Comic Sans MS',
              'size' : 10,
              'size2': 8,
             }    
else:
    faces = { 'times': 'Times',
              'mono' : 'Courier',
              'helv' : 'Helvetica',
              'other': 'new century schoolbook',
              'size' : 12,
              'size2': 10,
             }

#----------------------------------------------------------------------


class SqlStyleTextCtrl(stc.StyledTextCtrl):
    fold_symbols = 2

    def __init__(self, parent, ID,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=0):
        stc.StyledTextCtrl.__init__(self, parent, ID, pos, size, style)    
        self.popmenu = None
        self.frame = None
        self.adviceList = list()
        self.SetHighlightGuide(1)
#         self.CmdKeyAssign(ord('B'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
#         self.CmdKeyAssign(ord('N'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)
        # init key short cut
#         self.initKeyShortCut()
        self.SetLexer(stc.STC_LEX_SQL)
#         self.SetKeyWords(0, " ".join(keyword.kwlist))
        lowerKeyword = [element.lower() for element in SqliteKeywords.keyword]
        upperKeyword = [element.upper() for element in SqliteKeywords.keyword]
        keywords = list()
        keywords.extend(lowerKeyword)
        keywords.extend(upperKeyword)
        logger.debug("keywords: %s", keywords)
        self.SetKeyWords(0, " ".join(keywords))
        self.SetProperty("fold", "1")
        self.SetProperty("tab.timmy.whinge.level", "1")
        self.SetMargins(0, 0)
        # editor style
        self.SetMargins(2, 2)  # set left and right outer margins to 0 width
        self.SetMarginMask(1, 0)  # can't place any marker in margin 1
        self.SetMarginWidth(0, 0)  # used as symbol
        self.SetMarginWidth(2, 0)  # used as folder

        self.SetViewWhiteSpace(False)
        self.SetBufferedDraw(False)
        self.SetViewEOL(False)
        self.SetEOLMode(stc.STC_EOL_CRLF)
#         self.SetUseAntiAliasing(True)
        
        self.selection_column_mode = False
        
#         self.SetEdgeMode(stc.STC_EDGE_BACKGROUND)
#         self.SetEdgeColumn(78)
        # set backspace to unindent
        self.SetBackSpaceUnIndents(True)
        # set scroll bar range
        self.SetEndAtLastLine(False)

        # Setup a margin to hold fold markers
        # self.SetFoldFlags(16)  ###  WHAT IS THIS VALUE?  WHAT ARE THE OTHER FLAGS?  DOES IT MATTER?
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)        
        # Make some styles,  The lexer defines what each style is used for, we
        # just have to define what each style looks like.  This set is adapted from
        # Scintilla sample property files.
        # set style
#        font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font = wx.Font(8, wx.TELETYPE, wx.NORMAL, wx.NORMAL, True)
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%s,size:10" % font.GetFaceName())
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER, "back:#AAFFAA,face:%s,size:10" % font.GetFaceName())
        # Global default styles for all languages
#         self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % faces)
        self.StyleClearAll()  # Reset all to be like the default

        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER, "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT, "fore:#FFFFFF,back:#0000FF,bold")
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD, "fore:#000000,back:#FF0000,bold")   
        
        if self.fold_symbols == 0:
            # Arrow pointing right for contracted folders, arrow pointing down for expanded
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_ARROWDOWN, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_ARROW, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_EMPTY, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_EMPTY, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY, "white", "black")
            
        elif self.fold_symbols == 1:
            # Plus for contracted folders, minus for expanded
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_MINUS, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_PLUS, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY, "white", "black")

        elif self.fold_symbols == 2:
            # Like a flattened tree control using circular headers and curved joins
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_CIRCLEMINUS, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_CIRCLEPLUS, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_VLINE, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_LCORNERCURVE, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_CIRCLEPLUSCONNECTED, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_CIRCLEMINUSCONNECTED, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNERCURVE, "white", "#404040")

        elif self.fold_symbols == 3:
            # Like a flattened tree control using square headers
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_BOXMINUS, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_BOXPLUS, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_VLINE, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_LCORNER, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_BOXPLUSCONNECTED, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER, "white", "#808080")
             
        self.sqlStyle()
        self.registerAllImages()
        
#         stc.EVT_STC_MARGINCLICK(self, self.GetId(), self.OnMarginClick)
#         wx.EVT_RIGHT_DOWN(self, self.onRightMouseDown)
#         wx.EVT_LEFT_UP(self, self.onLeftMouseUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.onRightMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.onLeftMouseUp)
        self.Bind(stc.EVT_STC_UPDATEUI, self.OnUpdateUI)
        self.Bind(stc.EVT_STC_MARGINCLICK, self.OnMarginClick)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)

    def registerAllImages(self):
        path = os.path.abspath(__file__)
        tail = None
#         head, tail = os.path.split(path)
#         logger.debug(('createAuiManager',head, tail )
        try:
            while tail != 'src':
                path = os.path.abspath(os.path.join(path, '..',))
                head, tail = os.path.split(path)
        except Exception as e:
            logger.error(e, exc_info=True)
        logger.debug('registerAllImages: %s', path)
        path = os.path.abspath(os.path.join(path, "images"))
        # register some images for use in the AutoComplete box.
#         if "worksheet" == os.path.split(os.getcwd())[-1:][0]:
#             textImage = wx.Bitmap(os.path.join("..", "..", "images", "new.png"))
#         elif "view" == os.path.split(os.getcwd())[-1:][0]:
        textImage = wx.Bitmap(os.path.join(path, "new.png"))
        self.RegisterImage(1, textImage)
        self.RegisterImage(2,
            wx.ArtProvider.GetBitmap(wx.ART_NEW, size=(16, 16)))
        self.RegisterImage(3,
            wx.ArtProvider.GetBitmap(wx.ART_COPY, size=(16, 16)))
        
    def formatCode(self, inputText=None):
        logger.debug("formatCode: %s", inputText)
#         new = inputText + "1"
        formatted_sql = sqlparse.format(inputText, reindent=True, keyword_case='upper')
#         new=Beautify().format_sql(inputText)
        s = self.GetText()
#         s.replace
#         logger.debug("formatCode: %s \n   %s  \n  %s ", s, inputText, new)
        new_str = s.replace(inputText, formatted_sql, 1)
        self.SetText(new_str)
 
    def Undo(self, *args, **kwargs):
        return stc.StyledTextCtrl.Undo(self, *args, **kwargs)
    
    def Redo(self, *args, **kwargs):
        return stc.StyledTextCtrl.Redo(self, *args, **kwargs)

    def Paste(self):
        success = False
        do = wx.TextDataObject()
        if wx.TheClipboard.Open():
            success = wx.TheClipboard.GetData(do)
            wx.TheClipboard.Close()

        if success:
#             if not self.execplugin('on_paste', self, do.GetText()):
            stc.StyledTextCtrl.Paste(self) 
                
    def copyClipboard(self, text=None):
        """"""
        logger.debug("copyClipboard: %s", text)
        if self.SelectionIsRectangle():
            self.selection_column_mode = True
        else:
            self.selection_column_mode = False
        stc.StyledTextCtrl.Copy(self)
#         self.dataObj = wx.TextDataObject()
#         self.dataObj.SetText(text)
#         
#         try:
#             with wx.Clipboard.Get() as clipboard:
#                 clipboard.SetData(self.dataObj)
#         except TypeError:
#             wx.MessageBox("Unable to open the clipboard", "Error")            
    
    def OnKeyUp(self, event):
        if self.CallTipActive():
            self.CallTipCancel()
        key = event.GetKeyCode()
        logger.debug('OnKeyUp: GetKeyCode:%s ControlDown:%s ShiftDown:%s', event.GetKeyCode(), event.ControlDown(), event.ShiftDown())
        
        if event.ControlDown() and  key == 47:
            logger.debug('ctrl+/ %s', self.GetSelectedText())   
            if self.GetSelectedText():
                logger.debug(self.GetSelectedText())
                logger.debug(self.GetSelectionNStart())
                logger.debug(self.GetSelectionNEnd())
            else:
                logger.debug(self.CurLine[0])
                completeText=self.GetText()
                line = self.GetCurrentLine()
                lineText, column = self.GetCurLine()
                completeTextArray=completeText.split('\n')
                lineText=lineText.rstrip()
                replaceText=lineText
                if lineText.startswith('-- '):
                    replaceText=lineText.replace('-- ','')
                else:
                    replaceText='-- '+lineText
                completeTextArray[line]=replaceText
                self.SetText('\n'.join(completeTextArray))
                print(completeText)
#                 self.MoveCaretInsideView()
#                 self.SetText()
        
        elif event.ControlDown() and  key == 67:
            logger.debug('ctrl+C %s', self.GetSelectedText())
            self.copyClipboard(text=self.GetSelectedText())    
            if key == 86:
                self.Paste()

        elif event.ControlDown() and  key == 76:
            logger.debug('ctrl+L %s', self.GetSelectedText())
            dlg = CreatingGoToLinePanel(self, -1, "Go to Line", size=(350, 200),
                 style=wx.DEFAULT_DIALOG_STYLE,
                 )
            dlg.CenterOnScreen()
            
            # this does not return until the dialog is closed.
            val = dlg.ShowModal()
            
            if val == wx.ID_OK:
                lineNumber = dlg.lineNumberText.GetValue()
                logger.debug("You pressed OK %s", lineNumber)
                if lineNumber != '':
                    self.GotoLine(int(lineNumber))
                
            else:
                logger.debug("You pressed Cancel\n")
            
            dlg.Destroy()
#             app.MainLoop()
        elif event.ControlDown() and  key == 86:
            logger.debug('ctrl+V : paste')
            self.Paste()
        elif event.ControlDown() and  key == 90:
            logger.debug('Ctrl+Z: Undo')
            self.Undo()
            event.Skip()
        elif event.ControlDown() and  key == 88:
            logger.debug('ctrl+X: for cut')
            self.Cut()
            event.Skip()
        elif event.ControlDown() and  key == 89:
            logger.debug('Ctrl+Y: Redo')
            self.Redo()
            event.Skip()
#         elif event.ShiftDown() and key == 307:
#             logger.debug('Shift+down')
        elif key in (314, 315, 316, 317):
            line = self.GetCurrentLine()
            lineText, column = self.GetCurLine()
            logger.debug('left right up down. lineText: %s line: %s column:%s', lineText, line, column)
#             self.statusbar.SetStatusText(self.getCurrentCursorPosition(), 0)
            if hasattr(self.GetTopLevelParent(), 'statusbar'):
                self.GetTopLevelParent().statusbar.SetStatusText("Line " + str(line) + " , Column " + str(column), 0)
    
#     def duplicateLine(self, lineText, lineNo):
#         print('duplicateLine', lineText)       
#         s = self.GetText()
# #         lineText=lineText.strip('\n')
#         lines=s.split('\n')
#         self.AddText(lineText)
# #         lines.insert(lineNo, lineText)
# #         newString="\n".join(lines)
# #         self.SetText(newString)
# #         for idx, line in enumerate(lines):
# #             print(idx," : ",line)
# #             newString=
         
    def OnKeyPressed(self, event):
        if self.CallTipActive():
            self.CallTipCancel()
        key = event.GetKeyCode()
#         print('OnKeyPressed------->', event.GetKeyCode(), event.ControlDown(), event.ShiftDown())
        if event.ControlDown() and event.AltDown() and key == 317:
            logger.debug('ctrl+Alt+Down: duplicate line of code')
            selectedText = self.GetSelectedText()
            logger.debug(selectedText)
            lineNo = self.GetCurrentLine()
            lineText, column = self.GetCurLine()
            if selectedText != None:
                self.AddText(lineText)
            
        elif event.ControlDown() and event.ShiftDown() and key == 70:
            logger.debug('ctrl+Shtft+F: format code')
            selectedText = self.GetSelectedText()
            self.formatCode(inputText=selectedText)
            
            event.Skip()
        elif event.ControlDown() and  key == 70:
            logger.debug('ctrl+F: for find and relpace')
            if self.frame == None:
                self.frame = CreatingFindAndReplaceFrame(self, 'Find / Replace')
#             self.copyClipboard(text=self.GetSelectedText())
            event.Skip()            
        elif not event.ControlDown() and event.AltDown() and key == 317:
            logger.debug('Alt+Down: MoveSelectedLinesDown')
            self.MoveSelectedLinesDown()
            event.Skip()
        elif event.AltDown() and key == 315:
            logger.debug('Alt+up: MoveSelectedLinesUp')
            self.MoveSelectedLinesUp()
            event.Skip()

        elif key == wx.WXK_RETURN and event.ControlDown():
            logger.debug('ctrl+Enter: execute sql')
            self.executeSQL()
            
            # Refresh tree if it required
            
        elif key == wx.WXK_SPACE and event.ControlDown():
            pos = self.GetCurrentPos()
            logger.debug(self.GetSelectedText())
#             self.AddText('viajy')
#             self.AddSelection('viajy')
                
            # Tips
            if event.ShiftDown():
                self.CallTipSetBackground("yellow")
                self.CallTipShow(pos, 'lots of of text: blah, blah, blah\n\n'
                                 'show some suff, maybe parameters..\n\n'
                                 'fubar(param1, param2)')
            
            # Code completion
            
            else:
                # lst = []
                # for x in range(50000):
                #    lst.append('%05d' % x)
                # st = " ".join(lst)
                # logger.debug len(st)
                # self.AutoCompShow(0, st)

#                 kw = keyword.kwlist[:]
#                 self.AutoCompSetSeparator('|')
                # kw.append("this_is_a_much_much_much_much_much_much_much_longer_value")

#                 kw.sort()  # Python sorts are case sensitive
                self.AutoCompSetIgnoreCase(True)  # so this needs to match
                self.AutoCompSetSeparator(124)
                # Images are specified with a appended "?type"
#                 for i in range(len(kw)):
#                     if kw[i] in keyword.kwlist:
#                         kw[i] = kw[i] + "?1"

                self.AutoCompShow(0, "|".join(self.getAdvice()))
        else:
            event.Skip()
            
    def getAdvice(self):
        del self.adviceList[:]
        self.adviceList.append("select * from ")
        self.adviceList.append("create table Table_1 ( id number); ")
        self.adviceList.append("desc ")
        return self.adviceList

    def OnUpdateUI(self, evt):
        # check for matching braces
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = self.GetCurrentPos()

        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
            styleBefore = self.GetStyleAt(caretPos - 1)

        # check before
        if charBefore and chr(charBefore) in "[]{}()" and styleBefore == stc.STC_P_OPERATOR:
            braceAtCaret = caretPos - 1

        # check after
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            styleAfter = self.GetStyleAt(caretPos)

            if charAfter and chr(charAfter) in "[]{}()" and styleAfter == stc.STC_P_OPERATOR:
                braceAtCaret = caretPos

        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)

        if braceAtCaret != -1  and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)

            # pt = self.PointFromPosition(braceOpposite)
            # self.Refresh(True, wxRect(pt.x, pt.y, 5,5))
            # logger.debug pt
            # self.Refresh(False)
    def OnMarginClick(self, event):
        logger.debug('on_margin_click self:%s event:%s', self, event)
        # fold and unfold as needed
        if event.GetMargin() == 2:
            if event.GetShift() and event.GetControl():
                self.FoldAll()
            else:
                lineClicked = self.LineFromPosition(event.GetPosition())

                if self.GetFoldLevel(lineClicked) & stc.STC_FOLDLEVELHEADERFLAG:
                    if event.GetShift():
                        self.SetFoldExpanded(lineClicked, True)
                        self.Expand(lineClicked, True, True, 1)
                    elif event.GetControl():
                        if self.GetFoldExpanded(lineClicked):
                            self.SetFoldExpanded(lineClicked, False)
                            self.Expand(lineClicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(lineClicked, True)
                            self.Expand(lineClicked, True, True, 100)
                    else:
                        self.ToggleFold(lineClicked)

    def FoldAll(self):
        lineCount = self.GetLineCount()
        expanding = True

        # find out if we are folding or unfolding
        for lineNum in range(lineCount):
            if self.GetFoldLevel(lineNum) & stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldExpanded(lineNum)
                break

        lineNum = 0

        while lineNum < lineCount:
            level = self.GetFoldLevel(lineNum)
            if level & stc.STC_FOLDLEVELHEADERFLAG and \
               (level & stc.STC_FOLDLEVELNUMBERMASK) == stc.STC_FOLDLEVELBASE:

                if expanding:
                    self.SetFoldExpanded(lineNum, True)
                    lineNum = self.Expand(lineNum, True)
                    lineNum = lineNum - 1
                else:
                    lastChild = self.GetLastChild(lineNum, -1)
                    self.SetFoldExpanded(lineNum, False)

                    if lastChild > lineNum:
                        self.HideLines(lineNum + 1, lastChild)

            lineNum = lineNum + 1

    def Expand(self, line, doExpand, force=False, visLevels=0, level=-1):
        lastChild = self.GetLastChild(line, level)
        line = line + 1

        while line <= lastChild:
            if force:
                if visLevels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            else:
                if doExpand:
                    self.ShowLines(line, line)

            if level == -1:
                level = self.GetFoldLevel(line)

            if level & stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if visLevels > 1:
                        self.SetFoldExpanded(line, True)
                    else:
                        self.SetFoldExpanded(line, False)

                    line = self.Expand(line, doExpand, force, visLevels - 1)

                else:
                    if doExpand and self.GetFoldExpanded(line):
                        line = self.Expand(line, True, force, visLevels - 1)
                    else:
                        line = self.Expand(line, False, force, visLevels - 1)
            else:
                line = line + 1

        return line
    
    def onLeftMouseUp(self, event):
        line = self.GetCurrentLine()
        lineText, column = self.GetCurLine()
        logger.debug('onLeftMouseUp lineText:%s line:%s column:%s', lineText, line, column)
        logger.debug('GetHighlightGuide: %s', self.GetHighlightGuide())
#             self.statusbar.SetStatusText(self.getCurrentCursorPosition(), 0)
        if hasattr(self.GetTopLevelParent(), 'statusbar'):
            self.GetTopLevelParent().statusbar.SetStatusText("Line " + str(line) + " , Column " + str(column), 0)
        
        event.Skip()

    def onRightMouseDown(self, event):
        other_menus = []
        logger.debug('OnPopUp self:%s event:%s', self, event)
        if self.popmenu:
            self.popmenu.Destroy()
            self.popmenu = None
        fileMenu = wx.Menu()   
        imp = wx.Menu()
        imp.Append(wx.ID_ANY, 'Import newsfeed list...') 
        fileMenu.Append(wx.ID_ANY, 'I&mport', imp)
        if self.popmenu:
            self.popmenu.Append(fileMenu)
            self.PopupMenu(self.popmenu, event.GetPosition())
                
    def initKeyShortCut(self):
        self.CmdKeyClearAll()
        self.keydefs = {}
        action = [

#       wxSTC_CMD_BACKTAB Dedent the selected lines
            ('Shift+Tab', stc.STC_CMD_BACKTAB),
#       wxSTC_CMD_CANCEL Cancel any modes such as call tip or auto-completion list display
            ('Esc', stc.STC_CMD_CANCEL),
#       wxSTC_CMD_CHARLEFT Move caret left one character
            ('Left', stc.STC_CMD_CHARLEFT),
#       wxSTC_CMD_CHARLEFTEXTEND Move caret left one character extending selection to new caret position
            ('Shift+Left', stc.STC_CMD_CHARLEFTEXTEND),
#       wxSTC_CMD_CHARRIGHT Move caret right one character
            ('Right', stc.STC_CMD_CHARRIGHT),
#       wxSTC_CMD_CHARRIGHTEXTEND Move caret right one character extending selection to new caret position
            ('Shift+Right', stc.STC_CMD_CHARRIGHTEXTEND),
#       wxSTC_CMD_CLEAR
            ('Del', stc.STC_CMD_CLEAR),
#       wxSTC_CMD_COPY Copy the selection to the clipboard
           ('Ctrl+C', stc.STC_CMD_COPY),
#            ('Ctrl+Ins', stc.STC_CMD_COPY),
#       wxSTC_CMD_CUT Cut the selection to the clipboard
           ('Ctrl+X', stc.STC_CMD_CUT),
           ('Shift+Del', stc.STC_CMD_CUT),
#       wxSTC_CMD_DELETEBACK Delete the selection or if no selection, the character before the caret
            ('Back', stc.STC_CMD_DELETEBACK),
#       wxSTC_CMD_DELETEBACKNOTLINE Delete the selection or if no selection, the character before the caret. Will not delete the character before at the start of a line.
#       wxSTC_CMD_DELWORDLEFT Delete the word to the left of the caret
            ('Ctrl+Back', stc.STC_CMD_DELWORDLEFT),
#       wxSTC_CMD_DELWORDRIGHT Delete the word to the right of the caret
            ('Ctrl+Del', stc.STC_CMD_DELWORDRIGHT),
#       wxSTC_CMD_DOCUMENTEND Move caret to last position in document
            ('Ctrl+End', stc.STC_CMD_DOCUMENTEND),
#       wxSTC_CMD_DOCUMENTENDEXTEND Move caret to last position in document extending selection to new caret position
            ('Ctrl+Shift+End', stc.STC_CMD_DOCUMENTENDEXTEND),
#       wxSTC_CMD_DOCUMENTSTART Move caret to first position in document
            ('Ctrl+Home', stc.STC_CMD_DOCUMENTSTART),
#       wxSTC_CMD_DOCUMENTSTARTEXTEND Move caret to first position in document extending selection to new caret position
            ('Ctrl+Shift+Home', stc.STC_CMD_DOCUMENTSTARTEXTEND),
#       wxSTC_CMD_EDITTOGGLEOVERTYPE Switch from insert to overtype mode or the reverse
            ('Ins', stc.STC_CMD_EDITTOGGLEOVERTYPE),
#       wxSTC_CMD_FORMFEED Insert a Form Feed character
#       wxSTC_CMD_HOME Move caret to first position on line
#       wxSTC_CMD_HOMEDISPLAY Move caret to first position on display line
            ('Shift+Home', stc.STC_CMD_HOMEDISPLAY),
#       wxSTC_CMD_HOMEDISPLAYEXTEND Move caret to first position on display line extending selection to new caret position
            ('Shift+Alt+Home', stc.STC_CMD_HOMEDISPLAYEXTEND),
#       wxSTC_CMD_HOMEEXTEND Move caret to first position on line extending selection to new caret position
#       wxSTC_CMD_LINECUT Cut the line containing the caret
            ('Ctrl+Shift+D', stc.STC_CMD_LINECUT),
#       wxSTC_CMD_LINEDELETE Delete the line containing the caret
            ('Ctrl+D', stc.STC_CMD_LINEDELETE),
            ('Ctrl+Enter', 5000),
#       wxSTC_CMD_LINEDOWN Move caret down one line
            ('Down', stc.STC_CMD_LINEDOWN),
#       wxSTC_CMD_LINEDOWNEXTEND Move caret down one line extending selection to new caret position
            ('Shift+Down', stc.STC_CMD_LINEDOWNEXTEND),
#       wxSTC_CMD_LINEEND Move caret to last position on line
#       wxSTC_CMD_LINEENDDISPLAY Move caret to last position on display line
            ('End', stc.STC_CMD_LINEENDDISPLAY),
#       wxSTC_CMD_LINEENDDISPLAYEXTEND Move caret to last position on display line extending selection to new caret position
            ('Shift+End', stc.STC_CMD_LINEENDDISPLAYEXTEND),
#       wxSTC_CMD_LINEENDEXTEND Move caret to last position on line extending selection to new caret position
#       wxSTC_CMD_LINESCROLLDOWN Scroll the document down, keeping the caret visible
            ('Ctrl+Down', stc.STC_CMD_LINESCROLLDOWN),
#       wxSTC_CMD_LINESCROLLUP Scroll the document up, keeping the caret visible
            ('Ctrl+Up', stc.STC_CMD_LINESCROLLUP),
#       wxSTC_CMD_LINETRANSPOSE Switch the current line with the previous
            ('Alt+S', stc.STC_CMD_LINETRANSPOSE),
#       wxSTC_CMD_LINEUP Move caret up one line
            ('Up', stc.STC_CMD_LINEUP),
#       wxSTC_CMD_LINEUPEXTEND Move caret up one line extending selection to new caret position
            ('Shift+Up', stc.STC_CMD_LINEUPEXTEND),
#       wxSTC_CMD_LOWERCASE Transform the selection to lower case
            ('Ctrl+L', stc.STC_CMD_LOWERCASE),
#       wxSTC_CMD_NEWLINE Insert a new line, may use a CRLF, CR or LF depending on EOL mode
            ('Enter', stc.STC_CMD_NEWLINE),
#       wxSTC_CMD_PAGEDOWN Move caret one page down
            ('Pgdn', stc.STC_CMD_PAGEDOWN),
#       wxSTC_CMD_PAGEDOWNEXTEND Move caret one page down extending selection to new caret position
            ('Shift+Pgdn', stc.STC_CMD_PAGEDOWNEXTEND),
#       wxSTC_CMD_PAGEUP Move caret one page up
            ('Pgup', stc.STC_CMD_PAGEUP),
#       wxSTC_CMD_PAGEUPEXTEND Move caret one page up extending selection to new caret position
            ('Shift+Pgup', stc.STC_CMD_PAGEUPEXTEND),
            ('Ctrl+V', stc.STC_CMD_PASTE),
            ('Shift+Ins', stc.STC_CMD_PASTE),
#       wxSTC_CMD_REDO Redoes the next action on the undo history
            ('Ctrl+Y', stc.STC_CMD_REDO),
#       wxSTC_CMD_SELECTALL Select all the text in the document
            ('Ctrl+A', stc.STC_CMD_SELECTALL),
#       wxSTC_CMD_TAB If selection is empty or all on one line replace the selection with a tab character. If more than one line selected, indent the lines
            ('Tab', stc.STC_CMD_TAB),
#       wxSTC_CMD_UNDO Redoes the next action on the undo history
            ('Ctrl+Z', stc.STC_CMD_UNDO),
#       wxSTC_CMD_UPPERCASE Transform the selection to upper case
            ('Ctrl+U', stc.STC_CMD_UPPERCASE),
#       wxSTC_CMD_VCHOME Move caret to before first visible character on line. If already there move to first character on line
            ('Home', stc.STC_CMD_VCHOME),
#       wxSTC_CMD_VCHOMEEXTEND Like VCHome but extending selection to new caret position
            ('Shift+Home', stc.STC_CMD_VCHOMEEXTEND),
#       wxSTC_CMD_WORDLEFT Move caret left one word
            ('Ctrl+Left', stc.STC_CMD_WORDLEFT),
#       wxSTC_CMD_WORDLEFTEXTEND Move caret left one word extending selection to new caret position
            ('Ctrl+Shift+Left', stc.STC_CMD_WORDLEFTEXTEND),
#       wxSTC_CMD_WORDRIGHT Move caret right one word
            ('Ctrl+Right', stc.STC_CMD_WORDRIGHT),
#       wxSTC_CMD_WORDRIGHTEXTEND Move caret right one word extending selection to new caret position
            ('Ctrl+Shift+Right', stc.STC_CMD_WORDRIGHTEXTEND),
#       wxSTC_CMD_ZOOMIN Magnify the displayed text by increasing the sizes by 1 point
            ('Ctrl+B', stc.STC_CMD_ZOOMIN),
#       wxSTC_CMD_ZOOMOUT Make the displayed text smaller by decreasing the sizes by 1 point
            ('Ctrl+N', stc.STC_CMD_ZOOMOUT),
#       wxSTC_CMD_DELLINELEFT: Use 2395 Delete back from the current position to the start of the line
            ('Alt+Back', stc.STC_CMD_DELLINELEFT),
#       wxSTC_CMD_DELLINERIGHT: Use 2396 Delete forwards from the current position to the end of the line
            ('Alt+Del', stc.STC_CMD_DELLINERIGHT),
#       wxSTC_CMD_WORDPARTLEFT: Use 2390 Move to the next change in capitalisation
            ('Alt+Left', stc.STC_CMD_WORDPARTLEFT),
#       wxSTC_CMD_WORDPARTLEFTEXTEND: Use 2391 Move to the previous change in capitalisation extending selection to new caret position
            ('Alt+Shift+Left', stc.STC_CMD_WORDPARTLEFTEXTEND),
#       wxSTC_CMD_WORDPARTRIGHT: Use 2392 Move caret right one word extending selection to new caret position
            ('Alt+Right', stc.STC_CMD_WORDPARTRIGHT),
#       wxSTC_CMD_WORDPARTRIGHTEXTEND: Use 2393 Move to the next change in capitalisation extending selection to new caret position.
            ('Alt+Shift+Right', stc.STC_CMD_WORDPARTRIGHTEXTEND),
        ]

        for keys, cmd in action:
            self.keydefs[keys.upper()] = cmd
            f, ikey = self.convert_key(keys)
            self.CmdKeyAssign(ikey, f, cmd)  

    def convert_key(self, keydef):
        f = 0
        ikey = 0
#         logger.debug 'keydef-------------->', keydef
        for k in keydef.split('+'):
            uk = k.upper()
            if uk == 'CTRL':
                f |= stc.STC_SCMOD_CTRL
            elif uk == 'ALT':
                f |= stc.STC_SCMOD_ALT
            elif uk == 'SHIFT':
                f |= stc.STC_SCMOD_SHIFT
            elif uk in keylist:
                ikey = keylist[uk]
            elif len(uk) == 1:
                ikey = ord(uk)
            else:
                logger.debug("[TextEditor] Undefined char [%s]", uk)
                continue
        return f, ikey      

    def execute_key(self, keydef):
#         logger.debug 'execute_key--->', keydef
        if isinstance(keydef, str):
            cmd = self.keydefs.get(keydef.upper(), None)
        else:
            cmd = keydef
        if cmd:
            self.CmdKeyExecute(cmd)
    
    def executeSQL(self):
        '''
        '''
        error = 'success'
        sqlText = self.GetSelectedText()
        if self.GetSelectedText() == '' or self.GetSelectedText() == None:
            sqlText, column = self.GetCurLine()
        
        ##################################################################################
        selectedItemText, dbFilePath = self.findingConnectionName()
#         sqlExecuter = SQLExecuter(database='_opal.sqlite')
#         textCtrl = self.GetTopLevelParent()._ctrl
#         selectedItemText = textCtrl.GetValue()
#         dbFilePath = sqlExecuter.getDbFilePath(selectedItemText)
#         logger.debug("dbFilePath: %s", dbFilePath)
        
        ##################################################################################
        logger.debug('executeSQL: %s' , sqlText)
        try:
            if os.path.isfile(dbFilePath):
                sqlOutput = None
                startTime = time.time()
                try:
                    manageSqliteDatabase = ManageSqliteDatabase(connectionName=selectedItemText, databaseAbsolutePath=dbFilePath)
                    sqlOutput = manageSqliteDatabase.executeText(sqlText)
                except OperationalError as oe:
                    self.GetTopLevelParent()._mgr.GetPane("scriptOutput").window.text.AppendText("\n" + str(oe))
                except Exception as e:
                    logger.error(e, exc_info=True)
                endTime = time.time()
                logger.debug('duration: %s', endTime - startTime)
                duration = endTime - startTime
                if selectedItemText:
                    self.updateSqlLog(sqlText, duration, connectionName=selectedItemText)
        
                creatingWorksheetPanel = self.GetTopLevelParent()._mgr.GetPane("sqlExecution").window.GetChildren()[0].GetCurrentPage().Children[1]
                creatingWorksheetPanel.setResultData(data=sqlOutput)
                resultListPanel = self.GetTopLevelParent()._mgr.GetPane("sqlExecution").window.GetChildren()[0].GetCurrentPage().Children[1].splitter.Children[1]
        #         if sqlOutput:
                if resultListPanel._nb.GetCurrentPage():
                    resultListPanel._nb.GetCurrentPage().resultPanel.addData(data=sqlOutput)
        except TypeError as te:
            logger.error(te, exc_info=True)
            if not dbFilePath:
                error = 'Unable to connect. Please choose a database to execute Script.'
                self.GetTopLevelParent()._mgr.GetPane("scriptOutput").window.text.AppendText("\n" + error)
        except Exception as e:
            logger.error(e, exc_info=True)
            self.GetTopLevelParent()._mgr.GetPane("scriptOutput").window.text.AppendText("\n" + str(e))
#             print(e)
            error = str(e)
            
        self.refreshSqlLogUi()
#         updateStatus="Unable to connect '"+dbFilePath +". "+error
#         scriptOutputPanel = self.GetTopLevelParent()._mgr.GetPane("scriptOutput").window
#         scriptOutputPanel.text.AppendText(error)
#             font = self.GetTopLevelParent().statusbar.GetFont() 
#             font.SetWeight(wx.BOLD) 
#             self.GetTopLevelParent().statusbar.SetFont(font) 
#             self.GetTopLevelParent().statusbar.SetForegroundColour(wx.RED) 
#             self.GetTopLevelParent().statusbar.SetStatusText(updateStatus,1)
        # TODO Update update sql log history grid
        
    def findingConnectionName(self):
        '''
        This method defines connection name based on selected connection in the tree.
        @return: (connectionName, databaseAbsolutePath)
        '''
        ##################################################################################
        sqlExecuter = SQLExecuter(database='_opal.sqlite')
        textCtrl = self.GetTopLevelParent()._ctrl
        connectionName = textCtrl.GetValue()
        databaseAbsolutePath = sqlExecuter.getDbFilePath(connectionName)
        logger.debug("databaseAbsolutePath: %s", databaseAbsolutePath)
        
        ##################################################################################        
        return connectionName, databaseAbsolutePath
        
    def updateSqlLog(self, sqlText, duration, connectionName=None):
        logger.debug('updateSqlLog : %s', sqlText)
        sqlExecuter = SQLExecuter(database='_opal.sqlite')
        table = 'sql_log'
        rows = [{'id':None, 'sql':str(sqlText), 'connection_name':connectionName, 'created_time':datetime.now(), 'executed':'1', 'duration':duration}]
        sqlExecuter.sqlite_insert(table, rows)
        
    def refreshSqlLogUi(self):
        logger.debug('refreshSqlLogUi')
        historyGrid = self.GetTopLevelParent()._mgr.GetPane("sqlLog").window
        sqlText = 'select * from sql_log order by created_time desc;'
        sqlExecuter = SQLExecuter(database='_opal.sqlite')
        sqlOutput = sqlExecuter.executeText(sqlText)
        historyGrid.addData(data=sqlOutput)
              
    def sqlStyle(self):
        # Sql styles
        # Default 
        self.StyleSetSpec(stc.STC_P_DEFAULT, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        # Comments
        self.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:#007F00,face:%(other)s,size:%(size)d" % faces)
        # Number
        self.StyleSetSpec(stc.STC_P_NUMBER, "fore:#007F7F,size:%(size)d" % faces)
        # String
        self.StyleSetSpec(stc.STC_P_STRING, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
        # Single quoted string
        self.StyleSetSpec(stc.STC_P_CHARACTER, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
        # Keyword
        self.StyleSetSpec(stc.STC_P_WORD, "fore:#00007F,bold,size:%(size)d" % faces)
        # Triple quotes
        self.StyleSetSpec(stc.STC_P_TRIPLE, "fore:#7F0000,size:%(size)d" % faces)
        # Triple double quotes
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:#7F0000,size:%(size)d" % faces)
        # Class name definition
        self.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:#0000FF,bold,underline,size:%(size)d" % faces)
        # Function or method name definition
        self.StyleSetSpec(stc.STC_P_DEFNAME, "fore:#007F7F,bold,size:%(size)d" % faces)
        # Operators
        self.StyleSetSpec(stc.STC_P_OPERATOR, "bold,size:%(size)d" % faces)
        # Identifiers
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        # Comment-blocks
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:#7F7F7F,size:%(size)d" % faces)
        # End of line where string is not closed
        self.StyleSetSpec(stc.STC_P_STRINGEOL, "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces)

        self.SetCaretForeground("BLUE")        


class CreatingEditorPanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        
        vBox = wx.BoxSizer(wx.VERTICAL)

        ####################################################################
        self.sstc = SqlStyleTextCtrl(self, -1)
        self.sstc.initKeyShortCut()
        self.sstc.SetText(demoText)
        self.sstc.EmptyUndoBuffer()
        self.sstc.Colourise(0, -1)
        self.sstc.SetInitialSize(wx.Size(400, 400))
#         self.sstc.SetBestFittingSize(wx.Size(400, 400))

        # line numbers in the margin
        self.sstc.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.sstc.SetMarginWidth(1, 25)
        ####################################################################
        vBox.Add(self.sstc , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None)
    panel = CreatingEditorPanel(frame)
    frame.Show()
    app.MainLoop()
