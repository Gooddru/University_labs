from tqdm import tqdm

from src.lab5.research.age import age_predict
from src.lab5.research.network import *
from src.lab5.vkapi.friends import get_friends, get_mutual

print(get_friends(352105074))  # Тест друзей
print(get_mutual(source_uid=352105074, target_uids=[188997719]))  # Тест общих друзей
predicted_age = age_predict(352105074)  # Тест возраста
print(f"Прогнозируемый возраст пользователя : {predicted_age}")
print(ego_network(user_id=352105074))  # Получение связей
friends_response = get_friends(user_id=352105074, fields=["nickname"])  # Запрос к друзьям
active_users = [user["id"] for user in friends_response.items if
                not user.get("deactivated")]  # Активные (не удаленные пользователи)
print(len(active_users))
mutual_friends = get_mutual(source_uid=352105074, target_uids=active_users,
                            progress=tqdm)  # Общие друщья с пользователем
print(mutual_friends)

net = ego_network(user_id=352105074)
plot_ego_network(net)
plot_communities(net)

communities = get_communities(net)
df = describe_communities(communities, friends_response.items, fields=["first_name", "last_name"])
print(df.to_string())
