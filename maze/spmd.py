import pygame
from random import choice

RES = WIDTH, HEIGHT = 960, 640
TILE = 20
cols, rows = WIDTH // TILE, HEIGHT // TILE

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
    
    def draw_current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color('#f70067'),
                         (x + 2, y + 2, TILE - 2, TILE - 2))
    
    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, pygame.Color('#1e1e1e'),
                             (x, y, TILE, TILE))
        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('#1e4f5b'), 
                             (x, y), (x + TILE, y), 3)
        if self.walls['right']:
            pygame.draw.line(sc, pygame.Color('#1e4f5b'), 
                             (x + TILE, y), 
                             (x + TILE, y + TILE), 3)
        if self.walls['bottom']:
            pygame.draw.line(sc, pygame.Color('#1e4f5b'), 
                             (x + TILE, y + TILE),
                             (x , y + TILE), 3)
        if self.walls['left']:
            pygame.draw.line(sc, pygame.Color('#1e4f5b'), 
                             (x, y + TILE), (x, y), 3)
            
    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]
    
    def check_neighbors(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False   

def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False 

grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]
stack = []
colors, color = [], 40

player_pos = (0, 0)  # Player starts at the top-left corner

class Enemy:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.color = (0, 0, 255)  # Blue
        self.speed = 1  # Adjust speed as needed

    def move(self):
        next_cell = current_cell.check_neighbors()
        if next_cell:
            self.x, self.y = next_cell.x, next_cell.y

enemy = None

while True:
    sc.fill(pygame.Color('#a6d5e2'))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            # Move the player based on arrow key inputs
            if event.key == pygame.K_UP:
                next_cell = current_cell.check_cell(player_pos[0], player_pos[1] - 1)
                if next_cell and not current_cell.walls['top']:
                    player_pos = (player_pos[0], player_pos[1] - 1)
                    current_cell = next_cell
            elif event.key == pygame.K_DOWN:
                next_cell = current_cell.check_cell(player_pos[0], player_pos[1] + 1)
                if next_cell and not next_cell.walls['top']:
                    player_pos = (player_pos[0], player_pos[1] + 1)
                    current_cell = next_cell
            elif event.key == pygame.K_LEFT:
                next_cell = current_cell.check_cell(player_pos[0] - 1, player_pos[1])
                if next_cell and not current_cell.walls['left']:
                    player_pos = (player_pos[0] - 1, player_pos[1])
                    current_cell = next_cell
            elif event.key == pygame.K_RIGHT:
                next_cell = current_cell.check_cell(player_pos[0] + 1, player_pos[1])
                if next_cell and not next_cell.walls['left']:
                    player_pos = (player_pos[0] + 1, player_pos[1])
                    current_cell = next_cell
    
    [cell.draw() for cell in grid_cells]
    current_cell.visited = True
    current_cell.draw_current_cell()
    [pygame.draw.rect(sc, colors[i], 
                      (cell.x * TILE + 2, cell.y * TILE + 2,
                       TILE - 4, TILE - 4), border_radius=8) for i,
                       cell in enumerate(stack)] 
    
    next_cell = current_cell.check_neighbors()
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        colors.append((min(color, 255), 0, 103))
        color += 1
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack: 
        current_cell = stack.pop()
    
    # Draw the player
    pygame.draw.rect(sc, pygame.Color('#f9ed69'), (player_pos[0] * TILE, player_pos[1] * TILE, TILE, TILE))
    
    # Spawn enemy at halfway point
    if player_pos[0] >= cols // 2 and enemy is None:
        enemy = Enemy(0, 0)
    
    # Move the enemy
    if enemy:
        enemy.move()
        pygame.draw.rect(sc, enemy.color, (enemy.x * TILE, enemy.y * TILE, TILE, TILE))
        
        # Collision detection with player
        if enemy.x == player_pos[0] and enemy.y == player_pos[1]:
            player_pos = (0, 0)  # Respawn player
            enemy = None  # Remove enemy
        
    pygame.display.flip()
    clock.tick(30)
