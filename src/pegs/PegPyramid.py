from typing import List

try:
    from .PegNode import PegNode
    from .PegBoard import PegBoard
    from .PegNodeLink import PegNodeLink
except ImportError:
    print(  #
        "\n"
        "{}: Try running `pegs` from the command line!!"
        "\n"
        "or run with `python run_pegs.py` from root directory"
        "\n"  #
        .format(__file__)
    )


class PegPyramid(PegBoard):

    def __init__(self):

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

        _nodelist = [
            PegNode(1, id_str='1'),
            PegNode(2, id_str='2'),
            PegNode(3, id_str='3'),
            PegNode(4, id_str='4'),
            PegNode(5, id_str='5'),
            PegNode(6, id_str='6'),
            PegNode(7, id_str='7'),
            PegNode(8, id_str='8'),
            PegNode(9, id_str='9'),
            PegNode(10, id_str='a'),
            PegNode(11, id_str='b'),
            PegNode(12, id_str='c'),
            PegNode(13, id_str='d'),
            PegNode(14, id_str='e'),
            PegNode(15, id_str='f'),
        ]
        super().__init__(_nodelist)
        _setup_links(self)  # add the valid links that are legal jumps between nodes
        rows = [
            [self.node(1)],
            [self.node(2), self.node(3)],
            [self.node(4), self.node(5), self.node(6)],
            [self.node(7), self.node(8), self.node(9), self.node(10)],
            [self.node(11), self.node(12), self.node(13), self.node(14), self.node(15)],
        ]
        self.format_str = self._create_format_str(rows)
        self._valid_moves = None

    def __eq__(self, other):
        v1 = vars(self)
        v2 = vars(other)
        if not (v1.keys() == v2.keys()):
            return False
        # for index, var in enumerate(self.__dict__):
        #     if not (var == other.__dict__[index]):
        #         return False
        return True

    def _create_format_str(
        self,
        rows: List[list],  # game board rows, with each row a list of nodes
    ) -> str:  # the layout format str for the board, with {x[index]} at each node location
        """Create the format string for PegPyramid, that is used to print the game board"""
        ## Create a dict of rows with their lengths
        self._rows = rows
        row_lengths = [len(row) for row in rows]
        max_nodes_in_row = max(row_lengths)
        ## Now create a string for each row and combine them
        rows_str = []
        for row in rows:
            # Center each row by adding spaces
            row_center_spacing = ' ' * (max_nodes_in_row - len(row))
            rowstr = row_center_spacing
            for node in row:
                # Just in case the indexes are not deterministic, refigure them
                node_index = self.node_ids.index(node.node_id)
                rowstr += '{{x[{node_index}]}} '.format(node_index=node_index)
            rowstr += row_center_spacing
            # rowstr will have one extra space at the end from the loop, strip one off
            rows_str.append(rowstr[:-1])
            # Remove the final '\n' from outstr
        return '\n'.join(rows_str)

    def _create_link_by_id(self, start_node_id, adjacent_node_id, end_node_id) -> None:
        self.node(start_node_id).add_link(self.node(adjacent_node_id), self.node(end_node_id))

    def setup_game_board(self, start_node) -> bool:
        """Adds pegs to all positions except the given starting node
        
        Args:
            start_node (PegNode): the starting node on the game board.
            start_node (int): a PegNodeId for the starting node
            start_node (str): a PegNodeId string for the starting node
        
        Raises:
            ValueError: start_node is not a PegNode object
            AttributeError: start_node is not a node in this game board
        
        Returns:
            bool: True when board has been setup
        """
        if isinstance(start_node, str):
            start_node = self.node_from_node_id_str(start_node)
        elif start_node in self.node_ids:
            start_node = self.node(start_node)
        if not isinstance(start_node, PegNode):
            ValueError("{} is not a PegNode instance".format(start_node))
        if start_node in self.nodes:
            for node in self.nodes:
                # add a peg if this is not the starting node
                if start_node != node:
                    node.add_peg()
                self._valid_moves = self._find_valid_moves()
            return True
        else:
            raise AttributeError("{} is not a node in the GameBoard")

    def valid_moves(self):
        if self._valid_moves is None:
            self._valid_moves = self._find_valid_moves()
        return self._valid_moves

    def _find_valid_moves(self):
        ## TODO: Optimize this - its a very rough brute force calculation...
        moves = []
        for node in self.nodes:
            for link in node.links:
                if self.link_has_valid_jump(link):
                    moves.append(link)
        return moves

    def link_has_valid_jump(self, link):
        # If start node has a peg, and adjacent node has a peg to jump, and end node is empty to land, then link is valid for a jump
        return all([  #
            link.start_node.peg_is_present,
            link.adjacent_node.peg_is_present,
            not link.end_node.peg_is_present,
        ])

    def execute_jump_move(self, link):
        if self.link_has_valid_jump(link):
            link.adjacent_node.remove_peg()  # Jump over here and remove peg from board
            link.start_node.remove_peg()  # Jump from here, peg moves
            link.end_node.add_peg()  # peg lands here and fills the spot
            self._valid_moves = self._find_valid_moves()
        else:
            if not link.start_node.peg_is_present:
                raise ValueError(  #
                    'Link {} is not valid - No peg to jump with in start node {}'  #
                    .format(link, link.start_node.node_id_str)
                )
            elif not link.adjacent_node.peg_is_present:
                raise ValueError(  #
                    'Link {} is not valid - No peg to jump over in adjacent node {}'  #
                    .format(link, link.adjacent_node.node_id_str)
                )
            if link.end_node.peg_is_present:
                raise ValueError(  #
                    'Link {} is not valid - Peg already present in end node {}'  #
                    .format(link, link.end_node.node_id_str)
                )

    def board_id(self):
        """board_id provides a unique id for this board based on the current game board status
        
        board_id can be used to recreate the current board state, as a shorthand way of saving the board status, or determining if this board_state is already in the analysis database
        """
        pegs = self.pegs
        board_id = 0
        for index, peg in enumerate(pegs.values()):
            if peg.peg:
                board_id += (1 << index)
        return board_id

    def set_to_board_id(self, board_id):
        temp_board_id = board_id
        pegs = {}
        max_index = len(self.node_ids) - 1
        for index, node_id in enumerate(reversed(self.node_ids)):
            reversed_index = max_index - index
            value_of_this_node_id = (1 << reversed_index)
            if temp_board_id >= (value_of_this_node_id):
                temp_board_id -= value_of_this_node_id
                pegs.update({node_id: True})
            else:
                pegs.update({node_id: False})
        self.pegs = pegs

    def analyze_current_game_board(self) -> List[PegNodeLink]:
        valid_paths: List[PegNodeLink] = []
        # TODO: Need to make a copy of the board, and actually complete the moves on it to find the full path.

        # TODO: this will only work for a board that only has one move left...
        if self.count_nodes_with_pegs() == 2:
            return self.valid_moves()
        else:
            ## return an empty list if we couldn't analyze the board
            return []
