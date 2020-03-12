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
