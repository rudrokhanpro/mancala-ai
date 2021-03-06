# Main Menu
def main():
    print ("Welcome to Mancala,\n")
    print ("Please choose the mode you want to play:")
    print ("[1] Player vs Player")
    print ("[2] Player vs AI")
    print ("[0] Quit")

    option = -1
    while option != 0:
        option = int(input(">> "))

        if option == 1:
            print ("You selected Player vs Player \n")
            player1 = Player()
            player2 = MaximizingPlayer()
            game = Mancala(player1, player2)
                     
        elif option == 2:
            menu2()

        elif option == 0:
            print("See you next time !")
            exit()            
            
        else :
            print ("invalid option.\n")

     

# Menu VS AI with Difficulty Modes
def menu2():
    print ("You selected Player vs AI \n")
    print ("Please select your difficulty :")
    print ("[1] Tutorial")
    print ("[2] Easy")
    print ("[3] Medium")
    print ("[4] Extreme")
    print ("[9] Back")
    print ("[0] Quit")    
 
    option = -1
    while option != 0:
        option = int(input(">> "))

        if option == 1:
            print ("You selected Tutorial mode \n")
            player1 = Player()
            player2 = TutorialPlayer()
            game = Mancala(player1, player2)

        elif option == 2:
            print ("You selected Easy Mode \n")
            player1 = Player()
            player2 = MaximizingPlayer()
            game = Mancala(player1, player2)

        elif option == 3:
            print ("You selected Medium Mode \n")
            player1 = Player()
            player2 = MediumPlayer()
            game = Mancala(player1, player2)

        elif option == 4:
            print ("You selected Extreme Mode")
            print ("Good luck ! :) \n")
            player1 = Player()
            player2 = ExtremePlayer()
            game = Mancala(player1, player2)

        elif option == 9:
            main()

        elif option == 0:
            print("See you next time !")
            exit()
        

        else :
            print ("invalid option.\n")

if __name__ == "__main__":
	main()
