import sys
import wx
import wx.html2 as webview
import logging
from src.view.util.FileOperationsUtil import FileOperations
import os
try:
    from agw import aui
    from agw.aui import aui_switcherdialog as ASD
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.aui as aui
    from wx.lib.agw.aui import aui_switcherdialog as ASD
    
logger = logging.getLogger('extensive')
#----------------------------------------------------------------------

class WelcomePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        fileOperations=FileOperations()
        self.current = ""
        self.frame = self.GetTopLevelParent()
        self.titleBase = self.frame.GetTitle()

        sizer = wx.BoxSizer(wx.VERTICAL)
#         btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.wv = webview.WebView.New(self)
        self.Bind(webview.EVT_WEBVIEW_NAVIGATING, self.OnWebViewNavigating, self.wv)
        self.Bind(webview.EVT_WEBVIEW_NAVIGATED, self.OnWebViewNavigated, self.wv)
        self.Bind(webview.EVT_WEBVIEW_LOADED, self.OnWebViewLoaded, self.wv)
        self.Bind(webview.EVT_WEBVIEW_TITLE_CHANGED, self.OnWebViewTitleChanged, self.wv)
 
        # create some toolbars
        tb1 = aui.AuiToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                             agwStyle=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_OVERFLOW)
        tb1.SetToolBitmapSize(wx.Size(16, 16))
        backButtonId=wx.NewIdRef()
        homeButtonId=wx.NewIdRef()
        forwardButtonId=wx.NewIdRef()
        stopButtonId=wx.NewIdRef()
        refreshButtonId=wx.NewIdRef()
        openButtonId=wx.NewIdRef()
        
        tb1_back = wx.ArtProvider.GetBitmap(wx.ART_GO_BACK, wx.ART_OTHER, wx.Size(16, 16))
        backButton= tb1.AddSimpleTool(backButtonId, "Back", tb1_back, short_help_string="Back")
        self.Bind(wx.EVT_MENU, self.OnPrevPageButton, id=backButtonId)
        self.Bind(wx.EVT_UPDATE_UI, self.OnCheckCanGoBack, backButton)
        
        tb1_home = wx.ArtProvider.GetBitmap(wx.ART_GO_HOME, wx.ART_OTHER, wx.Size(16, 16))
        tb1.AddSimpleTool(homeButtonId, "Start Page", tb1_home, short_help_string="Start page")
        self.Bind(wx.EVT_MENU, self.OnHomeButton, id=homeButtonId)
        
        tb1_forward = wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_OTHER, wx.Size(16, 16))
        forwardButton= tb1.AddSimpleTool(forwardButtonId, "Forword", tb1_forward, short_help_string="Forword")
        self.Bind(wx.EVT_MENU, self.OnNextPageButton, id=forwardButtonId)
        self.Bind(wx.EVT_UPDATE_UI, self.OnCheckCanGoForward, forwardButton)
        
        tb1_stop = wx.ArtProvider.GetBitmap(wx.ART_ERROR, wx.ART_OTHER, wx.Size(16, 16))
        tb1.AddSimpleTool(stopButtonId, "Stop", tb1_stop, short_help_string="Stop")
        self.Bind(wx.EVT_MENU, self.OnStopButton, id=stopButtonId)
        
        tb1_refresh = wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_OTHER, wx.Size(16, 16))
        tb1.AddSimpleTool(refreshButtonId, "Refresh", tb1_refresh, short_help_string="Refresh")
        self.Bind(wx.EVT_MENU, self.OnRefreshPageButton, id=refreshButtonId)
        
        self.location = wx.ComboBox(
            tb1, -1, "", size=(400,-1) ,style=wx.CB_DROPDOWN|wx.TE_PROCESS_ENTER)
        self.location.AppendItems(['http://wxPython.org',
                                   'http://wxwidgets.org',
                                   'http://google.com'])
 
        for url in ['http://wxPython.org',
                    'http://wxwidgets.org',
                    'http://google.com']:
            item = webview.WebViewHistoryItem(url, url)
#             self.wv.LoadHistoryItem(item)
 
        self.Bind(wx.EVT_COMBOBOX, self.OnLocationSelect, self.location)
        self.location.Bind(wx.EVT_TEXT_ENTER, self.OnLocationEnter)
        tb1.AddControl(self.location, label="Location: ")
        
#         tb1_open = wx.ArtProvider.GetBitmap(wx.ART_TICK_MARK, wx.ART_OTHER, wx.Size(16, 16))
        tb1.AddSimpleTool(openButtonId, "Open", bitmap=fileOperations.getImageBitmap(imageName="triangle_green.png"), short_help_string="Open")
        self.Bind(wx.EVT_MENU, self.OnOpenButton, id=openButtonId)

        tb1.Realize()
#         sizer.Add(btnSizer, 0, wx.EXPAND)
        sizer.Add(tb1, 0, wx.EXPAND)
        sizer.Add(self.wv, 1, wx.EXPAND|wx.ALL,0)

#         self.wv.LoadURL(self.current)
        logger.debug("---------------------------------"+ os.getcwd())
        htmlData=FileOperations().readFile(filePath='./html/welcome.html')
        logger.debug(htmlData)
        
        self.wv.SetPage(htmlData,"/")
        self.SetSizer(sizer)



    # WebView events
    def OnWebViewNavigating(self, evt):
        # this event happens prior to trying to get a resource
        if evt.GetURL() == 'http://www.microsoft.com/':
            if wx.MessageBox("Are you sure you want to visit Microsoft?",
                             style=wx.YES_NO|wx.ICON_QUESTION) == wx.NO:
                # This is how you can cancel loading a page.
                evt.Veto()


    def OnWebViewNavigated(self, evt):
        if self.frame.GetStatusBar():
            self.frame.SetStatusText("Loading %s..." % evt.GetURL())


    def OnWebViewLoaded(self, evt):
        # The full document has loaded
        self.current = evt.GetURL()
        self.location.SetValue(self.current)
        if self.frame.GetStatusBar():
            self.frame.SetStatusText("Loaded")


    def OnWebViewTitleChanged(self, evt):
        # Set the frame's title to include the document's title
        self.frame.SetTitle("%s -- %s" % (self.titleBase, evt.GetString()))


    # Control bar events
    def OnLocationSelect(self, evt):
        url = self.location.GetStringSelection()
        logger.debug('OnLocationSelect: %s\n' % url)
        self.wv.LoadURL(url)

    def OnLocationEnter(self, evt):
        url = self.location.GetValue()
        self.location.Append(url)
        self.wv.LoadURL(url)

    def OnOpenButton(self, event):
        url= self.current = self.location.GetValue()
        logger.debug('OnLocationSelect: %s\n' % url)
        self.wv.LoadURL(url)

    def OnHomeButton(self, event):
        url = self.location.SetStringSelection("/")
        logger.debug('OnLocationSelect: %s\n' % url)
        self.wv.LoadURL(url)
    def OnPrevPageButton(self, event):
        for i in self.wv.GetBackwardHistory():
            logger.debug("%s %s" % (i.Url, i.Title))
        self.wv.GoBack()

    def OnNextPageButton(self, event):
        for i in self.wv.GetForwardHistory():
            logger.debug("%s %s" % (i.Url, i.Title))
        self.wv.GoForward()

    def OnCheckCanGoBack(self, event):
        event.Enable(self.wv.CanGoBack())

    def OnCheckCanGoForward(self, event):
        event.Enable(self.wv.CanGoForward())

    def OnStopButton(self, evt):
        self.wv.Stop()

    def OnRefreshPageButton(self, evt):
        self.wv.Reload()


#----------------------------------------------------------------------


def main():
    app = wx.App()
    frm = wx.Frame(None, title="html2.WebView sample", size=(700,500))
    frm.CreateStatusBar()
    pnl = WelcomePanel(frm)
    frm.Show()
    app.MainLoop()


#----------------------------------------------------------------------

if __name__ == '__main__':
    main()