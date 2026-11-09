#ifndef POLYGON_ALGOSI_H
#define POLYGON_ALGOSI_H

#include "../graph/graph.hpp"
#include <vector>
#include <queue>

// Функция для выполнения поиска в ширину (BFS)
// Находит кратчайший путь от узла start до узла goal в графе, если он существует
std::vector<Node *> bfs(Node *start, Node *goal);

// Функция для выполнения поиска в глубину (DFS)
// Находит путь от узла start до узла goal в графе. Не гарантирует кратчайший путь
std::vector<Node *> dfs(Node *start, Node *goal);

// Функция для выполнения алгоритма Дейкстры
// Находит кратчайший путь от узла start до узла goal с использованием алгоритма Дейкстры
// Требует граф с неотрицательными весами рёбер
std::vector<Node *> dijkstra(Graph &graph, Node *start, Node *goal);

// Функция для выполнения алгоритма A* (A-Звезда)
// Находит кратчайший путь от узла start до узла goal с использованием алгоритма A*
// Использует эвристическую функцию для оценки расстояния до цели
std::vector<Node *> A_Star(Graph &graph, Node *start, Node *goal);

#endif //POLYGON_ALGOSI_H
