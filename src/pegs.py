try:
    from .PegPyramid import PegPyramid
except ImportError:
    print("\n{}: Try running `pegs` from the command line!!\nor run with `python run_pegs.py` from root directory\n".format(__file__))

def main():
    print("Running Pegs Game...")
    pyramid = PegPyramid()
    print('\n'
          'Nodes on board:')
    print(pyramid.nodes_str(3))
    print('\nNo Pegs!!')
    print(pyramid.pegs_str(3))
    
    print('\nAdd a few pegs:')
    pyramid.node(1).set_peg()
    pyramid.node(5).set_peg()
    pyramid.node(15).set_peg()
    print(pyramid.pegs_str(3))
    print('\nFull Node output:')
    print(pyramid.full_str(3))
    print('\nNodes and Pegs output:')
    print(pyramid.node_and_pegs_str(3))