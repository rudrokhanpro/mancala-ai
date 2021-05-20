""" SCOREBOARD

    Amine 1 - 0 Rudro
    Daniel 1 - 0 Rudro
"""

from colorama import init, Fore, Back, Style

init()


class Mancala:
    # Index des mancala par joueur
    PLAYER1_MANCALA_INDEX = 6
    PLAYER2_MANCALA_INDEX = 13

    def __init__(self, player1, player2):
        self.board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
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
        if self._is_player1():
            top = player2_pits
            bottom = player1_pits
        # Point de vue du joueur 2
        else:
            top = player1_pits
            bottom = player2_pits

        # Vue inversée sur la rangée du haut
        top.reverse()

        # Version non colorée
        # print("   %2s %2s %2s %2s %2s %2s" % tuple(top[1:]))
        # print("%2s /----------------/ %2s" % (top[0], bottom[-1]))
        # print(">  %2s %2s %2s %2s %2s %2s" % tuple(bottom[:-1]))
        # print("   %2s %2s %2s %2s %2s %2s" % (1, 2, 3, 4, 5, 6))

        # Version colorée
        print((Fore.RED + "   %2s %2s %2s %2s %2s %2s") % tuple(top[1:]))
        print(((Fore.RED + "%2s ") + (Fore.YELLOW + "/----------------/") +
              (Fore.WHITE + " %2s")) % (top[0], bottom[-1]))
        print((Fore.WHITE + ">  %2s %2s %2s %2s %2s %2s") % tuple(bottom[:-1]))
        print((Fore.YELLOW + "   %2s %2s %2s %2s %2s %2s") %
              (1, 2, 3, 4, 5, 6))
        print(Style.RESET_ALL, end="")

    def move(self, pit_number):
        """
            Distribue pour le joueur actuel, les billes contenues dans un puit donnée,
            gère le système de tour
        """
        # Billes à répartir
        marbles_remaining = self.get_pit_value(pit_number)

        # Calcul de l'index du puit de départ
        if self._is_player1():
            curr_pit_index = pit_number - 1
        else:
            curr_pit_index = pit_number + self.PLAYER1_MANCALA_INDEX

        # Collecte des billes
        self.board[curr_pit_index] = 0
        curr_pit_index += 1

        # Pour chaque puit conséquent à l'exception du Mancala ennemi
        while marbles_remaining > 0:
            if self._is_player1() and curr_pit_index == self.PLAYER2_MANCALA_INDEX:
                pass
            elif self._is_player2() and curr_pit_index == self.PLAYER1_MANCALA_INDEX:
                pass
            # Dépôt d'une bille
            else:
                self.board[curr_pit_index] += 1
                marbles_remaining -= 1

            curr_pit_index = (curr_pit_index + 1) % len(self.board)

        # Index de la dernière bille déposée, équivalent à "reculer d'un puit dans le sens inverse"
        last_marble_index = (curr_pit_index - 1) % len(self.board)
        curr_player_mancala = self.PLAYER1_MANCALA_INDEX if self._is_player1(
        ) else self.PLAYER2_MANCALA_INDEX

        # Si la dernière bille est déposée dans le Mancala allié alors le joueur actuel rejoue
        if last_marble_index == curr_player_mancala:
            self._play_again()

        # Si    la dernière bille est déposée dans un puit allié auparavant vide
        #       et le puit est dans la rangée allié
        # alors le joueur récupère les billes du puit ennemi situé à l'opposée
        #       ainsi que la bille déposée
        # Pour le joueur 1:
        elif self._is_player1() and self.get_pit_value(last_marble_index + 1) - 1 == 0 \
                and (last_marble_index >= 0 and last_marble_index <= 6):
            opposite_pit_index = 12 - last_marble_index

            # Collecte des billes ennemies s'il y en a
            enemy_marbles = self.board[opposite_pit_index]

            if self.board[opposite_pit_index] > 0:
                self.board[opposite_pit_index] = 0
                # Collecte de la bille récemment déposée
                self.board[last_marble_index] = 0
                # Ajout au Mancala du joueur
                self.board[self.PLAYER1_MANCALA_INDEX] += (1 + enemy_marbles)

                print(
                    f'[CAPTURE] Capture of {enemy_marbles + 1} marbles'
                )

            # Passage de tour
            self._next_player()

        # Pour le joueur 2:
        elif self._is_player2() and self.get_pit_value(last_marble_index - 7 + 1) - 1 == 0 \
                and (last_marble_index >= 7 and last_marble_index <= 12):
            opposite_pit_index = 12 - last_marble_index

            # Collecte des billes ennemies
            enemy_marbles = self.board[opposite_pit_index]

            if self.board[opposite_pit_index] > 0:
                self.board[opposite_pit_index] = 0
                # Collecte de la bille récemment déposée
                self.board[last_marble_index] = 0
                # Ajout au Mancala du joueur
                self.board[self.PLAYER2_MANCALA_INDEX] += (1 + enemy_marbles)

                print(
                    f'[CAPTURE] Capture of {enemy_marbles + 1} marbles'
                )

            # Passage de tour
            self._next_player()

        # Si aucune ne s'applique alors passer la main au joueur ennemi
        else:
            self._next_player()

    def get_pit_value(self, number):
        """
            Renvoi le nombre de billes contenu dans un puit
            à l'aide de son numéro relatif au joueur actuel
        """
        if self._is_player1():
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

    def get_available_pits(self):
        """ Renvoi une liste de numéros de puits non-vide """
        # Récupération des puits du joueur actuel
        if self._is_player1():
            pits = self.board[:self.PLAYER1_MANCALA_INDEX]
        else:
            pits = self.board[self.PLAYER1_MANCALA_INDEX +
                              1: self.PLAYER2_MANCALA_INDEX]

        # Liste de numéros de puit non-vide
        non_empty_pits = []

        for i in range(len(pits)):
            if pits[i] != 0:
                non_empty_pits.append(i + 1)

        return non_empty_pits

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

    def clone(self):
        """ Renvoi un clone de la partie càd même valeurs """
        cloned_game = Mancala(self.player1, self.player2)
        cloned_game.board = list(self.board)
        cloned_game.current = self.current

        return cloned_game

    def _is_player1(self):
        """ `True` si le joueur actuel est le joueur 1. `False` sinon """
        return self.current == self.player1

    def _is_player2(self):
        """ `True` si le joueur actuel est le joueur 2. `False` sinon """
        return self.current == self.player2

    def _play_again(self):
        """ Le joueur actuel rejoue au prochain tour """
        self.current = self.current

    def _next_player(self):
        """ Passe la main au joueur ennemi """
        self.current = self.player2 if self._is_player1() else self.player1
