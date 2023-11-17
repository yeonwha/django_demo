from django.db import models
import random


class Board(models.Model):
    """
    Board object's elements to construct
    col = a board object's column
    row = a board objects' row
    label = the description of board to tell it's empty or not. initially '.'
    value = the treasure's value if it has. initially 0
    """
    col = models.IntegerField()
    row = models.IntegerField()
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
    tag = models.CharField(max_length=1)
    row = models.IntegerField()
    col = models.IntegerField()
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