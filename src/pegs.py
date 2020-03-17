try:
    from .PegPyramid import PegPyramid
except ImportError:
    print("\n{}: Try running `pegs` from the command line!!\nor run with `python run_pegs.py` from root directory\n".format(__file__))

def main():
    indent = 3
    print("Running Pegs Game...")
    pyramid = PegPyramid()
    print('\n'
          'Game board node names, but no pegs!!')
    print(pyramid.node_and_pegs_str(indent))
    
    ## Setup the game board
    valid_start_node = False
    while valid_start_node == False:
        start_node = input('\nStart: Which node on left should be empty? ')
        valid_start_node = pyramid.setup_game_board(start_node)
    print('\n'
          'All Nodes but Start Node filled')
    print(pyramid.node_and_pegs_str(indent))
    
    ## Begin play
    remaining_moves = True
    
    ## Evaluate available moves
    while remaining_moves:
        remaining_moves = pyramid.valid_moves()
        ## If there are available moves, print them and have user select one
        if remaining_moves:
            print('\nValid Remaining Moves:')
            for index, available_move in enumerate(remaining_moves):
                print('  Move #{}: {}'.format(index, available_move))
            print('')
            selected_move = None
            while selected_move == None:
                move_str = input('Which move will you make? ')
                try:
                    move_index = int(move_str)
                    if move_index < 0 or move_index > index:
                        raise ValueError
                    selected_move = remaining_moves[move_index]
                except:
                    if len(remaining_moves) == 1:
                        valid_range = '0'
                    else:
                        valid_range = '0 to {}'.format(len(remaining_moves) - 1)
                    print('ERROR!! Invalid selection... must be {}!'.format(valid_range))
                    continue
            # A valid move was picked, execute it
            pyramid.execute_jump_move(selected_move)
            print('\n  Peg in {} jumped to {}, removing {}'.format(selected_move.start_node().node_id(), selected_move.end_node().node_id(), selected_move.adjacent_node().node_id()))
            print('')
            print(pyramid.node_and_pegs_str(3))
        else:
            valid_moves_remain = False

    ## No more available moves, game is done!
    pegs = sum(node.peg() for node in pyramid.nodes().values())
    print('\n'
          'No moves available:')
    print('\n'
          '  You finished the game with {} remaining pegs'.format(pegs))
    if pegs >= 4:
        print('  It takes someone special to leave that many pegs on the board!!')
    elif pegs == 3:
        print('  I can do that well with random moves!!')
    elif pegs == 2:
        print('\n'
              '  You might be getting the hang of this!!\n'
              '  But you can still do better...')
    elif pegs == 1:
        print('\n'
              '  What? You solved it?!\n'
              '  We worship the ground you walk on!!\n'
              '  But can you do it again...')
    else:
        Exception('Not a possible outcome - someone cheated! (or someone didn\'t program right...)')
    
    ## Pause for user to press enter, so that window will not disappear if run directly from *.exe
    input('\n=== PRESS ENTER TO END GAME ===')
                
if __name__ == '__main__':
    main()
