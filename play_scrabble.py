from game import Game

if __name__ == "__main__":
    num_players = int(input("Hi! Please enter the number of players: "))
    game = Game(num_players)
    game.game_loop()
