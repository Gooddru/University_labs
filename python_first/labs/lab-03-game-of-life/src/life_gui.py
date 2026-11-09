import pygame
from .life import GameOfLife
from pygame.locals import *
from .ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size  # Размер клетки в пикселях
        self.speed = speed  # Скорость обновления экрана в кадрах в секунду
        self.height = self.life.rows * self.cell_size  # Высота игрового поля
        self.width = self.life.cols * self.cell_size  # Ширина окна

        # Добавляем дополнительное пространство под кнопки
        self.button_height = 50  # Высота области для кнопок
        self.screen_size = (
            self.width,
            self.height + self.button_height,
        )  # Создаем окно с кнопками

        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Состояния паузы и работы
        self.paused = True
        self.running = True

        # Кнопки "Start" и "Stop"
        self.button_start = pygame.Rect(10, self.height + 10, 80, 30)
        self.button_stop = pygame.Rect(100, self.height + 10, 80, 30)

    def draw_lines(self) -> None:
        # Рисуем линии сетки
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        # Рисуем клетки на поле
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                # Устанавливаем цвет клетки: зелёный для живой, белый для мёртвой
                color = "green" if self.life.curr_generation[i][j] == 1 else "white"
                # Вычисляем координаты клетки и рисуем её на экране
                coords = (
                    j * self.cell_size + 1,
                    i * self.cell_size + 1,
                    self.cell_size - 1,
                    self.cell_size - 1,
                )
                pygame.draw.rect(self.screen, color, coords)

    def draw_buttons(self) -> None:
        # Рисуем кнопки "Start" и "Stop"
        font = pygame.font.Font(None, 24)
        pygame.draw.rect(self.screen, pygame.Color("lightgray"), self.button_start)
        pygame.draw.rect(self.screen, pygame.Color("lightgray"), self.button_stop)
        text_start = font.render("Start", True, pygame.Color("black"))
        text_stop = font.render("Stop", True, pygame.Color("black"))
        self.screen.blit(text_start, (self.button_start.x + 10, self.button_start.y + 5))
        self.screen.blit(text_stop, (self.button_stop.x + 10, self.button_stop.y + 5))

    def run(self) -> None:
        # Запускаем игру
        pygame.init()
        clock = pygame.time.Clock()  # Создаем объект для управления временем
        pygame.display.set_caption("Game of Life")  # Устанавливаем заголовок окна для приложения
        self.screen.fill(pygame.Color("white"))  # Заливаем экран белым цветом
        self.draw_lines()  # Рисуем сетку

        # Текст "Paused"
        font = pygame.font.Font(None, 36)
        text_pause = font.render("Paused", True, pygame.Color("red"))
        text_pause_rect = text_pause.get_rect(center=(self.width // 2, 20))

        press_mouse = True  # Переменная для отслеживания состояния при нажатии мыши

        while self.running:
            for event in pygame.event.get():
                # Обработка закрытия окна
                if event.type == QUIT:
                    self.running = False

                # Обработка нажатий клавиш
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.paused = not self.paused  # Переключение паузы по пробелу
                    elif event.key == K_s:  # Запуск по кнопке S
                        self.paused = False
                    elif event.key == K_q:  # Выход по кнопке Q
                        self.running = False

                elif event.type == MOUSEBUTTONDOWN:  # Обработка нажатия левой кнопки мыши
                    if event.button == 1:
                        mouse_pos = event.pos  # Получаем координаты клика

                        # Проверяем, попадает ли клик в область кнопки "Start"
                        if self.button_start.collidepoint(mouse_pos):
                            self.paused = False

                        # Проверяем, попадает ли клик в область кнопки "Stop"
                        elif self.button_stop.collidepoint(mouse_pos):
                            self.paused = True

                        # Обработка нажатия на игровое поле для изменения состояния клетки
                        else:
                            button_j, button_i = mouse_pos
                            if button_i < self.height:  # Игнорируем нажатия на область с кнопками
                                i, j = (button_i - 1) // self.cell_size, (
                                    button_j - 1
                                ) // self.cell_size
                                # Меняем состояние клетки на противоположное
                                self.life.curr_generation = self.life.prev_generation
                                self.life.curr_generation[i][j] = 1 if press_mouse else 0
                                press_mouse = not press_mouse
                                self.draw_grid()  # Перерисовываем сетку
                                self.life.step()  # Переход к следующему шагу игры

            # Обновляем сетку и выполняем шаг игры, если не на паузе
            if (
                not self.paused
                and self.life.is_changing
                and not self.life.is_max_generations_exceeded
            ):
                self.draw_grid()
                self.life.step()

            # Отображение текста "Paused" при остановке
            if self.paused:
                self.screen.blit(text_pause, text_pause_rect)

            self.draw_buttons()  # Рисуем кнопки на экране
            pygame.display.flip()  # Обновляем экран
            clock.tick(self.speed)

        pygame.quit()


# Пример запуска игры
life = GameOfLife((40, 60), max_generations=50)
GUI(life).run()
