from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .models import Player, Board
from random import randrange

#..:*:..:*:..CONSTANTS..:*:..:*:..#
ROW = 10
COLUMN = 10
TREASURE_NUM = 5
PLAYER_NUM = 2
MIN_VAL = 1
MAX_VAL = 5
MIN_RANGE = 0
MAX_RANGE = 9
PLAYER1 = '1'
PLAYER2 = '2'
TREASURE_DESC = '$'
EMPTY_TILE = '.'
#..:*:..:*:..:*:..:*:..:*:..:*:..#

@transaction.atomic
def index(request):
    return HttpResponse('Hello world!')

def greet(request, name):
    return render(request, 'game/button.html', {'name': name})
    # return HttpResponse(f'Hello {name}')

@transaction.atomic
def create_board(request):
    """
    Creates a new board after deleting the previous board everytime called
    Plants treasures randomly on the board if there's no treasure.
    Then creates 2 Players and place them on a random point which is not occupied by the other player.
    Once the board created, the message instructs url to play the game.
    """
    Board.objects.all().delete()
    Player.objects.all().delete()

    for r in range(ROW):
        for c in range(COLUMN):
            Board.create_board(r, c).save()

    t = 0
    while t < TREASURE_NUM:
        trs_val = randrange(MIN_VAL, MAX_VAL+1)

        x = randrange(ROW)
        y = randrange(COLUMN)

        tile = Board.objects.filter(row=x, col=y)[0]
        if tile.value == 0:
            tile.value = trs_val
            tile.label = TREASURE_DESC
            tile.save()
            # print(tile.label, tile.row, tile.col)
            t += 1

    p_id = 1
    while p_id <= PLAYER_NUM:
        x = randrange(ROW)
        y = randrange(COLUMN)

        tile = Board.objects.filter(row=x, col=y)[0]
        if tile.label == EMPTY_TILE or tile.label == TREASURE_DESC:
            tile.label = str(p_id)
            Player.create_player(str(p_id), x, y).save()
            p = Player.objects.filter(tag=str(p_id))[0]
            p.score = tile.value
            tile.value = 0
            tile.save()
            p_id += 1

    return HttpResponse("Board is created. Go to '127.0.0.1:8000/game/' to play")

import pdb
@transaction.atomic
def show_board(request):
    """
    Calls board and player's information and render the html by packaging them

    """
    board_list = get_board(request)
    player_list = get_all_players(request)
    # pdb.set_trace()
    context = {'board_list': board_list, 'player_list': player_list}
    return render(request, 'game/board_form.html', context)

@transaction.atomic
def get_board(request):
    """
    Returns board objects in row and column order
    """
    query = Board.objects.all().order_by('row', 'col')
    board_list = []
    for b in query:
        board_list.append(b)
        # print(b.row, b.col)
    return board_list

@transaction.atomic
def get_player(request, player_id: int):
    """
    Gets a specific player's object by their ID and calls the board and the players' information
    Returns all of them to the html to load the specific player's playing page.

    :param player_id: Player's tag to play
    """
    player = Player.objects.filter(tag=str(player_id))[0]
    board_list = get_board(request)
    player_list = get_all_players(request)

    context = {'player': player, 'board_list': board_list, 'player_list': player_list}
    return render(request, 'game/player_form.html', context)

@transaction.atomic
def get_all_players(request):
    """
    Returns all of the existing players' objects
    """
    player_list = Player.objects.all()
    print(player_list)
    return player_list

@transaction.atomic
def update_game(request, player, board, attempt, r, c):
    """
    Updates player and board if the player's movement is valid
    and saves the boards and players information

    :param player: The player to move
    :param board: The previous position that had player or treasure
    :param attempt: The new position that player moves to
    :param r: Row where player's at currently
    :param c: Column where player's at currently
    """
    attempt.label = player.tag
    board.label = EMPTY_TILE
    player.score += attempt.value
    attempt.value = 0
    board.save()
    attempt.save()
    player.row = r
    player.col = c
    player.save()

@transaction.atomic
def move_player(request, player_id: str):
    """
    Based on the player_id, gets their position on the board
    and checks if their attempt to move is valid.
    Will move the player according to the direction button they clicked.
    Reloads the same page to reflect updated board and players' score

    :param player_id: Player's tag to move
    """
    try:
        player = Player.objects.filter(tag=player_id)[0]
        r = player.row
        c = player.col
        #print('label: ' + str(player))
        board = Board.objects.filter(row=r, col=c)[0]
        print(1234, vars(request.POST))
        dir = request.POST['button_id']
        print(dir)
        url = '/game/display/' + player_id + '/'
        match dir:
            case 'u':
                print('u start')
                if r != MIN_RANGE:
                    attempt = Board.objects.filter(row=r - 1, col=c)[0]
                    print('u step1')
                    if attempt.label == EMPTY_TILE or attempt.label == TREASURE_DESC:
                        print('u strp2')
                        update_game(request, player, board, attempt, r - 1, c)
                        print('u end')
            case 'd':
                if r != MAX_RANGE:
                    attempt = Board.objects.filter(row=r + 1, col=c)[0]
                    if attempt.label == EMPTY_TILE or attempt.label == TREASURE_DESC:
                        update_game(request, player, board, attempt, r + 1, c)

            case 'l':
                if c != MIN_RANGE:
                    attempt = Board.objects.filter(row=r, col=c - 1)[0]
                    if attempt.label == EMPTY_TILE or attempt.label == TREASURE_DESC:
                        update_game(request, player, board, attempt, r, c - 1)

            case 'r':
                if c != MAX_RANGE:
                    attempt = Board.objects.filter(row=r, col=c + 1)[0]
                    if attempt.label == EMPTY_TILE or attempt.label == TREASURE_DESC:
                        update_game(request, player, board, attempt, r, c + 1)

    except KeyError as d:
        print("6789", d)
        pass

    # url = '/game/display/' + player_id
    return HttpResponseRedirect(url)

class PlayerCreate(CreateView):
    model = Player
    fields = '__all__'
    success_url = reverse_lazy('players')  # what url will show up

class PlayerUpdate(UpdateView):
    model = Player
    fields = ['row', 'col']
    success_url = reverse_lazy('players')


class BoardCreator(CreateView):
    model = Board
    field = '__all__'
    success_url = reverse_lazy('show_board')