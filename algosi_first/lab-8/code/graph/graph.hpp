#ifndef POLYGON_GRAPH_H
#define POLYGON_GRAPH_H

#include <vector>
#include <string>
#include <unordered_map>
#include <memory>
#include <cmath>
#include <iostream>

// Класс для представления узла графа
class Node {
public:
    // Конструктор узла, принимает долготу и широту
    Node(double lon, double lat);

    // Получение долготы (longitude) узла
    double getLongitude() const;

    // Получение широты (latitude) узла
    double getLatitude() const;

    // Получение списка рёбер, связанных с данным узлом (вектор пар "соседний узел - вес рёбер")
    const std::vector<std::pair<Node *, double>> &getEdges() const;

    // Добавление рёбер (соседнего узла и веса рёбер)
    void addEdge(Node *node, double weight);

    // Список рёбер, каждое ребро - это пара (соседний узел, вес рёбер)
    std::vector<std::pair<Node *, double>> edges;

    // Широта (latitude) узла
    double lat;

    // Долгота (longitude) узла
    double lon;
};

// Класс для представления графа
class Graph {
public:
    // Добавление нового узла в граф
    Node *addNode(double lon, double lat);

    // Получение узла по его координатам (если узел не найден, возвращается nullptr)
    Node *getNode(double lon, double lat);

    // Чтение графа из файла, вероятно, используется для загрузки данных о рёбрах и узлах
    void readFromFile(const std::string &filename);

    // Поиск ближайшего узла в графе на основе координат (широты и долготы)
    Node *findClosestNode(double lat, double lon) const;

    // Функция для вывода пути, представленного вектором узлов
    void printPath(const std::vector<Node *> &path) const;

    // Вектор, содержащий все узлы графа (используется умный указатель для автоматического управления памятью)
    std::vector<std::unique_ptr<Node>> nodes;

private:
    // Структура данных для хранения узлов с ключом, генерируемым на основе координат
    std::unordered_map<std::string, Node *> node_map;
};

#endif // POLYGON_GRAPH_H
