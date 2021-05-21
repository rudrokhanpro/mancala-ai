from random import choice
from mancala import Mancala


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
                break



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


class MediumPlayer(BasePlayer):
    """
        IA avancée effectuant des choix légaux selon l'algorithme de Minmax.
        L'heuristique utilisée est le score que l'IA peut espérér
    """

    DEPTH = 4

    def get_pit_number(self, game: Mancala):
        # Pour chaque choix valide, calculer son score potentiel
        avalaible_pits = game.get_available_pits()
        avalaible_scores = []

        for avail_pit in avalaible_pits:
            # Simulation d'une action
            clone = game.clone()
            future_score = self.minmax(clone, avail_pit, MediumPlayer.DEPTH)

            # Sauvegarde des scores
            avalaible_scores.append(future_score)

        # Retenir uniquement le meilleur score
        best_score = max(avalaible_scores)

        # Retrouver le ou les puit permettant d'obtenir le meilleur score
        # Càd le puit permettant de maximiser l'utilité
        best_pits = []

        # Liason des p
        for pit, score in zip(avalaible_pits, avalaible_scores):
            if score == best_score:
                best_pits.append(pit)

        # S'il il y a plusieurs puits, choisir au hasard le meilleur puit
        if len(best_pits) == 0:
            return best_pits[0]
        else:
            return choice(best_pits)

    def minmax(self, game: Mancala, pit: int, depth: int):
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
            return clone.get_player_score(clone.player2)

        # Choix de l'agent
        maximizer = clone.current == clone.player1

        # Simulation des nouveaux choix légaux après le choix précedamment éffectué
        avalaible_pits = clone.get_available_pits()
        best_score = clone.get_player_score(clone.player2)

        for avail_pit in avalaible_pits:
            # Nouveau score potentiel après la suite des choix précedamment éffectué
            new_score = self.minmax(clone, avail_pit, depth-1)

            # Si c'est le tour de l'agent Maximisant càd l'IA
            if maximizer:
                best_score = max(new_score, best_score)
            else:
                best_score = min(new_score, best_score)

        return best_score
