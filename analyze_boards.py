import sys
from src.pegs.PegPyramidAnalyzer import PegPyramidAnalyzer
from src.pegs.PegPyramid import PegPyramid
from src.pegs.PegNodeLink import PegNodeLink

ppa = PegPyramidAnalyzer()
total_moves = 0
for node_id in range(15):
    ppa._board_moves_db = {}
    ppa.test.setup_game_board_from_initial_node(node_id)
    print(  #
        f'Analyzing board with starting node {node_id}..\n'
        f'{ppa.test.pegs_string(indent=5)}'
        '\n'
    )
    starting_board_id = ppa.test.board_id
    ppa.get_all_indiv_board_moves(starting_board_id)
    boards_with_1_peg_left = ppa._board_moves_db[1]
    total_moves_this_node = ppa.move_count_in_board_db
    total_moves += total_moves_this_node
    print(  #
        f'  - Node {node_id}: Total Moves in db: this {total_moves_this_node} / all {total_moves}'
        '\n'
    )
    for board in boards_with_1_peg_left:
        print(f'  - Node {node_id}: Final board with one peg: {board}, Pegs {list( i for i, x in enumerate(board) if x)}')
        if board[4]:
            print(  #
                '\n'
                '         ---- ==== CENTER PEG!!! ==== ----\n'
            )
    print()

    # print(  #
    #     '\n'
    #     f'SIZE OF DB: {sys.getsizeof(ppa._board_moves_db)}\n'
    # )
