# -*- coding: utf-8 -*-

"""
Created on Thu Mar 14 16:35:00 2019
@author: Alfonso
"""
line = list() #contains a single line
singleElement = list()
tasks = dict() #contains all the tasks
number = -1
list1=[]
list2=[]
fhand = open('G:/fresh grad/cpm1.txt') #TWO FILES: cpm.txt and cpm1.txt

for line in fhand: #slide the file line by line
    singleElement=(line.split(',')) #split a line in subparts
    number += 1
    for i in range(len(singleElement)): #creating the single task element
        tasks['task'+ str(singleElement[0])]= dict()
        tasks['task'+ str(singleElement[0])]['id'] = singleElement[0]
        tasks['task'+ str(singleElement[0])]['name'] = singleElement[1]
        tasks['task'+ str(singleElement[0])]['duration'] = singleElement[2]
        if(singleElement[3] != "\n"):
            tasks['task'+ str(singleElement[0])]['dependencies'] = singleElement[3].strip().split(';')
        else:
            tasks['task'+ str(singleElement[0])]['dependencies'] = ['-1']
        tasks['task'+ str(singleElement[0])]['ES'] = 0
        tasks['task'+ str(singleElement[0])]['EF'] = 0
        tasks['task'+ str(singleElement[0])]['LS'] = 0
        tasks['task'+ str(singleElement[0])]['LF'] = 0
        tasks['task'+ str(singleElement[0])]['float'] = 0
        tasks['task'+ str(singleElement[0])]['isCritical'] = False
    list2.append((tasks['task'+ str(singleElement[0])])["dependencies"])
    list1.append((tasks['task'+ str(singleElement[0])])["id"])
    ''',(tasks['task'+ str(singleElement[0])])["id"]'''


flattened=[]
for sublist in list2:
    for val in sublist:
        flattened.append(val)

list3=[]

#print("list1 :",list1)
#print("list2 :",list2)
l=0
merged_list=[]
for i in list2:
    for j in i:
        merged_list.append((list1[l],j))
    l+=1
#print("merger list:",merged_list)
#merged_list = [(list1[i], flattened[i]) for i in range(0, len(list1))] 

# =============================================================================
# FORWARD PASS
# =============================================================================
for taskFW in tasks: #slides all the tasks
    if('-1' in tasks[taskFW]['dependencies']): #checks if it's the first task
        tasks[taskFW]['ES'] = 1
        tasks[taskFW]['EF'] = (tasks[taskFW]['duration'])
    else: #not the first task
        for k in tasks.keys():
            for dipendenza in tasks[k]['dependencies']: #slides all the dependency in a single task
                #print('task ' + taskFW + ' k '+ k + ' dipendenza ' +dipendenza)
                if(dipendenza != '-1' and len(tasks[k]['dependencies']) == 1): #if the task k has only one dependency
                    tasks[k]['ES'] = int(tasks['task'+ dipendenza]['EF']) +1
                    tasks[k]['EF'] = int(tasks[k]['ES']) + int(tasks[k]['duration']) -1
                elif(dipendenza !='-1'): #if the task k has more dependency
                    if(int(tasks['task'+dipendenza]['EF']) > int(tasks[k]['ES'])):
                        tasks[k]['ES'] = int(tasks['task'+ dipendenza]['EF']) +1
                        tasks[k]['EF'] = int(tasks[k]['ES']) + int(tasks[k]['duration']) -1
        
aList = list() #list of task keys
for element in tasks.keys():
    aList.append(element)

bList = list() #reversed list of task keys
while len(aList) > 0:
    bList.append(aList.pop())
    
# =============================================================================
# BACKWARD PASS
# =============================================================================
for taskBW in bList:
    if(bList.index(taskBW) == 0): #check if it's the last task (so no more task)
        tasks[taskBW]['LF']=tasks[taskBW]['EF']
        tasks[taskBW]['LS']=tasks[taskBW]['ES']
        
    for dipendenza in tasks[taskBW]['dependencies']: #slides all the dependency in a single task
        if(dipendenza != '-1'): #check if it's NOT the last task
            if(tasks['task'+ dipendenza]['LF'] == 0): #check if the the dependency is already analyzed
                #print('ID dipendenza: '+str(tasks['task'+dipendenza]['id']) + ' taskBW: '+str(tasks[taskBW]['id']))
                tasks['task'+ dipendenza]['LF'] = int(tasks[taskBW]['LS']) -1
                tasks['task'+ dipendenza]['LS'] = int(tasks['task'+ dipendenza]['LF']) - int(tasks['task'+ dipendenza]['duration']) +1
                tasks['task'+ dipendenza]['float'] = int(tasks['task'+ dipendenza]['LF']) - int(tasks['task'+ dipendenza]['EF'])
                #print('IF1 dip LS: '+str(tasks['task'+dipendenza]['LS']) +' dip LF: '+str(tasks['task'+dipendenza]['LF']) + ' taskBW: '+str(tasks[taskBW]['id'])+' taskBW ES '+ str(tasks[taskBW]['ES']))
            if(int(tasks['task'+ dipendenza]['LF']) >int(tasks[taskBW]['LS']) ): #put the minimun value of LF for the dependencies of a task
                tasks['task'+ dipendenza]['LF'] = int(tasks[taskBW]['LS']) -1
                tasks['task'+ dipendenza]['LS'] = int(tasks['task'+ dipendenza]['LF']) - int(tasks['task'+ dipendenza]['duration']) +1
                tasks['task'+ dipendenza]['float'] = int(tasks['task'+ dipendenza]['LF']) - int(tasks['task'+ dipendenza]['EF'])
                #print('IF2 dip LS: '+str(tasks['task'+dipendenza]['LS']) +' dip LF: '+str(tasks['task'+dipendenza]['LF']) + ' taskBW: '+str(tasks[taskBW]['id']))
# =============================================================================
# PRINTING  
# =============================================================================
print('task id  task name  duration    ES      EF    LS      LF    float  isCritical')
litask=[]
durli=[]
i=0
for task in tasks:

    if(tasks[task]['float'] == 0):
        tasks[task]['isCritical'] = True
    print(str(tasks[task]['id']) +' \t '+str(tasks[task]['name']) + '\t\t'+str(tasks[task]['duration']) +'\t '+str(tasks[task]['ES']) +'\t '+str(tasks[task]['EF']) +'\t'+str(tasks[task]['LS']) +' \t'+str(tasks[task]['LF']) +'\t '+str(tasks[task]['float']) +'\t '+str(tasks[task]['isCritical']))
    if( str(tasks[task]['isCritical'])=='True'):
        litask.append((str(tasks[task]['name'])))
        
        durli.append(int(str(tasks[task]['duration'])))
print(litask)
print(durli)
print("Critical path: ",sum(durli))
import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(graph, labels=None, graph_layout='shell',
               node_size=1600, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):

    # create networkx graph
    G=nx.Graph()

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    # these are different layouts for the network you may try
    # shell seems to work best
    if graph_layout == 'spring':
        graph_pos=nx.spring_layout(G)
    elif graph_layout == 'spectral':
        graph_pos=nx.spectral_layout(G)
    elif graph_layout == 'random':
        graph_pos=nx.random_layout(G)
    else:
        graph_pos=nx.shell_layout(G)

    # draw graph
    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, 
                           alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,
                           alpha=edge_alpha,edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
                            font_family=text_font)

    if labels is None:
        labels = range(len(graph))

    edge_labels = dict(zip(graph, labels))
    nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels, 
                                 label_pos=edge_text_pos)

    # show graph
    plt.show()

graph =merged_list

#[(1, 0), (2, 1), (3, 1), (4, 1), (5, 2),(6,3),(6,4),(7,4),(8,5),(9,6),(10,7),(11,8),(11,9),(11,10)]

# you may name your edge labels
labels = map(chr, range(65, 65+len(graph)))
#draw_graph(graph, labels)

# if edge labels is not specified, numeric labels (0, 1, 2...) will be used
draw_graph(graph)