class BasePlayer:
    def __init__(self):
        pass

    def get_pit_number(self, game):
        pass


class Player(BasePlayer):
    def get_pit_number(self, game):
        # TODO Ajouter des gestionnaires d'erreurs
        return int(input(">> Enter a pit number (1-6): "))
