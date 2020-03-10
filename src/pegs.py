from PegNode import PegNode

class PegPyramid:
    def __init__(self):
        
        self._node_ids = list(range(1, 16))
        self._node_ids_str = [ '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' ]
        self._nodes = {}
        nodedict = { node_id: PegNode(self._nodes, node_id, self._node_ids_str[index]) for index, node_id in enumerate(self._node_ids)}
        self._nodes.update(nodedict)
        self._rows = [
                    [ self._nodes[1] ],
                    [ self._nodes[2], self._nodes[3] ],
                    [ self._nodes[4], self._nodes[5], self._nodes[6] ],
                    [ self._nodes[7], self._nodes[8], self._nodes[9], self._nodes[10] ],
                    [ self._nodes[11], self._nodes[12], self._nodes[13], self._nodes[14], self._nodes[15] ]
                   ]
        self._setup_links()
        self._format_str = self._create_format_str()
    
    def node(self, node_id):
        return self._nodes[node_id]
        
    def nodes(self):
        return _nodes

    def nodes_str(self, indent=0):
        outstr = self._format_str.format(x=self._node_ids_str)
        return self._indent_string(outstr, indent)
    
    def _indent_string(self, text, indent):
        spaces = ' ' * indent
        outstr = ''.join([spaces + line + '\n' for line in text.splitlines()])
        return outstr[:-1]
    
    def _create_format_str(self):
        ## Create a dict of rows with their lengths
        row_lengths = [ len(row) for row in self._rows ]
        max_nodes_in_row = max(row_lengths)
        ## Now create a string for each row and combine them
        outstr = ''
        for row in self._rows:
            # Center each row by adding spaces
            rowstr = ' ' * (max_nodes_in_row - len(row))
            for node in row:
                node_index = self._node_ids.index(node.node_id())
                rowstr += '{{x[{node_index}]}} '.format(node_index=node_index)
            outstr += rowstr[:-1] + '\n'
        # Remove the final '\n' from outstr
        return outstr[:-1]
    
    
    def _setup_links(self):
        self._create_link_by_id(1, 2, 4)
        self._create_link_by_id(1, 3, 6)
        self._create_link_by_id(2, 4, 7)
        self._create_link_by_id(2, 5, 9)
        self._create_link_by_id(3, 5, 8)
        self._create_link_by_id(3, 6, 10)
        self._create_link_by_id(4, 2, 1)
        self._create_link_by_id(4, 5, 6)
        self._create_link_by_id(4, 7, 11)
        self._create_link_by_id(4, 8, 13)
        self._create_link_by_id(5, 8, 12)
        self._create_link_by_id(5, 9, 14)
        self._create_link_by_id(6, 3, 1)
        self._create_link_by_id(6, 5, 4)
        self._create_link_by_id(6, 9, 13)
        self._create_link_by_id(6, 10, 15)
        self._create_link_by_id(7, 4, 2)
        self._create_link_by_id(7, 8, 9)
        self._create_link_by_id(8, 5, 3)
        self._create_link_by_id(8, 9, 10)
        self._create_link_by_id(9, 5, 2)
        self._create_link_by_id(9, 8, 7)
        self._create_link_by_id(10, 6, 3)
        self._create_link_by_id(10, 9, 8)
        self._create_link_by_id(11, 7, 4)
        self._create_link_by_id(11, 12, 13)
        self._create_link_by_id(12, 8, 5)
        self._create_link_by_id(12, 13, 14)
        self._create_link_by_id(13, 8, 4)
        self._create_link_by_id(13, 9, 6)
        self._create_link_by_id(13, 12, 11)
        self._create_link_by_id(13, 14, 15)
        self._create_link_by_id(14, 9, 5)
        self._create_link_by_id(14, 13, 12)
        self._create_link_by_id(15, 10, 6)
        self._create_link_by_id(15, 14, 13)
        
    def _create_link_by_id(self, start_node_id, adjacent_node_id, end_node_id):
        self._nodes[start_node_id].add_link(self.node(adjacent_node_id), self.node(end_node_id))

def main():
    print("Running Pegs Game...")
    pyramid = PegPyramid()
    print('\n'
          'Nodes on board:')
    print(pyramid.nodes_str(3))
    
if __name__ == '__main__':
    main()
