#include <iostream>
#include <chrono>
#include <vector>
#include "algorithms/pathfinding.hpp"
#include "graph/graph.hpp"

int main() {
    // Создаем граф из файла
    Graph graph;
    graph.readFromFile("../data/spb_graph.txt");

    // Исходные координаты стартовой и целевой точек
    double start_lon = 30.491759, start_lat = 59.910778;  // Координаты старта
    double goal_lon = 30.308405, goal_lat = 59.957237;    // Координаты цели

    // Находим ближайшие вершины (узлы) для заданных координат
    Node *start_node = graph.findClosestNode(start_lat, start_lon);  // Находим узел для старта
    Node *goal_node = graph.findClosestNode(goal_lat, goal_lon);    // Находим узел для цели

    // Проверяем, были ли найдены узлы для старта и цели
    if (!start_node || !goal_node) {
        std::cerr << "Error: start or goal vertex not found." << std::endl;  // Если хотя бы один узел не найден
        return 1;  // Завершаем программу с ошибкой
    }

    // BFS (Поиск в ширину)
    std::cout << "\nResult of BFS:" << std::endl;
    auto start_time = std::chrono::high_resolution_clock::now();  // Записываем время начала
    const std::vector<Node *> bfs_path = bfs(start_node, goal_node);  // Запускаем алгоритм BFS для поиска пути
    auto end_time = std::chrono::high_resolution_clock::now();  // Записываем время окончания
    graph.printPath(bfs_path);  // Выводим найденный путь
    auto bfs_duration = std::chrono::duration_cast<std::chrono::milliseconds>(
            end_time - start_time);  // Рассчитываем время выполнения BFS
    std::cout << "Time of BFS: " << bfs_duration.count() << " ms" << std::endl;  // Выводим время выполнения BFS

    // DFS (Поиск в глубину)
    std::cout << "\nResult of DFS:" << std::endl;
    start_time = std::chrono::high_resolution_clock::now();  // Записываем время начала
    const std::vector<Node *> dfs_path = dfs(start_node, goal_node);  // Запускаем алгоритм DFS для поиска пути
    end_time = std::chrono::high_resolution_clock::now();  // Записываем время окончания
    graph.printPath(dfs_path);  // Выводим найденный путь
    auto dfs_duration = std::chrono::duration_cast<std::chrono::milliseconds>(
            end_time - start_time);  // Рассчитываем время выполнения DFS
    std::cout << "Time of DFS: " << dfs_duration.count() << " ms" << std::endl;  // Выводим время выполнения DFS

    // Dijkstra (Алгоритм Дейкстры)
    std::cout << "\nResult of Dijkstra:" << std::endl;
    start_time = std::chrono::high_resolution_clock::now();  // Записываем время начала
    std::vector<Node *> dijkstra_path = dijkstra(graph, start_node,
                                                 goal_node);  // Запускаем алгоритм Дейкстры для поиска кратчайшего пути
    end_time = std::chrono::high_resolution_clock::now();  // Записываем время окончания
    graph.printPath(dijkstra_path);  // Выводим найденный путь
    auto dijkstra_duration = std::chrono::duration_cast<std::chrono::milliseconds>(
            end_time - start_time);  // Рассчитываем время выполнения Дейкстры
    std::cout << "Time of Dijkstra: " << dijkstra_duration.count() << " ms"
              << std::endl;  // Выводим время выполнения Дейкстры

    // A* (Алгоритм A*)
    std::cout << "\nResult of A*:" << std::endl;
    start_time = std::chrono::high_resolution_clock::now();  // Записываем время начала
    std::vector<Node *> a_star_path = A_Star(graph, start_node,
                                             goal_node);  // Запускаем алгоритм A* для поиска пути с учётом эвристики
    end_time = std::chrono::high_resolution_clock::now();  // Записываем время окончания
    graph.printPath(a_star_path);  // Выводим найденный путь
    auto a_star_duration = std::chrono::duration_cast<std::chrono::milliseconds>(
            end_time - start_time);  // Рассчитываем время выполнения A*
    std::cout << "Time of A*: " << a_star_duration.count() << " ms" << std::endl;  // Выводим время выполнения A*

    return 0;  // Завершаем программу
}
