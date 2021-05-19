class BasePlayer:
    def __init__(self):
        pass

    def get_pit_number(self):
        pass


class Player(BasePlayer):
    def get_pit_number(self, game):
        # TODO Ajouter des gestionnaires d'erreurs
        return int(input("Enter a pit number (1-6) > "))


class Mancala:
    # Index des mancala par joueur
    PLAYER1_MANCALA_INDEX = 6
    PLAYER2_MANCALA_INDEX = 13

    def __init__(self, player1, player2):
        self.board = [0, 0, 0, 0, 10, 0, 40, 0, 0, 0, 1, 2, 2, 2]
        self.player1 = player1
        self.player2 = player2
        self.current = player1

    def show_board(self):
        """
            Plateau:
                4  4  4  4  4  4
             4 /----------------/  4
            >   4  4  4  4  4  4
                1  2  3  4  5  6
        """

        # Rangée de chaque joueur
        player1_pits = self.board[:self.PLAYER1_MANCALA_INDEX+1]
        player2_pits = self.board[self.PLAYER1_MANCALA_INDEX +
                                  1: self.PLAYER2_MANCALA_INDEX+1]

        # Point de vue du joueur 1
        if self.current == self.player1:
            top = player2_pits
            bottom = player1_pits
        # Point de vue du joueur 2
        else:
            top = player1_pits
            bottom = player2_pits

        # Vue inversée sur la rangée du haut
        top.reverse()
        print("   %2s %2s %2s %2s %2s %2s" % tuple(top[1:]))
        print("%2s /----------------/ %2s" % (top[0], bottom[-1]))
        print(">  %2s %2s %2s %2s %2s %2s" % tuple(bottom[:-1]))
        print("   %2s %2s %2s %2s %2s %2s" % (1, 2, 3, 4, 5, 6))

    def move(self, pit_number):
        """
            Distribue pour le joueur actuel, les billes contenues dans un puit donnée,
            gère le système de tour
        """

        # Billes à répartir
        marbles_remaining = self.get_pit_value(pit_number)

        # Calcul de l'index du puit de départ
        if self.current == self.player1:
            curr_pit_index = pit_number - 1
        else:
            curr_pit_index = pit_number + self.PLAYER1_MANCALA_INDEX

        # Collecte des billes
        self.board[curr_pit_index] = 0
        curr_pit_index += 1

        # Pour chaque puit conséquent à l'exception du Mancala ennemi
        while marbles_remaining > 0:
            if self.current == self.player1 and curr_pit_index == self.PLAYER2_MANCALA_INDEX:
                pass
            elif self.current == self.player2 and curr_pit_index == self.PLAYER1_MANCALA_INDEX:
                pass
            # Dépôt d'une bille
            else:
                self.board[curr_pit_index] += 1
                marbles_remaining -= 1

            curr_pit_index = (curr_pit_index + 1) % len(self.board)

        # TODO: Implémenter les règles permettant au joueur actuel de rejouer
        # Index de la dernière bille déposée, équivalent à "reculer d'un puit dans le sens inverse"
        last_marble_index = (curr_pit_index - 1) % len(self.board)
        curr_player_mancala = self.PLAYER1_MANCALA_INDEX if self.current == self.player1 else self.PLAYER2_MANCALA_INDEX

        # Si la dernière bille est déposé dans le Mancala allié alors le joueur actuel rejoue
        if last_marble_index == curr_player_mancala:
            self.current = self.current
        # Passage de la main au joeur adverse
        else:
            self.current = self.player2 if self.current == self.player1 else self.player1

    def get_pit_value(self, number):
        """
            Renvoi le nombre de billes contenu dans un puit
            à l'aide de son numéro relatif au joueur actuel
        """

        if self.current == self.player1:
            return self.board[number - 1]
        else:
            return self.board[self.PLAYER1_MANCALA_INDEX + number]

    def get_player_pit_number(self):
        """
            Renvoi le numéro de puit sélectionné par le joueur actuel
        """
        pit_number = -1

        # Demander tant que la saisie n'est pas valide
        while (pit_number < 1 or pit_number > 6):
            pit_number = self.current.get_pit_number(game=self)

            # Numero invalide
            if (pit_number < 1 or pit_number > 6):
                print(f'Invalid pit number %s ! Try again please' % (pit_number))

            # Verification du puit vide
            elif (self.get_pit_value(pit_number) == 0):
                print(f'Empty pit ! Try another one please')
                pit_number = -1

            else:
                pass

        return pit_number

    def is_over(self):
        """ 
            Retourne `True` si au moins un des joueurs n'a plus de billes
            dans sa rangée à l'exception de son Mancala.
            Sinon, retourne `False`
        """
        # Billes restantes de chaque joueurs
        player1_remaining = sum(self.board[:Mancala.PLAYER1_MANCALA_INDEX])
        player2_remaining = sum(
            self.board[Mancala.PLAYER1_MANCALA_INDEX + 1: Mancala.PLAYER2_MANCALA_INDEX])

        return player1_remaining == 0 or player2_remaining == 0

    def get_score(self):
        """
            Renvoi le score de la partie sous forme de tuple.
            L'ordre est le suivant: `(J1, J2)`
        """

        # Score de chaque joueur
        player1_score = sum(self.board[:Mancala.PLAYER1_MANCALA_INDEX+1])
        player2_score = sum(
            self.board[Mancala.PLAYER1_MANCALA_INDEX + 1: Mancala.PLAYER2_MANCALA_INDEX+1])

        return player1_score, player2_score


def main():
    print('The Mancala Game')
    player1 = Player()
    player2 = Player()
    game = Mancala(player1, player2)

    while (not game.is_over()):
        curr_player = "Player 1" if game.current == game.player1 else "Player 2"
        print(f'[INFO] {curr_player}\'s turn')

        print()
        game.show_board()
        print()

        # Saisie du numéro de puit
        pit_number = game.get_player_pit_number()
        pit_value = game.get_pit_value(pit_number)
        # Déplacement de billes en partant du puit saisi
        print(
            f'[MOVE] {curr_player} moved {pit_value} marbles from pit n°{pit_value}')
        game.move(pit_number)

    # Fin de partie affichage du score
    p1_score, p2_score = game.get_score()
    print(f'Game finished ! Final score: (P1) {p1_score} - {p2_score} (P2)')


if __name__ == '__main__':
    main()
