#include <iostream>
#include <vector>
#include <queue>
#include <fstream>
#include <sstream>
#include <map>

const int MIN_INF = 1e-9;

// стрруктура ребра)

struct Edge
{
    std::string from, to; // Начальная и конечная вершина
    double capacity; // П(р)опускная способность ребра (вес, который может вместиь)
    double flow = 0; // Текущий поток
};

std::vector<Edge> edges; // Список всех ребер (включая обратные)
std::map<std::string, std::vector<int>> adj; // Список смежности: вершина -> индексы ребер
std::map<std::string, int> level; // Уровни вершин, поскольку алгоритм Диница
std::map<std::string, int> ptr; // Указатели на "текущий" ребро, как отслеживатель

/// Добавление ребра в граф

void add_edge(const std::string& u, const std::string& v, double cap)
{
    edges.push_back({u, v, cap}); // прямое ребро
    edges.push_back({v, u, 0}); // обратное ребро
    int id = edges.size();
    adj[u].push_back(id - 2); // индекс прямого ребра
    adj[v].push_back(id - 1); // индекс обратного ребра
}

/// Построение уровневого графа
/// Асимптотика: Время: O(V + E), где V - вершины, E - ребра
/// Память: O(V), где V - вершины


bool bfs(const std::string& s, const std::string& t)
{
    level.clear();
    std::queue<std::string> q;
    q.push(s); // Ну исток и исток че бубнить то
    level[s] = 0; // изначально нолик, логично же

    while (!q.empty()) // Обходим все вершинки
    {
        std::string v = q.front();
        q.pop();
        for (int id : adj[v]) // Проходим все ребра из этой вершинки
        {
            const Edge& e = edges[id];
            // Если вершина имеет еще п(р)опускную способность и мы её не посеетили
            if (e.capacity - e.flow > MIN_INF && !level.count(e.to))
            {
                level[e.to] = level[v] + 1; // повышаем уровень (в вовку поиграть хочу)
                q.push(e.to); // кидаем
            }
        }
    }
    return level.count(t); // Опа путь есть
}

/// DFS для нахождения блокирующего потока
/// Асимптотика: Время:  O(V + E), где V - вершины, E - ребра
///  Память: O(V), где V - вершины


double dfs(const std::string& v, const std::string& t, double pushed)
{
    if (pushed == 0) return 0; // Нет пути - нет поиска потоков
    if (v == t) return pushed; // ААААААААААААААА ОН ЕСТЬ
    // Путь из истока в сток(((((((

    for (int& cid = ptr[v]; cid < adj[v].size(); cid++) // Проходим по всем ребрам из вершины
    {
        int id = adj[v][cid];
        Edge& e = edges[id];
        // Переходим по ребру только если:
        // 1. Следующая вершина на уровне +1
        // 2. Остался ненулевой остаточный поток
        if (level[v] + 1 != level[e.to] || e.capacity - e.flow < 1e-9) continue;
        // Поток поток поточек
        double tr = dfs(e.to, t, std::min(pushed, e.capacity - e.flow));
        if (tr > MIN_INF)
        {
            edges[id].flow += tr; // Увеличиваем поток этого ребра
            edges[id ^ 1].flow -= tr; // Уменьшаем поток обратного ребра
            return tr; // ГООООООООЛ, наш текущий поток ребра
        }
    }
    return 0;
}

/// Алгоритм Диница для поиска максимального потока
/// Асимптотика:
///   - O(E * V²) в общем случае для графов с вещественными числами
///   - O(E * √V) для целочисленных графов

double dinic(const std::string& s, const std::string& t) // Исток сток как параметры
{
    double flow = 0; // Максмальный поточек)
    while (bfs(s, t)) // Пока мы можем построить уровневый граф => есть путь с потоком
    {
        ptr.clear();
        for (auto& [v, _] : adj) ptr[v] = 0;
        while (double pushed = dfs(s, t, 1e9)) // Пока не найдем поток, который превысит наш capacity
            flow += pushed; // Добавляем в макс поток текущий поток
    }
    return flow;
}

/// Загрузка графа из файла, который был создан в питончике, форматом:
/// vertex neighbor1?weight1 neighbor2?weight2 ...

void load_graph(const std::string& filename)
{
    std::ifstream file(filename);
    std::string line;

    while (getline(file, line))
    {
        std::stringstream ss(line);
        std::string vertex;
        ss >> vertex;

        std::string neighbor_weight;
        while (ss >> neighbor_weight)
        {
            size_t pos = neighbor_weight.find('?');
            if (pos != std::string::npos)
            {
                std::string neighbor = neighbor_weight.substr(0, pos);
                double weight = 1.0 / std::stod(neighbor_weight.substr(pos + 1));
                add_edge(vertex, neighbor, weight);
            }
        }
    }
}

void calculate_flow(const std::string& graph_path, // Путь до списка смежности
                    const std::string& source, // Исток
                    const std::string& sink, // Сток
                    const std::string& label) // Шо б красиво выводилось
{
    load_graph(graph_path);

    double flow = dinic(source, sink);

    std::cout << "[" << label << "]" << std::endl;
    std::cout << "Max flow: " << flow << "\n\n";
}
