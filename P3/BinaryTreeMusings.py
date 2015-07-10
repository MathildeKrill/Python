import random

  
# shuffle integers from 0 to upper_limit - 1      
def shuffle(upper_limit):
    unshuffled_numbers = range(upper_limit) 
    result = []
    while unshuffled_numbers:
        next_elem = random.randint(0, len(unshuffled_numbers) - 1)
        result.append(unshuffled_numbers[next_elem])
        del unshuffled_numbers[next_elem]
    return result 

class Graph:
    def __init__(self, number_nodes, max_number_edges = 0.5): 
        if (max_number_edges > 1) or (max_number_edges < 0):
            raise ValueError("max_number_edges is out of range")
        self.nodes_connections = {node_nb : range(node_nb+1, number_nodes) for node_nb in xrange(number_nodes)}
        for key, value in self.nodes_connections.iteritems():
            while len(value) > (max_number_edges * (number_nodes - key - 1)):
                index_to_remove = random.randint(0, len(value)-1)
                del value[index_to_remove]
                                
            new_scheduled_nodes_ids += [key for key, value in self.nodes_connections.iteritems() 
                                            if (node_id in value) and not (key in visited_nodes_ids or key in scheduled_nodes_ids)] 
            scheduled_nodes_ids += new_scheduled_nodes_ids 
            visited_nodes_ids.append(node_id)
            del scheduled_nodes_ids[0]
        return visited_nodes_ids
    
    def __IterateInDepth(self, start_node_id, visited_nodes):
        visited_nodes.append(start_node_id)
        for key, value in self.nodes_connections.iteritems():
            if start_node_id in value:
                if key not in visited_nodes:
                    self.__IterateInDepth(start_node_id = key, visited_nodes = visited_nodes)
        for value in self.nodes_connections[start_node_id]:
            if value not in visited_nodes:
                self.__IterateInDepth(start_node_id = value, visited_nodes = visited_nodes)            
        
    def IterateInDepth(self, start_node_id):
        visited_nodes = []
        self.__IterateInDepth(start_node_id, visited_nodes = visited_nodes)
        return visited_nodes
     
class BinaryTreeNode:
    def __init__(self, node_id, left_child = None, right_child = None):
        self.node_id = node_id
        self.left_child = left_child
        self.right_child = right_child 
    
    def print_node(self):
        result = str(self.node_id) + ", "
        if self.left_child:
            result += str(self.left_child.node_id) + ", "
        else:
            result += "None , "
        if self.right_child:
            result += str(self.right_child.node_id) 
        else:
            result += "None"
        return result

class BinaryTree:        
    def  __init__(self, nodes_qty, shuffle_node_ids = True, tree_type = None):
        if nodes_qty < 1:
            raise ValueError("not enough nodes")
        if shuffle_node_ids:
            nodes_ids = shuffle(nodes_qty)
        else: 
            nodes_ids = range(nodes_qty)
        self.all_nodes = [BinaryTreeNode(node_id) for node_id in nodes_ids]
        
        if tree_type == "rightChildIsChildless":
            if nodes_qty > 1:
                self.all_nodes[0].left_child = self.all_nodes[1]
            if nodes_qty > 2:
                self.all_nodes[0].right_child = self.all_nodes[2]
            node_iter = 1
            while (node_iter + 2) < nodes_qty:
                self.all_nodes[node_iter].left_child = self.all_nodes[node_iter + 2]
                if (node_iter + 3) < nodes_qty:
                    self.all_nodes[node_iter].right_child = self.all_nodes[node_iter + 3]
                node_iter += 2
            return

        if tree_type == "balanced":
            power_of_2 = 1
            while (power_of_2 * 2 - 1) < nodes_qty:
                node_numbers = range(power_of_2 - 1, power_of_2 * 2 - 1)
                child_iter = power_of_2 * 2 - 1
                for node_iter in node_numbers:
                    if (child_iter) < nodes_qty:
                        self.all_nodes[node_iter].left_child = self.all_nodes[child_iter]
                        child_iter += 1
                    else:
                        break
                    if (child_iter) < nodes_qty:
                        self.all_nodes[node_iter].right_child = self.all_nodes[child_iter]  
                        child_iter += 1                  
                    else:
                        break
                power_of_2 *= 2
            return
                            
        child_spaces = [(self.all_nodes[0], False), (self.all_nodes[0], True)]
        for node in self.all_nodes[1:]:
            # randomly pick an available child's space - this will be the node's parent
            indx = random.randint(0, len(child_spaces)-1)
            #print "node", node.node_id, "parent id",  child_spaces[indx][0].node_id, "is right", child_spaces[indx][1], "parent index", indx
            child_space = child_spaces[indx]
            if child_space[1]:
                child_space[0].left_child = node
            else:
                child_space[0].right_child = node 
            del child_spaces[indx] 
            
            #add two child spaces (they are in the new node)
            child_spaces += [(node, False), (node, True)]
        
    def Print(self):
        for node in self.all_nodes:
            print node.print_node()        
    
    def IterateInBreadth(self):
        if not self.all_nodes:
            return []
        visited_nodes_ids = []
        scheduled_nodes = [self.all_nodes[0]]
        scheduled_nodes_ids = [self.all_nodes[0].node_id]
        while scheduled_nodes:
            if scheduled_nodes[0].left_child:
                node_id = scheduled_nodes[0].left_child
                if not (node_id in scheduled_nodes_ids) and not (node_id in visited_nodes_ids):
                    scheduled_nodes.append(scheduled_nodes[0].left_child)
                    scheduled_nodes_ids.append(node_id)
            if scheduled_nodes[0].right_child:
                node_id = scheduled_nodes[0].right_child
                if not (node_id in scheduled_nodes_ids) and not (node_id in visited_nodes_ids):
                    scheduled_nodes.append(scheduled_nodes[0].right_child)
                    scheduled_nodes_ids.append(node_id)
            visited_nodes_ids.append(scheduled_nodes[0].node_id)
            del scheduled_nodes[0]
            del scheduled_nodes_ids[0]
        return visited_nodes_ids

    def __IterateInDepth(self, root):
        if not root:
            return []
        result = [root.node_id]
        result += self.__IterateInDepth(root.left_child)
        result += self.__IterateInDepth(root.right_child)
        return result
    
    def IterateInDepth(self):
        if self.all_nodes:
            return self.__IterateInDepth(self.all_nodes[0])
        return []
    
    def DeepestCommonAncestor(self, node_id_1, node_id_2):
        if self.all_nodes:
            return self.__DeepestCommonAncestor(node_id_1 = node_id_1, node_id_2 = node_id_2, root = self.all_nodes[0])
        return []
    
    def __DeepestCommonAncestor(self, node_id_1, node_id_2, root):
        if (root.node_id == node_id_1) or (root.node_id == node_id_2):
            return root
        left_ancestor = None
        if root.left_child:
            left_ancestor = self.__DeepestCommonAncestor(node_id_1 = node_id_1, node_id_2 = node_id_2, root = root.left_child)
        right_ancestor = None
        if root.left_child:
            right_ancestor = self.__DeepestCommonAncestor(node_id_1 = node_id_1, node_id_2 = node_id_2, root = root.right_child)
        if (not left_ancestor) and (not right_ancestor):
            return None
        if (left_ancestor) and (right_ancestor):
            return root
        if left_ancestor:
            return left_ancestor
        else:
            return right_ancestor

if __name__ == '__main__':
    #random.seed(1000)
    tree = BinaryTree(nodes_qty = 15, shuffle_node_ids = False, tree_type = "balanced")#"rightChildIsChildless")#
    tree.Print()
    x = tree.IterateInBreadth(); print x # x.sort(); 
    x = tree.IterateInDepth(); print x # x.sort(); 
    print tree.DeepestCommonAncestor(8, 14).node_id
    
    g = Graph(number_nodes = 11, max_number_edges = 0.33)
    g.Print()
    print g.IterateInBreadth(8)
    print g.IterateInBreadth(0)
    print g.IterateInDepth(8)
    print g.IterateInDepth(0)
