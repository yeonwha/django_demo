from django.db import models
from django.core.exceptions import ValidationError

def validate_col_range(value):
    if value < 1 or value > 10:
        raise ValidationError('Column out of range', code='col_value')

def validate_row_range(value):
    if value < 1 or value > 10:
        raise ValidationError('Row out of range', 'row_value')

def validate_unique_tag(value):
    players = Player.objects.filter(tag=value)
    if len(players) != 0:
        raise ValidationError('Tag already taken', code='tag_duplicate')

class Board(models.Model):
    """
    Board object's elements to construct
    col = a board object's column
    row = a board objects' row
    label = the description of board to tell it's empty or not. initially '.'
    value = the treasure's value if it has. initially 0
    """
    col = models.IntegerField(validators=[validate_col_range])
    row = models.IntegerField(validators=[validate_row_range])
    label = models.CharField(max_length=1)
    value = models.IntegerField()

    @classmethod
    def create_board(cls, row, col):
        """
        Create Board objects
        col = a board object's column
        row = a board objects' row
        label = initially '.'
        value = initially 0

        returns the objects
        """
        model = cls(label='.', row = row, col = col, value = 0)
        return model

    def __str__(self):
        return f'{self.label} '

class Player(models.Model):
    """
    Player object's elements to construct

    tag = the player's ID
    row = a player object's row on the board
    col = a player object's column on the board
    score = a player's score in the game
    """
    tag = models.CharField(max_length=1, validators=[validate_unique_tag])
    row = models.IntegerField(validators=[validate_row_range])
    col = models.IntegerField(validators=[validate_col_range])
    score = models.IntegerField()

    def __str__(self):
        return f'{self.tag}'

    @classmethod
    def create_player(cls, tag, row, col):
        """
        Create the player object

        :param tag: the player's ID
        :param row: a player object's row on the board
        :param col: a player object's column on the board
        :return: player object
        """
        model = cls(tag=tag, col=col, row=row, score=0)
        return model

    @classmethod
    def clean(self):
        prev = Player.objects.filter(pk=self.pk)
        if len(prev) > 0:
            if abs(self.row - prev[0].row) > 1:
                raise ValidationError('Row too far', code='row_distance')
            if abs(self.col - prev[0].col) > 1:
                raise ValidationError('Column too far', code='col_distance')