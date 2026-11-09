#include "MurmurHash3.cpp"

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cmath>
#include <algorithm>
#include <sstream>

#define HASH_DIM 1490 // Размерность
// я так устал методом научного тыка её подбирать

using FEATURE = std::vector<double>;
using LABEL = int;

/**
* Определение типов:
*   - FEATURE: вектор double для хранения признаков.
*   - LABEL: целочисленный тип для метки (0 или 1).
*   - целочисленная константа HASH_DIM (размерность хешированного пространства ).
*/
struct Sample
{
    FEATURE features;
    LABEL label;
};


/**
 * Перевести текст в фичи
 * 
 * Каждый токен к нижнему регистру -> хеш от строки -> feats[index] += 1, где index = хеш % HASH_DIM
 * Затем выполнить L2-нормализацию feats.
 * 
 * @param text 
 * @return vec<double> feats
 * 
 * @solve  
 */
std::vector<double> text_to_features(const std::string& text)
{
    std::vector<double> feats(HASH_DIM, 0.0); // Оп оп вектор для признаков
    std::string word; // оп оп текущее слово
    std::istringstream iss(text);
    while (iss >> word)
    {
        for (auto& symbol : word)
        {
            symbol = std::tolower(symbol);
        }
        uint32_t hash; // ну надо ж где-то хэш хранить
        MurmurHash3(word.c_str(), word.length(), 0, &hash); // ну хэшируем это че бубнить то
        size_t index = hash % HASH_DIM;
        feats[index] += 1;
        // feats[index] += 1, где index = хеш % HASH_DIM
    }

    // L2-нормализация
    // че мне расписывать как нормализация работает?
    // Нормализация L2 (евклидова норма) : масштабирует вектор таким образом, чтобы сумма квадратов его компонентов была равна 1.


    double norm = 0.0;
    for (double value : feats)
    {
        norm += pow(value, 2);
    }
    norm = std::sqrt(norm);
    if (norm > 0)
    {
        for (double& value : feats)
        {
            value /= norm;
        }
    }

    return feats;
}


// Можно использовать внешние источники, но обязательно укажите ссылку на них.
// Если источник = генеративные модели / не будет источников - будет больно на защите.
class LogisticRegression
{
public:
    size_t dim = HASH_DIM; // Размерность признаков ура ура люблю линал
    double lr = 0.01; // Скорость обучения
    double reg_lambda = 0.01; // Коэффициент регуляризации для предотвращения переобучения
    double class_weight_0 = 1.0; // вес для класса 0 (ham)
    double class_weight_1 = 1.0; // вес для класса 1 (spam)
    LogisticRegression()
        : weights(dim, 0.0),
          learning_rate(lr),
          lambda(reg_lambda),
          epochs(500) // ПРОСТО ЛУЧШИЙ ГИПЕРПАРАМЕТР ДЛЯ МЕТОДА НАУЧНОГО ТЫКА
    // ух ты ух ты конструктор с инициализацией =))))))))))
    {
    }

    /**
     * Обучаем логрег.
     * 
     * @param vec<Sample> trainData - наши фичи : labels
     * @param vec<Sample> validData - на чем считаем метрики
     * 
     * тут набросок, можете предложить свой вариант реализации. 
     * например - вывод лосса на обучении, или каджые M эпох уменьшает lr
     * 
     * при указании источника спрашивать как работает не будем.
     * 
     * функция должна обновить weights
     * @solve
     */

    // Логистическая регрессия с стохастическим градиентным спуском, взвешиванием классов, L2- регуляцией
    // тестируя, без регуляции значения были лучше, но пусть будет
    // И остановкой(потому что зачем нам обучать дальше)

    void train(const std::vector<Sample>& trainData, const std::vector<Sample>& validData)
    {
        double best_recall = 0.0;
        double best_accuracy = 0.0; // Лучшая найденная точность
        int improvement_count = 0; // Счетчик эпох без улучшений
        int stop = 200; // Пусть 200 эпох еще чет обучают (как же я устал это подбирать)

        for (size_t epoch = 0; epoch < epochs; epoch++)
        {
            for (const Sample& X : trainData)
            {
                // Вычисляем ошибку
                double error = X.label - sigmoid(dot_product(X.features, weights));
                // Как будто это бессмысленно, т.к данные имеют примерно одинаковое количество
                // UPD : НЕБЕССМЫСЛЕННО
                double class_weight = (X.label == 1) ? class_weight_1 * 3 : class_weight_0;
                error *= class_weight;

                // Обновляем веса градиентным спуском и L2- регуляцией
                for (size_t j = 0; j < weights.size(); j++)
                {
                    weights[j] += learning_rate * (X.features[j] * error - lambda * weights[j]);
                }
            }

            // Оценка точности на валидационной выборке
            std::vector<double> metrics = evaluate(validData);
            double accuracy = (metrics[0] + metrics[1]) / (metrics[0] + metrics[1] + metrics[2] + metrics[3]);
            double recall = metrics[0] / (metrics[0] + metrics[3]);

            /*std::cout << "Epoch " << epoch + 1
                << " | Accuracy: " << accuracy
                << " | Recall: " << recall << std::endl;*/

            // Лучше, значит обновим. Где мой смайлик с очками...
            if (accuracy > best_accuracy || recall > best_recall)
            {
                best_recall = recall;
                best_accuracy = accuracy;
                improvement_count = 0; // ура эпохи снова работают
            }
            else if (++improvement_count == stop) // точность не поменялась - значит эпохи не работают
            {
                /*std::cout << "stop epoch" << epoch + 1 << std::endl;*/
                break; // Че обучать то
            }
        }
    }


    /**
     * Предсказываем класс для новых фичей
     *
     * должна вернуть vec<double> metrics = {0, 0, 0, 0}; // TP, TN, FP, FN
     * @param data - vec<Sample> данные для валидации
     * @solve
     */
    std::vector<double> evaluate(const std::vector<Sample>& data) const
    {
        std::vector<double> metrics; // метрики так метрики
        double TP = 0, // True Positive: спам верно распознан как спам
               TN = 0, // True Negative: не спам верно распознан как не спам
               FP = 0, // False Positive: не спам ошибочно распознан как спам
               FN = 0; // False Negative: спам ошибочно распознан как не спам
        for (const auto& sample : data)
        {
            const int prediction = predict(sample.features);

            /*std::cout << "True label: " << sample.label << ", Prediction: " << prediction << std::endl;*/
            // вроде отдебажил

            if (sample.label == 1 && prediction == 1) // Если правильно определил спам
                TP++;
            else if (sample.label == 0 && prediction == 0) // Если правильно определил неспам
                TN++;
            else if (sample.label == 0 && prediction == 1) // Если неправильно определил спам (не спам == спам)
                FP++;
            else if (sample.label == 1 && prediction == 0) // Если неправильно определил неспам (спам == неспам)
                FN++;
        }
        /*
        std::cout << "TP: " << TP << ", TN: " << TN << ", FP: " << FP << ", FN: " << FN << std::endl;
        */
        // Тож для себя

        metrics.push_back(TP);
        metrics.push_back(TN);
        metrics.push_back(FP);
        metrics.push_back(FN);
        return metrics;
    }


    int predict(const FEATURE& feats) const
    {
        /*double dot_prod = dot_product(weights, feats);
        double sigmoid_value = sigmoid(dot_prod);
        std::cout << "Dot product: " << dot_prod << ", Sigmoid value: " << sigmoid_value << std::endl;*/
        // Для себе отладочка чет вроде как вышло, что у спамных в среднем >=55
        // Я знаю про существования дебагера, мне лень

        return (sigmoid(dot_product(weights, feats)) >= 0.55) ? 1 : 0;
    }

private:
    std::vector<double> weights;
    double learning_rate;
    double lambda;
    int epochs;

    static double dot_product(const FEATURE& w, const FEATURE& x)
    {
        double res = 0.0;
        for (size_t i = 0; i < w.size(); ++i)
        {
            res += w[i] * x[i];
        }
        return res;
    }

    // Ну скалярное произведение

    // можете использовать другую активацию
    static double sigmoid(double z)
    {
        return 1.0 / (1.0 + exp(-z));
    }
};

/**
 * Загрузить данные из csv
 * csv формата class,text
 *
 * затем загруженные данные нужно пропустить через text_to_features
 *
 * @param filename путь до файла, указывать как "entrypoiny/FILENAME"
 * @param vec<Sample> data - куда положить загруженные данные
 * @return bool если загрузка успешна
 *
 * @solve
 */
bool read_csv(const std::string& filename, std::vector<Sample>& data)
{
    std::ifstream file(filename);
    if (!file.is_open())
    {
        return false;
    }

    std::string line;
    while (std::getline(file, line))
    {
        size_t delim = line.find(',');
        if (delim == std::string::npos) continue;

        std::string label_str = line.substr(0, delim);
        std::string text = line.substr(delim + 1);

        data.push_back({
            text_to_features(text),
            (label_str == "spam") ? 1 : 0
        });
    }

    file.close();
    return true;
}
