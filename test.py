import pygame
import random
import sys

# pygame 모듈 초기화 확인
try:
    pygame.init()
    pygame.font.init()
except ImportError as e:
    print("pygame 모듈이 설치되지 않았습니다. pip install pygame 을 실행하세요.")
    sys.exit(1)

# 설정
CELL_SIZE = 15  # 미로 경로 폭을 더 줄이기
MARGIN = 10
FIXED_SIZE = 15  # 난이도 5 이후로 화면 크기 고정
MAX_SCREEN_SIZE = 800  # 최대 화면 크기

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# 방향 (상, 하, 좌, 우)
DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]


def generate_maze(size):
    maze = [[1] * (size * 2 + 1) for _ in range(size * 2 + 1)]
    start_x, start_y = 1, 1
    maze[start_y][start_x] = 0
    stack = [(start_x, start_y)]

    while stack:
        x, y = stack[-1]
        neighbors = []

        random.shuffle(DIRECTIONS)  # 미로를 더 복잡하게 만들기 위해 랜덤화 강화
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 < nx < size * 2 and 0 < ny < size * 2 and maze[ny][nx] == 1:
                neighbors.append((nx, ny, x + dx, y + dy))

        if neighbors:
            nx, ny, wall_x, wall_y = random.choice(neighbors)
            maze[ny][nx] = 0
            maze[wall_y][wall_x] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

    maze[size * 2 - 1][size * 2] = 0  # 출구
    return maze


def draw_maze(screen, maze, size, player, ghosts, checkpoints, exit_pos):
    for y in range(size * 2 + 1):
        for x in range(size * 2 + 1):
            color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * CELL_SIZE + MARGIN, y * CELL_SIZE + MARGIN, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, BLUE,
                     (player[0] * CELL_SIZE + MARGIN, player[1] * CELL_SIZE + MARGIN, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, YELLOW,
                     (exit_pos[0] * CELL_SIZE + MARGIN, exit_pos[1] * CELL_SIZE + MARGIN, CELL_SIZE, CELL_SIZE))
    for ghost in ghosts:
        pygame.draw.rect(screen, RED,
                         (ghost[0] * CELL_SIZE + MARGIN, ghost[1] * CELL_SIZE + MARGIN, CELL_SIZE, CELL_SIZE))
    for checkpoint in checkpoints:
        pygame.draw.rect(screen, GREEN,
                         (checkpoint[0] * CELL_SIZE + MARGIN, checkpoint[1] * CELL_SIZE + MARGIN, CELL_SIZE, CELL_SIZE))


def move_ghosts(ghosts, player, maze):
    for i in range(len(ghosts)):
        gx, gy = ghosts[i]
        possible_moves = [(gx + dx, gy + dy) for dx, dy in DIRECTIONS if maze[gy + dy][gx + dx] == 0]
        if possible_moves:
            ghosts[i] = min(possible_moves, key=lambda pos: abs(pos[0] - player[0]) + abs(pos[1] - player[1]))


def main():
    while True:  # 게임이 유령에게 잡히면 다시 시작
        size = FIXED_SIZE
        player = [1, 1]
        maze = generate_maze(size)
        exit_pos = [size * 2, size * 2 - 1]
        ghost1 = [(player[0] + exit_pos[0]) // 2, (player[1] + exit_pos[1]) // 2]
        ghost2 = [(player[0] + exit_pos[0]) // 2 + 1, (player[1] + exit_pos[1]) // 2]
        ghosts = [ghost1, ghost2]
        checkpoints = [
            (size // 2, size // 2),
            (size - 2, 2),
            (2, size - 2)
        ]

        screen_size = (size * 2 + 1) * CELL_SIZE + MARGIN * 2
        screen = pygame.display.set_mode((screen_size, screen_size))
        pygame.display.set_caption("미로 게임")

        running = True
        clock = pygame.time.Clock()

        while running:
            screen.fill(BLACK)
            draw_maze(screen, maze, size, player, ghosts, checkpoints, exit_pos)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    new_x, new_y = player
                    if event.key == pygame.K_w and maze[player[1] - 1][player[0]] == 0:
                        new_y -= 1
                    elif event.key == pygame.K_s and maze[player[1] + 1][player[0]] == 0:
                        new_y += 1
                    elif event.key == pygame.K_a and maze[player[1]][player[0] - 1] == 0:
                        new_x -= 1
                    elif event.key == pygame.K_d and maze[player[1]][player[0] + 1] == 0:
                        new_x += 1
                    if (new_x, new_y) not in ghosts:
                        player[0], player[1] = new_x, new_y

            move_ghosts(ghosts, player, maze)

            if player in ghosts:
                break  # 유령에게 잡히면 게임 처음부터 재시작

            if player == exit_pos:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    main()
