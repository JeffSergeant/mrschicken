from GameScene import GameScene
from SplashScreen import SplashScreen

if __name__ == '__main__':

    scene = SplashScreen()
    game_running = scene.initialise()

    while game_running:
        game_running = scene.update()
        if not game_running:
            scene = scene.close()

            if scene:
                game_running = scene.initialise()