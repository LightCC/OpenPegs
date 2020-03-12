try:
    from .PegNode import PegNode
    from .PegBoard import PegBoard
except ImportError:
    print("\n{}: Try running `pegs` from the command line!!\nor run with `python run_pegs.py` from root directory\n".format(__file__))
    
class PegPyramid(PegBoard):
    def __init__(self):
        node_ids = list(range(1, 16))
        node_ids_str = [ '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' ]
        nodes = {}
        node_dict = { node_id: PegNode(nodes, node_id, node_ids_str[index]) for index, node_id in enumerate(node_ids) }
        nodes.update(node_dict)
        super().__init__(node_ids, node_ids_str)
        self._rows = [
                    [ nodes[1] ],
                    [ nodes[2], nodes[3] ],
                    [ nodes[4], nodes[5], nodes[6] ],
                    [ nodes[7], nodes[8], nodes[9], nodes[10] ],
                    [ nodes[11], nodes[12], nodes[13], nodes[14], nodes[15] ]
                   ]
        self._setup_links()
        self._format_str = self._create_format_str()
    
    def _create_format_str(self):
        ## Create a dict of rows with their lengths
        row_lengths = [ len(row) for row in self._rows ]
        max_nodes_in_row = max(row_lengths)
        ## Now create a string for each row and combine them
        rows = []
        for row in self._rows:
            # Center each row by adding spaces
            row_center_spacing = ' ' * (max_nodes_in_row - len(row))
            rowstr = row_center_spacing
            for node in row:
                node_index = self._node_ids.index(node.node_id())
                rowstr += '{{x[{node_index}]}} '.format(node_index=node_index)
            rowstr += row_center_spacing
            # rowstr will have one extra space at the end from the loop, strip one off
            rows.append(rowstr[:-1])
        # Remove the final '\n' from outstr
        return '\n'.join(rows)
    
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

    def setup_game_board(self, start_node_id_str):
        if start_node_id_str in self._node_ids_str:
            for node in self._nodes.values():
                if start_node_id_str != node.node_id_str():
                    node.set_peg()
            return True
        else: # the node_id_str passed in was not found
            return False
        
    def valid_moves(self):
        moves = []
        for node in self._nodes.values():
            for link in node.links():
                if self.link_has_valid_jump(link):
                    moves.append(link)
        return moves
                
    def link_has_valid_jump(self, link):
        # If start node has a peg, and adjacent node has a peg to jump, and end node is empty to land, then link is valid for a jump
        return all( [link.start_node().peg(), link.adjacent_node().peg(), not link.end_node().peg()] )
    
    def execute_jump_move(self, link):
        if self.link_has_valid_jump(link):
            link.adjacent_node().clear_peg() # Jump over here and remove peg from board
            link.start_node().clear_peg() # Jump from here, peg moves
            link.end_node().set_peg() # peg lands here and fills the spot    
        else:
            if not link.start_node().peg():
                raise ValueError('Link {} is not valid - No peg to jump with in start node {}'.format(link, link.start_node().node_id_str))
            elif not link.adjacent_node().peg():
                raise ValueError('Link {} is not valid - No peg to jump over in adjacent node {}'.format(link, link.adjacent_node().node_id_str))
            if link.end_node().peg():
                raise ValueError('Link {} is not valid - Peg already present in end node {}'.format(link, link.end_node().node_id_str))
