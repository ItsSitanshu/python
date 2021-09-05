import discord
from discord.ext import commands

"""WAITING FOR STABLE VERSION CUZ UNSUOPPORTED ERRORS"""
# class TicTacToeButton(discord.ui.Button['TicTacToe']):
#     def __init__(self, x: int, y: int):
#         super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', group=y)
#         self.x = x
#         self.y = y
#     async def callback(self, interaction: discord.Interaction):
#         assert self.view is not None
#         view: TicTacToe = self.view
#         state = view.board[self.y][self.x]
#         if state in (view.X, view.O):
#             return
#         if view.current_player == view.X:
#             if not interaction.user == view.x:
#                 return
#             self.style = discord.ButtonStyle.danger
#             self.label = 'X'
#             self.disabled = True
#             view.board[self.y][self.x] = view.X
#             view.current_player = view.O
#             content = "It is now O's turn"
#         else:
#             if not interaction.user == view.y:
#                 return
#             self.style = discord.ButtonStyle.success
#             self.label = 'O'
#             self.disabled = True
#             view.board[self.y][self.x] = view.O
#             view.current_player = view.X
#             content = "It is now X's turn"
#         winner = view.check_board_winner()
#         if winner is not None:
#             if winner == view.X:
#                 content = 'X won!'
#             elif winner == view.O:
#                 content = 'O won!'
#             else:
#                 content = "It's a tie!"
#             for child in view.children:
#                 assert isinstance(child, discord.ui.Button) 
#                 child.disabled = True
#             view.stop()
#         await interaction.response.edit_message(content=content, view=view)
# class TicTacToe(discord.ui.View):
#     X = -1
#     O = 1
#     Tie = 2
#     def __init__(self, x: discord.Member, y: discord.Member):
#         super().__init__()
#         self.current_player = self.X
#         self.board = [
#             [0, 0, 0],
#             [0, 0, 0],
#             [0, 0, 0],
#         ]
#         self.x = x
#         self.y = y

#         for x in range(3):
#             for y in range(3):
#                 self.add_item(TicTacToeButton(x, y))
#     def check_board_winner(self):
#         for across in self.board:
#             value = sum(across)
#             if value == 3:
#                 return self.O
#             elif value == -3:
#                 return self.X
#         for line in range(3):
#             value = self.board[0][line] + self.board[1][line] + self.board[2][line]
#             if value == 3:
#                 return self.O
#             elif value == -3:
#                 return self.X
#         diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
#         if diag == 3:
#             return self.O
#         elif diag == -3:
#             return self.X
#         diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
#         if diag == 3:
#             return self.O
#         elif diag == -3:
#             return self.X
#         if all(i != 0 for row in self.board for i in row):
#             return self.Tie

#         return None

class TTT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["tictactoe"])
    async def ttt(self, ctx, member: discord.Member):
        await ctx.send('ON BREAK')# view=TicTacToe(ctx.author, member))

def setup(bot):
    bot.add_cog(TTT(bot))