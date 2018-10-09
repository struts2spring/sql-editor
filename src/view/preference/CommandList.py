#----------------------------------------------------------------------------
# Name:         ListCtrl.py
# Purpose:      Testing lots of stuff, controls, window types, etc.
#
# Author:       Robin Dunn & Gary Dumer
#
# Created:
# RCS-ID:       $Id$
# Copyright:    (c) 1998 by Total Control Software
# Licence:      wxWindows license
#----------------------------------------------------------------------------

import sys
import  wx
import  wx.lib.mixins.listctrl  as  listmix


# from src.static.constant import Workspace
import os
import logging

logger = logging.getLogger('extensive')
#---------------------------------------------------------------------------

musicdata = {
1 : ("Zoom in", "Ctrl + mouse scroll up", "Edit image","zoom_in.png"),
2 : ("Zoom out", "Ctrl + mouse scroll down", "Edit image","zoom_out.png"),
3 : ("Quit Opal", "Ctrl + Q", "Rock","exit-16.png"),
4 : ("Search", "Ctrl + F", "Rock","search.png"),
5 : ("Help", "F1", "Rock","help.png"),
6 : ("Open selected ebook", "O", "Open","openEbook.png"),
7 : ("Restart ", "Ctrl + R", "Restart","restart.png"),
8 : ("Remove selected ebook", "Delete", "delete","delete.png"),
9 : ("Edit metadata of selected ebook", "E", "Edit metadata","edit.png"),
10: ("Download metadata and cover of a ebook", "Ctrl + D", "Edit metadata","editMulti.png"),
}

#---------------------------------------------------------------------------

class CommandKeyListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)


class CommandKeyListCtrlPanel(wx.Panel, listmix.ColumnSorterMixin):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)

#         self.log = log
        tID = wx.NewId()
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        if wx.Platform == "__WXMAC__" and \
               hasattr(wx.GetApp().GetTopWindow(), "LoadDemo"):
            self.useNative = wx.CheckBox(self, -1, "Use native listctrl")
            self.useNative.SetValue( 
                not wx.SystemOptions.GetOptionInt("mac.listctrl.always_use_generic") )
            self.Bind(wx.EVT_CHECKBOX, self.OnUseNative, self.useNative)
            sizer.Add(self.useNative, 0, wx.ALL | wx.ALIGN_RIGHT, 4)
            
        self.il = wx.ImageList(16, 16)
        print('------------------>',os.getcwd())
        path=os.path.join('..',"images", "zoom_out.png")
        if os.path.exists(path):
            image = wx.Image(os.path.join('..',"images", "zoom_out.png"), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
            icon = wx.Icon()
            icon.CopyFromBitmap(image)
        
            self.idx1 = self.il.Add(image)
    #         self.idx1 = self.il.Add(images.Smiles.GetBitmap())
#             self.sm_up = self.il.Add(images.SmallUpArrow.GetBitmap())
#             self.sm_dn = self.il.Add(images.SmallDnArrow.GetBitmap())

        self.list = CommandKeyListCtrl(self, tID,
                                 style=wx.LC_REPORT 
                                 #| wx.BORDER_SUNKEN
                                 | wx.BORDER_NONE
                                 | wx.LC_EDIT_LABELS
                                 | wx.LC_SORT_ASCENDING
                                 #| wx.LC_NO_HEADER
                                 #| wx.LC_VRULES
                                 #| wx.LC_HRULES
                                 #| wx.LC_SINGLE_SEL
                                 )
        
        self.list.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        sizer.Add(self.list, 1, wx.EXPAND)

        self.PopulateList()

        # Now that the list exists we can init the other base class,
        # see wx/lib/mixins/listctrl.py
        self.itemDataMap = musicdata
        listmix.ColumnSorterMixin.__init__(self, 3)
        #self.SortListItems(0, True)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.list)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.list)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.list)
        self.Bind(wx.EVT_LIST_DELETE_ITEM, self.OnItemDelete, self.list)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick, self.list)
        self.Bind(wx.EVT_LIST_COL_RIGHT_CLICK, self.OnColRightClick, self.list)
        self.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self.OnColBeginDrag, self.list)
        self.Bind(wx.EVT_LIST_COL_DRAGGING, self.OnColDragging, self.list)
        self.Bind(wx.EVT_LIST_COL_END_DRAG, self.OnColEndDrag, self.list)
        self.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT, self.OnBeginEdit, self.list)

        self.list.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.list.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

        # for wxMSW
        self.list.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)

        # for wxGTK
        self.list.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)


    def OnUseNative(self, event):
        wx.SystemOptions.SetOptionInt("mac.listctrl.always_use_generic", not event.IsChecked())
        wx.GetApp().GetTopWindow().LoadDemo("ListCtrl")

    def PopulateList(self):
        if 0:
            # for normal, simple columns, you can add them like this:
            self.list.InsertColumn(0, "Command")
            self.list.InsertColumn(1, "Binding", wx.LIST_FORMAT_RIGHT)
            self.list.InsertColumn(2, "Category")
        else:
            # but since we want images on the column header we have to do it the hard way:
            info = wx.ListItem()
            info.m_mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
            info.m_image = 1
            info.m_format = 0
            info.m_text = "Command"
            self.list.InsertColumn(0, info)

            info.m_format = wx.LIST_FORMAT_RIGHT
            info.m_text = "Binding"
            self.list.InsertColumn(1, info)

            info.m_format = 0
            info.m_text = "Category"
            self.list.InsertColumn(2, info)

        items = musicdata.items()
        path = os.path.abspath(__file__)
        tail = None
        while tail != 'src':
            path = os.path.abspath(os.path.join(path, '..'))
            head, tail = os.path.split(path)
            
        imageLocation=os.path.join(path,  "images")
        count=0
        for key, data in items:
            image = wx.Image(os.path.join(imageLocation, data[3]), wx.BITMAP_TYPE_PNG).ConvertToBitmap()
            index = self.list.InsertItem(count, data[0], self.il.Add(image))
            self.list.SetItem(index, 1, data[1])
            self.list.SetItem(index, 2, data[2])
            self.list.SetItemData(index, key)
            count +=1

        self.list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.list.SetColumnWidth(2, 100)

        # show how to select an item
        self.list.SetItemState(5, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

        # show how to change the colour of a couple items
        item = self.list.GetItem(1)
        item.SetTextColour(wx.BLUE)
        self.list.SetItem(item)
        item = self.list.GetItem(4)
        item.SetTextColour(wx.RED)
        self.list.SetItem(item)

        self.currentItem = 0


    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetListCtrl(self):
        return self.list

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetSortImages(self):
        return (self.sm_dn, self.sm_up)


    def OnRightDown(self, event):
        x = event.GetX()
        y = event.GetY()
        logger.debug("OnRightDown x, y = %s\n" , str((x, y)))
        item, flags = self.list.HitTest((x, y))

        if item != wx.NOT_FOUND and flags & wx.LIST_HITTEST_ONITEM:
            self.list.Select(item)

        event.Skip()


    def getColumnText(self, index, col):
        item = self.list.GetItem(index, col)
        return item.GetText()


    def OnItemSelected(self, event):
        ##print event.GetItem().GetTextColour()
        self.currentItem = event.GetIndex()
        logger.debug("OnItemSelected: %s, %s, %s, %s\n" ,
                            self.currentItem,
                            self.list.GetItemText(self.currentItem),
                            self.getColumnText(self.currentItem, 1),
                            self.getColumnText(self.currentItem, 2))

        if self.currentItem == 10:
            logger.debug("OnItemSelected: Veto'd selection\n")
            #event.Veto()  # doesn't work
            # this does
            self.list.SetItemState(10, 0, wx.LIST_STATE_SELECTED)

        event.Skip()


    def OnItemDeselected(self, evt):
        item = evt.GetItem()
        logger.debug("OnItemDeselected: %d" , evt.GetIndex())

        # Show how to reselect something we don't want deselected
        if evt.GetIndex() == 11:
            wx.CallAfter(self.list.SetItemState, 11, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)


    def OnItemActivated(self, event):
        self.currentItem = event.GetIndex()
        logger.debug("OnItemActivated: %s\nTopItem: %s" ,
                           self.list.GetItemText(self.currentItem), self.list.GetTopItem())

    def OnBeginEdit(self, event):
        logger.debug("OnBeginEdit")
        event.Allow()

    def OnItemDelete(self, event):
        logger.debug("OnItemDelete\n")

    def OnColClick(self, event):
        print("OnColClick: %d\n" % event.GetColumn())
        event.Skip()

    def OnColRightClick(self, event):
        item = self.list.GetColumn(event.GetColumn())
        logger.debug("OnColRightClick: %d %s\n" ,
                           event.GetColumn(), (item.GetText(), item.GetAlign(),
                                                item.GetWidth(), item.GetImage()))
        if self.list.HasColumnOrderSupport():
            logger.debug("OnColRightClick: column order: %d\n" ,
                               self.list.GetColumnOrder(event.GetColumn()))

    def OnColBeginDrag(self, event):
        logger.debug("OnColBeginDrag\n")
        ## Show how to not allow a column to be resized
        #if event.GetColumn() == 0:
        #    event.Veto()


    def OnColDragging(self, event):
        logger.debug("OnColDragging\n")

    def OnColEndDrag(self, event):
        logger.debug("OnColEndDrag\n")

    def OnDoubleClick(self, event):
        logger.debug("OnDoubleClick item %s\n" , self.list.GetItemText(self.currentItem))
        event.Skip()

    def OnRightClick(self, event):
#         print("OnRightClick %s\n" % self.list.GetItemText(self.currentItem))

        # only do this part the first time so the events are only bound once
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.popupID3 = wx.NewId()
            self.popupID4 = wx.NewId()
            self.popupID5 = wx.NewId()
            self.popupID6 = wx.NewId()

            self.Bind(wx.EVT_MENU, self.OnPopupOne, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnPopupTwo, id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.OnPopupThree, id=self.popupID3)
            self.Bind(wx.EVT_MENU, self.OnPopupFour, id=self.popupID4)
            self.Bind(wx.EVT_MENU, self.OnPopupFive, id=self.popupID5)
            self.Bind(wx.EVT_MENU, self.OnPopupSix, id=self.popupID6)

        # make a menu
        menu = wx.Menu()
        # add some items
        menu.Append(self.popupID1, "FindItem tests")
        menu.Append(self.popupID2, "Iterate Selected")
        menu.Append(self.popupID3, "ClearAll and repopulate")
        menu.Append(self.popupID4, "DeleteAllItems")
        menu.Append(self.popupID5, "GetItem")
        menu.Append(self.popupID6, "Edit")

        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()


    def OnPopupOne(self, event):
        logger.debug("Popup one\n")
        logger.debug( "FindItem:", self.list.FindItem(-1, "Roxette"))
        logger.debug( "FindItemData:", self.list.FindItemData(-1, 11))

    def OnPopupTwo(self, event):
        logger.debug("Selected items:\n")
        index = self.list.GetFirstSelected()

        while index != -1:# def runTest(frame, nb, log):
#     win = TestListCtrlPanel(nb, log)
#     return win
            print("      %s: %s\n" % (self.list.GetItemText(index), self.getColumnText(index, 1)))
            index = self.list.GetNextSelected(index)

    def OnPopupThree(self, event):
        logger.debug("Popup three\n")
        self.list.ClearAll()
        wx.CallAfter(self.PopulateList)

    def OnPopupFour(self, event):
        self.list.DeleteAllItems()

    def OnPopupFive(self, event):
        item = self.list.GetItem(self.currentItem)
        print(item.m_text, item.m_itemId, self.list.GetItemData(self.currentItem))

    def OnPopupSix(self, event):
        self.list.EditLabel(self.currentItem)


#---------------------------------------------------------------------------

# def runTest(frame, nb, log):
#     win = TestListCtrlPanel(nb, log)
#     return win

#---------------------------------------------------------------------------




if __name__ == "__main__":

    app = wx.App()
    
    frame = wx.Frame(None, -1, 'CommandKeyListCtrl frame', size=(600,400))
    win = CommandKeyListCtrlPanel(frame)
    frame.Show()
    app.MainLoop()
