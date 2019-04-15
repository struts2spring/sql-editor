
import wx
import wx.richtext as rt
# import images
import os
# from StringIO import StringIO
# from src.view.views.calibre.book.browser.images import images
from src.view.views.calibre.book.browser.SearchBook import FindingBook
import logging
from _io import StringIO
from src.view.util.FileOperationsUtil import FileOperations

logger = logging.getLogger('extensive')


# import lxml
# import lxml.html
#----------------------------------------------------------------------
class Window(wx.App):

    def __init__(self, book=None):
        wx.App.__init__(self)
        self.init_ui(book=book)
        self.mainWindow.Show()

    def init_ui(self, book=None):
        self.mainWindow = wx.Frame(None)
        self.mainWindow.SetSize((800, 510))
#         self.vbox1 = wx.BoxSizer(wx.VERTICAL)
        panel = RichTextPanel(self.mainWindow, book)
#         panel.SetSizer(self.vbox1)
#         panel.SetSizer(sizer)
#         panel.Layout()


# html_content = '''
# <html>
#     <head></head>
#     <body>
#         <font face="Ubuntu" size="3" color="#4C4C4C">
#             <p align="center"><font face="Ubuntu" size="3" color="#4C4C4C"><b>asfd </b><b><i>asdf  s</i></b><b><i><u>tream.getvalue()</u></i></b></font></p>
#         </font>
#     </body>
# </html>
# 
# '''       
class RichTextPanel(wx.Panel):

    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent

#         self.MakeMenuBar()
        self.tbar = self.MakeToolBar()
#         self.CreateStatusBar()
#         self.SetStatusText("Welcome to wx.richtext.RichTextCtrl!")

        self.rtc = rt.RichTextCtrl(self, -1, style=wx.VSCROLL | wx.HSCROLL | wx.NO_BORDER);
#         handler = rt.RichTextHTMLHandler()
        wx.CallAfter(self.rtc.SetFocus)

#         self.rtc.Freeze()
#         self.rtc.BeginSuppressUndo()
# 
#         self.rtc.EndSuppressUndo()
#         self.rtc.Thaw()
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.tbar, 0, wx.EXPAND | wx.ALL, 1)
        sizer.Add(self.rtc, 1, wx.EXPAND | wx.ALL, 1)
#         sizer.Add(save_button, 1, wx.EXPAND | wx.ALL, 1)
 
        self.SetSizer(sizer)
        self.book = args[0]
        self.loadFile()
#         self.Show()
    
    def loadFile(self):
#         path = os.path.join('/docs/github/Opal/src/ui/view/opalview', 'bookInfo.html')

        out = StringIO()
        htmlhandler = rt.RichTextHTMLHandler()
        buffer = self.rtc.GetBuffer()
#         htmlhandler.SetFlags(rt.RICHTEXT_HANDLER_SAVE_IMAGES_TO_MEMORY)
        htmlhandler.SetFontSizeMapping([7, 9, 11, 12, 14, 22, 100])
        logger.debug('canload: %s', htmlhandler.CanLoad())
        logger.debug('cansave: %s', htmlhandler.CanSave())
        logger.debug('CanHandle: %s', htmlhandler.CanHandle('bookInfo.html'))
        rt.RichTextBuffer.AddHandler(htmlhandler)
#         buffer.AddHandler(htmlhandler)
        try:
            if self.book != None:
                out.write(self.book.bookDescription)
            out.seek(0)
        except Exception as e:
            logger.error(e)
#         htmlhandler.LoadStream(buffer, out)
#         htmlhandler.LoadFile(path,'text')
        if self.book != None and self.book.bookDescription != None:
            self.rtc.AppendText(self.book.bookDescription)
#         htmlhandler.LoadStream(buffer, out.getvalue())
        self.rtc.Refresh()
#         buffer = self.rtc.GetBuffer()
        # you have to specify the type of data to load and the control
        # must already have an instance of the handler to parse it
#         buffer.LoadStream(stream, rt.RICHTEXT_TYPE_HTML)
        
#         self.rtc.Refresh()
#         self.rtc.LoadFile(path,  type=1)
            
    def OnFileSave(self, evt):
#         self.loadFile()
        self.GetParent().save()
        
#         handler = rt.RichTextHTMLHandler()
#         handler.SetFlags(rt.RICHTEXT_HANDLER_SAVE_IMAGES_TO_MEMORY)
#         handler.SetFontSizeMapping([7, 9, 11, 12, 14, 22, 100])
# 
#         import cStringIO
#         stream = cStringIO.StringIO()
#         if not handler.SaveStream(self.rtc.GetBuffer(), stream):
#             return
#         html_content = stream.getvalue()
#         print html_content

    def SetFontStyle(self, fontColor=None, fontBgColor=None, fontFace=None, fontSize=None,
                     fontBold=None, fontItalic=None, fontUnderline=None):
        if fontColor:
            self.textAttr.SetTextColour(fontColor)
        if fontBgColor:
            self.textAttr.SetBackgroundColour(fontBgColor)
        if fontFace:
            self.textAttr.SetFontFaceName(fontFace)
        if fontSize:
            self.textAttr.SetFontSize(fontSize)
        if fontBold != None:
            if fontBold:
                self.textAttr.SetFontWeight(wx.FONTWEIGHT_BOLD)
            else:
                self.textAttr.SetFontWeight(wx.FONTWEIGHT_NORMAL)
        if fontItalic != None:
            if fontItalic:
                self.textAttr.SetFontStyle(wx.FONTSTYLE_ITALIC)
            else:
                self.textAttr.SetFontStyle(wx.FONTSTYLE_NORMAL)
        if fontUnderline != None:
            if fontUnderline:
                self.textAttr.SetFontUnderlined(True)
            else:
                self.textAttr.SetFontUnderlined(False)
        self.rtc.SetDefaultStyle(self.textAttr)

    def OnURL(self, evt):
        wx.MessageBox(evt.GetString(), "URL Clicked")

    def OnFileOpen(self, evt):
        # This gives us a string suitable for the file dialog based on
        # the file handlers that are loaded
        wildcard, types = rt.RichTextBuffer.GetExtWildcard(save=False)
        dlg = wx.FileDialog(self, "Choose a filename",
                            wildcard=wildcard,
                            )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if path:
                fileType = types[dlg.GetFilterIndex()]
                self.rtc.LoadFile(path, fileType)
        dlg.Destroy()
        
# 
#         if not self.rtc.GetFilename():
#             self.OnFileSaveAs(evt)
#             return
#         self.rtc.SaveFile()
        
    def OnFileSaveAs(self, evt):
        wildcard, types = rt.RichTextBuffer.GetExtWildcard(save=True)

        dlg = wx.FileDialog(self, "Choose a filename",
                            wildcard=wildcard,
                           )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if path:
                fileType = types[dlg.GetFilterIndex()]
                ext = rt.RichTextBuffer.FindHandlerByType(fileType).GetExtension()
                if not path.endswith(ext):
                    path += '.' + ext
                self.rtc.SaveFile(path, fileType)
        dlg.Destroy()
                
    def OnFileViewHTML(self, evt):
        # Get an instance of the html file handler, use it to save the
        # document to a StringIO stream, and then display the
        # resulting html text in a dialog with a HtmlWindow.
        handler = rt.RichTextHTMLHandler()
        handler.SetFlags(rt.RICHTEXT_HANDLER_SAVE_IMAGES_TO_MEMORY)
        handler.SetFontSizeMapping([7, 9, 11, 12, 14, 22, 100])

        import cStringIO
        stream = cStringIO()
        if not handler.SaveStream(self.rtc.GetBuffer(), stream):
            return

        import wx.html
        dlg = wx.Dialog(self, title="HTML", style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        html = wx.html.HtmlWindow(dlg, size=(500, 400), style=wx.BORDER_SUNKEN)
        html.SetPage(stream.getvalue())
        btn = wx.Button(dlg, wx.ID_CANCEL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.ALL | wx.EXPAND, 5)
        sizer.Add(btn, 0, wx.ALL | wx.CENTER, 10)
        dlg.SetSizer(sizer)
        sizer.Fit(dlg)

        dlg.ShowModal()

        handler.DeleteTemporaryImages()
    
    def OnFileExit(self, evt):
        self.Close(True)
      
    def OnBold(self, evt):
        self.rtc.ApplyBoldToSelection()
        
    def OnItalic(self, evt): 
        self.rtc.ApplyItalicToSelection()
        
    def OnUnderline(self, evt):
        self.rtc.ApplyUnderlineToSelection()
        
    def OnAlignLeft(self, evt):
        self.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_LEFT)
        
    def OnAlignRight(self, evt):
        self.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_RIGHT)
        
    def OnAlignCenter(self, evt):
        self.rtc.ApplyAlignmentToSelection(wx.TEXT_ALIGNMENT_CENTRE)
        
    def OnIndentMore(self, evt):
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetLeftIndent(attr.GetLeftIndent() + 100)
            attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
            self.rtc.SetStyle(r, attr)
        
    def OnIndentLess(self, evt):
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

        if attr.GetLeftIndent() >= 100:
            attr.SetLeftIndent(attr.GetLeftIndent() - 100)
            attr.SetFlags(wx.TEXT_ATTR_LEFT_INDENT)
            self.rtc.SetStyle(r, attr)
        
    def OnParagraphSpacingMore(self, evt):
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetParagraphSpacingAfter(attr.GetParagraphSpacingAfter() + 20);
            attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
            self.rtc.SetStyle(r, attr)
        
    def OnParagraphSpacingLess(self, evt):
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            if attr.GetParagraphSpacingAfter() >= 20:
                attr.SetParagraphSpacingAfter(attr.GetParagraphSpacingAfter() - 20);
                attr.SetFlags(wx.TEXT_ATTR_PARA_SPACING_AFTER)
                self.rtc.SetStyle(r, attr)
        
    def OnLineSpacingSingle(self, evt): 
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(10)
            self.rtc.SetStyle(r, attr)
                
    def OnLineSpacingHalf(self, evt):
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(15)
            self.rtc.SetStyle(r, attr)
        
    def OnLineSpacingDouble(self, evt):
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
        ip = self.rtc.GetInsertionPoint()
        if self.rtc.GetStyle(ip, attr):
            r = rt.RichTextRange(ip, ip)
            if self.rtc.HasSelection():
                r = self.rtc.GetSelectionRange()

            attr.SetFlags(wx.TEXT_ATTR_LINE_SPACING)
            attr.SetLineSpacing(20)
            self.rtc.SetStyle(r, attr)

    def OnFont(self, evt):
        if not self.rtc.HasSelection():
            return

        r = self.rtc.GetSelectionRange()
        fontData = wx.FontData()
        fontData.EnableEffects(False)
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_FONT)
        if self.rtc.GetStyle(self.rtc.GetInsertionPoint(), attr):
            fontData.SetInitialFont(attr.GetFont())

        dlg = wx.FontDialog(self, fontData)
        if dlg.ShowModal() == wx.ID_OK:
            fontData = dlg.GetFontData()
            font = fontData.GetChosenFont()
            if font:
                attr.SetFlags(wx.TEXT_ATTR_FONT)
                attr.SetFont(font)
                self.rtc.SetStyle(r, attr)
        dlg.Destroy()

    def OnColour(self, evt):
        colourData = wx.ColourData()
        attr = wx.TextAttr()
        attr.SetFlags(wx.TEXT_ATTR_TEXT_COLOUR)
        if self.rtc.GetStyle(self.rtc.GetInsertionPoint(), attr):
            colourData.SetColour(attr.GetTextColour())

        dlg = wx.ColourDialog(self, colourData)
        if dlg.ShowModal() == wx.ID_OK:
            colourData = dlg.GetColourData()
            colour = colourData.GetColour()
            if colour:
                if not self.rtc.HasSelection():
                    self.rtc.BeginTextColour(colour)
                else:
                    r = self.rtc.GetSelectionRange()
                    attr.SetFlags(wx.TEXT_ATTR_TEXT_COLOUR)
                    attr.SetTextColour(colour)
                    self.rtc.SetStyle(r, attr)
        dlg.Destroy()

    def OnUpdateBold(self, evt):
        evt.Check(self.rtc.IsSelectionBold())
    
    def OnUpdateItalic(self, evt): 
        evt.Check(self.rtc.IsSelectionItalics())
    
    def OnUpdateUnderline(self, evt): 
        evt.Check(self.rtc.IsSelectionUnderlined())
    
    def OnUpdateAlignLeft(self, evt):
        evt.Check(self.rtc.IsSelectionAligned(wx.TEXT_ALIGNMENT_LEFT))
        
    def OnUpdateAlignCenter(self, evt):
        evt.Check(self.rtc.IsSelectionAligned(wx.TEXT_ALIGNMENT_CENTRE))
        
    def OnUpdateAlignRight(self, evt):
        evt.Check(self.rtc.IsSelectionAligned(wx.TEXT_ALIGNMENT_RIGHT))
    
    def ForwardEvent(self, evt):
        # The RichTextCtrl can handle menu and update events for undo,
        # redo, cut, copy, paste, delete, and select all, so just
        # forward the event to it.
        self.rtc.ProcessEvent(evt)

#     def MakeMenuBar(self):
# 
#         def doBind(item, handler, updateUI=None):
#             self.Bind(wx.EVT_MENU, handler, item)
#             if updateUI is not None:
#                 self.Bind(wx.EVT_UPDATE_UI, updateUI, item)
#             
#         fileMenu = wx.Menu()
#         doBind(fileMenu.Append(-1, "&Open\tCtrl+O", "Open a file"),
#                 self.OnFileOpen)
#         doBind(fileMenu.Append(-1, "&Save\tCtrl+S", "Save a file"),
#                 self.OnFileSave)
#         doBind(fileMenu.Append(-1, "&Save As...\tF12", "Save to a new file"),
#                 self.OnFileSaveAs)
#         fileMenu.AppendSeparator()
#         doBind(fileMenu.Append(-1, "&View as HTML", "View HTML"),
#                 self.OnFileViewHTML)
#         fileMenu.AppendSeparator()
#         doBind(fileMenu.Append(-1, "E&xit\tCtrl+Q", "Quit this program"),
#                 self.OnFileExit)
#         
#         editMenu = wx.Menu()
#         doBind(editMenu.Append(wx.ID_UNDO, "&Undo\tCtrl+Z"),
#                 self.ForwardEvent, self.ForwardEvent)
#         doBind(editMenu.Append(wx.ID_REDO, "&Redo\tCtrl+Y"),
#                 self.ForwardEvent, self.ForwardEvent)
#         editMenu.AppendSeparator()
#         doBind(editMenu.Append(wx.ID_CUT, "Cu&t\tCtrl+X"),
#                 self.ForwardEvent, self.ForwardEvent)
#         doBind(editMenu.Append(wx.ID_COPY, "&Copy\tCtrl+C"),
#                 self.ForwardEvent, self.ForwardEvent)
#         doBind(editMenu.Append(wx.ID_PASTE, "&Paste\tCtrl+V"),
#                 self.ForwardEvent, self.ForwardEvent)
#         doBind(editMenu.Append(wx.ID_CLEAR, "&Delete\tDel"),
#                 self.ForwardEvent, self.ForwardEvent)
#         editMenu.AppendSeparator()
#         doBind(editMenu.Append(wx.ID_SELECTALL, "Select A&ll\tCtrl+A"),
#                 self.ForwardEvent, self.ForwardEvent)
#         
#         # doBind( editMenu.AppendSeparator(),  )
#         # doBind( editMenu.Append(-1, "&Find...\tCtrl+F"),  )
#         # doBind( editMenu.Append(-1, "&Replace...\tCtrl+R"),  )
# 
#         formatMenu = wx.Menu()
#         doBind(formatMenu.AppendCheckItem(-1, "&Bold\tCtrl+B"),
#                 self.OnBold, self.OnUpdateBold)
#         doBind(formatMenu.AppendCheckItem(-1, "&Italic\tCtrl+I"),
#                 self.OnItalic, self.OnUpdateItalic)
#         doBind(formatMenu.AppendCheckItem(-1, "&Underline\tCtrl+U"),
#                 self.OnUnderline, self.OnUpdateUnderline)
#         formatMenu.AppendSeparator()
#         doBind(formatMenu.AppendCheckItem(-1, "L&eft Align"),
#                 self.OnAlignLeft, self.OnUpdateAlignLeft)
#         doBind(formatMenu.AppendCheckItem(-1, "&Centre"),
#                 self.OnAlignCenter, self.OnUpdateAlignCenter)
#         doBind(formatMenu.AppendCheckItem(-1, "&Right Align"),
#                 self.OnAlignRight, self.OnUpdateAlignRight)
#         formatMenu.AppendSeparator()
#         doBind(formatMenu.Append(-1, "Indent &More"), self.OnIndentMore)
#         doBind(formatMenu.Append(-1, "Indent &Less"), self.OnIndentLess)
#         formatMenu.AppendSeparator()
#         doBind(formatMenu.Append(-1, "Increase Paragraph &Spacing"), self.OnParagraphSpacingMore)
#         doBind(formatMenu.Append(-1, "Decrease &Paragraph Spacing"), self.OnParagraphSpacingLess)
#         formatMenu.AppendSeparator()
#         doBind(formatMenu.Append(-1, "Normal Line Spacing"), self.OnLineSpacingSingle)
#         doBind(formatMenu.Append(-1, "1.5 Line Spacing"), self.OnLineSpacingHalf)
#         doBind(formatMenu.Append(-1, "Double Line Spacing"), self.OnLineSpacingDouble)
#         formatMenu.AppendSeparator()
#         doBind(formatMenu.Append(-1, "&Font..."), self.OnFont)
#         
#         mb = wx.MenuBar()
#         mb.Append(fileMenu, "&File")
#         mb.Append(editMenu, "&Edit")
#         mb.Append(formatMenu, "F&ormat")
#         self.SetMenuBar(mb)

    def MakeToolBar(self):

        def doBind(item, handler, updateUI=None):
            self.Bind(wx.EVT_TOOL, handler, item)
            if updateUI is not None:
                self.Bind(wx.EVT_UPDATE_UI, updateUI, item)

        self.fileOperations = FileOperations()
        tbar = wx.ToolBar(self, style=wx.TB_FLAT)
        doBind(tbar.AddTool(-1, "Open", self.fileOperations.getImageBitmap(imageName='eclipse_folder.png'), "Open"), self.OnFileOpen)
        doBind(tbar.AddTool(-1, "Save", self.fileOperations.getImageBitmap(imageName='save.png'), "Save"), self.OnFileSave)
        tbar.AddSeparator()
        doBind(tbar.AddTool(wx.ID_CUT, "Cut", self.fileOperations.getImageBitmap(imageName='cut_edit.png')), self.ForwardEvent, self.ForwardEvent)
        doBind(tbar.AddTool(wx.ID_COPY, "Copy", self.fileOperations.getImageBitmap(imageName='copy_edit_co.png')), self.ForwardEvent, self.ForwardEvent)
        doBind(tbar.AddTool(wx.ID_PASTE, "Paste", self.fileOperations.getImageBitmap(imageName='paste_edit.png')), self.ForwardEvent, self.ForwardEvent)
#         doBind(tbar.AddTool(wx.ID_COPY, images._rt_copy.GetBitmap(), shortHelpString="Copy"), self.ForwardEvent, self.ForwardEvent)
#         doBind(tbar.AddTool(wx.ID_PASTE, images._rt_paste.GetBitmap(), shortHelpString="Paste"), self.ForwardEvent, self.ForwardEvent)
        tbar.AddSeparator()
        doBind(tbar.AddTool(wx.ID_UNDO, "Undo", self.fileOperations.getImageBitmap(imageName='undo_edit.png')), self.ForwardEvent, self.ForwardEvent)
        doBind(tbar.AddTool(wx.ID_REDO, "Redo", self.fileOperations.getImageBitmap(imageName='redo_edit.png')), self.ForwardEvent, self.ForwardEvent)
#         doBind(tbar.AddTool(wx.ID_UNDO, images._rt_undo.GetBitmap(), shortHelpString="Undo"), self.ForwardEvent, self.ForwardEvent)
#         doBind(tbar.AddTool(wx.ID_REDO, images._rt_redo.GetBitmap(), shortHelpString="Redo"), self.ForwardEvent, self.ForwardEvent)
        tbar.AddSeparator()
        doBind(tbar.AddTool(-1, "Bold", self.fileOperations.getImageBitmap(imageName='redo_edit.png')), self.OnBold, self.OnUpdateBold)
        doBind(tbar.AddTool(-1, "Italic", self.fileOperations.getImageBitmap(imageName='redo_edit.png')), self.OnItalic, self.OnUpdateItalic)
        doBind(tbar.AddTool(-1, "Underline", self.fileOperations.getImageBitmap(imageName='redo_edit.png')), self.OnUnderline, self.OnUpdateUnderline)
#         doBind(tbar.AddTool(-1, images._rt_bold.GetBitmap(), isToggle=True, shortHelpString="Bold"), self.OnBold, self.OnUpdateBold)
#         doBind(tbar.AddTool(-1, images._rt_italic.GetBitmap(), isToggle=True, shortHelpString="Italic"), self.OnItalic, self.OnUpdateItalic)
#         doBind(tbar.AddTool(-1, images._rt_underline.GetBitmap(), isToggle=True, shortHelpString="Underline"), self.OnUnderline, self.OnUpdateUnderline)
        tbar.AddSeparator()
        doBind(tbar.AddTool(-1, "Align Left", self.fileOperations.getImageBitmap(imageName='redo_edit.png')), self.OnAlignLeft, self.OnUpdateAlignLeft)
        doBind(tbar.AddTool(-1, "Center", self.fileOperations.getImageBitmap(imageName='redo_edit.png')), self.OnAlignCenter, self.OnUpdateAlignCenter)
        doBind(tbar.AddTool(-1, "Align Right", self.fileOperations.getImageBitmap(imageName='redo_edit.png')), self.OnAlignRight, self.OnUpdateAlignRight)
#         doBind(tbar.AddTool(-1, images._rt_alignleft.GetBitmap(), isToggle=True, shortHelpString="Align Left"), self.OnAlignLeft, self.OnUpdateAlignLeft)
#         doBind(tbar.AddTool(-1, images._rt_centre.GetBitmap(), isToggle=True, shortHelpString="Center"), self.OnAlignCenter, self.OnUpdateAlignCenter)
#         doBind(tbar.AddTool(-1, images._rt_alignright.GetBitmap(), isToggle=True, shortHelpString="Align Right"), self.OnAlignRight, self.OnUpdateAlignRight)
        tbar.AddSeparator()
        doBind(tbar.AddTool(-1, "Indent Less", self.fileOperations.getImageBitmap(imageName='redo_edit.png')), self.OnIndentLess)
        doBind(tbar.AddTool(-1, "Indent More", self.fileOperations.getImageBitmap(imageName='redo_edit.png')), self.OnIndentMore)
#         doBind(tbar.AddTool(-1, images._rt_indentless.GetBitmap(), shortHelpString="Indent Less"), self.OnIndentLess)
#         doBind(tbar.AddTool(-1, images._rt_indentmore.GetBitmap(), shortHelpString="Indent More"), self.OnIndentMore)
        tbar.AddSeparator()
        doBind(tbar.AddTool(-1, "Font", self.fileOperations.getImageBitmap(imageName='redo_edit.png')), self.OnFont)
        doBind(tbar.AddTool(-1, "Font Colour", self.fileOperations.getImageBitmap(imageName='redo_edit.png')), self.OnColour)
#         doBind(tbar.AddTool(-1, images._rt_font.GetBitmap(), shortHelpString="Font"), self.OnFont)
#         doBind(tbar.AddTool(-1, images._rt_colour.GetBitmap(), shortHelpString="Font Colour"), self.OnColour)

        tbar.Realize()
        return tbar

#----------------------------------------------------------------------


class TestPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, "Show the RichTextCtrl sample", (50, 50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)

        self.AddRTCHandlers()

    def AddRTCHandlers(self):
        # make sure we haven't already added them.
        if rt.RichTextBuffer.FindHandlerByType(rt.RICHTEXT_TYPE_HTML) is not None:
            return
        
        # This would normally go in your app's OnInit method.  I'm
        # not sure why these file handlers are not loaded by
        # default by the C++ richtext code, I guess it's so you
        # can change the name or extension if you wanted...
        rt.RichTextBuffer.AddHandler(rt.RichTextHTMLHandler())
        rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler())

        # ...like this
        rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler(name="Other XML",
                                                           ext="ox",
                                                           type=99))

        # This is needed for the view as HTML option since we tell it
        # to store the images in the memory file system.
        wx.FileSystem.AddHandler(wx.MemoryFSHandler())

#     def OnButton(self, evt):
#         win = RichTextFrame(self, -1, "wx.richtext.RichTextCtrl",
#                             size=(700, 500),
#                             style = wx.DEFAULT_FRAME_STYLE)
#         win.Show(True)
# 
#         # give easy access to the demo's PyShell if it's running
#         self.rtfrm = win
#         self.rtc = win.rtc


#----------------------------------------------------------------------
class MyFrame(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, title='Richtext Test')
        win = TestPanel(self)
        self.Show()
# def runTest(frame, nb, log):
#     win = TestPanel(nb, log)
#     return win

#----------------------------------------------------------------------


overview = """<html><body>
<h2><center>wx.richtext.RichTextCtrl</center></h2>

</body></html>
"""

if __name__ == "__main__":
    books = FindingBook(libraryPath=r"c:\1\library").findAllBooks()
    book = None
    for b in books:
        book = b
        break
#     print book
    app = Window(book=book)
    app.MainLoop()
