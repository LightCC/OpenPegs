try:
    from .PegNode import PegNode
    from .PegBoard import PegBoard
except ImportError:
    print("\n{}: Try running `pegs` from the command line!!\nor run with `python run_pegs.py` from root directory\n".format(__file__))
    
class PegPyramid(PegBoard):
    def __init__(self):
        nodelist = [PegNode(node_id= 1, node_id_str='1'),
                    PegNode(node_id= 2, node_id_str='2'),
                    PegNode(node_id= 3, node_id_str='3'),
                    PegNode(node_id= 4, node_id_str='4'),
                    PegNode(node_id= 5, node_id_str='5'),
                    PegNode(node_id= 6, node_id_str='6'),
                    PegNode(node_id= 7, node_id_str='7'),
                    PegNode(node_id= 8, node_id_str='8'),
                    PegNode(node_id= 9, node_id_str='9'),
                    PegNode(node_id= 10, node_id_str='a'),
                    PegNode(node_id= 11, node_id_str='b'),
                    PegNode(node_id= 12, node_id_str='c'),
                    PegNode(node_id= 13, node_id_str='d'),
                    PegNode(node_id= 14, node_id_str='e'),
                    PegNode(node_id= 15, node_id_str='f')]
        super().__init__(nodelist)
        self._setup_links() # add the valid links that are legal jumps between nodes
        rows = [[ self.node(1) ],
                [ self.node(2), self.node(3) ],
                [ self.node(4), self.node(5), self.node(6) ],
                [ self.node(7), self.node(8), self.node(9), self.node(10) ],
                [ self.node(11), self.node(12), self.node(13), self.node(14), self.node(15) ]]
        self._format_str = self._create_format_str(rows)
    
    def _create_format_str(self, rows):
        ## Create a dict of rows with their lengths
        self._rows = rows
        row_lengths = [ len(row) for row in rows ]
        max_nodes_in_row = max(row_lengths)
        ## Now create a string for each row and combine them
        rows_str = []
        for row in rows:
            # Center each row by adding spaces
            row_center_spacing = ' ' * (max_nodes_in_row - len(row))
            rowstr = row_center_spacing
            for node in row:
                # Just in case the indexes are not deterministic, refigure them
                node_index = self.node_ids().index(node.node_id())
                rowstr += '{{x[{node_index}]}} '.format(node_index=node_index)
            rowstr += row_center_spacing
            # rowstr will have one extra space at the end from the loop, strip one off
            rows_str.append(rowstr[:-1])
        # Remove the final '\n' from outstr
        return '\n'.join(rows_str)
    
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
        self.node(start_node_id).add_link(self.node(adjacent_node_id), self.node(end_node_id))

    def setup_game_board(self, start_node_id_str):
        if start_node_id_str in self._node_ids_str:
            for node in self.nodes():
                if start_node_id_str != node.node_id_str():
                    node.add_peg()
                self._current_valid_moves = self._find_valid_moves()
            return True
        else: # the node_id_str passed in was not found
            return False
    
    def current_valid_moves(self):
        try:
            return self._current_valid_moves
        except AttributeError:
            self._current_valid_moves = self._find_valid_moves()
            return self._current_valid_moves
    
    def _find_valid_moves(self):
        ## TODO: Optimize this - its a very rough brute force calculation...
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
            link.adjacent_node().remove_peg() # Jump over here and remove peg from board
            link.start_node().remove_peg() # Jump from here, peg moves
            link.end_node().add_peg() # peg lands here and fills the spot
            self._current_valid_moves = self._find_valid_moves()    
        else:
            if not link.start_node().peg():
                raise ValueError('Link {} is not valid - No peg to jump with in start node {}'.format(link, link.start_node().node_id_str))
            elif not link.adjacent_node().peg():
                raise ValueError('Link {} is not valid - No peg to jump over in adjacent node {}'.format(link, link.adjacent_node().node_id_str))
            if link.end_node().peg():
                raise ValueError('Link {} is not valid - Peg already present in end node {}'.format(link, link.end_node().node_id_str))

    def analyze_current_game_board(self):
        valid_paths = []
        # TODO: Need to make a copy of the board, and actually complete the moves on it to find the full path.

        # TODO: this will only work for a board that only has one move left...
        if sum(self.pegs().values()) == 2:
            return self.current_valid_moves()
