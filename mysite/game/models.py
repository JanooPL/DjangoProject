# models.py

from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone

class Game(models.Model):
    game_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    board = models.CharField(max_length=9, default=" " * 9)
    current_turn = models.CharField(max_length=1, default="X")
    winner = models.CharField(max_length=1, null=True, blank=True)
    gamer1 = models.ForeignKey(User, related_name='game_gamer1', on_delete=models.CASCADE, null=True, blank=True)
    gamer2 = models.ForeignKey(User, related_name='game_gamer2', on_delete=models.CASCADE, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)  # Automatycznie aktualizuje się przy każdej zmianie

    def make_move(self, position):
        if self.board[position] == " " and not self.winner:
            board_list = list(self.board)
            board_list[position] = self.current_turn
            self.board = "".join(board_list)
            self.current_turn = "O" if self.current_turn == "X" else "X"
            self.check_winner()
            self.save()

    def check_winner(self):
        winning_positions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6)              # diagonals
        ]
        for a, b, c in winning_positions:
            if self.board[a] == self.board[b] == self.board[c] != " ":
                self.winner = self.board[a]
                if self.winner == 'X':
                    self.winner = self.gamer1.username
                elif self.winner == 'O':
                    self.winner = self.gamer2.username
                return
        if " " not in self.board:
            self.winner = "D"  # Draw

    def reset(self):
        self.board = " " * 9
        self.current_turn = "X"
        self.winner = None
        self.save()
