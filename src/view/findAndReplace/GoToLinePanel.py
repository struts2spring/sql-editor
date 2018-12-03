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
            self, parent, id, title, size=(485, 192), pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE, name='Go to Line', numberOfLines=1
            ):
        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
        wx.Dialog.__init__(self)
        self.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.Create(parent, id, title, pos, size, style, name)
        # Now continue with the normal construction of the dialog
        # contents
        sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, -1, "Enter line number (1..{}):".format(numberOfLines))
        label.SetHelpText("Enter line number")
        sizer.Add(label, 0, wx.ALIGN_LEFT|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

#         label = wx.StaticText(self, -1, "")
#         label.SetHelpText("This is the help text for the label")
#         box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.lineNumberText = wx.TextCtrl(self, -1, "", size=(80,-1))
        self.lineNumberText.SetHelpText("Here's some help text for field #1")
        box.Add(self.lineNumberText, 1, wx.ALIGN_CENTRE|wx.ALL, 10)

        sizer.Add(box, 0, wx.EXPAND|wx.ALL, 5)

#         box = wx.BoxSizer(wx.HORIZONTAL)
# 
#         label = wx.StaticText(self, -1, "Field #2:")
#         label.SetHelpText("This is the help text for the label")
#         box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
# 
#         text = wx.TextCtrl(self, -1, "", size=(80,-1))
#         text.SetHelpText("Here's some help text for field #2")
#         box.Add(text, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
# 
#         sizer.Add(box, 0, wx.EXPAND|wx.ALL, 5)

#         line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
#         sizer.Add(line, 0, wx.EXPAND|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()

        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_OK,"&Go to Line")
        btn.SetHelpText("Go to line number")
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btn.SetHelpText("The Cancel button cancels the dialog. (Cool, huh?)")
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 1, wx.EXPAND|wx.RIGHT|wx.BOTTOM, 5)

        self.SetSizer(sizer)
#         sizer.Fit(self)
        
        self.parent = parent
     
#---------------------------------------------------------------------------

      
if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, title="go to line", size=(700,500))
    panel=wx.Panel(frame,-1)
#     frame = CreatingFindAndReplaceFrame(None, 'Find / Replace')
    dlg = CreatingGoToLinePanel(panel, -1, title="Go to Line", size=(485, 192), style=wx.DEFAULT_DIALOG_STYLE)
#     dlg.CenterOnScreen()
    
    # this does not return until the dialog is closed.
    val = dlg.ShowModal()
     
    if val == wx.ID_OK:
        logger.debug("You pressed OK\n")
    else:
        logger.debug("You pressed Cancel\n")
      
    dlg.Destroy()
    frame.Show()
    app.MainLoop()
