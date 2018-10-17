'''
Created on 05-Feb-2017

@author: vijay
'''
import wx

import logging

logger = logging.getLogger('extensive')



#---------------------------------------------------------------------------
class CreatingGoToLinePanel(wx.Dialog):

    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE,
            ):
        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
        pre = wx.Dialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
#         self.PostCreate(pre)
        
        self.parent = parent
        vBox = wx.BoxSizer(wx.VERTICAL)
#         import  wx.lib.rcsizer  as rcs
#         rowColumnSizer = rcs.RowColSizer()
# #         sizer = wx.GridBagSizer(hgap=3, vgap=3)
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         h1 = wx.BoxSizer(wx.VERTICAL)
#         
#         h1.Add((1, 1), -1, wx.ALL)  # this is a spacer
#         lineNumberLabel = wx.StaticText(self, id=-1, label="Enter line number (1..95):")
#         self.lineNumberText = wx.TextCtrl(self, -1, '')
#         
# 
#         
#         h1.Add(lineNumberLabel, 0, wx.ALL, 2)
#         h1.Add(self.lineNumberText, 0, wx.ALL, 2)
        
        
        
        btnsizer = wx.StdDialogButtonSizer()
        
        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        
#         btn = wx.Button(self, wx.ID_OK)
#         btn.SetHelpText("The OK button completes the dialog")
#         btn.SetDefault()
#         btnsizer.AddButton(btn)
# 
#         btn = wx.Button(self, wx.ID_CANCEL)
#         btn.SetHelpText("The Cancel button cancels the dialog. (Cool, huh?)")
#         btnsizer.AddButton(btn)
#         btnsizer.Realize()


#         self.okButton = wx.Button(self, -1, "OK", pos=(50, 20))
# #         self.Bind(wx.EVT_BUTTON, self.onFindClicked, self.findButton)
#         self.okButton.SetDefault()
#         
#         self.cancelButton = wx.Button(self, -1, "Cancel", pos=(50, 20))
# #         self.Bind(wx.EVT_BUTTON, self.onFindClicked, self.findButton)
#         self.cancelButton.SetDefault()
 
         
#         rowColumnSizer.Add(self.okButton,row=1, col=1)
#         rowColumnSizer.Add(self.cancelButton,row=1, col=2)
 
         
#         hbox000 = wx.BoxSizer(wx.HORIZONTAL)
#         hbox000.Add((2,2),1, wx.EXPAND | wx.ALL , 2) 
#         hbox000.Add(rowColumnSizer)
         
         
         
#         hbox001 = wx.BoxSizer(wx.HORIZONTAL)
#         vBox.Add(hbox001, 0, wx.EXPAND | wx.ALL, 0)  
#         vBox.Add(h1, 0, wx.EXPAND , 0)  
#         vBox.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
#         vBox.Add(vBox1, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
#         vBox.Add(self.tb, 0, wx.EXPAND)
#         vBox.Add(self.list, 1, wx.EXPAND)
        ####################################################################
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(vBox, 1, wx.EXPAND , 0)
#         self.SetSizer(vBox)
#         self.SetAutoLayout(True)        
#---------------------------------------------------------------------------

      
if __name__ == '__main__':
    app = wx.App(False)
#     frame = CreatingFindAndReplaceFrame(None, 'Find / Replace')
    dlg = CreatingGoToLinePanel(None, -1, "Sample Dialog", size=(350, 200) )
    dlg.CenterOnScreen()
    
    # this does not return until the dialog is closed.
    val = dlg.ShowModal()
    
    if val == wx.ID_OK:
        logger.debug("You pressed OK\n")
    else:
        logger.debug("You pressed Cancel\n")
    
    dlg.Destroy()
    app.MainLoop()
