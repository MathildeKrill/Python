import random

class WeightedGraph:
    # constructor randomley generates a graph, 
    # given the number of vertice, min and max number of vertice from each vertex
    def __init__(self, number_vertice, 
                 min_edges_per_vertice, 
                 max_edges_per_vertice, 
                 negative_weights_allowed = False):
        assert number_vertice > 0
        assert min_edges_per_vertice >= 0
        assert max_edges_per_vertice < number_vertice 
        assert min_edges_per_vertice <= max_edges_per_vertice 

        self.edges_per_vertice = [[] for _ in xrange(number_vertice)]
        for vertex_from in xrange(number_vertice):
            number_of_edges = random.randint(min_edges_per_vertice, max_edges_per_vertice)
            # to make sure there are no self loops, 
            # sample ends < counter and ends > counter separately
            qty_edges_before = int(round(number_of_edges * vertex_from / number_vertice))
            if qty_edges_before > number_of_edges:
                qty_edges_before = number_of_edges 
            if qty_edges_before >= vertex_from:
                qty_edges_before = vertex_from
            if (number_of_edges-qty_edges_before) >= (number_vertice - vertex_from - 1):
                qty_edges_before = number_of_edges + vertex_from - number_vertice + 1
                                
            vertice_to = []
            if qty_edges_before > 0:
                vertice_to += random.sample(xrange(vertex_from), qty_edges_before) 
            if qty_edges_before < number_of_edges:
                vertice_to += random.sample(xrange(vertex_from+1, number_vertice), number_of_edges-qty_edges_before)
                
            if negative_weights_allowed:
                self.edges_per_vertice[vertex_from] = [(v, 2*random.random()-1) for v in vertice_to]                
            else:
                self.edges_per_vertice[vertex_from] = [(v, random.random()) for v in vertice_to]
            self.edges_per_vertice[vertex_from].sort(key = lambda x:x[0]) 
            
    def Print(self):
        vertex = -1
        for epv in self.edges_per_vertice: # iterate over ends of the edge
            vertex += 1
            for other_vertice, weight in epv:
                print "edge (", vertex, ", ", other_vertice, "), weight = ", weight
             
    def BellmanFordPathToSrource(self, single_source):
        assert single_source >= 0
        assert single_source < len(self.edges_per_vertice)
        
        # first element of a tuple is the distance, the second one is the ancestor
        result = [(None, None) for _ in self.edges_per_vertice]
        result[single_source] = (0, None) # distance to itself is 0
        negative_loop_edge = None
        for iteration in range(len(self.edges_per_vertice)): # iterate over lengths of paths, last loop for checking
            for vertex_from in range(len(self.edges_per_vertice)): # iterate over beginning of the edge
                for vertex_to, weight in self.edges_per_vertice[vertex_from]:
                    if result[vertex_to][0] == None: # we differentiate between 0 and None
                        continue # we cannot relax the edge that comes from unreachable vertice
                    new_distance = result[vertex_to][0] + weight
                    if (result[vertex_from][0] == None) or (result[vertex_from][0] > new_distance):
                        if iteration == len(self.edges_per_vertice) - 1:
                            negative_loop_edge = (vertex_from, vertex_to)
                        else:
                            result[vertex_from] = (new_distance, vertex_to)               
                                                                 
        for vertex in xrange(len(result)):
            print "vertex ", vertex, ", distance ", result[vertex][0], ", ancestor ", result[vertex][1]            
        if negative_loop_edge:
            print "negative_loop_edge: ", negative_loop_edge[0], ", ", negative_loop_edge[1]            
        return result, negative_loop_edge
    
    def BellmanFordPathFromSource(self, single_source):
        if not self.edges_per_vertice:
            return
        assert single_source >= 0
        assert single_source < len(self.edges_per_vertice)
        
        # first element of a tuple is the distance, the second one is the ancestor
        result = [(None, None) for _ in self.edges_per_vertice]
        result[single_source] = (0, None) # distance to itself is 0
        for _ in self.edges_per_vertice: # iterate over lengths of paths, last loop for checking
            relaxed_edge = None
            for vertex_from in range(len(self.edges_per_vertice)): # iterate over the beginnings of the edge
                relaxed_edge_this_vertex = self.__RelaxEdgesFromSource(result = result, vertex_from = vertex_from)
                if not relaxed_edge:
                    relaxed_edge = relaxed_edge_this_vertex
            if not relaxed_edge:
                break #stop if during the iteration no edge was relaxed
            
        negative_loop_edge = relaxed_edge   
        for vertex in xrange(len(result)):
            print "vertex ", vertex, ", distance ", result[vertex][0], ", ancestor ", result[vertex][1]            
        if negative_loop_edge:
            print "negative_loop_edge: ", negative_loop_edge[0], ", ", negative_loop_edge[1]            
        return result, negative_loop_edge  
      
    def __RelaxEdgesFromSource(self, result, vertex_from): #direction from source outwards
        if result[vertex_from][0] == None: # we differentiate between 0 and None
            return None # we cannot relax the edge that comes from unreachable vertice
        relaxed_edge = None
        for vertex_to, weight in self.edges_per_vertice[vertex_from]:
            new_distance = result[vertex_from][0] + weight
            if (result[vertex_to][0] == None) or (result[vertex_to][0] > new_distance):
                result[vertex_to] = (new_distance, vertex_from)
                relaxed_edge = (vertex_from, vertex_to) # this edge has been relaxed
        return relaxed_edge # we return **any** relaxed edge, provided at least one edge was relaxed
   
    def DijkstraFromSource(self, single_source):
        assert single_source >= 0
        assert single_source < len(self.edges_per_vertice)
        
        visited_vertice = set()
        queueing_vertice = {v for v in range(len(self.edges_per_vertice))} 
        result = [(None, None) for _ in range(len(self.edges_per_vertice))]#(distance, ancestor)
        result[single_source] = (0, None) # distance to itself is 0
        
        current_vertex = single_source        
        while current_vertex != None: #differentiate between 0 and None
            
            #relax all edges from current_vertex
            queueing_vertice.remove(current_vertex)
            visited_vertice.add(current_vertex)
            self.__RelaxEdgesFromSource(result = result, vertex_from = current_vertex)
            
            # find next current vertex
            current_vertex_candidate = None
            min_distance_so_far = None
            for vertex in queueing_vertice:
                if (result[vertex][0] == None):
                    continue
                if (min_distance_so_far != None): 
                    if min_distance_so_far <= result[vertex][0]:
                        continue 
                current_vertex_candidate = vertex
                min_distance_so_far = result[vertex][0]
            current_vertex = current_vertex_candidate                    
            
        for vertex in xrange(len(result)):
            print "vertex ", vertex, ", distance ", result[vertex][0], ", ancestor ", result[vertex][1]
        return result            

if __name__ == '__main__':
    random.seed(10000)
    wg = WeightedGraph(5, 0, 0)
    wg.Print()
    wg.BellmanFordPathFromSource(single_source = 0); wg.DijkstraFromSource(single_source = 0);
    wg = WeightedGraph(5, 4, 4)
    wg.Print()
    wg.BellmanFordPathFromSource(single_source = 0); wg.DijkstraFromSource(single_source = 0);
    wg = WeightedGraph(5, 2, 3)
    wg.Print()
    wg.BellmanFordPathFromSource(single_source = 0); wg.DijkstraFromSource(single_source = 0);
    wg = WeightedGraph(5, 1, 1, True)
    wg.Print()
    wg.BellmanFordPathFromSource(single_source = 0)
