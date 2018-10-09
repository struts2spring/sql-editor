'''
Created on 08-Mar-2017

@author: keshvij
'''


try:
    import os
    from graphviz import Digraph
    os.environ['PATH'] = os.environ['PATH'] + ";C:\\soft\\graphviz-2.38\\release\\bin\\"
except:
    pass
    


class GraphvizDiagram():
    def __init__(self, style=None):
        self.styles = {
        'graph': {
                  
            'rankdir' : "LR",
            'label': 'A Fancy Graph',
    #         'fontsize': '16',
    #         'fontcolor': 'white',
    #         'bgcolor': '#333333',
    #         'rankdir': 'BT',
        },
        'nodes': {
    #         'fontname': 'Helvetica',
            'shape': 'record',
            'fontsize':'16',
            'fontcolor': 'black',
    #         'color': 'white',
    #         'style': 'filled',
            'fillcolor': '#006699',
        },
        'edges': {
            'style': 'dashed',
    #         'color': 'white',
            'arrowhead': 'open',
            'fontname': 'Courier',
            'fontsize': '12',
            'fontcolor': 'black',
        }
    }
    
    def add_nodes(self, graph, nodes):
        for n in nodes:
            if isinstance(n, tuple):
                graph.node(n[0], **n[1])
            else:
                graph.node(n)
        return graph
    
    def add_edges(self, graph, edges):
        for e in edges:
            if isinstance(e[0], tuple):
                graph.edge(*e[0], **e[1])
            else:
                graph.edge(*e)
        return graph
    
    def apply_styles(self, graph):
        graph.graph_attr.update(
            ('graph' in self.styles and self.styles['graph']) or {}
        )
        graph.node_attr.update(
            ('nodes' in self.styles and self.styles['nodes']) or {}
        )
        graph.edge_attr.update(
            ('edges' in self.styles and self.styles['edges']) or {}
        )
        return graph



if __name__ == '__main__':
    gd=GraphvizDiagram()
    g6 = gd.add_edges(
                      gd.add_nodes(Digraph(format='svg'), [
                                                           ('node0', {'label': "<f0> 0x10ba8| <f1> ", }),
                                                           ('node1', {'label': "<f0> 0xf7fc4380| <f1> | <f2> |-1", }),
                                                           ('node2', {'label': "<f0> 0xf7fc44b8| | |2", })
                                                           ]
                                   ),[
                                      (('node0:f0', 'node1:f0'), {'id': '0'}),
                                      (('node0:f1', 'node2:f0'), {'id': '1'}),
                                                    #         ('B:f0', 'C:f0')
                                                        ]
    )
    
    
    g6 = gd.apply_styles(g6)
    g6.render('img/g6')
    pass
