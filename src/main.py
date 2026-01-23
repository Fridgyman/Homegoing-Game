from src.game import Game

def main():
    game: Game = Game(60, "assets/audio", "assets/fonts", "assets/images")
    game.run()

if __name__ == "__main__":
    main()