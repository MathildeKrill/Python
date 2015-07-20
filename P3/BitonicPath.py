import math
# see https://en.wikipedia.org/wiki/Bitonic_tour for the statement of the problem

# this class contains all distances between vertices
class Distances:
    def __init__(self, vertice): 
        # avoid altering input
        sorted_indices = range(len(vertice))
        sorted_indices.sort(key = lambda index_:vertice[index_][0])
        self.__distances = [[math.sqrt((vertice[i][0]-vertice[j][0])**2 + (vertice[i][1]-vertice[j][1])**2)
                                                for i in sorted_indices] for j in sorted_indices]
       
    def get_(self, vertice_1, vertice_2):
        return self.__distances[vertice_1][vertice_2]

# this class contains information about two partial paths. 
# For each path, it know the sequence of vertices and total length
# It stores an instance of distances to avoid passing it as a parameter
class TwoPartialPaths:
    def __init__(self, path_to_rightmost, distance_to_rightmost, 
                       path_to_another_extreme, distance_to_another_extreme, distances):
        self.path_to_rightmost = path_to_rightmost
        self.distance_to_rightmost = distance_to_rightmost
        self.path_to_another_extreme = path_to_another_extreme
        self.distance_to_another_extreme = distance_to_another_extreme
        self.distances = distances
        
    def print_out(self):
        print "path 1 is", self.path_to_rightmost
        print "distance 1 is", self.distance_to_rightmost
        print "path 2 is", self.path_to_another_extreme
        print "distance 2 is", self.distance_to_another_extreme
        print "overall distance", self.get_total_distance()
        
    def add_to_rightmost(self):
        new_vertex = self.path_to_rightmost[-1] + 1
        result = TwoPartialPaths(path_to_rightmost = self.path_to_rightmost + [new_vertex],
                                 distance_to_rightmost = self.distance_to_rightmost 
                                                        + self.distances.get_(new_vertex, new_vertex-1),
                                 path_to_another_extreme = self.path_to_another_extreme,
                                 distance_to_another_extreme = self.distance_to_another_extreme,
                                 distances = self.distances)
        return result

    def add_to_another(self):
        new_vertex = self.path_to_rightmost[-1] + 1
        another_extreme = self.path_to_another_extreme[-1]
        result = TwoPartialPaths(path_to_rightmost = self.path_to_another_extreme + [new_vertex],
                                 distance_to_rightmost = self.distance_to_another_extreme 
                                                        + self.distances.get_(new_vertex, another_extreme),
                                 path_to_another_extreme = self.path_to_rightmost,
                                 distance_to_another_extreme = self.distance_to_rightmost,
                                 distances = self.distances)
        return result
    
    def add_to_both(self):
        new_vertex = self.path_to_rightmost[-1] + 1
        another_extreme = self.path_to_another_extreme[-1]
        result = TwoPartialPaths(path_to_rightmost = self.path_to_another_extreme + [new_vertex],
                                 distance_to_rightmost = self.distance_to_another_extreme 
                                    + self.distances.get_(new_vertex, another_extreme),
                                 path_to_another_extreme = self.path_to_rightmost + [new_vertex],
                                 distance_to_another_extreme = self.distance_to_rightmost 
                                    + self.distances.get_(new_vertex, new_vertex-1),
                                 distances = self.distances)
        return result
    
    def get_total_distance(self):
        return self.distance_to_rightmost + self.distance_to_another_extreme

# solve it
def find_bitonic_path(vertice):    
    # initialise the distances
    distances = Distances(vertice = vertice)  
      
    # initialisation for 2 leftmost vertice
    shortest_paths_given_ends = [TwoPartialPaths(path_to_rightmost = [0, 1], 
                                                 distance_to_rightmost = distances.get_(1, 0), 
                                                 path_to_another_extreme = [0], 
                                                 distance_to_another_extreme = 0.,
                                                 distances = distances)]         
    
    # do other vertice, except the last one
    for _ in xrange(len(vertice) - 3):
        # find the last element, when we add to another extreme
        best_last = shortest_paths_given_ends[0].add_to_another()
        for pspge in shortest_paths_given_ends[1:]:
            challenger = pspge.add_to_another()
            if challenger.get_total_distance() < best_last.get_total_distance():
                best_last = challenger 
        # handle simple cases, when we add to the rightmost extreme,
        # and the other extreme does not change
        shortest_paths_given_ends = [
            spge.add_to_rightmost() for spge in shortest_paths_given_ends] + [best_last]
            
    # do the rightmost vertex
    result = shortest_paths_given_ends[0].add_to_both()    
    for spge in shortest_paths_given_ends[1:]:
        challenger = spge.add_to_both()
        if challenger.get_total_distance() < result.get_total_distance():
            result = challenger
        
    return result

if __name__ == '__main__':    
    vertice = [[0,0], [3,4], [7,0], [10,4]] # [(random.random(), random.random()) for _ in xrange(4)]
    for v in vertice:
        print v
    result = find_bitonic_path(vertice = vertice)
    result.print_out()