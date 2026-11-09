WITH VideoStats AS (SELECT c.name               AS channel_name,
                           v.video_id,
                           v.title,
                           v.channel_id,
                           COUNT(vl.channel_id) AS likes_count
                    FROM videos v
                             JOIN channels c ON v.channel_id = c.channel_id
                             LEFT JOIN video_likes vl ON v.video_id = vl.video_id
                    GROUP BY v.video_id, v.title, v.channel_id, c.name)
SELECT channel_name,
       title,
       likes_count,
       ROUND(AVG(likes_count) OVER (PARTITION BY channel_id), 2)               AS avg_channel_likes,
       ROUND(likes_count - AVG(likes_count) OVER (PARTITION BY channel_id), 2) AS diff_from_avg
FROM VideoStats
ORDER BY channel_name, likes_count DESC;