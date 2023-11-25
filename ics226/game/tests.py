from django.test import TestCase
from .models import Board, Player

#..:*:..:*:..CONSTANTS..:*:..:*:..#
ROW = 10
COLUMN = 10
TILE_NUM = 100
TREASURE_NUM = 5
PLAYER_NUM = 2
MIN_RANGE = 0
MAX_RANGE = 9
PLAYER1 = '1'
PLAYER2 = '2'
TREASURE_DESC = '$'
EMPTY_TILE = '.'
UP = 'u'
LEFT = 'l'
RIGHT = 'r'
DOWN = 'd'
#..:*:..:*:..:*:..:*:..:*:..:*:..#

# Create your tests here.
class PlayerTestCase(TestCase):
    def test_create(self):
        """
        Test objects after creating the board.
        Check list:
        1. number of board objects (10*10, total 100)
        2. number of treasures (total 5)
        3. number of players (total 2)
        """
        Board.objects.all().delete()
        Player.objects.all().delete()
        cr = self.client.post('/game/create/')

        # print(vars(cr))
        b = Board.objects.all()
        self.assertEqual(len(b),TILE_NUM)
        trs = Board.objects.filter(label = TREASURE_DESC)
        # print(trs)
        self.assertEqual(len(trs), TREASURE_NUM)
        plrs = Player.objects.all()
        self.assertEqual(len(plrs), PLAYER_NUM)

    def test_move_prayer(self):
        """
        Test if player's all moving direction to an available tile.
        Place PLAYER1 to top left (0, 0) first, then check right, down, left, up.

        PLAYER2 is removed for testing.
        """
        Board.objects.all().delete()
        Player.objects.all().delete()
        cr = self.client.post('/game/create/')

        p2_board = Board.objects.get(label=PLAYER2)
        p2_board.label = EMPTY_TILE
        p2_board.save()

        p1_pre = Board.objects.get(label=PLAYER1)

        while p1_pre.row > MIN_RANGE:
            response = self.client.post(f'/game/move/{p1_pre.label}/', {'button_id': UP})
            p1_pre = Board.objects.get(label=PLAYER1)

        while p1_pre.col > MIN_RANGE:
            response = self.client.post(f'/game/move/{p1_pre.label}/', {'button_id': LEFT})
            p1_pre = Board.objects.get(label=PLAYER1)

        response = self.client.post(f'/game/move/{p1_pre.label}/', {'button_id': RIGHT})
        p1_now = Board.objects.get(label=PLAYER1)
        self.assertEqual(p1_now.row, p1_pre.row)
        self.assertEqual(p1_now.col, p1_pre.col + 1)

        p1_pre = Board.objects.get(label=PLAYER1)
        response = self.client.post(f'/game/move/{p1_pre.label}/', {'button_id': DOWN})
        p1_now = Board.objects.get(label=PLAYER1)
        self.assertEqual(p1_now.row, p1_pre.row + 1)
        self.assertEqual(p1_now.col, p1_pre.col)

        p1_pre = Board.objects.get(label=PLAYER1)
        response = self.client.post(f'/game/move/{p1_pre.label}/', {'button_id': LEFT})
        p1_now = Board.objects.get(label=PLAYER1)
        self.assertEqual(p1_now.row, p1_pre.row)
        self.assertEqual(p1_now.col, p1_pre.col - 1)

        p1_pre = Board.objects.get(label=PLAYER1)
        response = self.client.post(f'/game/move/{p1_pre.label}/', {'button_id': UP})
        p1_now = Board.objects.get(label=PLAYER1)
        self.assertEqual(p1_now.row, p1_pre.row - 1)
        self.assertEqual(p1_now.col, p1_pre.col)

    def test_out_of_bounds(self):
        """
        Test if player can not move out of bounds.
        Place PLAYER1 at each corner then check if player's attempt to move is ignored.
        Check list:
        1. top-left: UP, LEFT
        2. top-right: UP, RIGHT
        3. bottom-right: DOWN, RIGHT
        4. botton-left: DOWN, LEFT

        PLAYER2 is removed for testing.
        """
        Board.objects.all().delete()
        Player.objects.all().delete()
        cr = self.client.post('/game/create/')

        p2_board = Board.objects.get(label=PLAYER2)
        p2_board.label = EMPTY_TILE
        p2_board.save()

        p1_now = Board.objects.get(label=PLAYER1)

        print('a start')
        while p1_now.row > MIN_RANGE:
            response = self.client.post(f'/game/move/{p1_now.label}/', {'button_id': UP})
            p1_now = Board.objects.get(label=PLAYER1)
        print("test a end")

        print("test b start")
        while p1_now.col > MIN_RANGE:
            response = self.client.post(f'/game/move/{p1_now.label}/', {'button_id': LEFT})
            p1_now = Board.objects.get(label=PLAYER1)
        print("test b end")

        response = self.client.post(f'/game/move/{p1_now.label}/', {'button_id': LEFT})
        p1_now = Board.objects.get(label=PLAYER1)

        self.assertEqual(p1_now.row, MIN_RANGE)
        self.assertEqual(p1_now.col, MIN_RANGE)

        response = self.client.post(f'/game/move/{p1_now.label}/', {'button_id': UP})
        p1_now = Board.objects.get(label=PLAYER1)

        self.assertEqual(p1_now.row, MIN_RANGE)
        self.assertEqual(p1_now.col, MIN_RANGE)

        print("test c start")
        while p1_now.col < MAX_RANGE:
            response = self.client.post(f'/game/move/{p1_now.label}/', {'button_id': RIGHT})
            p1_now = Board.objects.get(label=PLAYER1)

        print("test c end")

        response = self.client.post(f'/game/move/{p1_now.label}/', {'button_id': RIGHT})
        p1_now = Board.objects.get(label=PLAYER1)

        self.assertEqual(p1_now.row, MIN_RANGE)
        self.assertEqual(p1_now.col, MAX_RANGE)

        response = self.client.post(f'/game/move/{p1_now.label}/', {'button_id': UP})
        p1_now = Board.objects.get(label=PLAYER1)

        self.assertEqual(p1_now.row, MIN_RANGE)
        self.assertEqual(p1_now.col, MAX_RANGE)

        print('test d start')
        while p1_now.row < MAX_RANGE:
            response = self.client.post(f'/game/move/{p1_now.label}/', {'button_id': DOWN})
            p1_now = Board.objects.get(label=PLAYER1)
        print('test d end')

        response = self.client.post(f'/game/move/{p1_now.label}/', {'button_id': DOWN})
        p1_now = Board.objects.get(label=PLAYER1)

        self.assertEqual(p1_now.row, MAX_RANGE)
        self.assertEqual(p1_now.col, MAX_RANGE)

        response = self.client.post(f'/game/move/{p1_now.label}/', {'button_id': RIGHT})
        p1_now = Board.objects.get(label=PLAYER1)

        self.assertEqual(p1_now.row, MAX_RANGE)
        self.assertEqual(p1_now.col, MAX_RANGE)

        print('test e start')
        while p1_now.col > MIN_RANGE:
            response = self.client.post(f'/game/move/{p1_now.label}/', {'button_id': LEFT})
            p1_now = Board.objects.get(label=PLAYER1)
        print('test e end')

        response = self.client.post(f'/game/move/{p1_now.label}/', {'button_id': DOWN})
        p1_now = Board.objects.get(label=PLAYER1)

        self.assertEqual(p1_now.row, MAX_RANGE)
        self.assertEqual(p1_now.col, MIN_RANGE)

        response = self.client.post(f'/game/move/{p1_now.label}/', {'button_id': LEFT})
        p1_now = Board.objects.get(label=PLAYER1)

        self.assertEqual(p1_now.row, MAX_RANGE)
        self.assertEqual(p1_now.col, MIN_RANGE)

    def test_players_collide(self):
        """
        Test if a player's moving attempt is ignored if there is already another player
        Place PLAYER1 to top-left(0,0) then place PLAYER2 to the left next(0,1).
        Try moving PLAYER2 to top-left and check their position is same as before the attempt.  
        """
        Board.objects.all().delete()
        Player.objects.all().delete()
        cr = self.client.post('/game/create/')

        p1_board = Board.objects.get(label=PLAYER1)
        p2_board = Board.objects.get(label=PLAYER2)

        p2_board.label = EMPTY_TILE
        p2_board.save()

        print('test f start')
        while p1_board.row > MIN_RANGE:
            response = self.client.post(f'/game/move/{p1_board.label}/', {'button_id': UP})
            p1_board = Board.objects.get(label=PLAYER1)
        print("test f end")

        print("test g start")
        while p1_board.col > MIN_RANGE:
            response = self.client.post(f'/game/move/{p1_board.label}/', {'button_id': LEFT})
            p1_board = Board.objects.get(label=PLAYER1)
        print("test g end")

        p2_board.label = PLAYER2
        p2_board.save()

        print('h start')
        while p2_board.col > MIN_RANGE+1:
            response = self.client.post(f'/game/move/{p2_board.label}/', {'button_id': LEFT})
            p2_board = Board.objects.get(label=PLAYER2)
        print('h start')

        print('i start')
        while p2_board.row > MIN_RANGE:
            response = self.client.post(f'/game/move/{p2_board.label}/', {'button_id': UP})
            p2_board = Board.objects.get(label=PLAYER2)
        print('i end')

        response = self.client.post(f'/game/move/{p2_board.label}/', {'button_id': LEFT})
        p2_board = Board.objects.get(label=PLAYER2)

        print(vars(response))
        self.assertEqual(p1_board.row, MIN_RANGE)
        self.assertEqual(p1_board.col, MIN_RANGE)
        self.assertEqual(p2_board.row, MIN_RANGE)
        self.assertEqual(p2_board.col, MIN_RANGE+1)

    def test_score_update(self):
        """
        Test if treasures are picked up by the player properly.
        Get total value of treasures and move PLAYER1 from top-left to bottom-right.
        then compare the total value and the PLAYER1's score.

        PLAYER2 is removed for testing
        """
        Board.objects.all().delete()
        Player.objects.all().delete()
        cr = self.client.post('/game/create/')

        t_tiles = []
        total_value = 0
        t = Board.objects.filter(label=TREASURE_DESC)
        for tile in t:
            t_tiles.append((tile.row, tile.col))
            total_value += tile.value

        p1_board = Board.objects.get(label=PLAYER1)
        p2_board = Board.objects.get(label=PLAYER2)

        p2_board.label = EMPTY_TILE
        p2_board.save()

        print('j start')
        while p1_board.row > MIN_RANGE:
            response = self.client.post(f'/game/move/{p1_board.label}/', {'button_id': UP})
            p1_board = Board.objects.get(label=PLAYER1)
        print('j end')

        print('k start')
        while p1_board.col > MIN_RANGE:
            response = self.client.post(f'/game/move/{p1_board.label}/', {'button_id': LEFT})
            p1_board = Board.objects.get(label=PLAYER1)
        print('k end')

        for row in range(ROW):
            for col in range(COLUMN):
                while p1_board.row > row:
                    response = self.client.post(f'/game/move/{p1_board.label}/', {'button_id': UP})
                    p1_board = Board.objects.get(label=PLAYER1)

                while p1_board.row < row:
                    response = self.client.post(f'/game/move/{p1_board.label}/', {'button_id': DOWN})
                    p1_board = Board.objects.get(label=PLAYER1)

                while p1_board.col > col:
                    response = self.client.post(f'/game/move/{p1_board.label}/', {'button_id': LEFT})
                    p1_board = Board.objects.get(label=PLAYER1)

                while p1_board.col < col:
                    response = self.client.post(f'/game/move/{p1_board.label}/', {'button_id': RIGHT})
                    p1_board = Board.objects.get(label=PLAYER1)

        p1 = Player.objects.filter(tag=PLAYER1)[0]
        self.assertEqual(p1.score, total_value)