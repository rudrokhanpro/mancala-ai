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
