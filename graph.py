import networkx as nx                   #导入networkx包
import matplotlib.pyplot as plt 
from ipdb import set_trace 
import pandas
import os

def createGraph(filename, G, labels) :
    

    df = pandas.read_excel(filename,
                       sheetname='Sheet1',
                       header=0)
    l = len(df)
    i = 0
    
    while i<l:
        if (df[5][i] >= 1)  and (df['9'][i] != 'W9999998'):
         n1 = df['8'][i]
         n2 = df['9'][i]
         node_group.append(df[4][i])           
         weight = df[5][i]
         G.add_nodes_from(n1)
         G.add_nodes_from(n2)
         G.add_weighted_edges_from([(n1, n2, weight)])
         labels[n1] = df[0][i]
         labels[n2] = df[4][i]
        i = i+1        
    return G, labels
    
if __name__=='__main__':
   file_init = '政治'
   ii = 0
   node_group = ['政治']
   G = nx.DiGraph()
   # plt.figure(1, figsize=(80,80))
   old_node = set()
   labels = {}
   while ii<len(node_group):
      # set_trace()
      
      file_init = node_group[ii]
      if (file_init not in old_node) and (type(file_init) == type('a')):
          if os.path.isfile(file_init+'_new.xlsx'):
             G, labels = createGraph(file_init+'_new.xlsx', G, labels)
             old_node.add(file_init)
             #if (ii == 3) or (ii == 500) or (ii == 50000):
             # G1 = nx.Graph()
             # G1 = G
              #nx.draw(G1, font_family='SimHei', pos = nx.spring_layout(G), alpha = 0.6, node_size = 1, font_color = 'red', with_labels=True)  # , with_labels=True
              # plt.savefig(file_init+".png")           
          print(file_init)
          print(ii)   
      ii = ii+1
   H = nx.relabel_nodes(G, labels)
   #nx.draw(G)
   #plt.savefig("ba.png")
   # nx.draw(G, font_family='SimHei', pos = nx.spring_layout(G), alpha = 0.6, node_size = 1, font_color = 'red', with_labels=True)  # , with_labels=True
   # plt.savefig(file_init+'final_'+".png")           
   # plt.show() 
   nx.write_gexf(H,'wiki-3.gexf')
   nx.write_yaml(H, 'wiki-3.yaml')