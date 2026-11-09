#include <sstream>
#include <string>
#include <cmath>
#include <limits>

enum Color {
    RED,
    BLACK
};

struct Node {
    std::string film_name;
    double sum_ratings;
    double avg_rating;
    int count_ratings;

    Color color;
    Node *left, *right, *parent;

    Node(const std::string &name, double rating)
        : film_name(name), sum_ratings(rating), avg_rating(rating), count_ratings(1),
          color(RED), left(nullptr), right(nullptr), parent(nullptr) {
    }

    /**
     * Обновить значение рейтиинга.
     * 
     * @note При добавлении новой оценки к фильму:
     * 
        - Обновите сумму оценок и увеличьте количество оценок.

        - Пересчитайте среднюю оценку.
        Если текущая средняя оценка равна `avg`,
        количество оценок равно `n`,
        а новая оценка равна `r`,
        то новое значение средней оценки вычисляется по формуле:  
            
        `новое среднее = ((avg × n) + r) / (n + 1)`
     
     */
    void updateRating(double newRating) {
        // Вычисляем среднее из уже поставленных оценок фильма
        avg_rating = ((avg_rating * count_ratings) + newRating) / (count_ratings + 1);
        sum_ratings = sum_ratings + newRating;
        // Обновляем сумму всех оценок фильма, шо б обидно не было, тем, кто поставил
        count_ratings++;
        // Увеличиваем количество оценок фильма
    }
};


class RBTree {
public:
    Node *root;

    RBTree() : root(nullptr) {
    }

    /**
     * Левое вращение вокруг узла x.
     * 
     * @param x нода, вокруг которой будет выполняться вращение
     *
     * Асимптотика:
     * - Время: О(1)
     * - Память: О(1)
     */

    void leftRotate(Node *x) {
        Node *y = x->right; // Сохраняем правое дите x в y
        x->right = y->left; // Перемещаем левое поддерево y в правое поддерево x
        if (y->left) {
            // Если левое поддерево y существует, обновляем его папу или маму
            y->left->parent = x;
        }
        y->parent = x->parent; // Переносим родителя x в y

        // Обновляем корень дерева
        if (x->parent == nullptr) {
            root = y;
            // Если x был корнем, y становится новым корнем дерева
        } else if (x == x->parent->left) {
            x->parent->left = y;
            // Если x был левым потомком, y становится новым левым потомком
        } else {
            x->parent->right = y;
            // Если x был правым потомком, y становится новым правым потомком
        }
        y->left = x; // х - левый потомок у
        x->parent = y; // родитель у х - у
    }

    /**
     * Правок вращение вокруг узла x.
     * 
     * @param x нода, вокруг которой будет выполняться вращение
     *
     * Асимптотика:
     * - Время: О(1)
     * - Память: О(1)
     */

    void rightRotate(Node *y) {
        Node *x = y->left; // Сохраняем левый дите y в x
        y->left = x->right; // Перемещаем правое поддерево x в левое поддерево y

        // Если правое поддерево x существует, его папу или маму
        if (x->right != nullptr) {
            x->right->parent = y;
        }
        x->parent = y->parent; // Переносим родителя y в x

        // Обновляем корень дерева
        if (y->parent == nullptr) {
            root = x;
            // Если y был корнем, x становится новым корнем
        } else if (y == y->parent->left) {
            y->parent->left = x;
            // Если y был левым потомком, x становится новым левым потомком
        } else {
            y->parent->right = x;
            // Если y был правым потомком, x становится новым правым потомком
        }

        x->right = y; // Делаем y правым потомком x
        y->parent = x; // Родитель у y - x
    }

    /**
     * Вставить/обновить фильм и рейтинг
     * 
     * @param film_name название фильма
     * @param rating рейтинг
     *
     * Асимптотика:
     *  - Время: O(log n)
     *  - Память: О(1)

     */

    void insert(const std::string &film_name, double rating) {
        Node *x = root; // Текущий узел (корень)
        Node *y = nullptr; // Родительский узел
        Node *z = new Node(film_name, rating); // Узел для вставки
        while (x) {
            y = x;
            if (x->film_name == film_name) {
                // Проверяем есть ли у нас уже такой фильм
                x->updateRating(rating); // Тогда обновляем его рейтинг
                delete z; // Шо б не было бабах-бубух компу
                return;
            }
            if (film_name < x->film_name) {
                // Смотрим куда вставить
                x = x->left; // В левое поддерево
            } else {
                x = x->right; // В правое
            }
        }
        z->parent = y; // Родитель для нового узла
        if (!y) {
            // Если дерево пустое
            root = z; // Этот узел и будет корнем
        } else if (y->film_name < film_name) {
            // Проверяем чтоб правильно вставить в бинарное дерево (в данном случае лексико-графический порядок)
            y->right = z; // Вставляем в правое поддерево
        } else {
            y->left = z; // Вставляем в левое поддерево
        }
        fixInsert(z); // Восстанавливаем свойства к-ч дерева
    }

    /**
     * Восстановить свойства красно-черного дерева после вставки.
     * 
     * @param node вставленный узел, который нужно исправить
     *
     * Асимптотика:
     * - Время: O(log n)
     * - Память: О(1)
     */

    void fixInsert(Node *node) {
        // Проверяем не стоят ли два красных подряд (родитель и потомок)
        while (node->parent && node->parent->color == RED) {
            if (node->parent == node->parent->parent->left) {
                // Наш родитель левый потомок своего родителя и он - красный
                Node *y = node->parent->parent->right; // получаем этого родителя (Дядя)
                if (y && y->color == RED) {
                    // Если он красный, то перекрашиваем
                    y->color = BLACK;
                    node->parent->color = BLACK;
                    node->parent->parent->color = RED;
                    node = node->parent->parent; // проверяем то же самое, только для родительского узла нашего узла
                } else {
                    // Если дядя черный
                    if (node == node->parent->right) {
                        node = node->parent;
                        leftRotate(node); // Делаем левый поворот для восстановления баланса в дереве (от родителя)
                    }
                    // Перекрашиваем и делаем правый поворот (от дедуса)
                    node->parent->color = BLACK;
                    node->parent->parent->color = RED;
                    rightRotate(node->parent->parent);
                }
            } else {
                // Наш родитель правый потомок своего родителя и он - красный
                Node *y = node->parent->parent->left;
                if (y && y->color == RED) {
                    // Если дед красный просто перекрашиваем
                    y->color = BLACK;
                    node->parent->color = BLACK;
                    node->parent->parent->color = RED;
                    node = node->parent->parent;
                } else {
                    // Дядя - раб (черный)
                    if (node == node->parent->left) {
                        node = node->parent;
                        rightRotate(node); // Делаем правый поворот для восстановления баланса в дереве (от родителя)
                    }
                    // Перекрашиваем и делаем левый поворот (от дедуса)
                    node->parent->color = BLACK;
                    node->parent->parent->color = RED;
                    leftRotate(node->parent->parent);
                }
            }
        }
        // ну и по базе корень должен быть черным (дешевым)
        root->color = BLACK;
    }

    /**
     * Найти фильм по названию
     * 
     * @param film_name название фильма
     * 
     * @return указатель на ноду, содержащий фильм. nullptr если не найдено.
     *
     * Асимптотика:
     * - Время: O(log n)
     * - Память: О(1)
     */
    Node *search(const std::string &film_name) {
        Node *current = root; // Пусть наш поиск начнется с корня
        while (current) {
            if (film_name == current->film_name) return current; // Ищем узел с требуемым названием, если он текущий
            // возвращаем его
            if (film_name < current->film_name) // Смотрим в какое поддерво нам идти
                current = current->left; // Левое
            else
                current = current->right; // Правое
        }
        return nullptr; // Если такого нет - нуллптр =)
    }

    /**
     * Обход по порядку для поиска узла со средним рейтингом, наиболее близким к target_rating.
     * 
     * @param node
     * @param target_rating таргетный рейтинг
     * 
     * @param bestMatch наиболее подходящий узел, найденный на данный момент. 
     * @param bestDiff наименьшая разница между целевым и фактическим рейтингами, найденными на данный момент.
     *
     * Асимптотика:
     * - Время: O(n)
     * - Память O(h), где h - высота дерева (в худшем случае O(n)) (РЕКУРСИЯ БРАТЬЯ)
     */
    void inOrderRecommend(Node *node, double target_rating, Node *&bestMatch, double &bestDiff) {
        if (!node) return; // Заканчием рекурсию ататата, если конец узла
        inOrderRecommend(node->left, target_rating, bestMatch, bestDiff); // Обходим левое поддерево
        double diff = std::abs(node->avg_rating - target_rating);
        // Посчитаем отклонение среднего рейтинга от нашего заданного по поиску
        if (diff < bestDiff) {
            // Если наше отклонение меньше, чем лучшее
            bestDiff = diff; // Лучшее становится нашим
            bestMatch = node; // Это и будет лучший фильм с заданным рейтингом
            if (bestDiff == 0) return; // Его и выведем, усе, ценок
        }
        inOrderRecommend(node->right, target_rating, bestMatch, bestDiff); // Обходим правое поддерево, если не нашли
    }

    /**
     * Получить рекомендацию — фильм со средним рейтингом, наиболее близким к target_rating.
     *
     * @param target_rating таргет тейтинг
     *
     * @return нода на лучшее совпадение. если не найдено - nullptr
     * Асимптотика:
     * - Время: O(n)
     * - Память: O(h) - рекурсия
     */
    Node *recommend(double target_rating) {
        Node *bestMatch = nullptr; // Пусть лучшего фильма не существует (лучшее совпадение)
        double bestDiff = INFINITY; // Чтоб быстренько всегда искало, сделаем бесконечностью
        inOrderRecommend(root, target_rating, bestMatch, bestDiff); // Ищем такое совпадение
        return bestMatch;
    }
};
