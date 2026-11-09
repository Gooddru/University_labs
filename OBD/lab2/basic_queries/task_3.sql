SELECT c.name, COUNT(v.video_id) AS videos_count
FROM channels c
         LEFT JOIN videos v ON c.channel_id = v.channel_id
GROUP BY c.channel_id, c.name
ORDER BY videos_count DESC;