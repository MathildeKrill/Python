import math
# see https://en.wikipedia.org/wiki/Bitonic_tour for the statement of the problem

# this class contains all distances between vertices
class Vertice(object):
    def __init__(self, vertice_coordinates):
        
        self.__vertice_coordinates = vertice_coordinates 
        # avoid altering input
        self.sorted_to_original_absciss_indices = range(len(vertice_coordinates))
        self.sorted_to_original_absciss_indices.sort(key = lambda index_:vertice_coordinates[index_][0])
        
        self.original_to_sorted_absciss_indices = range(len(vertice_coordinates))
        self.original_to_sorted_absciss_indices.sort(key = lambda index_:self.sorted_to_original_absciss_indices[index_])
        
        # precompute neighbouring distances
        self.distances_neighbours = [self.get_distance(self.sorted_to_original_absciss_indices[i], 
                                                       self.sorted_to_original_absciss_indices[i+1]) 
                                                                        for i in xrange(len(vertice_coordinates)-1)]
       
    def get_distance(self, ind_original_1, ind_original_2):
        return math.sqrt((self.__vertice_coordinates[ind_original_1][0] - self.__vertice_coordinates[ind_original_2][0])**2 + 
                         (self.__vertice_coordinates[ind_original_1][1] - self.__vertice_coordinates[ind_original_2][1])**2)
     
    # given an index in the original array, find next to the right and output it and the distance between the two   
    def find_next_to_the_right_and_distance(self, ind_original):
        ind_sorted = self.original_to_sorted_absciss_indices[ind_original]
        ind_original_next = self.sorted_to_original_absciss_indices[ind_sorted + 1]
        return self.distances_neighbours[ind_sorted], ind_original_next
    
    def get_first_node_TwoPartialPaths(self):
        ind_leftmost = self.sorted_to_original_absciss_indices[0]
        return TwoPartialPaths(path_to_rightmost = [ind_leftmost], 
                               distance_to_rightmost = 0., 
                               path_to_another_extreme = [ind_leftmost], 
                               distance_to_another_extreme = 0.,
                               vertice = self)

# this class contains information about two partial paths. 
# For each path, it know the sequence of vertices and total length
# It stores an instance of distances to avoid passing it as a parameter
class TwoPartialPaths(object):
    def __init__(self, path_to_rightmost, distance_to_rightmost, 
                       path_to_another_extreme, distance_to_another_extreme, vertice):
        self.path_to_rightmost = path_to_rightmost
        self.distance_to_rightmost = distance_to_rightmost
        self.path_to_another_extreme = path_to_another_extreme
        self.distance_to_another_extreme = distance_to_another_extreme
        self.vertice = vertice
        
    def __str__(self):
        result = "path 1 is {}\ndistance 1 is {}\npath 2 is {}\ndistance 2 is {}\noverall distance is {}".\
            format(self.path_to_rightmost, self.distance_to_rightmost, self.path_to_another_extreme,
                   self.distance_to_another_extreme, self.get_total_distance())
        return result
        
    def add_to_rightmost(self):
        additional_distance, next_vertex = self.vertice.find_next_to_the_right_and_distance(self.path_to_rightmost[-1])
        result = TwoPartialPaths(path_to_rightmost = self.path_to_rightmost + [next_vertex],
                                 distance_to_rightmost = self.distance_to_rightmost + additional_distance,
                                 path_to_another_extreme = self.path_to_another_extreme,
                                 distance_to_another_extreme = self.distance_to_another_extreme,
                                 vertice = self.vertice)
        return result

    def add_to_another(self):
        _, next_vertex = self.vertice.find_next_to_the_right_and_distance(self.path_to_rightmost[-1])
        another_extreme = self.path_to_another_extreme[-1]
        result = TwoPartialPaths(path_to_rightmost = self.path_to_another_extreme + [next_vertex],
                                 distance_to_rightmost = self.distance_to_another_extreme 
                                                        + self.vertice.get_distance(another_extreme, next_vertex),
                                 path_to_another_extreme = self.path_to_rightmost,
                                 distance_to_another_extreme = self.distance_to_rightmost,
                                 vertice = self.vertice)
        return result
    
    def add_to_both(self):
        additional_distance, next_vertex = self.vertice.find_next_to_the_right_and_distance(self.path_to_rightmost[-1])
        another_extreme = self.path_to_another_extreme[-1]
        result = TwoPartialPaths(path_to_rightmost = self.path_to_another_extreme + [next_vertex],
                                 distance_to_rightmost = self.distance_to_another_extreme 
                                    + self.vertice.get_distance(another_extreme, next_vertex),
                                 path_to_another_extreme = self.path_to_rightmost + [next_vertex],
                                 distance_to_another_extreme = self.distance_to_rightmost + additional_distance,
                                 vertice = self.vertice)
        return result
    
    def get_total_distance(self):
        return self.distance_to_rightmost + self.distance_to_another_extreme

# solve it
def find_bitonic_path(vertice_coordinates):    
    # initialise the distances
    vertice = Vertice(vertice_coordinates = vertice_coordinates)  
      
    # initialisation for 2 leftmost vertice
    leftmode_vertex_node = vertice.get_first_node_TwoPartialPaths() # only leftmost vertex node
    shortest_paths_given_ends = [leftmode_vertex_node.add_to_rightmost()] # add second leftmost        
    
    # do other vertice, except the last one
    for _ in xrange(len(vertice_coordinates) - 3):
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
    vertice_coordinates = [[3,4], [7,0], [10,4], [0,0], [1.5,2]] # [(random.random(), random.random()) for _ in xrange(4)]
    for v in vertice_coordinates:
        print v
    result = find_bitonic_path(vertice_coordinates = vertice_coordinates)
    print result