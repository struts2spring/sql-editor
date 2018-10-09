'''
Created on 07-Mar-2017

@author: keshvij
'''
import wx
import os
import sys
try:
    import cairo
    import rsvg
except:
    pass
from src.view.schema.GraphvizCreator import GraphvizDiagram
try:
    from graphviz.dot import Digraph
except:
    pass

import logging
import tempfile

logger = logging.getLogger('extensive')


SCALE = 1.0  # Default is 1.
INCREMENT = 0.1
gTmpPngPath = os.path.expandvars(tempfile.gettempdir() + os.sep + 'tmpSVG.png')

class SVGViewerPanel(wx.Panel):
    def __init__(self, parent=None, *args, **kw):
        wx.Panel.__init__(self, parent, id=-1)
        self.parent = parent
        self.tables = None
        
#         for filePath in os.listdir(gAppDir):
#             fp = (gAppDir + os.sep + filePath).lower().endswith('.svg')
#             if fp and os.path.exists(gAppDir + os.sep + filePath):
#                 sys.argv.append(gAppDir + os.sep + filePath)

#                 break        
        
        
        
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def setTableDetail(self, tables=None):
        
        tableDict = dict()
        logger.debug(tables)
        for table in tables:
            logger.debug(table)
            columns=list()
            for col in table.values()[0]:
                columns.append(col[1])
            tableDict[table.keys()[0]]=columns
#         tables['book'] = ['id', 'book_name', ]
#         tables['author'] = ['id', 'author_name', ]
#         tables['book_author'] = ['id', 'author_id', 'book_id']
#         tables.iteritems()
        self.tables = tableDict

    def createGraphviz(self):
#         self.getTableDetail()
        nodes = list()
        idx = 0
        for  k, columns in self.tables.iteritems():
            node = list()
#             print(idx, k, columns)
            nodeColumnName = dict()
            label = ''
            for index, column_name in enumerate(columns):
#                 print(column_name)
                label = label + '| <f' + str(index + 1) + '> ' + column_name
            nodeColumnName['label'] = '<f0> ' + k + label
#             print(nodeColumnName)
            node.append('node' + str(idx))
            node.append(nodeColumnName)
            nodes.append(tuple(node))
            idx += 1
            
        logger.debug(nodes)
        gd = GraphvizDiagram()
        
        g6 = gd.add_edges(
                          gd.add_nodes(Digraph(format='svg'), nodes
                                       ), [
                                          (('node0:f0', 'node1:f0'), {'id': '0'}),
                                          (('node0:f1', 'node2:f0'), {'id': '1'}),
                                                        #         ('B:f0', 'C:f0')
                                                            ]
        )
        g6 = gd.apply_styles(g6)
        g6.render(tempfile.gettempdir() + os.sep + 'g6')
    def OnMouseWheel(self, event):
        global SCALE
        if event.GetWheelRotation() > 0:
            SCALE = SCALE + INCREMENT
        else:
            SCALE = SCALE - INCREMENT
        if SCALE <= INCREMENT:
            SCALE = INCREMENT
        self.Refresh()

    def OnPaint(self, event):
        # # gSVG = rsvg.Handle(file=sys.argv[1])
        # # gDimensionData = gSVG.get_dimension_data()

        scaledSize = (self.gDimensionData[0] * SCALE, self.gDimensionData[1] * SCALE)
        surface = cairo.SVGSurface(None, scaledSize[0], scaledSize[1])
        ctx = cairo.Context(surface)
        if self.gSVG != None:
            matrix = cairo.Matrix(xx=SCALE, yx=0, xy=0, yy=SCALE, x0=0, y0=0)
            ctx.transform(matrix)
            self.gSVG.render_cairo(ctx)

        surface.write_to_png(gTmpPngPath)
        surface.finish()

        svgBmp = wx.Bitmap(gTmpPngPath, wx.BITMAP_TYPE_PNG)

        dc = wx.PaintDC(self)
        dc.DrawBitmap(svgBmp, 0, 0)    

class CreateErDiagramFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "SVG Viewer", size=(640, 480))
        self.svgViewer = SVGViewerPanel(self)
        
    def setDbObjects(self, dbObjects=None):
        logger.debug('setDbObjects')
        dbObjects[1].sort()
        tables = dbObjects[1][1]['table']
        self.svgViewer.setTableDetail(tables=tables)
        self.svgViewer.createGraphviz()
#         self.svgViewer.
        path = os.path.abspath(os.path.join(tempfile.gettempdir(), 'g6.svg'))
        logger.debug(path)
        self.svgViewer.gSVG = rsvg.Handle(file=path)
        self.svgViewer.gDimensionData = self.svgViewer.gSVG.get_dimension_data()
#---------------------------------------------------------------------------
if __name__ == '__main__':
    app = wx.App(False)
#     frame = wx.Frame(None)

    frame = CreateErDiagramFrame(None)
    frame.Show()
    app.MainLoop()
