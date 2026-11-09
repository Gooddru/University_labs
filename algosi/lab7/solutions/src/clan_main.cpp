#include "../include/clan.hpp"
#include <iostream>
#include <ctime>
#include <sstream>
#include <locale>
#include <windows.h>

std::vector<std::string> split_string(const std::string& s)
{
    std::stringstream ss(s);
    std::vector<std::string> tokens;
    std::string token;
    while (ss >> token)
    {
        tokens.push_back(token);
    }
    return tokens;
}

int main()
{
    SetConsoleOutputCP(CP_UTF8);

    std::srand(std::time(0));
    ClanManager clan_manager;

    for (int i = 1; i <= 20; i++)
    {
        clan_manager.create(i);
    }
    clan_manager.unite(1, 2);
    clan_manager.unite(1, 10);
    clan_manager.unite(3, 5);
    clan_manager.unite(4, 6);
    clan_manager.unite(4, 8);
    clan_manager.unite(4, 9);
    clan_manager.unite(9, 15);
    clan_manager.unite(9, 14);
    clan_manager.unite(7, 11);
    clan_manager.unite(7, 12);
    clan_manager.unite(1, 20);
    clan_manager.unite(18, 19);
    clan_manager.unite(16, 17);

    clan_manager.currentClan = 1;
    bool game_running = true;

    std::cout << "Война кланов!\n";
    std::cout << "Вы управляете кланом " << clan_manager.currentClan << ". Захвати все!\n\n";
    std::cout << "Доступные команды:\n"
        << "attack <цель(id)>       - атаковать другой клан\n"
        << "unite <цель(id)>        - объединить с другим кланом\n"
        << "check <id1> <id2>       - проверить отношения между пользователями\n"
        << "disband             - распустить свой клан\n"
        << "switch <id>         - переключиться на другой клан\n"
        << "status              - показать все кланы\n"
        << "current             - показать текущий клан\n"
        << "help                - показать команды\n"
        << "exit                - выйти из игры\n\n";

    while (game_running)
    {
        std::cout << "> ";
        std::string input;
        std::getline(std::cin, input);
        auto tokens = split_string(input);

        if (tokens.empty()) continue;

        try
        {
            if (tokens[0] == "exit")
            {
                game_running = false;
            }
            else if (tokens[0] == "help")
            {
                std::cout << "Доступные команды:\n"
                    << "attack <цель(id)>       - атаковать другой клан\n"
                    << "unite <цель(id)>        - объединить с другим кланом\n"
                    << "check <id1> <id2>       - проверить отношения между пользователями\n"
                    << "disband             - распустить свой клан\n"
                    << "switch <id>         - переключиться на другой клан\n"
                    << "status              - показать все кланы\n"
                    << "current             - показать текущий клан\n"
                    << "help                - показать команды\n"
                    << "exit                - выйти из игры\n\n";
            }
            else if (tokens[0] == "create_user")
            {
                std::cout << "Ошибка: Создание новых кланов отключено. Объединяйте существующие!\n";
            }
            else if (tokens[0] == "attack")
            {
                if (tokens.size() < 2)
                {
                    std::cout << "Ошибка: Требуется указать цель для атаки\n";
                    continue;
                }

                int defender = std::stoi(tokens[1]);
                std::cout << "Клан " << clan_manager.currentClan << " атакует клан " << defender << "!\n";
                clan_manager.attack(clan_manager.currentClan, defender);
                clan_manager.current();
                if (clan_manager.count() == 1)
                {
                    clan_manager.status();
                    std::cout << "  ВАШ КЛАН " << clan_manager.currentClan << " ПОБЕДИЛ!\n";
                    game_running = false;
                }
            }
            else if (tokens[0] == "unite")
            {
                if (tokens.size() < 2)
                {
                    std::cout << "Ошибка: Требуется указать цель для объединения\n";
                    continue;
                }

                int target = std::stoi(tokens[1]);
                std::cout << "Клан " << clan_manager.currentClan << " объединяется с кланом " << target << "!\n";
                clan_manager.unite(clan_manager.currentClan, target);
                clan_manager.current();

                if (clan_manager.count() == 1)
                {
                    clan_manager.status();
                    std::cout << "  ВАШ КЛАН " << clan_manager.currentClan << " ПОБЕДИЛ!\n";
                    game_running = false;
                }
            }
            else if (tokens[0] == "check")
            {
                if (tokens.size() < 3)
                {
                    std::cout << "Ошибка: Требуется два аргумента\n";
                    continue;
                }

                int id1 = std::stoi(tokens[1]);
                int id2 = std::stoi(tokens[2]);

                std::cout << (clan_manager.are_in_same(id1, id2) ? "Союзники" : "Враги") << "\n";
            }
            else if (tokens[0] == "disband")
            {
                std::cout << "Клан " << clan_manager.currentClan << " распускается!\n";
                clan_manager.disband(clan_manager.currentClan);
                std::cout << "Ваш клан " << clan_manager.currentClan << " распался. Игра окончена.\n";
                game_running = false;
            }
            else if (tokens[0] == "switch")
            {
                if (tokens.size() < 2)
                {
                    std::cout << "Ошибка: Требуется указать новый клан\n";
                    continue;
                }

                int new_clan = std::stoi(tokens[1]);
                try
                {
                    clan_manager.find(new_clan);
                    clan_manager.currentClan = new_clan;
                    std::cout << "Теперь вы управляете кланом " << clan_manager.currentClan << "\n";
                    clan_manager.current();
                }
                catch (const std::exception& e)
                {
                    std::cout << "Ошибка: " << e.what() << "\n";
                }
            }
            else if (tokens[0] == "current")
            {
                clan_manager.current();
            }
            else if (tokens[0] == "status")
            {
                clan_manager.status();
                std::cout << "Всего кланов: " << clan_manager.count() << "\n";
                std::cout << "Вы управляете кланом " << clan_manager.currentClan << "\n";
            }
            else
            {
                std::cout << "Неизвестная команда. Введите 'help' для помощи.\n";
            }
        }
        catch (const std::exception& e)
        {
            std::cout << "Ошибка: " << e.what() << "\n";
        }
    }
}
