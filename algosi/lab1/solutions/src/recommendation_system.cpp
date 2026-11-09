
#include <iostream>
#include <fstream>
#include <unordered_map>
#include <vector>
#include <algorithm>
#include <string>

#include "red_black_tree.cpp"

int main() {
    // Create separate trees for each genre
    std::vector<std::string> genresTags = {"Биографии", "Комедии", "Ужасы", "Исторические", "Детские",
        "Приключения", "Короткометражки", "Анимация", "Мультфильмы",
        "Криминал", "Военные", "Фантастика", "Игры", "Семейные",
        "Документальные", "Драмы", "Спортивные", "Вестерны", "Музыкальные",
        "Фильмы-нуар", "Мелодрамы", "Реальное ТВ", "Триллеры", "Боевики",
        "Детективы", "Мюзиклы", "Фэнтези"};

    std::unordered_map<std::string, RBTree> genresTrees;
    for (const auto& genre : genresTags) {
        genresTrees[genre] = RBTree();
    }

    std::ifstream infile("data/films.csv");
    if (!infile.is_open()) {
        std::cout << "Error opening films.csv file.\n";
        return 1;
    }

    std::string line;
    std::getline(infile, line); // Header ignore

    while (std::getline(infile, line)) {
        if (line.empty())
            continue;

        std::istringstream iss(line);
        std::string film_name, ratingStr, genre;
        double rating;

        if (std::getline(iss, film_name, ';') &&
            std::getline(iss, ratingStr, ';') &&
            std::getline(iss, genre)) {

            try {
                // genre.erase(std::remove(genre.begin(), genre.end(), "\r"), genre.end());
                genre.erase(std::remove(genre.begin(), genre.end(), '\r'), genre.end());
                rating = std::stod(ratingStr);
                genresTrees.at(genre).insert(film_name, rating);
            } catch (const std::invalid_argument &e) {
                std::cout << "Invalid rating value: " << ratingStr << " in line: " << line << "\n";
                continue;
            } catch (const std::out_of_range &e) {
                std::cout << "Unknow genre: " << genre << "\n";
            } 
        } else {
            std::cout << "Invalid line format: " << line << "\n";
        }
    }
    infile.close();

    // search films
    {
        Node* node = genresTrees.at("Анимация").search("Аладдин (1992)");
    if (node)
        std::cout << "Film '" << node->film_name << "' has an average rating of " << node->avg_rating << "\n";
    else
        std::cout << "Film Аладдин (1992) not found.\n";
    }
    {
        Node* node = genresTrees.at("Фантастика").search("Назад в будущее 2 (1989)");
    if (node)
        std::cout << "Film '" << node->film_name << "' has an average rating of " << node->avg_rating << "\n";
    else
        std::cout << "Film Аладдин (1992) not found.\n";
    }
    {
        Node* node = genresTrees.at("Анимация").search("Шрек (2001)");
    if (node)
        std::cout << "Film '" << node->film_name << "' has an average rating of " << node->avg_rating << "\n";
    else
        std::cout << "Film Аладдин (1992) not found.\n";
    }
    {
        Node* node = genresTrees.at("Мультфильмы").search("ВАЛЛ·И (2008)");
    if (node)
        std::cout << "Film '" << node->film_name << "' has an average rating of " << node->avg_rating << "\n";
    else
        std::cout << "Film Аладдин (1992) not found.\n";
    }

    double target_rating = 8.5f;
    std::cout << "\nRecommendations for target rating = " << target_rating << ":\n";
    for (int i = 0; i < genresTrees.size(); i++) {
        std::string currentGenre = genresTags[i];
        Node* currentRec = genresTrees.at(currentGenre).recommend(target_rating);
        if (currentRec)
            std::cout << currentGenre << ": " << currentRec->film_name << " (avg rating: " << currentRec->avg_rating << ")\n";
    }
    return 0;
}
