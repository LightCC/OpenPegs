try:
    from .PegPyramid import PegPyramid
    from .PegNodeLink import PegNodeLink
except ImportError:
    print("\n"  #
            "{}: Try running `pegs` from the command line!!"  #
            "\n"  #
            "or run with `python run_pegs.py` from root directory\n"  #
            .format(__file__))


def main():

    def setup_new_game():
        """Create a new game board, ask user which position to leave open, and setup board
        
        Returns:
            PegPyramid -- a new game board setup per user input
        """
        ## Setup the game board
        new_pyramid = PegPyramid()
        valid_start_node = False
        while valid_start_node == False:
            print(new_pyramid.nodes_string(indent=3))
            start_node_str = input('\nWhich position should be empty to start with? ')
            try:
                start_node = new_pyramid.node_from_node_str(start_node_str)
                new_pyramid.setup_game_board_from_initial_node(start_node)
                valid_start_node = True
            except Exception:
                print( \
                    "\n"
                    "Error!! Invalid Entry - must be 1-9 or a-f")
        print( \
            '\n'
            'All Nodes but "{}" filled with a peg. Begin!'
            .format(start_node_str))
        print(new_pyramid.node_and_pegs_string(indent))
        return new_pyramid

    def handle_end_of_game(game_board):
        """Evaluate the status at the end of the game and report results to user.
        
        Arguments:
            game_board<PegPyramid>: a game_board that is ready for final evaluation
            
        Returns:
            (result_str): result_str to print for user
        """
        remaining_pegs = game_board.count_pegs()
        outstr = (  #
            '\n'
            'No moves available:\n'
            '\n'
            '  You finished the game with {} remaining pegs\n'.format(remaining_pegs)
        )
        if remaining_pegs >= 4:
            outstr += '  It takes someone special to leave that many pegs on the board!!'
        elif remaining_pegs == 3:
            outstr += '  I can do that well with random moves!!'
        elif remaining_pegs == 2:
            outstr += (  #
                '\n'
                '  You might be getting the hang of this!!\n'
                '  But you can still do better...'
            )
        elif remaining_pegs == 1:
            outstr += (  #
                '\n'
                '  What? You solved it?!\n'
                '  We worship the ground you walk on!!\n'
                '  But can you do it again...'
            )
        else:
            Exception('Not a possible outcome - someone cheated! (or someone didn\'t program something right...)')
        return outstr

    def get_command_or_move_from_user():
        """Asks the user which move to make and accepts a move # or a separate command
        
        Returns:
            [None] -- [If command was not valid]
            [str] -- [indicates individual command, i.e. 'analyze']
            [PegNodeLink] -- [if an available move is selected, the node link to use for a jump]
        """
        move_str = input('Which move will you make (or "a" to analyze)? ')
        try:
            if move_str[:1] == 'a':
                command = 'analyze'
                move_index = -1
            else:
                move_index = int(move_str)
                if move_index < 0 or move_index > index:
                    raise ValueError
                command = available_moves[move_index]
            return command
        except:
            # Issue with user input - command not recognized
            if len(available_moves) == 1:
                valid_range_str = '0 (or "a")'
            else:
                valid_range_str = '0 to {} (or "a")'.format(len(available_moves) - 1)
            print('ERROR!! Invalid selection... must be {}!'.format(valid_range_str))
            return None

    def execute_command(command, game_board=None):
        """Using the game_board, execute a given command
        
        Arguments:
            game_board {PegPyramid} -- a PegPyramid game board
            command {str, PegNodeLink} -- if a string, execute the specific command; if a PegNodeLink, execute it as a legal jump move on the game_board
            
        Returns:
            {string} -- output for the console for execution of the command
        """
        outstr = ''
        if command == 'analyze':
            results = pyramid.analyze_current_game_board()
            outstr += (  #
                '\n'
                'Need to print results of analysis!!!\n'
                '\n'
            )
        elif isinstance(command, PegNodeLink):
            game_board.execute_jump_move(command)
            outstr += (  #
                '\n'
                '  Peg in {} jumped to {}, removing {}'
                '\n'  #
                .format(
                    command.start,
                    command.end,
                    command.adjacent,
                )
            )
            outstr += pyramid.node_and_pegs_string(indent=3)
        else:
            raise ValueError('{} of type {} is not a valid game command'.format(command, type(command)))
        return outstr

    ### START OF MAIN FUNCTION ###
    indent = 3
    print("Running Pegs Game...")

    ## Begin play
    pyramid = setup_new_game()
    available_moves = True
    while available_moves:
        ## TODO: clean this up in the future so we don't reanalyze the moves if we didn't change the board
        available_moves = pyramid.valid_moves
        ## If there are available moves, print them and have user enter a move # or a command
        if available_moves:
            print('\nValid Remaining Moves:')
            for index, available_move in enumerate(available_moves):
                print('  Move #{}: {}'.format(index, available_move))
            print('')
            selected_command = None
            while selected_command is None:
                selected_command = get_command_or_move_from_user()
            ## A valid move was picked, execute it
            print(execute_command(selected_command, game_board=pyramid))

    ## No more available moves, game is done!
    print(handle_end_of_game(pyramid))
    input('\n=== PRESS ENTER TO END GAME ===')


if __name__ == '__main__':
    main()
