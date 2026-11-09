#include "pathfinding.hpp"
#include <queue>
#include <stack>
#include <cmath>
#include <limits>
#include <algorithm>

// BFS (Обход в ширину)
// Находит кратчайший путь от стартового узла до целевого в графе, если он существует
std::vector<Node *> bfs(Node *start, Node *goal) {
    if (!start || !goal) {
        return {}; // Возвращаем пустой путь, если start или goal равны nullptr
    }

    std::queue<Node *> queue; // Очередь для обработки узлов
    std::unordered_map<Node *, Node *> came_from; // Хэш-мапа для отслеживания предков узлов
    std::unordered_map<Node *, bool> visited; // Хэш-мапа для отслеживания посещённых узлов
    // Хэш-мапы для оптимизации, чтобы работало не О(ДОХЕРА)

    queue.push(start);
    visited[start] = true;

    // Обрабатываем очередь до тех пор, пока она не пуста
    while (!queue.empty()) {
        Node *current = queue.front();
        queue.pop();

        // Если мы дошли до целевого узла, восстанавливаем путь
        if (current == goal) {
            std::vector<Node *> path;
            for (Node *at = goal; at != nullptr; at = came_from[at]) {
                path.push_back(at);
            }
            std::reverse(path.begin(), path.end()); // Разворачиваем путь
            return path;
        }

        // Для каждого соседа текущего узла
        for (const auto &edge: current->edges) {
            Node *neighbor = edge.first;
            if (!visited[neighbor]) {
                queue.push(neighbor); // Добавляем соседа в очередь
                visited[neighbor] = true; // Помечаем как посещённого
                came_from[neighbor] = current; // Запоминаем, откуда пришли в соседний узел
            }
        }
    }

    return {}; // Путь не найден
}

// DFS (Обход в глубину)
// Находит путь от стартового узла до целевого в графе, используя алгоритм поиска в глубину
std::vector<Node *> dfs(Node *start, Node *goal) {
    if (!start || !goal) {
        return {}; // Возвращаем пустой путь, если start или goal равны nullptr
    }

    std::unordered_map<Node *, bool> visited; // Хэш-мапа для отслеживания посещённых узлов
    std::unordered_map<Node *, Node *> came_from; // Хэш-мапа для отслеживания предков узлов
    std::stack<Node *> stack; // Стек для обработки узлов

    stack.push(start);
    visited[start] = true;

    // Обрабатываем стек до тех пор, пока он не пуст
    while (!stack.empty()) {
        Node *current = stack.top();
        stack.pop();

        // Если достигнут целевой узел, восстанавливаем путь
        if (current == goal) {
            std::vector<Node *> path;
            for (Node *at = goal; at != nullptr; at = came_from[at]) {
                path.push_back(at);
            }
            std::reverse(path.begin(), path.end()); // Разворачиваем путь
            return path;
        }

        // Для каждого соседа текущего узла
        for (const auto &edge: current->edges) {
            Node *neighbor = edge.first;
            if (!visited[neighbor]) {
                stack.push(neighbor); // Добавляем соседа в стек
                visited[neighbor] = true; // Помечаем как посещённого
                came_from[neighbor] = current; // Запоминаем, откуда пришли в соседний узел
            }
        }
    }

    return {}; // Путь не найден
}

// Dijkstra (Алгоритм Дейкстры)
// Находит кратчайший путь от стартового узла до целевого, используя алгоритм Дейкстры
std::vector<Node *> dijkstra(Graph &graph, Node *start, Node *goal) {
    if (!start || !goal) {
        return {}; // Возвращаем пустой путь, если start или goal равны nullptr
    }

    // Минимальные расстояния до узлов
    std::unordered_map<Node *, double> distances;
    // Хэш-мапа для отслеживания, откуда пришли в узел
    std::unordered_map<Node *, Node *> came_from;
    // Хэш-мапа для отслеживания посещённых узлов
    std::unordered_map<Node *, bool> visited;

    // Инициализация расстояний до всех узлов
    for (const auto &node: graph.nodes) {
        distances[node.get()] = std::numeric_limits<double>::infinity();
    }
    distances[start] = 0.0; // Для стартового узла расстояние равно 0

    // Очередь с приоритетом для обработки узлов по минимальному расстоянию
    using PQElement = std::pair<double, Node *>;
    std::priority_queue<PQElement, std::vector<PQElement>, std::greater<>> pq;
    pq.emplace(0.0, start);

    while (!pq.empty()) {
        auto [current_distance, current_node] = pq.top();
        pq.pop();

        if (visited[current_node]) {
            continue; // Если узел уже был посещён, пропускаем его
        }
        visited[current_node] = true;

        // Если текущий узел — это цель, восстанавливаем путь
        if (current_node == goal) {
            std::vector<Node *> path;
            for (Node *at = goal; at != nullptr; at = came_from[at]) {
                path.push_back(at);
            }
            std::reverse(path.begin(), path.end()); // Разворачиваем путь
            return path;
        }

        // Обновление расстояний для соседей текущего узла
        for (const auto &edge: current_node->edges) {
            Node *neighbor = edge.first;
            double weight = edge.second;

            double new_distance = current_distance + weight;
            if (new_distance < distances[neighbor]) {
                distances[neighbor] = new_distance; // Обновляем минимальное расстояние до соседа
                came_from[neighbor] = current_node; // Запоминаем, откуда пришли в соседний узел
                pq.emplace(new_distance, neighbor); // Добавляем соседа в очередь с приоритетом
            }
        }
    }

    return {}; // Путь не найден
}

// A* (Алгоритм A*)
// Функция эвристики: Евклидово расстояние между двумя точками
double heuristic(Node *a, Node *b) {
    return std::sqrt(std::pow(a->lat - b->lat, 2) + std::pow(a->lon - b->lon, 2));
}

// Алгоритм A*
// Находит кратчайший путь от стартового узла до целевого, используя алгоритм A*
// С применением эвристической функции для улучшения производительности
std::vector<Node *> A_Star(Graph &graph, Node *start, Node *goal) {
    if (!start || !goal) {
        return {}; // Возвращаем пустой путь, если start или goal равны nullptr
    }

    // gScore — это стоимость пути от старта до узла
    // fScore — это оценка стоимости пути от старта до цели через узел
    std::unordered_map<Node *, double> gScore;
    std::unordered_map<Node *, double> fScore;
    // Хэщ-мапа — карта для отслеживания, откуда пришли в узел
    std::unordered_map<Node *, Node *> came_from;

    // Инициализация значений для всех узлов
    for (const auto &node: graph.nodes) {
        gScore[node.get()] = std::numeric_limits<double>::infinity();
        fScore[node.get()] = std::numeric_limits<double>::infinity();
    }
    gScore[start] = 0.0;
    fScore[start] = heuristic(start, goal); // Инициализируем fScore для старта

    // Очередь с приоритетом для обработки узлов с наименьшей оценкой fScore
    using PQElement = std::pair<double, Node *>;
    std::priority_queue<PQElement, std::vector<PQElement>, std::greater<>> openSet;
    openSet.emplace(fScore[start], start);

    while (!openSet.empty()) {
        Node *current = openSet.top().second;
        openSet.pop();

        if (current == goal) {
            std::vector<Node *> path;
            for (Node *at = goal; at != nullptr; at = came_from[at]) {
                path.push_back(at);
            }
            std::reverse(path.begin(), path.end()); // Разворачиваем путь
            return path;
        }

        // Для каждого соседа текущего узла
        for (const auto &edge: current->edges) {
            Node *neighbor = edge.first;
            double weight = edge.second;

            double tentative_gScore = gScore[current] + weight;
            if (tentative_gScore < gScore[neighbor]) {
                came_from[neighbor] = current;
                gScore[neighbor] = tentative_gScore;
                fScore[neighbor] = tentative_gScore + heuristic(neighbor, goal); // fScore включает эвристику

                openSet.emplace(fScore[neighbor], neighbor);
            }
        }
    }

    return {}; // Путь не найден
}
