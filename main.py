from players import Player, TutorialPlayer, MaximizingPlayer, MinMaxPlayer
from mancala import Mancala


def main():
    print_menu()

    while True:
        try:
            option = int(input('>> '))

            player1 = Player()

            if option == 1:
                print("[INFO] You have choose Player vs Player")
                player2 = Player()
            elif option == 2:
                print("[INFO] You have choose Player vs AI (Tutorial)")
                player2 = TutorialPlayer()
            elif option == 3:
                print("[INFO] You have choose Player vs AI (Easy)")
                player2 = MaximizingPlayer()
            elif option == 4:
                print("[INFO] You have choose Player vs AI (Medium)")
                player2 = MinMaxPlayer()
            elif option == 0:
                exit()
            else:
                raise ValueError()

            ai_options = [2, 3, 4]

            start_game(
                player1=player1,
                player2=player2,
                # Ne pas pivoter le plateau lorsqu'on joue contre une IA
                rotate_board=(option not in ai_options)
            )

            print_menu()

        except ValueError:
            print('Enter a valid option. Accepted options: 1, 2, 3, 4, 0')


def print_menu():
    print("Welcome to Mancala")
    print()
    print("[MENU] Please choose the mode you want to play:")
    print("\t[1] Player vs Player")
    print("\t[2] Player vs AI (Tutorial)")
    print("\t[3] Player vs AI (Easy)")
    print("\t[4] Player vs AI (Medium)")
    print("\t[0] Quit")


def start_game(player1, player2, rotate_board):
    """ Lance la partie avec les joeurs indiquées """
    print(" ----------------------------------------------------")
    print("|\t\t/!\  HOW TO PLAY  /!\\                |")
    print(" ----------------------------------------------------")
    print("START : At the start of the game each pit has 4 stones\n")
    print("MOVE : Select a pit from 1-6 to move the stones in an anti-clockwise direction\n")
    print("RE-TURN : When the last stone ends in your Mancala, you can play again\n")
    print("SCORE : Scores are counted in your Mancala (left and right extremities)")
    print("\tWhen a stone you moved passes in your Mancala you add +1 point\n")
    print("END : The game ends when either your side or the enemy side has no more playable pit")
    print("     We count the stones in your Mancala + the stones on your side to determine the winner\n")

    game = Mancala(
        player1=player1,
        player2=player2,
        rotate_board=rotate_board
    )

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
    print(
        f'Game finished ! Final score: (P1) {p1_score} - {p2_score} (P2)')


if __name__ == '__main__':
    main()
