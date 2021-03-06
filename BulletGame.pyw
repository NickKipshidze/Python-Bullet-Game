import pygame, keyboard, random

s_width, s_height = 800, 600

win = pygame.display.set_mode((s_width, s_height), pygame.RESIZABLE)
pygame.display.set_caption("Bullet Game - By Nick")

field = [100, 100, 600, 400]

class Bullet(object):
    def __init__(self, surface, color, position, size, velocity, radius, mode, damage=3):
        self.bofs = [0, 20, 20, 20]
        self.surface = surface
        self.color = color
        self.width = size[0]
        self.height = size[1]
        self.xpos = position[0]
        self.ypos = position[1]
        self.xvel = velocity[0]
        self.yvel = velocity[1]
        self.radius = radius
        self.mode = mode
        self.damage = damage

    def check_collision(self, rect):
        hit = pygame.Rect.colliderect(self.projectile, rect)
        if hit > 0: return True
        else: return False
    
    def check_bounds(self, s_width, s_height):
        if self.xpos+field[0] < field[0]-self.bofs[0] or self.xpos+field[0] > field[2]+field[0]-self.bofs[1] or \
        self.ypos+field[1] < field[1]-self.bofs[2] or self.ypos+field[1] > field[3]+field[1]-self.bofs[3]: return True
        else: return False

    def get_damage(self):
        return self.damage

    def draw(self):
        self.projectile = pygame.draw.rect(self.surface, self.color, (self.xpos+field[0], self.ypos+field[1], self.width, self.height), width=self.mode, border_radius=self.radius,
        border_top_left_radius=-self.radius, border_top_right_radius=-self.radius, border_bottom_left_radius=-self.radius, border_bottom_right_radius=-self.radius)

    def update(self):
        self.xpos += self.xvel
        self.ypos += self.yvel
        self.draw()

class Player(object):
    def __init__(self, surface, color, position, size, radius, mode, stats):
        self.surface = surface
        self.color = color
        self.xpos = position[0]
        self.ypos = position[1]
        self.width = size[0]
        self.height = size[1]
        self.radius = radius
        self.mode = mode
        self.walkspeed = stats[0]
        self.health = stats[1]
        self.maxhealth = stats[1]

    def check_collision(self):
        if self.xpos+field[0] < field[0] or self.xpos+field[0] > field[2]+field[0]-30 or self.ypos+field[1] < field[1] or self.ypos+field[1] > field[3]+field[1]-30: return True
        else: return False

    def get_input(self):
        if keyboard.is_pressed("w"):
            self.ypos -= self.walkspeed
            if self.check_collision(): self.ypos += self.walkspeed
        if keyboard.is_pressed("a"):
            self.xpos -= self.walkspeed
            if self.check_collision(): self.xpos += self.walkspeed
        if keyboard.is_pressed("s"):
            self.ypos += self.walkspeed
            if self.check_collision(): self.ypos -= self.walkspeed
        if keyboard.is_pressed("d"):
            self.xpos += self.walkspeed
            if self.check_collision(): self.xpos -= self.walkspeed

    def get_character(self):
        return self.character

    def get_health(self):
        return self.health

    def get_maxhealth(self):
        return self.maxhealth

    def damage(self, dmg):
        self.health -= dmg

    def draw(self):
        self.character = pygame.draw.rect(self.surface, self.color, (self.xpos+field[0], self.ypos+field[1], self.width, self.height), width=self.mode, border_radius=self.radius,
        border_top_left_radius=-self.radius, border_top_right_radius=-self.radius, border_bottom_left_radius=-self.radius, border_bottom_right_radius=-self.radius)
    
    def update(self):
        self.get_input()
        self.draw()

def redraw_window(surface):
    surface.fill((30, 30, 30, 255))

    pygame.draw.rect(surface, (255, 255, 255), (field[0]-10, field[1]-10, field[2]+10, field[3]+10), width=10, border_radius=5, border_top_left_radius=-5, border_top_right_radius=-5,
                     border_bottom_left_radius=-5, border_bottom_right_radius=-5)

def draw_healthbar(surface, player, width, height):
    pygame.draw.rect(surface, (100, 100, 100), (10, 10, player.get_maxhealth()*width, height), width=0, border_radius=5, border_top_left_radius=-5, border_top_right_radius=-5,
                     border_bottom_left_radius=-5, border_bottom_right_radius=-5)
    pygame.draw.rect(surface, (255, 0, 0), (10, 10, player.get_health()*width, height), width=0, border_radius=5, border_top_left_radius=-5, border_top_right_radius=-5,
                     border_bottom_left_radius=-5, border_bottom_right_radius=-5)

def check_gameover(surface, health):
    if health <= 0:
        pygame.font.init()
        text = pygame.font.SysFont("Arcade", 120).render("GAME OVER!", True, (255, 255, 255))
        surface.blit(text, (s_width/2-text.get_width()/2, 100))
        for wait in range(100):
            pygame.time.delay(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: break
            pygame.display.update()
        return True
    else: return False

def launch_projectile(projectiles, pattern):
    if pattern == "Random Beam":
        height = random.randint(20, 200)
        if random.randint(1, 2) == 1:
            projectiles.append(Bullet(win, (255, 255, 255), (0, random.randint(0, field[3]-height)), (10, height), (random.randint(2, 10), 0), 5, 0))
        else:
            projectiles.append(Bullet(win, (255, 255, 255), (field[2]-20, random.randint(0, field[3]-height)), (10, height), (random.randint(-10, -2), 0), 5, 0))
    if pattern == "Bullet":
        if random.randint(1, 2) == 1:
            projectiles.append(Bullet(win, (255, 0, 0), (0, random.randint(10, field[3]-10)), (10, 10), (random.randint(6, 20), 0), 5, 0))
        else:
            projectiles.append(Bullet(win, (255, 0, 0), (field[2]-20, random.randint(0, field[3])), (10, 10), (random.randint(-20, -6), 0), 5, 0))
    if pattern == "Fixed Beam":
        if random.randint(1, 2) == 1:
            projectiles.append(Bullet(win, (255, 255, 255), (0, -10), (10, random.randint(20, field[3]//2)), (random.randint(2, 10), 0), 5, 0))
        else:
            height = random.randint(20, field[3]/2)
            projectiles.append(Bullet(win, (255, 255, 255), (field[2]-20, field[3]-height), (10, height), (random.randint(-10, -2), 0), 5, 0))
    if pattern == "Double":
        height = field[3]/2
        projectiles.append(Bullet(win, (255, 255, 255), (0, -10), (10, height), (5, 0), 5, 0))
        projectiles.append(Bullet(win, (255, 255, 255), (field[2]-20, field[3]-height), (10, height), (-5, 0), 5, 0))

def resize():
    global s_width, s_height, field
    field[0] = s_width/2-field[2]/2
    field[1] = s_height/2-field[3]/2
    s_width, s_height = pygame.display.get_surface().get_size()

def main():
    run = True
    
    clock = pygame.time.Clock()
    timecount = 0
    projectiles = []
    player = Player(win, (50, 50, 255), (100, 100), (20, 20), 5, 0, (5, 20))

    while run:
        clock.tick(60)
        timecount += clock.get_rawtime()

        if timecount/1000 >= 0.1:
            timecount = 0
            launch_projectile(projectiles, "Fixed Beam")
            launch_projectile(projectiles, "Bullet")
            launch_projectile(projectiles, "Random Beam")
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        resize()
        redraw_window(win)
        player.update()
        if check_gameover(win, player.get_health()):
            run = False
        
        projectile = 0
        while projectile < len(projectiles)-1:
            if projectiles[projectile].check_bounds(s_width, s_height): del projectiles[projectile]
            else:
                projectiles[projectile].update()
                if projectiles[projectile].check_collision(player.get_character()):
                    player.damage(projectiles[projectile].get_damage())
                    del projectiles[projectile]
                else: projectile += 1
        
        draw_healthbar(win, player, 20, 20)
        pygame.display.update()
        
    pygame.display.quit()

if __name__ == "__main__":
    main()
