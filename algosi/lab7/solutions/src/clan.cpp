#include "../include/clan.hpp"
#include <iostream>
#include <algorithm>
#include <stdexcept>
#include <cstdlib>

void ClanManager::create(int user_id)
{
    if (parent.count(user_id))
    {
        throw std::runtime_error("Ошибка: Пользователь " + std::to_string(user_id) + " уже существует");
    }
    parent[user_id] = user_id;
    clans[user_id] = {user_id};
    rank[user_id] = 1;
}

int ClanManager::find(int user_id)
{
    if (!parent.count(user_id))
    {
        throw std::runtime_error("Ошибка: Пользователь " + std::to_string(user_id) + " не найден");
    }
    int root = user_id;
    while (parent[root] != root)
    {
        root = parent[root];
    }
    while (user_id != root)
    {
        int next = parent[user_id];
        parent[user_id] = root;
        user_id = next;
    }
    return root;
}

void ClanManager::unite(int user1, int user2)
{
    int root1 = find(user1);
    int root2 = find(user2);
    if (root1 == root2) return;

    if (rank[root1] < rank[root2])
    {
        std::swap(root1, root2);
    }

    parent[root2] = root1;
    clans[root1].insert(clans[root1].end(), clans[root2].begin(), clans[root2].end());
    clans.erase(root2);

    if (rank[root1] == rank[root2])
    {
        rank[root1]++;
    }
}

bool ClanManager::are_in_same(int user1, int user2)
{
    return find(user1) == find(user2);
}

void ClanManager::disband(int user)
{
    int root = find(user);
    if (!clans.count(root))
        return;

    auto members = clans[root];
    for (int member : members)
    {
        parent[member] = member;
        clans[member] = {member};
        rank[member] = 1;
    }
    clans.erase(root);
}

void ClanManager::attack(int attacker_user, int defender_user)
{
    int root_att = find(attacker_user);
    int root_def = find(defender_user);
    if (root_att == root_def)
    {
        throw std::runtime_error("Нельзя атаковать свой клан");
    }

    size_t size_attackers = clans[root_att].size();
    size_t size_defenders = clans[root_def].size();
    double win_chance = static_cast<double>(size_attackers) / (size_attackers + size_defenders);
    double roll = static_cast<double>(std::rand()) / RAND_MAX;

    if (roll < win_chance)
    {
        parent[root_def] = root_att;
        clans[root_att].insert(clans[root_att].end(), clans[root_def].begin(), clans[root_def].end());
        clans.erase(root_def);
        std::cout << "Клан " << root_def << " присоединился к вашему клану!\n";
    }
    else
    {
        disband(root_att);
        std::cout << "Атака провалилась! Ваш клан был уничтожен.\n";
    }
}

void ClanManager::status() const
{
    std::cout << "\nТекущее состояние кланов:\n";
    for (const auto& clan_pair : clans)
    {
        std::cout << "Клан " << clan_pair.first << ": [";
        const auto& members = clan_pair.second;
        for (size_t i = 0; i < members.size(); ++i)
        {
            std::cout << members[i];
            if (i != members.size() - 1) std::cout << ", ";
        }
        std::cout << "]\n";
    }
}


void ClanManager::current() const
{
    if (currentClan == 0)
    {
        std::cout << "Нет текущего клана.\n";
        return;
    }

    auto it = clans.find(currentClan);
    if (it == clans.end())
    {
        std::cout << "Клан " << currentClan << " не найден.\n";
        return;
    }

    std::cout << "Клан: " << currentClan << "\n";
    std::cout << "Состав клана: [";

    const auto& members = it->second;
    for (size_t i = 0; i < members.size(); ++i)
    {
        std::cout << members[i];
        if (i != members.size() - 1)
            std::cout << ", ";
    }
    std::cout << "]\n";

}

int ClanManager::count() const
{
    return static_cast<int>(clans.size());
}
