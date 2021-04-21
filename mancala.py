class Mancala:
    board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]

    PLAYER_MANCALA_INDEX = 6
    BOT_MANCALA_INDEX = 13

    def __init__(self):
        pass

    def show_board(self):
        """
            Intial board :
                ( 4) ( 4) ( 4) ( 4) ( 4) ( 4)
            ( 0)                               ( 0)
                ( 4) ( 4) ( 4) ( 4) ( 4) ( 4)
        """
        player_pits = self.board[self.PLAYER_MANCALA_INDEX +
                                 1:self.BOT_MANCALA_INDEX]

        bot_pits = self.board[:self.PLAYER_MANCALA_INDEX]

        mancalas = self.board[self.BOT_MANCALA_INDEX], self.board[
            self.PLAYER_MANCALA_INDEX]

        print("    (%2s) (%2s) (%2s) (%2s) (%2s) (%2s)" % tuple(bot_pits))
        print("(%s)                               (%s)" % mancalas)
        print("    (%2s) (%2s) (%2s) (%2s) (%2s) (%2s)" % tuple(player_pits))


def main():
    print('Welcome to Mancala !')

    game = Mancala()

    game.show_board()


if __name__ == '__main__':
    main()