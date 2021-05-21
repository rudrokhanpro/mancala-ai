from random import choice


class BasePlayer:
    def __init__(self):
        pass

    def get_pit_number(self, game):
        pass


class Player(BasePlayer):
    def get_pit_number(self, game):
        # TODO Ajouter des gestionnaires d'erreurs
        return int(input(">> Enter a pit number (1-6): "))


class TutorialPlayer(BasePlayer):
    """
        IA basique effectuant des choix légaux au hasard.
        Autrement dit: Choisi un puit valide au hasard 
    """

    def get_pit_number(self, game):
        # Get available pits
        available_pits = game.get_available_pits()
        random_pit = choice(available_pits)

        return random_pit

class MaximizingPlayer(BasePlayer):
    #Veut obtenir un maximum de point en un tour
    def get_pit_number(self, game):
        available_pits = game.get_available_pits()
        available_scores = []

        for pit in available_pits:
            clone=game.clone()
            clone.move(pit)

            future_score= clone.get_player_score(game.current)

            available_scores.append(future_score)

        max_score = max(available_scores) 
        
        ## on ne garde que les meilleurs scores
        best_pits = []
        for score,pit in zip(available_scores, available_pits):
            if score == max_score: best_pits.append(pit)

        
        best_pit=choice(best_pits)

        return best_pit
