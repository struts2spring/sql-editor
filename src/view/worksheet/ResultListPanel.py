
import wx
import wx.dataview as dv
import wx.lib.agw.aui.auibook as aui
import os
from src.view.constants import ID_RUN,ID_EXECUTE_SCRIPT, ID_RESULT_REFRESH,\
    ID_ROW_ADD, ID_ROW_DELETE, ID_RESULT_NEXT, ID_RESULT_PREVIOUS,\
    ID_APPLY_CHANGE, ID_RESULT_FIRST, ID_RESULT_LAST
from src.view.worksheet.ResultGrid import ResultDataGrid
import logging
from wx import StaticText

logger = logging.getLogger('extensive')
#----------------------------------------------------------------------

# This model class provides the data to the view when it is asked for.
# Since it is a list-only model (no hierachical data) then it is able
# to be referenced by row rather than by item object, so in this way
# it is easier to comprehend and use than other model types.  In this
# example we also provide a Compare function to assist with sorting of
# items in our model.  Notice that the data items in the data model
# object don't ever change position due to a sort or column
# reordering.  The view manages all of that and maps view rows and
# columns to the model's rows and columns as needed.
#
# For this example our data is stored in a simple list of lists.  In
# real life you can use whatever you want or need to hold your data.

class ResultModel(dv.PyDataViewIndexListModel):
    def __init__(self, data):
        dv.PyDataViewIndexListModel.__init__(self, len(data))
        self.data = data

    # All of our columns are strings.  If the model or the renderers
    # in the view are other types then that should be reflected here.
    def GetColumnType(self, col):
        return "string"

    # This method is called to provide the data object for a
    # particular row,col
    def GetValueByRow(self, row, col):
        return self.data[row][col]

    # This method is called when the user edits a data item in the view.
    def SetValueByRow(self, value, row, col):
        print("SetValue: (%d,%d) %s\n" % (row, col, value))
        self.data[row][col] = value

    # Report how many columns this model provides data for.
    def GetColumnCount(self):
        return len(self.data[0])

    # Report the number of rows in the model
    def GetCount(self):
        #print('GetCount')
        return len(self.data)
    
    # Called to check if non-standard attributes should be used in the
    # cell at (row, col)
    def GetAttrByRow(self, row, col, attr):
        ##print('GetAttrByRow: (%d, %d)' % (row, col))
        if col == 3:
            attr.SetColour('gray')
            attr.SetBold(True)
            return True
        return False


    # This is called to assist with sorting the data in the view.  The
    # first two args are instances of the DataViewItem class, so we
    # need to convert them to row numbers with the GetRow method.
    # Then it's just a matter of fetching the right values from our
    # data set and comparing them.  The return value is -1, 0, or 1,
    # just like Python's cmp() function.
    def Compare(self, item1, item2, col, ascending):
        if not ascending: # swap sort order?
            item2, item1 = item1, item2
        row1 = self.GetRow(item1)
        row2 = self.GetRow(item2)
        if col == 0:
            return (int(self.data[row1][col])> int(self.data[row2][col])) -(int(self.data[row1][col])< int(self.data[row2][col]))
        else:
            return (int(self.data[row1][col])> int(self.data[row2][col])) -(int(self.data[row1][col])< int(self.data[row2][col]))

        
    def DeleteRows(self, rows):
        # make a copy since we'll be sorting(mutating) the list
        rows = list(rows)
        # use reverse order so the indexes don't change as we remove items
        rows.sort(reverse=True)
        
        for row in rows:
            # remove it from our data structure
            del self.data[row]
            # notify the view(s) using this model that it has been removed
            self.RowDeleted(row)
            
            
    def AddRow(self, value):
        # update data structure
        self.data.append(value)
        # notify views
        self.RowAppended()

        
            
class ResultPanel(wx.Panel):
    def __init__(self, parent,model=None, data=None):
        wx.Panel.__init__(self, parent, -1)
        self.data=data
        # Create a dataview control
        self.dvc = dv.DataViewCtrl(self,
                                   style=wx.BORDER_THEME
                                   | dv.DV_ROW_LINES # nice alternating bg colors
                                   #| dv.DV_HORIZ_RULES
                                   | dv.DV_VERT_RULES
                                   | dv.DV_MULTIPLE
                                   )
        
        # Create an instance of our simple model...
#         if model is None:
#             self.model = ResultModel(self.data)
#         else:
#             self.model = model            


#         self.createDataViewCtrl()


        # set the Sizer property (same as SetSizer)
        self.Sizer = wx.BoxSizer(wx.VERTICAL) 
        self.Sizer.Add(self.dvc, 1, wx.EXPAND)
        
        # Add some buttons to help out with the tests
        b1 = wx.Button(self, label="New View", name="newView")
        self.Bind(wx.EVT_BUTTON, self.OnNewView, b1)
        b2 = wx.Button(self, label="Add Row")
        self.Bind(wx.EVT_BUTTON, self.OnAddRow, b2)
        b3 = wx.Button(self, label="Delete Row(s)")
        self.Bind(wx.EVT_BUTTON, self.OnDeleteRows, b3)

#         btnbox = wx.BoxSizer(wx.HORIZONTAL)
#         btnbox.Add(b1, 0, wx.LEFT|wx.RIGHT, 5)
#         btnbox.Add(b2, 0, wx.LEFT|wx.RIGHT, 5)
#         btnbox.Add(b3, 0, wx.LEFT|wx.RIGHT, 5)
        self.Sizer.Add(self.constructBottomResultToolBar(), 0, wx.TOP|wx.BOTTOM, 5)

        # Bind some events so we can see what the DVC sends us
        self.Bind(dv.EVT_DATAVIEW_ITEM_EDITING_DONE, self.OnEditingDone, self.dvc)
        self.Bind(dv.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.OnValueChanged, self.dvc)

    def setModel(self, model=None,data=None):
        # Create an instance of our simple model...
        if model is None:
            self.model = ResultModel(data)
        else:
            self.model = model      
    def createDataViewCtrl(self,data=None, headerList=None):

        # ...and associate it with the dataview control.  Models can
        # be shared between multiple DataViewCtrls, so this does not
        # assign ownership like many things in wx do.  There is some
        # internal reference counting happening so you don't really
        # need to hold a reference to it either, but we do for this
        # example so we can fiddle with the model from the widget
        # inspector or whatever.
        self.setModel( data=data)
        self.dvc.AssociateModel(self.model)

        # Now we create some columns.  The second parameter is the
        # column number within the model that the DataViewColumn will
        # fetch the data from.  This means that you can have views
        # using the same model that show different columns of data, or
        # that they can be in a different order than in the model.
        for header in headerList:
            self.dvc.AppendTextColumn(header,  1, width=170, mode=dv.DATAVIEW_CELL_EDITABLE)
#         self.dvc.AppendTextColumn("Title",   2, width=260, mode=dv.DATAVIEW_CELL_EDITABLE)
#         self.dvc.AppendTextColumn("Genre",   3, width=80,  mode=dv.DATAVIEW_CELL_EDITABLE)

        # There are Prepend methods too, and also convenience methods
        # for other data types but we are only using strings in this
        # example.  You can also create a DataViewColumn object
        # yourself and then just use AppendColumn or PrependColumn.
        c0 = self.dvc.PrependTextColumn("Id", 0, width=40)

        # The DataViewColumn object is returned from the Append and
        # Prepend methods, and we can modify some of it's properties
        # like this.
        c0.Alignment = wx.ALIGN_RIGHT
        c0.Renderer.Alignment = wx.ALIGN_RIGHT
        c0.MinWidth = 40

        # Through the magic of Python we can also access the columns
        # as a list via the Columns property.  Here we'll mark them
        # all as sortable and reorderable.
        for c in self.dvc.Columns:
            c.Sortable = True
            c.Reorderable = True
            
        # Let's change our minds and not let the first col be moved.
        c0.Reorderable = False     
             
    def OnNewView(self, evt):
        f = wx.Frame(None, title="New view, shared model", size=(600,400))
        ResultPanel(f,  self.model)
        b = f.FindWindowByName("newView")
        b.Disable()
        f.Show()


    def OnDeleteRows(self, evt):
        # Remove the selected row(s) from the model. The model will take care
        # of notifying the view (and any other observers) that the change has
        # happened.
        items = self.dvc.GetSelections()
        rows = [self.model.GetRow(item) for item in items]
        self.model.DeleteRows(rows)

        
    def OnAddRow(self, evt):
        # Add some bogus data to a new row in the model's data
#         id = len(self.model.data) + 1
#         value = [str(id),
#                  'new artist %d' % id,
#                  'new title %d' % id,
#                  'genre %d' % id]
#         self.model.AddRow(value)
        pass
                

    def OnEditingDone(self, evt):
        print("OnEditingDone\n")

    def OnValueChanged(self, evt):
        print("OnValueChanged\n")
        
    def constructBottomResultToolBar(self):
        
        # create some toolbars
        tb1 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER)
        tb1.SetToolBitmapSize(wx.Size(16, 16))
        playImage = None
        if "worksheet" == os.path.split(os.getcwd())[-1:][0]:
            imageLocation = os.path.join("..", "..", "images")

        elif "view" == os.path.split(os.getcwd())[-1:][0]:
            imageLocation = os.path.join("..", "images")
        tb1.AddLabelTool(id=ID_ROW_ADD, label="Row add", shortHelp="Row add ", bitmap=wx.Bitmap(os.path.join(imageLocation, "row_add.png")))
        tb1.AddLabelTool(id=ID_ROW_DELETE, label="Row delete", shortHelp="Row delete ", bitmap=wx.Bitmap(os.path.join(imageLocation, "row_delete.png")))
        tb1.AddLabelTool(id=ID_APPLY_CHANGE, label="Apply data change", shortHelp="Apply data change ", bitmap=wx.Bitmap(os.path.join(imageLocation, "accept.png")))
        tb1.AddSeparator()
        tb1.AddLabelTool(id=ID_RESULT_REFRESH, label="Result refresh", shortHelp="Result refresh ", bitmap=wx.Bitmap(os.path.join(imageLocation, "resultset_refresh.png")))
        tb1.AddLabelTool(id=ID_RESULT_FIRST, label="Result first", shortHelp="Result first ", bitmap=wx.Bitmap(os.path.join(imageLocation, "resultset_first.png")))
        tb1.AddLabelTool(id=ID_RESULT_NEXT, label="Result next", shortHelp="Result next ", bitmap=wx.Bitmap(os.path.join(imageLocation, "resultset_next.png")))
        tb1.AddLabelTool(id=ID_RESULT_PREVIOUS, label="Result previous", shortHelp="Result previous ", bitmap=wx.Bitmap(os.path.join(imageLocation, "resultset_previous.png")))
        tb1.AddLabelTool(id=ID_RESULT_LAST, label="Result last", shortHelp="Result last ", bitmap=wx.Bitmap(os.path.join(imageLocation, "resultset_last.png")))
        tb1.AddSeparator()

        tb1.Realize()
        
        return tb1 
        
#----------------------------------------------------------------------

# def runTest(frame, nb, log):
#     # Get the data from the ListCtrl sample to play with, converting it
#     # from a dictionary to a list of lists, including the dictionary key
#     # as the first element of each sublist.
#     import ListCtrl
#     musicdata = ListCtrl.musicdata.items()
#     musicdata.sort()
#     musicdata = [[str(k)] + list(v) for k,v in musicdata]
# 
#     win = TestPanel(nb, log, data=musicdata)
#     return win


#         sizer.Fit(self)
class CreatingResultWithToolbarPanel(wx.Panel):
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        self.data=list()
        vBox = wx.BoxSizer(wx.VERTICAL)

        ####################################################################
        self.topResultToolbar = self.constructTopResultToolBar()
        self.bottomResultToolbar = self.constructBottomResultToolBar()
#         self.resultPanel = ResultPanel(self, data=self.getData())
        self.resultPanel = ResultDataGrid(self, data=self.getData())
#         bottomResultToolbar = self.constructBottomResultToolBar()
        
        ####################################################################
        vBox.Add(self.topResultToolbar , 0, wx.EXPAND | wx.ALL, 0)
        vBox.Add(self.resultPanel , 1, wx.EXPAND | wx.ALL, 0)
        vBox.Add(self.bottomResultToolbar , 0, wx.EXPAND | wx.ALL, 0)
#         vBox.Add(bottomResultToolbar , 0, wx.EXPAND | wx.ALL, 0)
#         vBox.Add(resultPanel , 1, wx.EXPAND | wx.ALL)
        sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(worksheetToolbar ,.9, wx.EXPAND | wx.ALL, 0)
        sizer.Add(vBox, 1, wx.EXPAND , 0)
        self.SetSizer(sizer)    
    
    def constructBottomResultToolBar(self):
        tb2 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                 wx.TB_FLAT | wx.TB_NODIVIDER)
        str = "This is a different font."
        bottomBarText = StaticText(self, -1, str, (20, 120))
        tb2.AddLabelTool('asfd')
        
        tb2.Realize()
        return tb2   
    def constructTopResultToolBar(self):
        path = os.path.abspath(__file__)
        tail = None
#         head, tail = os.path.split(path)
#         print('createAuiManager',head, tail )
        try:
            while tail != 'src':
                path = os.path.abspath(os.path.join(path, '..',))
                head, tail = os.path.split(path)
        except Exception as e:
            logger.error(e, exc_info=True)
        print('------------------------------------------------------------------------->',path)
        path = os.path.abspath(os.path.join(path, "images"))        
        # create some toolbars
        tb1 = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                         wx.TB_FLAT | wx.TB_NODIVIDER)
        tb1.SetToolBitmapSize(wx.Size(16, 16))
#         playImage = None
#         if "worksheet" == os.path.split(os.getcwd())[-1:][0]:
#             imageLocation = os.path.join("..", "..", "images")
# 
#         elif "view" == os.path.split(os.getcwd())[-1:][0]:
#             imageLocation = os.path.join("..", "images")
        tb1.AddTool(ID_RUN, "Pin", wx.Bitmap(os.path.join(path, "pin2_green.png")))
        tb1.AddTool(ID_EXECUTE_SCRIPT, "Result refresh", wx.Bitmap(os.path.join(path, "resultset_refresh.png")))
        tb1.AddSeparator()

        tb1.Realize()
        
        return tb1     
  
    def getData(self):
        # Get the data from the ListCtrl sample to play with, converting it
        # from a dictionary to a list of lists, including the dictionary key
        # as the first element of each sublist.
#         self.data=music
        return self.data
#---------------------------------------------------------------------------
class CreateResultSheetTabPanel(wx.Panel):
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        path = os.path.abspath(__file__)
        tail = None
#         head, tail = os.path.split(path)
#         print('createAuiManager',head, tail )
        try:
            while tail != 'src':
                path = os.path.abspath(os.path.join(path, '..',))
                head, tail = os.path.split(path)
        except Exception as e:
            logger.error(e, exc_info=True)
        print('------------------------------------------------------------------------->',path)
        path = os.path.abspath(os.path.join(path, "images"))
                
        # Attributes
        self._nb = aui.AuiNotebook(self)
#         if "worksheet" == os.path.split(os.getcwd())[-1:][0]:
#             imageLocation = os.path.join("..", "..", "images")
#         #             playImage=wx.Bitmap(os.path.join("..","..", "images", "play.png"))
#         elif "view" == os.path.split(os.getcwd())[-1:][0]:
#         imageLocation = os.path.join(path)
        imgList = wx.ImageList(16, 16)
        imgList.Add(wx.Bitmap(os.path.join(path, "sql_script.png")))
        
        self._nb.AssignImageList(imgList) 
        
        self.addTab()
        #         self._nb.AddPage(worksheetPanel, "2", imageId=0)
        # Layout
        
        self.__DoLayout()
        
    def addTab(self, name='Start Page'):
        resultSheetPanel = CreatingResultWithToolbarPanel(self._nb, -1, style=wx.CLIP_CHILDREN)
#             worksheetPanel.worksheetPanel.editorPanel
        name='ResultSheet '
        self._nb.AddPage(resultSheetPanel, name)      
        self.Bind(aui.EVT_AUINOTEBOOK_TAB_RIGHT_DOWN, self.onTabRightDown, self._nb)
        self.Bind(aui.EVT_AUINOTEBOOK_BG_DCLICK, self.onBgDoubleClick, self._nb)  
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.onCloseClick, self._nb)  
        
    def __DoLayout(self):
        """Layout the panel"""
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._nb, 1, wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        self.Layout()
    def SetCurrentPage(self, page):
        """
        Set the current page to the page given
        """
        n = self._nb.GetPageIndex(page)
        if n!=-1:
            self._nb.SetSelection(n)
            return True
        return False    
    
    def GetCurrentPage(self):
        """
        Get the current active Page page
        """
        num  = self._nb.GetSelection()
        if num==-1:
            page = None
        else:
            page = self._nb.GetPage(num)
        return page

    def GetPages(self, page_type):
        """
        Get all the Page pages of a particular type
        """
        npages = self._nb.GetPageCount()
        res = []
        for n in range(0,npages):
            page = self._nb.GetPage(n)
            if isinstance(page, page_type):
                res.append(page)
        return res                
    def onTabRightDown(self,event):
        print('onTabRightDown')
        
    def onBgDoubleClick(self,event):
        print('onBgDoubleClick')
        
    def onCloseClick(self,event):
        print('onCloseClick')
        self.GetCurrentPage()

#---------------------------------------------------------------------------
if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None)
    
    

#     panel = ResultPanel(frame, data=musicdata)
    panel = CreateResultSheetTabPanel(frame)
#     panel = CreatingResultWithToolbarPanel(frame)
    frame.Show()
    app.MainLoop()

