from random import choice
from mancala import Mancala
import sys


class BasePlayer:
    def __init__(self):
        pass

    def get_pit_number(self, game):
        pass


class Player(BasePlayer):
    def get_pit_number(self, game: Mancala):
        while True:
            try:
                value = int(input(">> Enter a pit number (1-6): "))
            except ValueError:
                print("Invalid input, please input an integer")
                continue
            else:
                return value


class TutorialPlayer(BasePlayer):
    """
        IA basique effectuant des choix légaux au hasard.
        Autrement dit: Choisi un puit valide au hasard 
    """

    def get_pit_number(self, game: Mancala):
        """ Renvoi un numéro de puit au hasard parmi les choix valides """
        available_pits = game.get_available_pits()
        random_pit = choice(available_pits)

        return random_pit


class MaximizingPlayer(BasePlayer):
    # Veut obtenir un maximum de point en un tour
    def get_pit_number(self, game):
        available_pits = game.get_available_pits()
        available_scores = []

        for pit in available_pits:
            clone = game.clone()
            clone.move(pit)

            future_score = clone.get_player_score(game.current)

            available_scores.append(future_score)

        max_score = max(available_scores)

        # on ne garde que les meilleurs scores
        best_pits = []
        for score, pit in zip(available_scores, available_pits):
            if score == max_score:
                best_pits.append(pit)

        best_pit = choice(best_pits)

        return best_pit


class MinMaxPlayer(BasePlayer):
    """
        IA avancée effectuant des choix légaux selon l'algorithme de Minmax.
        L'heuristique utilisée est le score que l'IA peut espérér
    """

    DEPTH = 4
    pruning = False
    # counter = 0

    def get_pit_number(self, game: Mancala):
        # Pour chaque choix valide, calculer son score potentiel
        avalaible_pits = game.get_available_pits()
        avalaible_scores = []

        for avail_pit in avalaible_pits:
            # Simulation d'une action
            clone = game.clone()

            if self.pruning:
                alpha = -sys.maxsize
                beta = sys.maxsize
                future_score = self.minmax_ab_pruning(
                    clone, avail_pit, self.DEPTH, alpha, beta)
            else:
                future_score = self.minmax(clone, avail_pit, self.DEPTH)
                _, my_future_score = future_score
            # self.counter += 1

            # Sauvegarde des scores
            avalaible_scores.append(my_future_score)

        # Retenir uniquement le meilleur score
        best_score = max(avalaible_scores)

        # Retrouver le ou les puit permettant d'obtenir le meilleur score
        # Càd le puit permettant de maximiser l'utilité
        best_pits = []

        # Liason des p
        for pit, score in zip(avalaible_pits, avalaible_scores):
            if score == best_score:
                best_pits.append(pit)

        # print(f'counter = {self.counter}')
        # self.counter = 0

        # S'il il y a plusieurs puits, choisir au hasard le meilleur puit
        if len(best_pits) == 0:
            return best_pits[0]
        else:
            return choice(best_pits)

    def minmax(self, game: Mancala, pit: int, depth: int) -> int:
        """
            Fonction simulant récursivement et à tour de rôle
            les différents choix éffectués par les joueurs
        """

        # Copie de la partie en cours
        clone = game.clone()
        # Simulation du choix
        clone.move(pit, silent=True)

        # Si nombre de tours épuissés, renvoyer le score potentiel de l'IA
        if depth == 0:
            return clone.get_score()

        # Choix de l'agent
        maximizer = clone.current == clone.player2

        # Simulation des nouveaux choix légaux après le choix précedamment éffectué
        avalaible_pits = clone.get_available_pits()
        best_score = clone.get_score()
        enemy_best_score, my_best_score = best_score

        for avail_pit in avalaible_pits:
            # Nouveau score potentiel après la suite des choix précedamment éffectué
            new_score = self.minmax(clone, avail_pit, depth-1)
            enemy_new_score, my_new_score = new_score

            # self.counter += 1

            # Si c'est le tour de l'agent Maximisant càd l'IA
            if maximizer and my_new_score > my_best_score:
                best_score = new_score
                my_best_score = my_new_score
            else:
                if my_new_score < my_best_score or enemy_new_score > enemy_best_score:
                    best_score = new_score
                    my_best_score = my_new_score

        return best_score

    def minmax_ab_pruning(self, game: Mancala, pit: int, depth: int, alpha: int, beta: int) -> int:
        """
            Fonction simulant récursivement et à tour de rôle
            les différents choix éffectués par les joueurs
        """
        # Copie de la partie en cours
        clone = game.clone()
        # Simulation du choix
        clone.move(pit, silent=True)

        # Si nombre de tours épuissés, renvoyer le score potentiel de l'IA
        if depth == 0:
            # return clone.get_player_score(clone.player2)
            return clone.get_score()

        # Choix de l'agent
        maximizer = clone.current == clone.player2

        # Simulation des nouveaux choix légaux après le choix précedamment éffectué
        avalaible_pits = clone.get_available_pits()

        best_score = clone.get_score()
        enemy_best_score, my_best_score = best_score

        for avail_pit in avalaible_pits:
            # Nouveau score potentiel après la suite des choix précedamment éffectué
            new_score = self.minmax_ab_pruning(
                clone, avail_pit, depth-1, alpha, beta)
            # self.counter += 1

            # Si c'est le tour de l'agent Maximisant càd l'IA
            enemy_new_score, my_new_score = new_score

            if maximizer:
                # Mise à jour du meilleur score pour l'IA
                if my_new_score > my_best_score:
                    best_score = new_score
                    my_best_score = my_new_score

                alpha = max(my_best_score, alpha)

            else:
                # Mise à jour du meilleur score pour l'IA et le sien
                if my_new_score < my_best_score or enemy_new_score > enemy_best_score:
                    best_score = new_score
                    my_best_score = my_new_score
                beta = max(my_best_score, beta)

            # Condition d'arrêt
            if beta <= alpha:
                return best_score

        return best_score
