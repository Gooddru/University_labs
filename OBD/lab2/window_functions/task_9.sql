WITH RankedVideos AS (SELECT c.name                                                                           AS channel_name,
                             v.title,
                             COUNT(vl.channel_id)                                                             AS likes_count,
                             DENSE_RANK() OVER (PARTITION BY v.channel_id ORDER BY COUNT(vl.channel_id) DESC) as rank
                      FROM videos v
                               JOIN channels c ON v.channel_id = c.channel_id
                               LEFT JOIN video_likes vl ON v.video_id = vl.video_id
                      GROUP BY v.channel_id, c.name, v.title)
SELECT channel_name, title, likes_count, rank
FROM RankedVideos
WHERE rank <= 3;