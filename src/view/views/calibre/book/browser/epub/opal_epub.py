
import wx
import wx.aui
import wx.html
import sys


overview = '''
    <!DOCTYPE html>
<html>
    <head>
        <style>
            div.img {
                height: auto;
                width: auto;
                float: left;
            }

            div.img img {
                display: inline;
            }

            div.img a:hover img {
            }

            div.desc {
                font-weight: normal;
                width: 120px;
            }
        </style>
    </head>
    <body>
    this is a test message.
            <a target="_blank" href="klematis_big.htm"><img src="/home/vijay/Documents/Aptana_Workspace/Better/seleniumone/books/1/a_peek_at_computer_electronics.jpg" alt="Professional Java for Web Applications" title="Professional Java for Web Applications" width="200" ></a>

    </body>
</html>

    '''
ID_search=wx.ID_ANY
class MainFrame(wx.Frame):

    def __init__(self, parent):
        title = "Opal"
        style = wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE
#         wx.Frame.__init__(self, parent, wx.ID_ANY, title, pos, size, style)
        wx.Frame.__init__(self, parent, wx.ID_ANY, title=title, style=style)
        self._mgr = wx.aui.AuiManager()
        self._mgr.SetManagedWindow(self)
        # create menu
        mb = wx.MenuBar()
        self.SetMenuBar(mb)
        self.SetMinSize(wx.Size(500, 400))
        
        tb1 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize, wx.TB_FLAT | wx.TB_NODIVIDER)
        tb1.SetToolBitmapSize(wx.Size(24, 24))
        tb1.AddLabelTool(ID_search, "Search", wx.ArtProvider_GetBitmap(wx.ART_FIND))
        self.Bind(wx.EVT_MENU, self.onSearch, id=ID_search)
        
        tb1.AddSeparator()
        tb1.Realize()
        # add the toolbars to the manager
        self._mgr.AddPane(tb1, wx.aui.AuiPaneInfo().Name("tb1").Caption("Big Toolbar").ToolbarPane().Top().Show())
        
        
        html_content = wx.aui.AuiPaneInfo().Caption("Book Information").Name("html_content").Centre().Layer(1).Position(1).CloseButton(True).MaximizeButton(True)
        self._mgr.AddPane(self.CreateHTMLCtrl(), html_content)
        perspective_all = self._mgr.SavePerspective()
        self.perspective_default = self._mgr.SavePerspective()
        self._mgr.Update()
        
        self.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
   

    def CreateHTMLCtrl(self):
#         self.ctrl = wx.html.HtmlWindow(self, -1, wx.DefaultPosition, wx.Size(600, 400))
#         if "gtk2" in wx.PlatformInfo or "gtk3" in wx.PlatformInfo:
#             self.ctrl.SetStandardFonts()
#         self.ctrl.SetPage(self.GetIntroText())
        if sys.platform == 'win32':
            self.browser = wx.html2.WebView.New(self)
            self.browser.LoadURL("C:\\Users\\vijay\\workspace\\3d_cover_flow\\WebContent\\3D-Cover-Flip-Animations-with-jQuery-CSS3-Transforms-Cover3D\\indexSimpleDemo.html")
        else:
            self.browser = wx.html.HtmlWindow(self, -1, wx.DefaultPosition, wx.Size(600, 400))
            if "gtk2" in wx.PlatformInfo or "gtk3" in wx.PlatformInfo:
                self.browser.SetStandardFonts()
        return self.browser     
    def OnClose(self, event):
        print 'OnClose'
        self._mgr.UnInit()
        del self._mgr
        self.Destroy()

    def onSearch(self, event):
        print 'onSearch'
        
    def OnSize(self, event):
        event.Skip()
    def OnEraseBackground(self, event):
        event.Skip()    
        
    def OnPaneClose(self, event):
        caption = event.GetPane().caption
        print caption

        if caption in ["Tree Pane", "Dock Manager Settings", "Fixed Pane"]:
            msg = "Are You Sure You Want To Close This Pane?"
            dlg = wx.MessageDialog(self, msg, "AUI Question", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

            if dlg.ShowModal() in [wx.ID_NO, wx.ID_CANCEL]:
                event.Veto()
            dlg.Destroy()    

if __name__ == "__main__":

    app = wx.App()
    frame = MainFrame(None)
    frame.Show()
    app.MainLoop()