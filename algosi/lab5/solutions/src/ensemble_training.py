import folium
import numpy as np
import pandas as pd
import random

from math import radians, sin, cos, sqrt, atan2, degrees
from itertools import combinations
from typing import Union, List, Dict, Optional
from tabulate import tabulate

# from IPython.display import display

R_EARTH_METERS = 6371000  # радиус земли(увы)
STATION_SEARCH_RADIUS_M = 400  # радиус поиска станций
ERROR_THRESHOLD_METERS = 50  # Герман я тебя люблю

converter_instance = None


def haversine(lat1, lon1, lat2, lon2):
    """считаем расстояние в метрах между двумя точками (lat, lon)"""
    if any(coord is None for coord in [lat1, lon1, lat2, lon2]):
        return float('inf')  # координатов нет ну бан)

    # переводим всё в радианы (люблю профмат)
    r_lat1, r_lon1, r_lat2, r_lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon, dlat = r_lon2 - r_lon1, r_lat2 - r_lat1
    # формула гаверсинуса(описана ниже)
    a = sin(dlat / 2) ** 2 + cos(r_lat1) * cos(r_lat2) * sin(dlon / 2) ** 2
    return R_EARTH_METERS * 2 * atan2(sqrt(a), sqrt(1 - a))


class CoordinateConverter:
    def __init__(self, ref_lat, ref_lon):
        self.ref_lat_rad = radians(ref_lat)
        self.ref_lon_rad = radians(ref_lon)
        self.cos_ref_lat = cos(self.ref_lat_rad)

    def to_cartesian(self, lat, lon):
        x = R_EARTH_METERS * (radians(lon) - self.ref_lon_rad) * self.cos_ref_lat
        y = R_EARTH_METERS * (radians(lat) - self.ref_lat_rad)
        return x, y

    def to_latlon(self, x, y):
        if x is None or y is None: return None, None
        lat_rad = self.ref_lat_rad + y / R_EARTH_METERS
        if abs(self.cos_ref_lat) < 1e-9:
            lon_rad = self.ref_lon_rad
        else:
            lon_rad = self.ref_lon_rad + x / (R_EARTH_METERS * self.cos_ref_lat)
        return degrees(lat_rad), degrees(lon_rad)


def trilaterate_3_stations_cartesian(s1_x, s1_y, d1, s2_x, s2_y, d2, s3_x, s3_y, d3):
    A = 2 * (s2_x - s1_x);
    B = 2 * (s2_y - s1_y)
    C = d1 ** 2 - d2 ** 2 - s1_x ** 2 + s2_x ** 2 - s1_y ** 2 + s2_y ** 2
    D = 2 * (s3_x - s1_x);
    E = 2 * (s3_y - s1_y)
    F = d1 ** 2 - d3 ** 2 - s1_x ** 2 + s3_x ** 2 - s1_y ** 2 + s3_y ** 2
    denom = (A * E - B * D)
    if abs(denom) < 1e-9: return None, None
    return (C * E - F * B) / denom, (A * F - C * D) / denom


def find_nearby_stations(
        lat: float,
        lon: float,
        stations: pd.DataFrame,
        R: float
) -> pd.DataFrame:
    """
    Найти ближайшие станции в радиусе R от точки
    """
    stations['distance_to_user'] = stations.apply(
        lambda row: haversine(lat, lon, row['lat'], row['lon']), axis=1
    )
    nearby = stations[stations['distance_to_user'] <= R].copy()
    return nearby


def compute_distances(
        user_lat: float,
        user_lon: float,
        nearby_stations: pd.DataFrame
) -> Union[np.ndarray, Dict[int, float], pd.DataFrame]:
    """
    Вычислить расстояния от точки до всех ближайших станций
    """
    if 'distance_to_user' in nearby_stations.columns:
        return nearby_stations['distance_to_user'].values
    return nearby_stations.apply(
        lambda row: haversine(user_lat, user_lon, row['lat'], row['lon']), axis=1
    ).values


def triangulate(
        stations: pd.DataFrame,
        distances: Union[np.ndarray, Dict[int, float], pd.DataFrame]
) -> Union[np.ndarray, List[float]]:
    """
    Решить задачу триангуляции по заданным координатам станции и измерениями до точки
    Возвращает предсказанные координаты
    """
    if len(stations) < 3 or len(stations) != len(distances):
        return None  # ну 3, потому что ТРИ(Е)угольник, ю ноу

    s_list_for_triang = []
    for i in range(len(stations)):
        s_list_for_triang.append({
            'x': stations.iloc[i]['x'], 'y': stations.iloc[i]['y'],
            'd': distances[i]
        })

    results_xy = []

    for s1, s2, s3 in combinations(s_list_for_triang, 3):
        pred_x, pred_y = trilaterate_3_stations_cartesian(
            s1['x'], s1['y'], s1['d'], s2['x'], s2['y'], s2['d'], s3['x'], s3['y'], s3['d']
        )
        if pred_x is not None:
            results_xy.append((pred_x, pred_y))

    if not results_xy: return None

    all_x = [res[0] for res in results_xy]
    all_y = [res[1] for res in results_xy]
    return [np.median(all_x), np.median(all_y)]  # возвращаем усредненные координаты


def calculate_metrics(error_meters_list):
    # Посчитаем ошибки в предсказаниях
    valid_errors = [e for e in error_meters_list if e is not None and e != float('inf')]
    mean_err_m = np.mean(valid_errors) if valid_errors else float('nan')
    median_err_m = np.median(valid_errors) if valid_errors else float('nan')

    # По тз нормированные же и по всем (
    norm_metrics = []
    for err in error_meters_list:
        if err is not None and err != float('inf') and err <= ERROR_THRESHOLD_METERS:
            norm_metrics.append(err / ERROR_THRESHOLD_METERS)
        else:
            norm_metrics.append(0.0)

    mean_norm = np.mean(norm_metrics) if norm_metrics else float('nan')
    median_norm = np.median(norm_metrics) if norm_metrics else float('nan')

    return {
        'mean_error_m': mean_err_m, 'median_error_m': median_err_m,
        'mean_norm_metric': mean_norm, 'median_norm_metric': median_norm
    }


def plot_triangulation(
        true_lat: float,
        true_lon: float,
        pred_lat: float,
        pred_lon: float,
        nearby_stations: pd.DataFrame = None,
        distances_plot: np.ndarray = None,
        map_filename="map.html"
) -> Optional[folium.Map]:
    """
    <i>Опционально к реализации.</i>

    Отрисовывает карту с истинным местоположением абонента, Предсказанным и ближайшими станциями
    """
    if true_lat is None or true_lon is None: return None  # Нет реальных, че рисовать то
    m = folium.Map(location=[true_lat, true_lon], zoom_start=14)

    # Зеленый - истинное значение
    folium.Marker([true_lat, true_lon], popup="Истина", icon=folium.Icon(color="green")).add_to(m)
    # Красное - предсказание
    if pred_lat is not None and pred_lon is not None:
        folium.Marker([pred_lat, pred_lon], popup="Предсказание", icon=folium.Icon(color="red")).add_to(m)
        # Ошибки в виде линии (фиолетовые)
        folium.PolyLine([(true_lat, true_lon), (pred_lat, pred_lon)], color="purple").add_to(m)

    # Вышки, шо б было информативно
    if nearby_stations is not None and not nearby_stations.empty:
        for i in range(len(nearby_stations)):
            s = nearby_stations.iloc[i]
            popup_text = f"ID: {s.get('stationid', 'N/A')}"

            if distances_plot is not None and i < len(distances_plot):
                folium.Circle([s['lat'], s['lon']], radius=distances_plot[i],
                              color='blue', fill=True, fill_opacity=0.1).add_to(m)
                popup_text += f"<br>Расстояние: {distances_plot[i]:.1f}м"
            folium.Marker([s['lat'], s['lon']], popup=popup_text,
                          icon=folium.Icon(color="blue", icon="signal", prefix='fa')).add_to(m)

    m.save(map_filename)
    print(f"Карта триангуляции сохранена: {map_filename}")
    # return display(m)
    return m


def plot_all_users(
        predictions_df: pd.DataFrame,
        stations_df: pd.DataFrame,
        map_filename: str = "map_all_users.html"
) -> Optional[folium.Map]:
    """
    Отрисовывает карту со всеми пользователями, их предсказаниями и базовыми станциями
    в том же стиле, что и plot_triangulation.
    """
    if predictions_df.empty or stations_df.empty:
        return None

    avg_lat = predictions_df['true_lat'].mean()
    avg_lon = predictions_df['true_lon'].mean()
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

    for _, station in stations_df.iterrows():
        folium.Marker(
            location=[station['lat'], station['lon']],
            popup=f"Station ID: {station['stationid']}",
            icon=folium.Icon(color="blue", icon="signal", prefix='fa')
        ).add_to(m)

    for _, user in predictions_df.iterrows():
        true_lat = user['true_lat']
        true_lon = user['true_lon']
        pred_lat = user['pred_lat']
        pred_lon = user['pred_lon']
        error = user['error_m']

        folium.Marker(
            [true_lat, true_lon],
            popup=f"User: {user['uuid'][:8]} (True)",
            icon=folium.Icon(color="green")
        ).add_to(m)

        if not pd.isna(pred_lat) and not pd.isna(pred_lon):
            folium.Marker(
                [pred_lat, pred_lon],
                popup=f"User: {user['uuid'][:8]} (Pred) | Ошибка: {error:.1f} м",
                icon=folium.Icon(color="red")
            ).add_to(m)

            folium.PolyLine(
                locations=[[true_lat, true_lon], [pred_lat, pred_lon]],
                color="purple",
                weight=1.5,
                opacity=0.7
            ).add_to(m)

    m.save(map_filename)
    print(f"Карта всех пользователей сохранена: {map_filename}")
    # return display(m)
    return m


def main():
    global converter_instance
    stations_df = pd.read_csv("data/stations.csv")
    users_df = pd.read_csv("data/users_public.csv")

    converter_instance = CoordinateConverter(users_df['lat'].mean(), users_df['lon'].mean())

    stations_df[['x', 'y']] = stations_df.apply(
        lambda r: pd.Series(converter_instance.to_cartesian(r['lat'], r['lon'])), axis=1
    )

    stations_all_prepared = stations_df.drop_duplicates(subset=['x', 'y']).copy()

    all_errors = []
    predictions_log = []

    for idx, user in users_df.iterrows():
        user_lat, user_lon = user['lat'], user['lon']

        nearby_s_with_dist = find_nearby_stations(user_lat, user_lon, stations_all_prepared, STATION_SEARCH_RADIUS_M)

        pred_lat_final, pred_lon_final = None, None
        error_val = float('inf')

        nearby_s_indexed = nearby_s_with_dist.reset_index(drop=True)
        distances_arr_for_this_user = None

        if len(nearby_s_indexed) >= 3:
            distances_arr_for_this_user = compute_distances(user_lat, user_lon, nearby_s_indexed)

            pred_xy_cart = triangulate(nearby_s_indexed[['stationid', 'x', 'y']], distances_arr_for_this_user)

            if pred_xy_cart:
                pred_lat_final, pred_lon_final = converter_instance.to_latlon(pred_xy_cart[0], pred_xy_cart[1])
                if pred_lat_final is not None:
                    error_val = haversine(user_lat, user_lon, pred_lat_final, pred_lon_final)

        all_errors.append(error_val)
        predictions_log.append({
            'uuid': user['uuid'], 'true_lat': user_lat, 'true_lon': user_lon,
            'pred_lat': pred_lat_final, 'pred_lon': pred_lon_final,
            'error_m': error_val if error_val != float('inf') else None,
            'nearby_count': len(nearby_s_with_dist)
        })

    valid_users = [u for u in predictions_log if u['pred_lat'] is not None]
    if valid_users:

        random_users = random.sample(valid_users, min(2, len(valid_users)))

        for user in random_users:
            nearby_s = find_nearby_stations(
                user['true_lat'],
                user['true_lon'],
                stations_all_prepared,
                STATION_SEARCH_RADIUS_M
            )
            distances = compute_distances(user['true_lat'], user['true_lon'], nearby_s)

            plot_triangulation(
                user['true_lat'], user['true_lon'],
                user['pred_lat'], user['pred_lon'],
                nearby_s[['lat', 'lon', 'stationid']],
                distances,
                map_filename=f"map_user_{user['uuid'][:8]}.html"
            )

    predictions_df = pd.DataFrame(predictions_log)
    print("\nРезультаты предсказаний:")
    print(tabulate(
        predictions_df[['uuid', 'true_lat', 'true_lon', 'pred_lat', 'pred_lon', 'error_m', 'nearby_count']],
        headers=['Айди', 'Реальная широта', 'Реальная долгота', 'Предсказанная широта', 'Предсказанная долгота',
                 'Ошибка (м)', 'Станций рядом'],
        tablefmt='fancy_grid',
        floatfmt=".1f",
        showindex=False,
        missingval="N/A"
    ))

    metrics = calculate_metrics(all_errors)
    if not np.isnan(metrics['mean_error_m']):
        print(f"Средняя ошибка (для успешных): {metrics['mean_error_m']} метров")
        print(f"Медианная ошибка (для успешных): {metrics['median_error_m']} метров")
    if not np.isnan(metrics['mean_norm_metric']):
        print(f"Средняя нормированная метрика: {metrics['mean_norm_metric']} метров")
        print(f"Медианная нормированная метрика: {metrics['median_norm_metric']} метров")

    plot_all_users(
        predictions_df,
        stations_all_prepared,
        map_filename="map_all_users.html"
    )


if __name__ == '__main__':
    main()
