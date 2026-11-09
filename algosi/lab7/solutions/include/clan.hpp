#ifndef CLAN_H
#define CLAN_H

#include <unordered_map>
#include <vector>

class ClanManager
{
    std::unordered_map<int, int> parent;
    std::unordered_map<int, std::vector<int>> clans;
    std::unordered_map<int, int> rank;


public:
    int currentClan = 0;
    // Функции для юзера
    void create(int user_id);
    int find(int user_id);

    // Функции для кланов
    void unite(int user1, int user2);
    bool are_in_same(int user1, int user2);
    void disband(int user);
    void attack(int attacker_user, int defender_user);

    // Вспомогательные для кланов
    void status() const;
    void current() const;
    int count() const;
};
#endif // CLAN_H