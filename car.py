import random
import pygame
from time import sleep

class CarRacing:
    def __init__(self):
        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.crashed = False
        self.level = 1  # Starting level
        self.blast_count = 0  # Count of enemy cars blasted
        self.paused = False  # Track if the game is paused

        # Load images and scale them to fit the game
        self.car_img = pygame.image.load("C:\\Users\\abhis\\Downloads\\read_car.png")
        self.car_img = pygame.transform.scale(self.car_img, (60, 120))  # Scale player car
        self.enemy_car_img1 = pygame.image.load("C:\\Users\\abhis\\Downloads\\pink_car.png")
        self.enemy_car_img1 = pygame.transform.scale(self.enemy_car_img1, (60, 120))  # Scale enemy car 1
        self.enemy_car_img2 = pygame.image.load("C:\\Users\\abhis\\Downloads\\monstre care.png")
        self.enemy_car_img2 = pygame.transform.scale(self.enemy_car_img2, (60, 120))  # Scale enemy car 2
        self.enemy_car_img3 = pygame.image.load("C:\\Users\\abhis\\Downloads\\pink car.png")
        self.enemy_car_img3 = pygame.transform.scale(self.enemy_car_img3, (60, 120))  # Scale enemy car 3
        self.background_img = pygame.image.load("C:\\Users\\abhis\\Downloads\\rod.jpg")
        self.background_img = pygame.transform.scale(self.background_img, (self.display_width, self.display_height))  # Scale background

        # Initialize car positions
        self.car_x = (self.display_width * 0.45)
        self.car_y = (self.display_height * 0.8)
        self.car_width = self.car_img.get_width()

        # Enemy cars
        self.enemy_cars = []
        self.spawn_enemy_cars()

        # Background position for scrolling
        self.bg_y1 = 0
        self.bg_y2 = -self.display_height  # Second image to create the illusion of scrolling
        self.bg_speed = 6  # Speed of the background movement

        # Load sounds
        self.crash_sound = pygame.mixer.Sound("C:\\Users\\abhis\\Downloads\\box-crash-106687.mp3")
        self.blast_sound = pygame.mixer.Sound("C:\\Users\\abhis\\Downloads\\blast_sound.mp3")  # Load blast sound

    def spawn_enemy_cars(self):
        # Create a specific number of enemy cars
        self.enemy_cars = []
        for _ in range(5):  # Change the number of enemy cars
            enemy_x = random.randint(150, 650)  # Spawn within a specific range
            enemy_y = random.randint(-600, -100)
            speed = random.randint(3, 6)
            enemy_img = random.choice([self.enemy_car_img1, self.enemy_car_img2, self.enemy_car_img3])
            self.enemy_cars.append([enemy_x, enemy_y, speed, enemy_img])

    def draw_car(self, x, y):
        self.game_display.blit(self.car_img, (x, y))

    def draw_enemy_cars(self):
        for enemy in self.enemy_cars:
            self.game_display.blit(enemy[3], (enemy[0], enemy[1]))

    def draw_background(self):
        # Draw the two background images for scrolling effect
        self.game_display.blit(self.background_img, (0, self.bg_y1))
        self.game_display.blit(self.background_img, (0, self.bg_y2))

    def update_background_position(self):
        # Move the background images down
        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        # Reset the background images when they move off-screen
        if self.bg_y1 >= self.display_height:
            self.bg_y1 = self.bg_y2 - self.display_height
        if self.bg_y2 >= self.display_height:
            self.bg_y2 = self.bg_y1 - self.display_height

    def display_score(self, score):
        font = pygame.font.SysFont(None, 25)
        text = font.render(f"Score: {score}", True, self.white)
        self.game_display.blit(text, (10, 10))

    def display_blast_count(self):
        font = pygame.font.SysFont(None, 25)
        text = font.render(f"Blasts: {self.blast_count}", True, self.white)
        self.game_display.blit(text, (10, 30))

    def run_game(self):
        self.game_display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Car Racing Game')

        score = 0

        while not self.crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True

            if self.paused:
                self.show_pause_menu()
                continue

            # Check for key states for continuous movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.car_x -= 5  # Move left at a speed of 5 pixels
            if keys[pygame.K_RIGHT]:
                self.car_x += 5  # Move right at a speed of 5 pixels
            if keys[pygame.K_SPACE]:  # Fire blast
                self.blast_enemy_cars()

            # Implement jumping
            if keys[pygame.K_z]:
                self.jump_car()

            # Ensure the car does not move out of bounds
            if self.car_x < 150:  # Left boundary
                self.car_x = 150
            elif self.car_x > 650 - self.car_width:  # Right boundary
                self.car_x = 650 - self.car_width

            # Update background position
            self.update_background_position()

            # Background and car rendering
            self.game_display.fill(self.black)
            self.draw_background()

            # Move and draw enemy cars
            for enemy in self.enemy_cars:
                enemy[1] += enemy[2]  # Update enemy car's y position
                if enemy[1] > self.display_height:  # Reset enemy car position if it goes off screen
                    enemy[1] = random.randint(-600, -100)
                    enemy[0] = random.randint(150, 650)  # Random x position, ensure it fits on the road
                    score += 1  # Increase score

            self.draw_enemy_cars()
            self.draw_car(self.car_x, self.car_y)
            self.display_score(score)
            self.display_blast_count()

            # Collision detection
            for enemy in self.enemy_cars:
                if self.car_y < enemy[1] + enemy[3].get_height() and self.car_y + self.car_img.get_height() > enemy[1]:
                    if (self.car_x < enemy[0] + enemy[3].get_width() and self.car_x + self.car_width > enemy[0]):
                        self.crashed = True
                        self.crash_sound.play()  # Play crash sound
                        self.show_crash_message()

            # Boundary check for the player's car
            if self.car_x < 150 or self.car_x > 650 - self.car_width:  # Adjusted to match enemy car spawning range
                self.crashed = True
                self.show_crash_message()

            pygame.display.update()
            self.clock.tick(60)

    def jump_car(self):
        original_y = self.car_y
        jump_height = 100  # Height to jump
        jump_speed = 5  # Speed of the jump
        for _ in range(jump_height // jump_speed):
            self.car_y -= jump_speed
            self.game_display.fill(self.black)
            self.draw_background()
            self.draw_enemy_cars()
            self.draw_car(self.car_x, self.car_y)
            pygame.display.update()
            self.clock.tick(60)

        # Descend back down
        for _ in range(jump_height // jump_speed):
            self.car_y += jump_speed
            self.game_display.fill(self.black)
            self.draw_background()
            self.draw_enemy_cars()
            self.draw_car(self.car_x, self.car_y)
            pygame.display.update()
            self.clock.tick(60)

        self.car_y = original_y  # Reset to original position

    def blast_enemy_cars(self):
        for enemy in self.enemy_cars:
            if (self.car_y < enemy[1] + enemy[3].get_height() and
                    self.car_y + self.car_img.get_height() > enemy[1] and
                    self.car_x < enemy[0] + enemy[3].get_width() and
                    self.car_x + self.car_width > enemy[0]):
                self.blast_count += 1  # Increase blast count
                enemy[1] = self.display_height + 100  # Move enemy car off-screen
                self.blast_sound.play()  # Play blast sound
                break  # Exit after blasting one car

    def show_crash_message(self):
        self.game_display.fill(self.black)
        font = pygame.font.SysFont(None, 55)
        text = font.render("Crashed! Game Over", True, self.white)
        self.game_display.blit(text, (self.display_width // 2 - 150, self.display_height // 2))
        pygame.display.update()
        sleep(2)  # Pause for 2 seconds before closing the game
        self.show_restart_menu()  # Show restart menu after crash

    def show_pause_menu(self):
        self.game_display.fill(self.black)
        font = pygame.font.SysFont(None, 55)
        text = font.render("Game Paused", True, self.white)
        self.game_display.blit(text, (self.display_width // 2 - 150, self.display_height // 2 - 50))
        resume_text = font.render("Abhi you are loss Press R to Resume", True, self.white)
        quit_text = font.render("Press Q to Quit", True, self.white)
        self.game_display.blit(resume_text, (self.display_width // 2 - 150, self.display_height // 2))
        self.game_display.blit(quit_text, (self.display_width // 2 - 150, self.display_height // 2 + 50))
        pygame.display.update()

        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.paused = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Resume game
                        self.paused = False
                    elif event.key == pygame.K_q:  # Quit game
                        pygame.quit()
                        quit()

    def show_restart_menu(self):
        self.game_display.fill(self.black)
        font = pygame.font.SysFont(None, 55)
        text = font.render("Game Over!", True, self.white)
        self.game_display.blit(text, (self.display_width // 2 - 150, self.display_height // 2 - 50))
        restart_text = font.render("Press R to Restart", True, self.white)
        quit_text = font.render("Press Q to Quit", True, self.white)
        new_game_text = font.render("Press N for New Game", True, self.white)
        self.game_display.blit(restart_text, (self.display_width // 2 - 150, self.display_height // 2))
        self.game_display.blit(quit_text, (self.display_width // 2 - 150, self.display_height // 2 + 50))
        self.game_display.blit(new_game_text, (self.display_width // 2 - 150, self.display_height // 2 + 100))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart game
                        self.restart_game()
                        return  # Exit the restart menu
                    elif event.key == pygame.K_q:  # Quit game
                        pygame.quit()
                        quit()
                    elif event.key == pygame.K_n:  # Start a new game
                        self.new_game()
                        return  # Exit the restart menu

    def restart_game(self):
        self.crashed = False
        self.level = 1
        self.blast_count = 0
        self.spawn_enemy_cars()
        self.run_game()

    def new_game(self):
        self.crashed = False
        self.level = 1
        self.blast_count = 0
        self.spawn_enemy_cars()
        self.car_x = (self.display_width * 0.45)
        self.car_y = (self.display_height * 0.8)
        self.run_game()

if __name__ == '__main__':
    game = CarRacing()
    game.run_game()
