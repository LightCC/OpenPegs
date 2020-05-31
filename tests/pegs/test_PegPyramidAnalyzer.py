import pytest
from src.pegs.PegPyramidAnalyzer import PegPyramidAnalyzer, PegMove, MoveChain, FoundChain
from src.pegs.PegPyramid import PegPyramid, PyramidId
from src.pegs.PegNodeLink import PegNodeLink


@pytest.fixture()
def sut():
    yield PegPyramidAnalyzer()


@pytest.fixture()
def boards():
    boards = {
        'empty': PyramidId.make(*([False] * 15)),
        'full': PyramidId.make(*([True] * 15)),
        '0-1-2': PyramidId.make(' x xx ooo oooo ooooo '),
        '2-3': PyramidId.make('o ox xoo ooooooooo'),
        '1-5': PyramidId.make('oxoooxooooooooo'),
    }
    yield boards


class TestPegMove:

    def test_PegMove_init(self):
        move1 = PegMove(PegNodeLink(1, 2, 5), PyramidId.make('o ox xoo oooo ooooo'))
        assert str(move1) == f'PegMove(1->2->5->Pyr(o ox xoo oooo ooooo))'
        move2 = PegMove(link=PegNodeLink(2, 3, 4), idx=PyramidId.make('ooxxooooooxxxxx'))
        assert str(move2) == f'PegMove(2->3->4->Pyr(o ox xoo oooo xxxxx))'
        move3 = PegMove()
        assert move3.link is None
        assert move3.idx is None


class TestPegBoardAnalyzer:

    def test_analyzer_base_setup(self, sut, boards):
        PegPyramidAnalyzer._board_moves_db == None
        # sut = PegPyramidAnalyzer()
        sut._board_moves_db == {}
        sut.test.board_id == boards['empty']

    def test_move_is_valid(self, sut, boards):
        # sut = PegPyramidAnalyzer()
        assert sut.move_is_valid(boards['0-1-2'], PegNodeLink(0, 1, 3))
        assert sut.move_is_valid(boards['0-1-2'], PegNodeLink(0, 2, 5))
        assert not sut.move_is_valid(boards['0-1-2'], PegNodeLink(5, 4, 3))
        assert not sut.move_is_valid(boards['0-1-2'], PegNodeLink(1, 3, 6))
        assert not sut.move_is_valid(boards['0-1-2'], PegNodeLink(6, 3, 1))

    def test_find_valid_moves(self, sut, boards):
        moves = sut.find_valid_moves(boards['0-1-2'])
        assert moves == {PegNodeLink(0, 1, 3), PegNodeLink(0, 2, 5)}

    def test_get_board_from_move(self, sut, boards):
        board_id = sut.get_board_from_move(boards['0-1-2'], PegNodeLink(0, 1, 3))
        assert board_id == boards['2-3']
        with pytest.raises(ValueError):
            board_id = sut.get_board_from_move(boards['2-3'], PegNodeLink(7, 8, 9))

    def test_get_current_board_moves(self, sut, boards):
        moves = sut.get_current_board_moves(boards['0-1-2'])
        assert moves == {
            PegNodeLink(0, 1, 3): boards['2-3'],
            PegNodeLink(0, 2, 5): boards['1-5'],
        }

    def test_get_all_indiv_board_moves_quick(self, sut, boards):
        sut.get_all_indiv_board_moves(boards['0-1-2'])
        move_db = sut._board_moves_db
        peg_count_list = [peg_count for peg_count in move_db.keys()]
        moves_3 = move_db[3]
        moves_2 = move_db[2]
        assert sut.move_count_in_board_db == 2
        assert set(peg_count_list) == set((3, 2))
        assert len(moves_3) == 1
        assert moves_3[boards['0-1-2']] == {
            PegNodeLink(0, 2, 5): boards['1-5'],
            PegNodeLink(0, 1, 3): boards['2-3'],
        }
        assert len(moves_2) == 2
        assert moves_2[boards['1-5']] == {}
        assert moves_2[boards['2-3']] == {}

    # @pytest.mark.slow
    def test_get_all_indiv_board_moves_slow(self, sut, boards):
        board = PegPyramid(initial_node=0)
        sut.get_all_indiv_board_moves(board.board_id)
        assert sut.move_count_in_board_db == 10306

    def test_get_all_indiv_board_moves_recursion_error(self, sut, boards):
        board = PegPyramid(initial_node=0)
        with pytest.raises(RecursionError):
            ## Start with just enough recursion to trigger a Recursion error
            sut.get_all_indiv_board_moves(board.board_id, _recursion=2)

    def test_get_all_move_chains_quick(self, sut, boards):
        setup_info = (
            """
            ## Start with board_id = PyramidId.make('x xx xxx xxxx xxoxx'), which allows getting to the perfect end board.
            # Create the move database, then find all boards with the perfect end board Pyr(o oo oxo oooo ooooo'),
            # The found_moves chain will be 1550 entries. Choosing the first entry, the move chain will have the following moves:
            found_chains[0].chain.chain[0] = PegMove(None->Pyr(x xx xxx xxxx xxoxx))
            # 7 more intermediate moves, then
            found_chains[0].chain.chain[8] = PegMove(11->12->13->Pyr(o ox xox oxxo oooxo))
            found_chains[0].chain.chain[9] = PegMove(3->7->12->Pyr(o ox oox ooxo ooxxo))
            found_chains[0].chain.chain[10] = PegMove(13->12->11->Pyr(o ox oox ooxo oxooo))
            found_chains[0].chain.chain[11] = PegMove(2->5->9->Pyr(o oo ooo ooxx oxooo))
            found_chains[0].chain.chain[12] = PegMove(9->8->7->Pyr(o oo ooo oxoo oxooo))
            found_chains[0].chain.chain[13] = PegMove(11->7->4->Pyr(o oo oxo oooo ooooo)) # Perfect game ending point
            
            # Here are the final stats on several of these, that can be used for a shorter test to generating all moves from a starting board
            # Using chain[8].idx board as the starting point,
            #    the final move chain database has 83 total MoveChains, and 5 chains that will resolve to the perfect game board:
            #    which are indexes: [45, 53, 54, 75, and 76] in found_chains
            # Using chain[9].idx as the starting point,
            #    the final move chain database has 24 total MoveChains, and 3 chains that will resolve to the perfect game board:
            #    which are indexes: [11, 19, 20] in the found_chains
            # Using chain[10].idx as the starting point,
            #    the final move chain database has 4 total MoveChains, and 1 chains that will resolve to the perfect game board:
            #    which is index: [3]
        """
        )

        expected_found_chains = {
            'final_board_4':
                "FoundChain(index=3, chain=MoveChain(end_pegs=1, len=4, PegMove(None->Pyr(o ox oox ooxo oxooo)), PegMove(2->5->9->Pyr(o oo ooo ooxx oxooo)), PegMove(9->8->7->Pyr(o oo ooo oxoo oxooo)), PegMove(11->7->4->Pyr(o oo oxo oooo ooooo))))",  # for final board is Pyr(o oo oxo oooo ooooo)
            'pegs 1':
                "FoundChain(index=3, chain=MoveChain(end_pegs=1, len=4, PegMove(None->Pyr(o ox oox ooxo oxooo)), PegMove(2->5->9->Pyr(o oo ooo ooxx oxooo)), PegMove(9->8->7->Pyr(o oo ooo oxoo oxooo)), PegMove(11->7->4->Pyr(o oo oxo oooo ooooo))))",
            'pegs 2-0':
                "FoundChain(index=0, chain=MoveChain(end_pegs=2, len=3, PegMove(None->Pyr(o ox oox ooxo oxooo)), PegMove(5->8->12->Pyr(o ox ooo oooo oxxoo)), PegMove(11->12->13->Pyr(o ox ooo oooo oooxo))))",
            'pegs 2-1':
                "FoundChain(index=1, chain=MoveChain(end_pegs=2, len=3, PegMove(None->Pyr(o ox oox ooxo oxooo)), PegMove(5->8->12->Pyr(o ox ooo oooo oxxoo)), PegMove(12->11->10->Pyr(o ox ooo oooo xoooo))))",
            'pegs 3': "FoundChain(index=2, chain=MoveChain(end_pegs=3, len=2, PegMove(None->Pyr(o ox oox ooxo oxooo)), PegMove(5->2->0->Pyr(x oo ooo ooxo oxooo))))",  # for remaining pegs = 3
        }

        start_board = PyramidId.make('o ox oox ooxo oxooo')
        mdb = sut.get_all_move_chains(start_board)
        db = sut.board_moves_db
        assert len(db) == 4
        assert list(db.keys()) == [4, 3, 2, 1]
        assert db[1] == {PyramidId.make('o oo oxo oooo ooooo'): {}}
        end_board = PyramidId.make('o oo oxo oooo ooooo')
        found_chains = sut.find_move_chains(end_board_id=end_board)
        assert len(found_chains) == 1
        assert found_chains[0].index == 3
        assert str(found_chains[0]) == expected_found_chains['final_board_4']
        found_chains_pegs_1 = sut.find_move_chains(remaining_pegs=1)
        assert len(found_chains_pegs_1) == 1
        assert str(found_chains_pegs_1[0]) == expected_found_chains['pegs 1']
        found_chains_pegs_2 = sut.find_move_chains(remaining_pegs=2)
        assert len(found_chains_pegs_2) == 2
        assert str(found_chains_pegs_2[0]) == expected_found_chains['pegs 2-0']
        assert str(found_chains_pegs_2[1]) == expected_found_chains['pegs 2-1']
        found_chains_pegs_3 = sut.find_move_chains(remaining_pegs=3)
        assert len(found_chains_pegs_3) == 1
        assert str(found_chains_pegs_3[0]) == expected_found_chains['pegs 3']

    #  @pytest.mark.slow
    def test_get_all_move_chains_slow(self, sut, boards):
        board = PegPyramid(initial_node=12)
        mdb = sut.get_all_move_chains(board.board_id)
        assert len(mdb) == 1149568
        db = sut.board_moves_db
        assert len(db) == 14

        end_board = PyramidId.make('o oo oxo oooo ooooo')  # board with peg in middle as end board
        found_chains = sut.find_move_chains(end_board_id=end_board)
        assert len(found_chains) == 1550
        assert str(
            found_chains[0]
        ) == "FoundChain(index=636026, chain=MoveChain(end_pegs=1, len=14, PegMove(None->Pyr(x xx xxx xxxx xxoxx)), PegMove(10->11->12->Pyr(x xx xxx xxxx ooxxx)), PegMove(13->12->11->Pyr(x xx xxx xxxx oxoox)), PegMove(5->8->12->Pyr(x xx xxo xxox oxxox)), PegMove(14->9->5->Pyr(x xx xxx xxoo oxxoo)), PegMove(1->4->8->Pyr(x ox xox xxxo oxxoo)), PegMove(6->3->1->Pyr(x xx oox oxxo oxxoo)), PegMove(0->1->3->Pyr(o ox xox oxxo oxxoo)), PegMove(11->12->13->Pyr(o ox xox oxxo oooxo)), PegMove(3->7->12->Pyr(o ox oox ooxo ooxxo)), PegMove(13->12->11->Pyr(o ox oox ooxo oxooo)), PegMove(2->5->9->Pyr(o oo ooo ooxx oxooo)), PegMove(9->8->7->Pyr(o oo ooo oxoo oxooo)), PegMove(11->7->4->Pyr(o oo oxo oooo ooooo))))"

        found_chains_1_peg = sut.find_move_chains(remaining_pegs=1)
        assert len(found_chains_1_peg) == 85258
        assert str(
            found_chains_1_peg[0]
        ) == "FoundChain(index=492, chain=MoveChain(end_pegs=1, len=14, PegMove(None->Pyr(x xx xxx xxxx xxoxx)), PegMove(5->8->12->Pyr(x xx xxo xxox xxxxx)), PegMove(14->9->5->Pyr(x xx xxx xxoo xxxxo)), PegMove(12->13->14->Pyr(x xx xxx xxoo xxoox)), PegMove(1->4->8->Pyr(x ox xox xxxo xxoox)), PegMove(6->3->1->Pyr(x xx oox oxxo xxoox)), PegMove(0->1->3->Pyr(o ox xox oxxo xxoox)), PegMove(3->7->12->Pyr(o ox oox ooxo xxxox)), PegMove(11->12->13->Pyr(o ox oox ooxo xooxx)), PegMove(2->5->9->Pyr(o oo ooo ooxx xooxx)), PegMove(14->9->5->Pyr(o oo oox ooxo xooxo)), PegMove(5->8->12->Pyr(o oo ooo oooo xoxxo)), PegMove(13->12->11->Pyr(o oo ooo oooo xxooo)), PegMove(10->11->12->Pyr(o oo ooo oooo ooxoo))))"
