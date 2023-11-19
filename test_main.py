import pygame
import os
import unittest
from unittest.mock import create_autospec
from pygame import Surface
from pygame import mixer
from unittest.mock import Mock
from objects import Player, Bar, ScoreCard, Ball

pygame.init()
SCREEN = WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode(SCREEN)
script_dir = os.path.dirname(os.path.realpath(__file__))

#testing game initialization
class TestGameInitialization(unittest.TestCase):
   def test_game_window_initialization(self):
       self.assertIsNotNone(pygame.display.get_surface(), "Game window not initialized")

   def test_sound_initialization(self):
       coin_fx = pygame.mixer.Sound(os.path.join(script_dir, 'Sounds/coin.mp3'))
       death_fx = pygame.mixer.Sound(os.path.join(script_dir, 'Sounds/death.mp3'))
       move_fx = pygame.mixer.Sound(os.path.join(script_dir,'Sounds/move.mp3'))
       self.assertIsNotNone(coin_fx)
       self.assertIsNotNone(death_fx)
       self.assertIsNotNone(move_fx)

   def test_object_initialization(self):
       p = Player(win)
       self.assertIsNotNone(p)

   def test_background_initialization(self):
       home_bg = pygame.image.load(os.path.join(script_dir, "Assets/homePage.png"))
       self.assertIsNotNone(home_bg)

   def test_font_initialization(self):
       pygame.font.init()
       score_font = pygame.font.Font(os.path.join(script_dir, 'Fonts/BubblegumSans-Regular.ttf'), 50)
       self.assertIsNotNone(score_font)

#testing player movement
class TestPlayerMovement(unittest.TestCase):

 def setUp(self):
     self.player = Player(win)

 def test_player_movement_right(self):
     initial_position = self.player.rect.x
     self.player.move_right(10) # Move player 10 pixels to the right
     self.assertEqual(self.player.rect.x, initial_position + 10, "Player did not move correctly to the right")

 def test_player_movement_left(self):
     initial_position = self.player.rect.x
     self.player.move_left(10) # Move player 10 pixels to the left
     self.assertEqual(self.player.rect.x, initial_position - 10, "Player did not move correctly to the left")

#testing collision detection
class TestCollisionDetection(unittest.TestCase):

 def setUp(self):
  self.player = Player(win)
  self.bar = Bar(400, 450, 44, 44, (255, 0, 0))
  self.bar_group = pygame.sprite.Group()
  self.bar_group.add(self.bar)

 def test_collision_detection(self):
  self.player.move_right(10) # Move player 10 pixels to the right
  self.bar.rect.x -= 10 # Move bar 10 pixels to the left
  self.assertTrue(pygame.sprite.spritecollide(self.player, self.bar_group, False), "Collision detection failed")

#testing score page
class TestScoreCard(unittest.TestCase):

    def test_score_card_update(self):
        # Mock the Pygame window
        mock_win = Mock()

        # Create a ScoreCard instance for testing
        score_card = ScoreCard(x=100, y=100, win=mock_win)

        # Call the update method with a test score
        score_card.update(score=42)

        # Assert that the blit method was called at least once
        mock_win.blit.assert_called()

script_dir = os.path.dirname(os.path.realpath(__file__))

#testing sound effect
class TestSoundEffects(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize Pygame mixer
        mixer.init()

    def setUp(self):
        self.win = Surface((800, 600))  # Create a real Pygame Surface
        self.player = Player(self.win)
        self.ball = Ball(0, 0, 'type', 'red', self.win)  # Pass a valid color to the Ball class
        self.score_card = ScoreCard(0, 0, self.win)
        self.sound_effect = mixer.Sound(os.path.join(script_dir, "Sounds/coin.mp3"))

    def test_sound_effect(self):
        # Simulate a player collecting a ball
        self.player.rect.x = self.ball.rect.x
        self.player.rect.y = self.ball.rect.y
        self.player.collect_ball(self.ball)

        # Play the sound effect
        self.sound_effect.play()

        # Check if any sound is still playing
        self.assertTrue(mixer.get_busy())

    @classmethod
    def tearDownClass(cls):
        # Deinitialize Pygame after all tests are done
        mixer.quit()

if __name__ == '__main__':
   unittest.main()
