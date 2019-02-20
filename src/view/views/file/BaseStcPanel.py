
import wx
import wx.stc as stc
from src.view.util.common.FileObjectWrapper import FileObject
from src.view.util.common.FileStyle import StyleManager
from src.view.util.syntax.syntax import SyntaxMgr
from src.view.util.common.ed_marker import NewMarkerId, Marker, Breakpoint, \
    BreakpointDisabled, BreakpointStep, LintMarker, LintMarkerWarning, \
    LintMarkerError, ErrorMarker, StackMarker, Bookmark, FoldMarker
from src.view.util.common.eclutil import Freezer, HexToRGB
from src.view.util.syntax.synglob import FEATURE_STYLETEXT, FEATURE_AUTOINDENT
from src.view.util.common.ed_glob import ID_ZOOM_OUT, ID_ZOOM_IN
from src.view.util.common.fileutil import GetFileName
from src.view.util.common.vertedit import VertEdit

import logging.config
from src.view.constants import LOG_SETTINGS
logging.config.dictConfig(LOG_SETTINGS)
logger = logging.getLogger('extensive')

#-----------------------------------------------------------------------------#

# Margins
MARK_MARGIN = 0
NUM_MARGIN = 1
FOLD_MARGIN = 2

# Markers (3rd party)
MARKER_VERT_EDIT = NewMarkerId()

# Key code additions
ALT_SHIFT = stc.STC_SCMOD_ALT | stc.STC_SCMOD_SHIFT
CTRL_SHIFT = stc.STC_SCMOD_CTRL | stc.STC_SCMOD_SHIFT

#-----------------------------------------------------------------------------#


class BaseStc(stc.StyledTextCtrl, StyleManager):
    """Base StyledTextCtrl that provides all the base code editing functionality.

    """    
    ED_STC_MASK_MARKERS = ~stc.STC_MASK_FOLDERS

    def __init__(self, parent, id_=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        
        stc.StyledTextCtrl.__init__(self, parent, id_, pos, size, style)
        StyleManager.__init__(self, self.GetStyleSheet())
        self.file = FileObject()
        self._code = dict(
            compsvc=None, #autocomp.AutoCompService.GetCompleter(self),
            synmgr=SyntaxMgr(),
            keywords=[ ' ' ],
            comment=list(),
            clexer=None,  # Container lexer method
            indenter=None,  # Auto indenter
            lang_id=0)  # Language ID from syntax module
        self.vert_edit = VertEdit(self, markerNumber=MARKER_VERT_EDIT)
        self._line_num = True  # Show line numbers
        self._last_cwidth = 1  # one pixel

        # Set Up Margins
        # # Outer Left Margin Bookmarks
        self.SetMarginType(MARK_MARGIN, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(MARK_MARGIN, BaseStc.ED_STC_MASK_MARKERS)
        self.SetMarginSensitive(MARK_MARGIN, True)
        self.SetMarginWidth(MARK_MARGIN, 16)

        # # Middle Left Margin Line Number Indication
        self.SetMarginType(NUM_MARGIN, stc.STC_MARGIN_NUMBER)
        self.SetMarginMask(NUM_MARGIN, 0)

        # # Inner Left Margin Setup Folders
        self.SetMarginType(FOLD_MARGIN, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(FOLD_MARGIN, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(FOLD_MARGIN, True)

        # Set Mac specific keybindings
        if wx.Platform == '__WXMAC__':
            for keys in _GetMacKeyBindings():
                self.CmdKeyAssign(*keys)

        # Set default EOL format
        if wx.Platform != '__WXMSW__':
            self.SetEOLMode(stc.STC_EOL_LF)

        # Setup Auto-comp images
        # TODO: should be called on theme change messages
        self.RegisterImages()

        # Event Handlers
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroy, self)
        self.Bind(stc.EVT_STC_CHANGE, self.OnChanged)
        self.Bind(stc.EVT_STC_MODIFIED, self.OnModified)
        self.Bind(stc.EVT_STC_AUTOCOMP_SELECTION, self.OnAutoCompSel)

    def OnDestroy(self, evt):
        if evt.GetId() == self.GetId():
            # Cleanup the file object callbacks
            self.file.RemoveModifiedCallback(self.FireModified)
            self.file.CleanUp()
        evt.Skip()

    #---- Public Methods ----#

    # General marker api
    def AddMarker(self, marker, line=-1):
        """Add a bookmark and return its handle
        @param marker: Marker instance
        @keyword line: if < 0 bookmark will be added to current line

        """
        assert isinstance(marker, Marker)
        if line < 0:
            line = self.GetCurrentLine()
        marker.Set(self, line)
        return marker.Handle

    def RemoveMarker(self, marker, line):
        """Remove the book mark from the given line
        @param marker: Marker instance
        @param line: int

        """
        assert isinstance(marker, Marker)
        marker.Set(self, line, delete=True)

    def RemoveAllMarkers(self, marker):
        """Remove all the bookmarks in the buffer
        @param marker: Marker instance

        """
        assert isinstance(marker, Marker)
        marker.DeleteAll(self)

    # -- Breakpoint marker api --#
    def DeleteAllBreakpoints(self):
        """Delete all the breakpoints in the buffer"""
        Breakpoint().DeleteAll(self)
        BreakpointDisabled().DeleteAll(self)
        BreakpointStep().DeleteAll(self)

    def DeleteBreakpoint(self, line):
        """Delete the breakpoint from the given line"""
        Breakpoint().Set(self, line, delete=True)
        BreakpointDisabled().Set(self, line, delete=True)

    def _SetBreakpoint(self, mobj, line=-1):
        """Set the breakpoint state
        @param mtype: Marker object
        @return: int (-1 if already set)

        """
        handle = -1
        if line < 0:
            line = self.GetCurrentLine()
        if not mobj.IsSet(self, line):
            # Clear other set breakpoint marker states on same line
            Breakpoint().Set(self, line, delete=True)
            BreakpointDisabled().Set(self, line, delete=True)
            mobj.Set(self, line, delete=False)
            handle = mobj.Handle
        return handle

    def SetBreakpoint(self, line=-1, disabled=False):
        """Set a breakpoint marker on the given line
        @keyword line: line number
        @keyword disabled: bool
        @return: breakpoint handle

        """
        if not disabled:
            handle = self._SetBreakpoint(Breakpoint(), line)
        else:
            handle = self._SetBreakpoint(BreakpointDisabled(), line)
        return handle

    def ShowStepMarker(self, line=-1, show=True):
        """Show the step (arrow) marker to the given line."""
        if line < 0:
            line = self.GetCurrentLine()
        mark = BreakpointStep()
        if show:
            mark.Set(self, line, delete=False)
        else:
            mark.DeleteAll(self)

    def AddLine(self, before=False, indent=False):
        """Add a new line to the document
        @keyword before: whether to add the line before current pos or not
        @keyword indent: autoindent the new line
        @postcondition: a new line is added to the document

        """
        if before:
            self.LineUp()

        self.LineEnd()

        if indent:
            self.AutoIndent()
        else:
            self.InsertText(self.GetCurrentPos(), self.GetEOLChar())
            self.LineDown()

    def AutoIndent(self):
        """Indent from the current position to match the indentation
        of the previous line. Unless the current file type has registered
        a custom AutoIndenter in which case it will implement its own
        behavior.

        """
        cpos = self.GetCurrentPos()

        # Check if a special purpose indenter has been registered
        if self._code['indenter'] is not None:
            self.BeginUndoAction()
            self._code['indenter'](self, cpos, self.GetIndentChar())
            self.EndUndoAction()
        else:
            # Default Indenter
            line = self.GetCurrentLine()
            text = self.GetTextRange(self.PositionFromLine(line), cpos)
            if text.strip() == u'':
                self.AddText(self.GetEOLChar() + text)
                self.EnsureCaretVisible()
                return
            indent = self.GetLineIndentation(line)
            i_space = int( indent / self.GetTabWidth())
            try:
                ndent = self.GetEOLChar() + self.GetIndentChar() * i_space
                txt = ndent + ((indent - (self.GetTabWidth() * i_space)) * u' ')
                self.AddText(txt)
                self.EnsureCaretVisible()
            except Exception as e:
                logger.error(e, exc_info=True)


    def BackTab(self):
        """Unindent or remove excess whitespace to left of cursor"""
        sel = self.GetSelection()
        if sel[0] == sel[1]:
            # There is no selection
            cpos = self.GetCurrentPos()
            cline = self.GetCurrentLine()
            cipos = self.GetLineIndentPosition(cline)
            if cpos <= cipos:
                # In indentation so simply backtab
                super().BackTab()
            else:
                # In middle of line somewhere
                text = self.GetLine(cline)
                column = max(0, self.GetColumn(cpos) - 1)
                if len(text) > column and text[column].isspace():

                    # Find the end of the whitespace
                    end = column
                    while end < len(text) and \
                          text[end].isspace() and \
                          text[end] not in '\r\n':
                        end += 1

                    # Find the start of the whitespace
                    end -= 1
                    start = end
                    while end > 0 and text[start].isspace():
                        start -= 1

                    diff = end - start
                    if diff > 1:
                        # There is space to compress
                        isize = self.GetIndent()
                        if isize < diff:
                            # More space than indent to remove
                            repeat = isize
                        else:
                            # Less than one indent width to remove
                            repeat = end - (start + 1)

                        # Update the control
                        self.BeginUndoAction()
                        self.SetCurrentPos(cpos + (end - column))
                        for x in range(repeat):
                            self.DeleteBack()
                        self.EndUndoAction()

        else:
            # There is a selection
            super().BackTab()

    def SetBlockCaret(self):
        """Change caret style to block"""
        if hasattr(self, 'SetCaretStyle'):  # wxPython 2.9 or greater
            self.SetCaretStyle(stc.STC_CARETSTYLE_BLOCK)
        else:
            # Alternatively, just make the caret a bit thicker!
            # best we can do on 2.8
            self.SetCaretWidth(3)

    def SetLineCaret(self):
        """Change caret style to line"""
        if hasattr(self, 'SetCaretStyle'):
            self.SetCaretStyle(stc.STC_CARETSTYLE_LINE)
#         else:
#             pwidth = Profile_Get('CARETWIDTH', default=1)
#             self.SetCaretWidth(pwidth)

    def BraceBadLight(self, pos):
        """Highlight the character at the given position
        @param pos: position of character to highlight with STC_STYLE_BRACEBAD

        """
        # Check if we are still alive or not, as this may be called
        # after we have been deleted.
        if self:
            super().BraceBadLight(pos)

    def BraceHighlight(self, pos1, pos2):
        """Highlight characters at pos1 and pos2
        @param pos1: position of char 1
        @param pos2: position of char 2

        """
        # Check if we are still alive or not, as this may be called
        # after we have been deleted.
        if self:
            super().BraceHighlight(pos1, pos2)

    def CanCopy(self):
        """Check if copy/cut is possible"""
        return self.HasSelection()

    CanCut = CanCopy

    def Comment(self, start, end, uncomment=False):
        """(Un)Comments a line or a selected block of text
        in a document.
        @param start: beginning line (int)
        @param end: end line (int)
        @keyword uncomment: uncomment selection

        """
        if len(self._code['comment']):
            sel = self.GetSelection()
            c_start = self._code['comment'][0]
            c_end = u''
            if len(self._code['comment']) > 1:
                c_end = self._code['comment'][1]

            # Modify the selected line(s)
            self.BeginUndoAction()
            try:
                nchars = 0
                lines = range(start, end + 1)
                lines.reverse()
                for line_num in lines:
                    lstart = self.PositionFromLine(line_num)
                    lend = self.GetLineEndPosition(line_num)
                    text = self.GetTextRange(lstart, lend)
                    tmp = text.strip()
                    if len(tmp):
                        if uncomment:
                            if tmp.startswith(c_start):
                                text = text.replace(c_start, u'', 1)
                            if c_end and tmp.endswith(c_end):
                                text = text.replace(c_end, u'', 1)
                            nchars = nchars - len(c_start + c_end)
                        else:
                            text = c_start + text + c_end
                            nchars = nchars + len(c_start + c_end)

                        self.SetTargetStart(lstart)
                        self.SetTargetEnd(lend)
                        self.ReplaceTarget(text)
            finally:
                self.EndUndoAction()
                if sel[0] != sel[1]:
                    self.SetSelection(sel[0], sel[1] + nchars)
                else:
                    if len(self._code['comment']) > 1:
                        nchars = nchars - len(self._code['comment'][1])
                    self.GotoPos(sel[0] + nchars)

    def ConfigureAutoComp(self):
        """Sets up the Autocompleter, the autocompleter
        configuration depends on the currently set lexer
        @postcondition: autocomp is configured

        """
        self.AutoCompSetAutoHide(False)
        self.InitCompleter()
#         self.AutoCompSetChooseSingle(self._code['compsvc'].GetChooseSingle())
#         self.AutoCompSetIgnoreCase(not self._code['compsvc'].GetCaseSensitive())
#         self.AutoCompStops(self._code['compsvc'].GetAutoCompStops())
        # TODO: come back to this it can cause some annoying behavior where
        #       it automatically completes strings that you don't want to be
        #       inserted in the buffer. (i.e typing self._value will bring up
        #       the autocomp list but if self._value is not in the list and you
        #       hit space it will automatically insert something from the list.)
#        self.AutoCompSetFillUps(self._code['compsvc'].GetAutoCompFillups())

    def ConfigureLexer(self, file_ext):
        """Sets Lexer and Lexer Keywords for the specified file extension
        @param file_ext: a file extension to configure the lexer from

        """
        syn_data = self._code['synmgr'].GetSyntaxData(file_ext)

        # Set the ID of the selected lexer
        self._code['lang_id'] = syn_data.LangId

        lexer = syn_data.Lexer
        # Check for special cases
        # TODO: add fetch method to check if container lexer requires extra
        #       style bytes beyond the default 5.
        if lexer in [ stc.STC_LEX_HTML, stc.STC_LEX_XML]:
            self.SetStyleBits(7)
        elif lexer == stc.STC_LEX_NULL:
            self.SetStyleBits(5)
            self.SetLexer(lexer)
            self.ClearDocumentStyle()
            self.UpdateBaseStyles()
            return True
        else:
            self.SetStyleBits(5)

        # Set Lexer
        self.SetLexer(lexer)
        # Set Keywords
        self.SetKeyWords(syn_data.Keywords)
        # Set Lexer/Syntax Specifications
        self.SetSyntax(syn_data.SyntaxSpec)
        # Set Extra Properties
        self.SetProperties(syn_data.Properties)
        # Set Comment Pattern
        self._code['comment'] = syn_data.CommentPattern

        # Get Extension Features
        clexer = syn_data.GetFeature(FEATURE_STYLETEXT)
        indenter = syn_data.GetFeature(FEATURE_AUTOINDENT)

        # Set the Container Lexer Method
        self._code['clexer'] = clexer
        # Auto-indenter function
        self._code['indenter'] = indenter

    def DefineMarkers(self):
        """Defines the folder and bookmark icons for this control
        @postcondition: all margin markers are defined

        """
        # Get the colours for the various markers
        style = self.GetItemByName('foldmargin_style')
        back = style.GetFore()
        if back and back != '':
            rgb = HexToRGB(back[1:])
            back = wx.Colour(red=rgb[0], green=rgb[1], blue=rgb[2])
        else:
            back = wx.BG_STYLE_COLOUR

        fore = style.GetBack()
        rgb = HexToRGB(fore[1:])
        fore = wx.Colour(red=rgb[0], green=rgb[1], blue=rgb[2])

        # Buffer background highlight
        caret_line = self.GetItemByName('caret_line').GetBack()
        rgb = HexToRGB(caret_line[1:])
        clback = wx.Colour(*rgb)

        # Code Folding markers
        folder = FoldMarker()
        folder.Foreground = fore
        folder.Background = back
        folder.RegisterWithStc(self)

        # Bookmarks
        Bookmark().RegisterWithStc(self)

        # Breakpoints
        Breakpoint().RegisterWithStc(self)
        BreakpointDisabled().RegisterWithStc(self)
        step = BreakpointStep()
        step.Background = clback
        step.RegisterWithStc(self)
        StackMarker().RegisterWithStc(self)

        # Other markers
        errmk = ErrorMarker()
        errsty = self.GetItemByName('error_style')
        rgb = HexToRGB(errsty.GetBack()[1:])
        errmk.Background = wx.Colour(*rgb)
        rgb = HexToRGB(errsty.GetFore()[1:])
        errmk.Foreground = wx.Colour(*rgb)
        errmk.RegisterWithStc(self)
        # Lint Marker
        LintMarker().RegisterWithStc(self)
        LintMarkerWarning().RegisterWithStc(self)
        LintMarkerError().RegisterWithStc(self)

    def DoZoom(self, mode):
        """Zoom control in or out
        @param mode: either zoom in or out

        """
        id_type = mode
        zoomlevel = self.GetZoom()
        if id_type == ID_ZOOM_OUT:
            if zoomlevel > -9:
                self.ZoomOut()
        elif id_type == ID_ZOOM_IN:
            if zoomlevel < 19:
                self.ZoomIn()
        else:
            self.SetZoom(0)
        return self.GetZoom()

    def EnableLineNumbers(self, enable=True):
        """Enable/Disable line number margin
        @keyword enable: bool

        """
        if enable:
            self.SetMarginWidth(NUM_MARGIN, 30)
        else:
            self.SetMarginWidth(NUM_MARGIN, 0)
        self._line_num = enable

    def FindChar(self, char, repeat=1, reverse=False, extra_offset=0):
        """Find the position of the next (ith) 'char' character
        on the current line and move caret to it

        @note: used by vim motions for finding a character on a line (f,F,t,T)
        @param char: the character to be found
        @keyword repeat: how many times to repeat the search
        @keyword reverse: whether to search backwards
        @keyword extra_offset: extra offset to be applied to the movement

        """
        text, pos = self.GetCurLine()
        oldpos = pos
        if not reverse:
            # search forward
            for i in range(repeat):
                pos = text.find(char, pos + 1)
                if pos == -1:
                    return
        else:
            # search backward
            for i in range(repeat):
                pos = text.rfind(char, 0, pos)
                if pos == -1:
                    return

        newpos = pos + extra_offset
        if newpos in range(len(text)):
            self.MoveCaretPos(newpos - oldpos)

    @property
    def File(self):
        """Reference to this buffers file object"""
        return self.file

    def FindLexer(self, set_ext=u''):
        """Sets Text Controls Lexer Based on File Extension
        @param set_ext: explicit extension to use in search
        @postcondition: lexer is configured for file

        """
        if set_ext != u'':
            ext = set_ext.lower()
        else:
            ext = self.file.getExtension().lower()

        if ext == u'':
            fname = self.GetFileName()
            ext = GetFileName(fname).lower()

        self.ClearDocumentStyle()

        # Configure Lexer from File Extension
        self.ConfigureLexer(ext)

        # If syntax auto detection fails from file extension try to
        # see if there is an interpreter line that can be parsed.
        if self.GetLexer() == stc.STC_LEX_NULL:
            interp = self.GetLine(0)
            if interp != wx.EmptyString:
                interp = interp.split(u"/")[-1]
                interp = interp.strip().split()
                if len(interp) and interp[-1][0] != u"-":
                    interp = interp[-1]
                elif len(interp):
                    interp = interp[0]
                else:
                    interp = u''
                # TODO: should check user config to ensure the explict
                #       extension is still associated with the expected
                #       file type.
                ex_map = { "python" : "py", "wish" : "tcl", "ruby" : "rb",
                           "bash" : "sh", "csh" : "csh", "perl" : "pl",
                           "ksh" : "ksh", "php" : "php", "booi" : "boo",
                           "pike" : "pike"}
                self.ConfigureLexer(ex_map.get(interp, interp))
        self.Colourise(0, -1)

    def FireModified(self):
        """Fire a modified event"""
        self.OnChanged(stc.StyledTextEvent(stc.wxEVT_STC_CHANGE, self.GetId()))

    def GetCommandStr(self, line=None, col=None):
        """Gets the command string to the left of the autocomp
        activation character.
        @keyword line: optional if None current cursor position used
        @keyword col: optional if None current cursor position used
        @return: the command string to the left of the autocomp char

        """
        if None in (line, col):
            # NOTE: the column position returned by GetCurLine is not correct
            #       for multibyte characters.
            line, col = self.GetCurLine()
            col = self.GetColumn(self.GetCurrentPos())
        try:
            cmd = self._code['compsvc'].GetCommandString(self, line, col)
        except Exception as e:
            logger.error(e)
        return cmd

    def GetCommentChars(self):
        """Return the list of characters used to comment a string in the
        current language.
        @return: list of strings

        """
        return self._code['comment']

    def GetCompleter(self):
        """Get this buffers completer object
        @return: Completer

        """
        return self._code['compsvc']

    def GetDocument(self):
        """Return a reference to the document object represented in this buffer.
        @return: EdFile
        @see: L{ed_txt.EdFile}

        """
        return self.file

    def GetEOLChar(self):
        """Gets the eol character used in document
        @return: the character used for eol in this document

        """
        m_id = self.GetEOLMode()
        if m_id == stc.STC_EOL_CR:
            return u'\r'
        elif m_id == stc.STC_EOL_CRLF:
            return u'\r\n'
        else:
            return u'\n'

    def GetFileName(self):
        """Returns the full path name of the current file
        @return: full path name of document

        """
        return self.file.GetPath()

    def GetIndentChar(self):
        """Gets the indentation char used in document
        @return: indentation char used either space or tab

        """
        if self.GetUseTabs():
            return u'\t'
        else:
            return u' ' * self.GetIndent()

    def GetKeywords(self):
        """Get the keyword set for the current document.
        @return: list of strings

        """
        return self._code['keywords']

    def GetLangId(self):
        """Returns the language identifier of this control
        @return: language identifier of document

        """
        return self._code['lang_id']

    def GetModTime(self):
        """Get the value of the buffers file last modtime"""
        return self.file.ModTime

    def GetPos(self):
        """Update Line/Column information
        @return: tuple (line, column)

        """
        return (self.GetCurrentLine() + 1, self.GetColumn(self.GetCurrentPos()))

    GetRange = stc.StyledTextCtrl.GetTextRange

    def GetWordFromPosition(self, pos):
        """Get the word at the given position
        @param pos: int
        @return: (string, int_start, int_end)

        """
        end = self.WordEndPosition(pos, True)
        start = self.WordStartPosition(pos, True)
        word = self.GetTextRange(start, end)
        return (word, start, end)

    def IsColumnMode(self):
        """Is the buffer in column edit mode
        @return: bool

        """
        return self.VertEdit.Enabled

    def IsComment(self, pos):
        """Is the given position in a comment region of the current buffer
        @param pos: int position in buffer
        @return: bool

        """
        pos = max(0, pos - 1)
        return 'comment' in self.FindTagById(self.GetStyleAt(pos))

    def IsString(self, pos):
        """Is the given position in a string region of the current buffer
        @param pos: int position in buffer
        @return: bool

        """
        style = self.GetStyleAt(pos)
        return self.FindTagById(style) in ('string_style', 'char_style')

    def IsNonCode(self, pos):
        """Is the passed in position in a non code region
        @param pos: buffer position
        @return: bool

        """
        return self.IsComment(pos) or self.IsString(pos)

    def HasMarker(self, line, marker):
        """Check if the given line has the given marker set
        @param line: line number
        @param marker: marker id

        """
        mask = self.MarkerGet(line)
        return bool(1 << marker & mask)

    def HasSelection(self):
        """Check if there is a selection in the buffer
        @return: bool

        """
        sel = super().GetSelection()
        return sel[0] != sel[1]

    def HasMultilineSelection(self):
        """Is the selection over multiple lines?
        @return: bool

        """
        bMulti = False
        sel = super().GetSelection()
        if sel[0] != sel[1]:
            sline = self.LineFromPosition(sel[0])
            eline = self.LineFromPosition(sel[1])
            bMulti = sline != eline
        return bMulti

    def CallTipCancel(self):
        """Cancel any active calltip(s)"""
        if self.CallTipActive():
            super().CallTipCancel()

    def CallTipShow(self, position, tip):
        """Show a calltip at the given position in the control
        @param position: int
        @param tip: unicode

        """
        self.CallTipCancel()
        super().CallTipShow(position, tip)

    def HidePopups(self):
        """Hide autocomp/calltip popup windows if any are active"""
        if self.AutoCompActive():
            self.AutoCompCancel()

        self.CallTipCancel()

    def InitCompleter(self):
        """(Re)Initialize a completer object for this buffer
        @todo: handle extended autocomp for plugins?

        """
        # Check for plugins that may extend or override functionality for this
        # file type.
        self._code['compsvc'] = None
#         autocomp_ext = AutoCompExtension(wx.GetApp().GetPluginManager())
#         completer = autocomp_ext.GetCompleter(self)
#         if completer is not None:
#             self._code['compsvc'] = completer
#         else:
#             extend = Profile_Get('AUTO_COMP_EX') # Using extended autocomp?
#             self._code['compsvc'] = autocomp.AutoCompService.GetCompleter(self, extend)

    def LoadFile(self, path):
        """Load the file at the given path into the buffer. Returns
        True if no errors and False otherwise. To retrieve the errors
        check the last error that was set in the file object returned by
        L{GetDocument}.
        @param path: path to file

        """
        # Post notification that a file load is starting
#         ed_msg.PostMessage(ed_msg.EDMSG_FILE_OPENING, path)
        self.file.SetPath(path)
        txt = self.file.Read()
        if txt is not None:
            if self.file.IsRawBytes() :
                self.AddStyledText(txt)
                self.SetReadOnly(True)  # Don't allow editing of raw bytes
            else:
                self.SetText(txt)
        else:
            self.file.SetPath('')
            return False

        if self.file.GetLastError() != 'None':
            # Return false if there was an encoding error and a fallback
            # was used. So the caller knows to check the error status
            return False
        else:
            return True

    def MoveCaretPos(self, offset):
        """Move caret by the given offset
        @param offset: int (+ move right, - move left)

        """
        pos = max(self.GetCurrentPos() + offset, 0)
        pos = min(pos, self.GetLength())
        self.GotoPos(pos)
        self.ChooseCaretX()

    def OnAutoCompSel(self, evt):
        """Handle when an item is inserted from the autocomp list"""
        text = evt.GetText()
        cpos = evt.GetPosition()
        self._code['compsvc'].OnCompletionInserted(cpos, text)

    def OnChanged(self, evt):
        """Handles updates that need to take place after
        the control has been modified.
        @param evt: stc.StyledTextEvent

        """
        if self._line_num:
            # Adjust line number margin width to expand as needed when line
            # number width over fills the area.
            lines = self.GetLineCount()
            mwidth = self.GetTextExtent(str(lines))[0]

            adj = 8
            if wx.Platform == '__WXMAC__':
                adj = 2

            nwidth = max(15, mwidth + adj)
            if self.GetMarginWidth(NUM_MARGIN) != nwidth:
                self.SetMarginWidth(NUM_MARGIN, nwidth)

        wx.PostEvent(self.GetParent(), evt)
#         ed_msg.PostMessage(ed_msg.EDMSG_UI_STC_CHANGED, context=self)

    def OnModified(self, evt):
        """Handle modify events, includes style changes!"""
        if self.VertEdit.Enabled:
            self.VertEdit.OnModified(evt)
        else:
            evt.Skip()

    def OnStyleNeeded(self, evt):
        """Perform custom styling when registered for a container lexer"""
        if self._code['clexer'] is not None:
            self._code['clexer'](self, self.GetEndStyled(), evt.GetPosition())
        else:
            evt.Skip()

    def PutText(self, text):
        """Put text in the buffer. Like AddText but does the right thing
        depending upon the input mode and buffer state.
        @param text: string

        """
        if not self.HasSelection():
            cpos = self.GetCurrentPos()
            lepos = self.GetLineEndPosition(self.GetCurrentLine())
            if self.GetOvertype() and cpos != lepos:
                self.CharRight()
                self.DeleteBack()
            self.AddText(text)
        else:
            self.ReplaceSelection(text)

    def RegisterImages(self):
        """Register the images for the autocomp popup list"""
        pass
#         images = [(autocomp.TYPE_FUNCTION, ID_FUNCT_TYPE),
#                   (autocomp.TYPE_METHOD, ID_METHOD_TYPE),
#                   (autocomp.TYPE_PROPERTY, ID_PROPERTY_TYPE),
#                   (autocomp.TYPE_ATTRIBUTE, ID_ATTR_TYPE),
#                   (autocomp.TYPE_CLASS, ID_CLASS_TYPE),
#                   (autocomp.TYPE_VARIABLE, ID_VARIABLE_TYPE),
#                   (autocomp.TYPE_ELEMENT, ID_ELEM_TYPE)]
#         for idx, img in images:
#             bmp = wx.ArtProvider.GetBitmap(str(img), wx.ART_MENU)
#             if bmp.IsOk():
#                 self.RegisterImage(idx, bmp)

    def SearchText(self, text, regex=False, back=False):
        """Search for text forward or backward
        @param text: string
        @keyword regex: bool
        @keyword back: bool

        """
        flags = stc.STC_FIND_MATCHCASE
        if regex:
            flags = flags | stc.STC_FIND_REGEXP

        self.SearchAnchor()
        if not back:
            # Search forward
            res = self.SearchNext(flags, text)
            if res == -1:
                # Nothing found, search from top
                self.DocumentStart()
                self.SearchAnchor()
                res = self.SearchNext(flags, text)
        else:
            # Search backward
            res = self.SearchPrev(flags, text)
            if res == -1:
                # Nothing found, search from bottom
                self.DocumentEnd()
                self.SearchAnchor()
                res = self.SearchPrev(flags, text)
        return res  # returns -1 if nothing found even after wrapping around

    def SetDocument(self, doc):
        """Change the document object used.
        @param doc: an L{ed_txt.EdFile} instance

        """
        del self.file
        self.file = doc

    def SetEncoding(self, enc):
        """Sets the encoding of the document
        @param enc: encoding to set for document

        """
        self.file.SetEncoding(enc)

    def GetEncoding(self):
        """Get the document objects encoding
        @return: string

        """ 
        return self.file.GetEncoding()

    def SetFileName(self, path):
        """Set the buffers filename attributes from the given path"""
        self.file.SetPath(path)

    def SetKeyWords(self, kw_lst):
        """Sets the keywords from a list of keyword sets
        @param kw_lst: [ (KWLVL, "KEWORDS"), (KWLVL2, "KEYWORDS2"), ect...]

        """
        # Parse Keyword Settings List simply ignoring bad values and badly
        # formed lists
        self._code['keywords'] = list()
        kwlist = ""
        for keyw in kw_lst:
            if len(keyw) != 2:
                continue
            else:
                if not isinstance(keyw[0], int) or \
                   not isinstance(keyw[1], str):
                    continue
                else:
                    kwlist += keyw[1]
                    super().SetKeyWords(keyw[0], keyw[1])

        # Can't have ? in scintilla autocomp list unless specifying an image
        # TODO: this should be handled by the autocomp service
        if '?' in kwlist:
            kwlist.replace('?', '')

        kwlist = kwlist.split()  # Split into a list of words
        kwlist = list(set(kwlist))  # Remove duplicates from the list
        kwlist.sort()  # Sort into alphabetical order

        self._code['keywords'] = kwlist

    def SetLexer(self, lexer):
        """Set the buffers lexer
        @param lexer: lexer to use
        @note: Overrides StyledTextCtrl.SetLexer

        """
        if lexer == stc.STC_LEX_CONTAINER:
            # If setting a container lexer only bind the event if it hasn't
            # been done yet.
            if self._code['clexer'] is None:
                self.Bind(stc.EVT_STC_STYLENEEDED, self.OnStyleNeeded)
        else:
            # If changing from a container lexer to a non container
            # lexer we need to unbind the event.
            if self._code['clexer'] is not None:
                self.Unbind(stc.EVT_STC_STYLENEEDED)
                self._code['clexer'] = None

        super().SetLexer(lexer)

    def SetModTime(self, modtime):
        """Set the value of the files last modtime"""
        self.file.SetModTime(modtime)

    def SetProperties(self, prop_lst):
        """Sets the Lexer Properties from a list of specifications
        @param prop_lst: [ ("PROPERTY", "VAL"), ("PROPERTY2", "VAL2) ]

        """
        # Parses Property list, ignoring all bad values
        for prop in prop_lst:
            if len(prop) != 2:
                continue
            else:
                if not isinstance(prop[0], str) or not \
                   isinstance(prop[1], str):
                    continue
                else:
                    self.SetProperty(prop[0], prop[1])
        return True

    def BaseSetSelection(self, start, end):
        """Call base STC SetSelection method, for use with internal utf-8
        indexes in use by derived classes, STC hell...

        """
        super().SetSelection(start, end)

    def SetSelection(self, start, end):
        """Override base method to make it work correctly using
        Unicode character positions instead of UTF-8.

        """
        # STC HELL - some methods require UTF-8 offsets while others work
        #            with Unicode...
        # Calculate UTF-8 offsets in buffer
        unicode_txt = self.GetText()
#         if start != 0:
#             start = len(ed_txt.EncodeString(unicode_txt[0:start], 'utf-8'))
#         if end != 0:
#             end = len(ed_txt.EncodeString(unicode_txt[0:end], 'utf-8'))
        del unicode_txt
        super().SetSelection(start, end)

    def GetSelection(self):
        """Get the selection positions in Unicode instead of UTF-8"""
        # STC HELL
        # Translate the UTF8 byte offsets to unicode
        start, end = super().GetSelection()
        utf8_txt = self.GetText()
        del utf8_txt
        return start, end

    def ShowAutoCompOpt(self, command):
        """Shows the autocompletion options list for the command
        @param command: command to look for autocomp options for

        """
        pos = self.GetCurrentPos()
        # symList is a list(completer.Symbol)
        symList = self._code['compsvc'].GetAutoCompList(command)
        
        # Build a list that can be feed to Scintilla
#         lst = map(unicode, symList)
#         if lst is not None and len(lst):
#             self.BeginUndoAction()
#             lst = u' '.join(lst)
#             if lst.isspace():
#                 return
#             self.AutoCompShow(pos - self.WordStartPosition(pos, True), lst)
# 
#             # Check if something was inserted due to there only being a 
#             # single choice returned from the completer and allow the completer
#             # to adjust caret position as necessary.
#             curpos = self.GetCurrentPos()
#             if curpos != pos:
#                 text = self.GetTextRange(pos, curpos)
#                 self._code['compsvc'].OnCompletionInserted(pos, text)
#             self.EndUndoAction()
#             self.SetFocus()

    def GetViewWhiteSpace(self):
        """Get if view whitespace is turned on
        @return: bool

        """
        val = super().GetViewWhiteSpace()
        return val != stc.STC_WS_INVISIBLE

    def SetViewWhiteSpace(self, viewws):
        """Overrides base method to make it a simple bool toggle"""
        if viewws:
            val = stc.STC_WS_VISIBLEALWAYS
        else:
            val = stc.STC_WS_INVISIBLE
        super().SetViewWhiteSpace(val)

    def GetWrapMode(self):
        """Get if word wrap is turned on
        @return: bool

        """
        val = super().GetWrapMode()
        return val != stc.STC_WRAP_NONE

    def SetWrapMode(self, wrap):
        """Overrides base method to make it a simple toggle operation
        @param wrap: bool

        """
        if wrap:
            val = stc.STC_WRAP_WORD
        else:
            val = stc.STC_WRAP_NONE
        super().SetWrapMode(val)

    def ShowCallTip(self, command):
        """Shows call tip for given command
        @param command: command to  look for calltips for

        """
        self.CallTipCancel()

        tip = self._code['compsvc'].GetCallTip(command)
        if len(tip):
            curr_pos = self.GetCurrentPos()
            tip_pos = curr_pos - (len(command.split('.')[-1]) + 1)
            fail_safe = curr_pos - self.GetColumn(curr_pos)
            self.CallTipShow(max(tip_pos, fail_safe), tip)

    def ToggleColumnMode(self):
        """Toggle the column edit mode"""
        self.VertEdit.enable(not self.VertEdit.Enabled)

    def ToggleComment(self):
        """Toggle the comment of the selected region"""
        if len(self._code['comment']):
            sel = self.GetSelection()
            start = self.LineFromPosition(sel[0])
            end = self.LineFromPosition(sel[1])
            c_start = self._code['comment'][0]

            if end > start and self.GetColumn(sel[1]) == 0:
                end = end - 1

            # Analyze the selected line(s)
            comment = 0
            for line in range(start, end + 1):
                txt = self.GetLine(line)
                if txt.lstrip().startswith(c_start):
                    comment += 1

            lcount = end - start
            mod = 1
            if lcount == 0:
                mod = 0

            if comment > (lcount / 2) + mod:
                # Uncomment
                self.Comment(start, end, True)
            else:
                self.Comment(start, end, False)

    def ToggleLineNumbers(self, switch=None):
        """Toggles the visibility of the line number margin
        @keyword switch: force a particular setting

        """
        if (switch is None and \
            not self.GetMarginWidth(NUM_MARGIN)) or switch:
            self.EnableLineNumbers(True)
        else:
            self.EnableLineNumbers(False)

    @property
    def VertEdit(self):
        """Vertical edit mode accessor."""
        return self.vert_edit

    #---- Style Function Definitions ----#

    def RefreshStyles(self):
        """Refreshes the colorization of the window by reloading any
        style tags that may have been modified.
        @postcondition: all style settings are refreshed in the control

        """
        with Freezer(self) as _tmp:
            self.StyleClearAll()
            self.SetSyntax(self.GetSyntaxParams())
            self.DefineMarkers()
        self.Refresh()

    def UpdateBaseStyles(self):
        """Update the controls basic styles"""
        super().UpdateBaseStyles()

        # Set control specific styles
        sback = self.GetItemByName('select_style')
        if not sback.IsNull():
            sback = sback.GetBack()
        else:
            sback = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
        self.VertEdit.SetBlockColor(sback)
        self.DefineMarkers()
#-----------------------------------------------------------------------------#


def _GetMacKeyBindings():
    """Returns a list of 3-element tuples defining the standard key
    bindings for Mac text editors -- i.e., the behavior of option-arrow,
    shift-delete, and so on.

    @return: list of (key code, modifier keys, STC action)

    """
    # A good reference for these: http://www.yellowbrain.com/stc/keymap.html
    return [
            # Move/select/delete by word
            (stc.STC_KEY_LEFT, stc.STC_SCMOD_ALT,
             stc.STC_CMD_WORDLEFT),
            (stc.STC_KEY_RIGHT, stc.STC_SCMOD_ALT,
             stc.STC_CMD_WORDRIGHT),
            (stc.STC_KEY_LEFT, ALT_SHIFT, stc.STC_CMD_WORDLEFTEXTEND),
            (stc.STC_KEY_RIGHT, ALT_SHIFT, stc.STC_CMD_WORDRIGHTEXTEND),
            (stc.STC_KEY_BACK, stc.STC_SCMOD_ALT,
             stc.STC_CMD_DELWORDLEFT),
            (stc.STC_KEY_DELETE, stc.STC_SCMOD_ALT,
             stc.STC_CMD_DELWORDRIGHT),
            (stc.STC_KEY_BACK, ALT_SHIFT, stc.STC_CMD_DELWORDRIGHT),
            (stc.STC_KEY_DELETE, ALT_SHIFT, stc.STC_CMD_DELWORDLEFT),

            # Move/select/delete by line
            (stc.STC_KEY_LEFT, stc.STC_SCMOD_CTRL,
             stc.STC_CMD_VCHOME),
            (stc.STC_KEY_LEFT, CTRL_SHIFT, stc.STC_CMD_VCHOMEEXTEND),
            (stc.STC_KEY_RIGHT, stc.STC_SCMOD_CTRL,
             stc.STC_CMD_LINEEND),
            (stc.STC_KEY_RIGHT, CTRL_SHIFT, stc.STC_CMD_LINEENDEXTEND),
            (stc.STC_KEY_BACK, stc.STC_SCMOD_CTRL,
             stc.STC_CMD_DELLINELEFT),
            (stc.STC_KEY_DELETE, stc.STC_SCMOD_CTRL,
             stc.STC_CMD_DELLINERIGHT),
            (stc.STC_KEY_BACK, CTRL_SHIFT, stc.STC_CMD_DELLINERIGHT),
            (stc.STC_KEY_DELETE, CTRL_SHIFT, stc.STC_CMD_DELLINELEFT),

            # By-character deletion behavior
            (stc.STC_KEY_BACK, stc.STC_SCMOD_NORM,
             stc.STC_CMD_DELETEBACK),
            (stc.STC_KEY_DELETE, stc.STC_SCMOD_SHIFT,
             stc.STC_CMD_DELETEBACK),

            # NOTE: The following two are a special case, since Scintilla
            # doesn't have a forward-delete action.  So here we just cancel any
            # tip our auto-completion display, and then implement forward
            # delete in OnKeyDown.
            # (stc.STC_KEY_DELETE, 0, stc.STC_CMD_CANCEL),
            (stc.STC_KEY_BACK, stc.STC_SCMOD_SHIFT,
             stc.STC_CMD_CANCEL),
            ]
