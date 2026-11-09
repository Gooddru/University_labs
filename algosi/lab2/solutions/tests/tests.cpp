#include "../src/feature_hashing.cpp"

#include <cassert>

void testingHash()
{
    uint32_t hash1 = 100, hash2 = 100, hash3 = 100, hash4 = 10; // Изначальные значения хэша

    MurmurHash3("cutecute", 8, 0, &hash1); // Должно получиться магическое число хэша
    MurmurHash3("cutecute", 8, 0, &hash3); // Должно получиться такое же

    assert(hash1 == hash3);

    MurmurHash3("cutecute", 8, 0, &hash1); // Уже было
    MurmurHash3("nocute", 6, 0, &hash2); // Должен получиться другой хэш

    assert(hash1 != hash2);

    MurmurHash3("", 0, 0, &hash4); // Пустое => хэшироваться нечему, тады 0
    // а вот с пробелом тоже будет 0
    /*MurmurHash3("", 0, 0, &hash4);*/

    assert(hash4 == 0);

    std::cout << "testingHash passed!" << std::endl;
}

void testing_Predict_of_model()
{
    Sample s1, s2; // Тестовый сэмпл
    s1.features = text_to_features("spamspamspam");
    s1.label = 1; // спам
    s2.features = text_to_features("hamhamham");
    s2.label = 0; // не спам

    std::vector<Sample> trainData = {
        s1, s2
    }; // ну надо ж данные
    LogisticRegression model; // используем конструктор

    model.train(trainData, trainData); // Обучим ее на этих же данных
    // Мне лень писать другие

    int pred1 = model.predict(s1.features); // Должно быть >=0.55 => 1 - спам
    int pred2 = model.predict(s2.features); // Должно быть <=0.55 => 0 - спам


    assert(pred1 == 1);
    assert(pred2 == 0);

    std::cout << "testing_Predict_of_model passed!" << std::endl;
}

void test_normalization_features()
{
    std::vector<double> feats = text_to_features("normalization"); // ну фичи

    double norm = 0.0; // считаем нормализацию
    for (double v : feats)
    {
        norm += pow(v, 2);
    }
    norm = std::sqrt(norm);

    assert(std::abs(norm - 1.0) < 1e-5); // Ура это не питон, тут нормально работают дробные значения
    // Мантиссу люблю

    std::cout << "test_normalization_features passed!" << std::endl;
}

int main()
{
    testingHash();
    std::cout << "========================================\n";
    testing_Predict_of_model();
    std::cout << "========================================\n";
    test_normalization_features();
    std::cout << "========================================\n";

    std::cout << "All tests passed!" << std::endl;

    return 0;
}
