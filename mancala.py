class Mancala:
    board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]

    # Nom des joueurs
    PLAYER = "PLAYER"
    BOT = "BOT"

    # Index des mancala par joueur
    PLAYER_MANCALA_INDEX = 6
    BOT_MANCALA_INDEX = 13

    def __init__(self):
        pass

    def show_board(self):
        """
            Intial board :
                ( 4) ( 4) ( 4) ( 4) ( 4) ( 4)
            ( 0)                             ( 0)
                ( 4) ( 4) ( 4) ( 4) ( 4) ( 4)
        """
        player_pits = self.board[:Mancala.PLAYER_MANCALA_INDEX]

        bot_pits = self.board[Mancala.PLAYER_MANCALA_INDEX +
                              1:Mancala.BOT_MANCALA_INDEX]
        bot_pits.reverse()

        mancalas = self.board[Mancala.BOT_MANCALA_INDEX], self.board[
            Mancala.PLAYER_MANCALA_INDEX]

        print("    (%2s) (%2s) (%2s) (%2s) (%2s) (%2s)" % tuple(bot_pits))
        print("(%2s)                             (%2s)" % mancalas)
        print("    (%2s) (%2s) (%2s) (%2s) (%2s) (%2s)" % tuple(player_pits))

    def move(self, player, pit_number):
        """ Distribue les billes contenues dans un puit donnée """
        pit_index = self._get_player_pit_index(player, pit_number)

        # Collecter toutes les billes du puit
        marble_count = self.board[pit_index]
        self.board[pit_index] = 0

        print("[{}] Déplacement de {} billes du puit n° {}".format(
            player.ljust(len(Mancala.PLAYER)), marble_count, pit_number))

        # Pour chaque puit suivant dans le sens anti-horaire,
        # distribuer 1 bille
        for i in range(pit_index + 1, pit_index + 1 + marble_count):
            i_pit_index = i % len(self.board)

            self.board[i_pit_index] += 1

    def is_over(self):
        player_marble_count = sum(self.board[:Mancala.PLAYER_MANCALA_INDEX])
        bot_marble_count = sum(
            self.board[Mancala.PLAYER_MANCALA_INDEX + 1: Mancala.BOT_MANCALA_INDEX])

        return (player_marble_count == 0 or bot_marble_count == 0)

    def _get_player_pit_index(self, player, pit_number):
        """ Renvoi l'index du puit selon le joueur """

        # Renvoyer une erreur si le numero de puit est invalide
        if pit_number < 1 or pit_number > 6:
            raise ValueError(
                'Invalid pit number %d. Pit number should be between 1 and 6' %
                pit_number)
        else:
            # player: 1 => 0, 6 => 5
            # bot:    1 => 7, 6 => 12
            return pit_number - 1 if player == Mancala.PLAYER else Mancala.PLAYER_MANCALA_INDEX + 1 + (
                pit_number - 1)


def main():
    print('Bienvenue sur Mancala !')

    game = Mancala()

    game.show_board()


if __name__ == '__main__':
    main()
