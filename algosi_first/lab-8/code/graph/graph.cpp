#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <unordered_map>
#include <cmath>
#include <limits>
#include "graph.hpp"
#include <iomanip>
#include <algorithm>

// Конструктор узла графа, принимает долготу и широту
Node::Node(double lon, double lat) : lon(lon), lat(lat) {}

// Получение долготы (longitude) узла
double Node::getLongitude() const {
    return lon;
}

// Получение широты (latitude) узла
double Node::getLatitude() const {
    return lat;
}

// Получение списка рёбер, связанных с данным узлом
const std::vector<std::pair<Node *, double>> &Node::getEdges() const {
    return edges;
}

// Добавление рёбер (соседнего узла и веса рёбер)
void Node::addEdge(Node *node, double weight) {
    edges.emplace_back(node, weight);
}

// Добавление нового узла в граф
Node *Graph::addNode(double lon, double lat) {
    auto node = std::make_unique<Node>(lon, lat);  // Создаем новый узел
    Node *node_ptr = node.get();  // Получаем указатель на этот узел
    nodes.push_back(std::move(node));  // Добавляем узел в вектор

    // Генерация ключа для узла, основываясь на его координатах
    std::ostringstream key_stream;
    key_stream << std::fixed << std::setprecision(10) << lon << "," << lat;
    std::string key = key_stream.str();

    // Добавление узла в мапу с использованием координат в качестве ключа
    node_map[key] = node_ptr;
    return node_ptr;
}

// Получение узла по его координатам (если узел не найден, возвращается nullptr)
Node *Graph::getNode(double lon, double lat) {
    // Генерация ключа для поиска узла по его координатам
    std::ostringstream key_stream;
    key_stream << std::fixed << std::setprecision(10) << lon << "," << lat;
    std::string key = key_stream.str();

    // Поиск узла в мапе по ключу
    if (node_map.find(key) != node_map.end()) {
        return node_map[key];
    }
    return nullptr;
}

// Чтение графа из файла
void Graph::readFromFile(const std::string &filename) {
    std::ifstream file(filename);  // Открытие файла
    if (!file.is_open()) {  // Если файл не открылся, выводим ошибку
        std::cerr << "Error: can't open file" << filename << std::endl;
        return;
    }

    std::string line;
    // Чтение файла построчно
    while (std::getline(file, line)) {
        std::istringstream line_stream(line);  // Поток для обработки строки
        std::string parent_data, edges_data;

        // Получаем данные родительского узла
        if (std::getline(line_stream, parent_data, ':')) {
            double lon1, lat1;
            // Заменяем запятые пробелами для корректного парсинга
            std::replace(parent_data.begin(), parent_data.end(), ',', ' ');
            std::istringstream parent_stream(parent_data);
            // Чтение координат родительского узла
            if (!(parent_stream >> lon1 >> lat1)) {
                std::cerr << "Error parsing coordinates parents nodes: " << parent_data << std::endl;
                continue;
            }

            // Поиск родительского узла в графе, если его нет — добавляем
            Node *parent_node = getNode(lon1, lat1);
            if (!parent_node) {
                parent_node = addNode(lon1, lat1);
            }

            // Чтение рёбер, связанных с родительским узлом
            while (std::getline(line_stream, edges_data, ';')) {
                double lon2, lat2, weight;
                std::replace(edges_data.begin(), edges_data.end(), ',', ' ');
                std::istringstream edge_stream(edges_data);
                // Чтение координат и веса рёбер
                if (!(edge_stream >> lon2 >> lat2 >> weight)) {
                    std::cerr << "Error parsing edges: " << edges_data << std::endl;
                    continue;
                }

                // Поиск дочернего узла, если его нет — добавляем
                Node *child_node = getNode(lon2, lat2);
                if (!child_node) {
                    child_node = addNode(lon2, lat2);
                }

                // Добавляем рёбра в граф, для обоих узлов
                parent_node->addEdge(child_node, weight);
                child_node->addEdge(parent_node, weight);
            }
        }
    }

    file.close();  // Закрытие файла после чтения
}


// Вывод пути, представленного вектором узлов
void Graph::printPath(const std::vector<Node *> &path) const {
    if (path.empty()) {  // Если путь пуст, выводим сообщение об ошибке
        std::cout << "Path is not find.\n";
        return;
    }

    double total_length = 0.0;  // Инициализация переменной для вычисления общей длины пути
    std::cout << "Path:" << std::endl;
    for (size_t i = 0; i < path.size(); ++i) {
        std::cout << "(" << path[i]->getLatitude() << ", " << path[i]->getLongitude() << ")";
        if (i < path.size() - 1) {
            std::cout << " -> ";
            // Поиск длины ребра между текущим и следующим узлом
            for (const auto &edge: path[i]->getEdges()) {
                if (edge.first == path[i + 1]) {  // Если нашли следующее ребро
                    total_length += edge.second;  // Добавляем его длину
                    break;
                }
            }
        }
    }
    std::cout << "\nTotal length of path: " << total_length << std::endl;  // Выводим общую длину пути
}

// Поиск ближайшего узла в графе на основе координат
Node *Graph::findClosestNode(double lat, double lon) const {
    double minDistance = std::numeric_limits<double>::max();  // Инициализация минимального расстояния
    Node *closestNode = nullptr;

    // Перебираем все узлы в графе
    for (const auto &node: nodes) {
        // Расстояние между узлом и точкой
        double distance = std::sqrt(std::pow(node->getLatitude() - lat, 2) + std::pow(node->getLongitude() - lon, 2));
        if (distance < minDistance) {
            closestNode = node.get();  // Обновляем ближайший узел
            minDistance = distance;    // Обновляем минимальное расстояние
        }
    }

    return closestNode;  // Возвращаем ближайший узел
}
