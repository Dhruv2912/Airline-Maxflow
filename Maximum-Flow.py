import pandas as pd
import networkx as nx

# Function to Add edges between Two Nodes
def AddEdges(Graph,flightdata):
    
    # Get total number of connections
    totalconnections = len(flightdata['FlightNumber'])
    
    # Add Edges between the connections with their Capacity
    rows = 0
    while rows < totalconnections:
        Graph.add_edge(flightdata['Dept_Air_Time'][rows],flightdata['Arr_Air_Time'][rows],capacity=flightdata['Capacity'][rows])
        rows+=1
    return Graph

# Function to find list of all nodes for particular airport 
def Particular_node(airport,data):
    List = [i for i in data if i.startswith(airport)]
    return List

# Function to Sort all nodes as per Time
def Sort_nodes_time(airport,data):
    Sort = sorted(Particular_node(airport,data)) 
    return Sort

# Function to add Starting ('LAX') and Ending ('JFK') node
def Add_start_end_node(data,node):
    rows,capacity = 0,0
    nodes = sorted(Particular_node(node,data))
    while rows < len(nodes):
        if node == 'LAX':
            after_LAX = list(Graph.neighbors(nodes[rows]))
            if after_LAX != 0:
                for items in range(len(after_LAX)):
                    capacity += Graph[nodes[rows]][after_LAX[items]]['capacity']
                Graph.add_edge(node,nodes[rows],capacity=capacity)
        if node == 'JFK':
            before_JFK = list(Graph.predecessors(nodes[rows]))
            if before_JFK != 0:
                for items in range(len(before_JFK)):
                    capacity += Graph[before_JFK[items]][nodes[rows]]['capacity']
                Graph.add_edge(nodes[rows],node,capacity=capacity)
        rows += 1

# Function to add edges between a particular airport nodes which can be taken keeping start and finish time in mind        
def Add_intermediate_edges(airports, airport_sorted_nodes):
    sublist = 0
    for airport in airports:
        while sublist < len(airport_sorted_nodes):
            for sublistelements in range(len(airport_sorted_nodes[sublist])):
                temp = airport_sorted_nodes[sublist]
                capacity = 0 
                before_node = list(Graph.predecessors(temp[sublistelements]))
                if before_node != 0:
                    for items in range(len(before_node)):
                        capacity += Graph[before_node[items]][temp[sublistelements]]['capacity']
                for nextelement in range(sublistelements+1,len(airport_sorted_nodes[sublist])):
                    Graph.add_edge(temp[sublistelements],airport_sorted_nodes[sublist][nextelement],capacity=capacity)
            sublist += 1
            
# Access the CSV file
flightdata = pd.read_csv('Flights_Data.csv')

# Make a graph using Networkx 
Graph = nx.DiGraph()

# Make Column for Departure Airport Nodes and Arrival Airport Nodes with Time Constraints
flightdata['Dept_Air_Time'] = flightdata[['DepartureAirport', 'StartTime']].apply(lambda x: '-'.join(x), axis=1)
flightdata['Arr_Air_Time'] = flightdata[['ArrivalAirport', 'FinishTime']].apply(lambda x: '-'.join(x), axis=1)

# Call of function to make edges between Departing node to Arrival node from data
AddEdges(Graph,flightdata)

# Get List of Each Airport with Nodes Sorted with respect to time
airports = ['SFO','PHX','SEA','DEN','ATL','ORD','BOS','IAD']
airport_sorted_nodes = []
for airport in airports:
    sort = Sort_nodes_time(airport,list(Graph.nodes))
    airport_sorted_nodes.append(sort)

# Call of function to make edges from LAX node connecting LAX time dependent nodes
Add_start_end_node(list(Graph.nodes),"LAX")

# Call of function to make edges from JFK time dependent nodes to JFK node
Add_start_end_node(list(Graph.nodes),"JFK")

# Call of function to make edges between possible connections within a particular airport
Add_intermediate_edges(airports,airport_sorted_nodes)

# Function to calculate Max-Flow from LAX to JFK
flow_value = nx.maximum_flow_value(Graph,'LAX','JFK')
print('\n\n Maximum Capacity between LAX to JFK on 6th Jan 2020 is:',flow_value)
