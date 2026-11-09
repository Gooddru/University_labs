import curses

from .life import GameOfLife
from .ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        try:
            screen.subwin(self.life.rows + 2, self.life.cols + 2, 0, 0).box("|", "=")
        except curses.error:
            pass

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                try:
                    if self.life.curr_generation[i][j]:
                        screen.addstr(1 + i, 1 + j, "█")  # Живая клетка
                    else:
                        screen.addstr(1 + i, 1 + j, " ")  # Мертвая клетка
                except curses.error:
                    pass

    def run(self) -> None:
        screen = curses.initscr()  # Инициализация основного окна
        curses.noecho()  # Отключение отображения вводимых символов
        curses.curs_set(0)  # Скрытие курсора
        screen.nodelay(True)
        try:
            # Отрисовка начальных рамок и состояния игрового поля
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            UI.run(self)

            while self.life.is_changing and not self.life.is_max_generations_exceeded:
                self.life.step()  # Переход к следующему поколению
                self.draw_grid(screen)  # Отрисовка нового состояния
                screen.refresh()  # Обновление экрана для отображения изменений
                UI.run(self)
                curses.napms(200)
        except curses.error:
            pass
        finally:
            curses.endwin()


# Пример игры
game = GameOfLife((40, 60), max_generations=50)
console_ui = Console(game)
console_ui.run()
