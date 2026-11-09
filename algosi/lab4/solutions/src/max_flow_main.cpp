#include "max_flow.cpp"


int main()
{
    std::string source = "кое-кто_NOUN"; // Исток
    std::string sink = "идиот_NOUN"; // Сток

    // Изначальный граф без обучения (бож лучше б я траву трогал)
    calculate_flow("../adj_graph_with_weights.txt", source, sink, "Flow from graph before training");

    // Граф на обученной модельке
    calculate_flow("../adj2_with_weights.txt", source, sink, "Flow from graph after training");

    return 0;
}
