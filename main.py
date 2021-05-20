from players import Player, TutorialPlayer
from mancala import Mancala


def main():
    print('The Mancala Game')
    player1 = Player()

    # # JvsJ
    # player2 = Player()

    # J vs IA niveau Tutoriel
    player2 = TutorialPlayer()

    game = Mancala(player1, player2)

    # Boucle de jeu ne s'arretant seulement si la partie est terminée
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
            f'[MOVE] {curr_player} moved {pit_value} marbles from pit n°{pit_number}')
        game.move(pit_number)

    # Fin de partie affichage du score
    p1_score, p2_score = game.get_score()
    print(f'Game finished ! Final score: (P1) {p1_score} - {p2_score} (P2)')


if __name__ == '__main__':
    main()
