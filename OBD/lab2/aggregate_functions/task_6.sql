SELECT c.name, COUNT(v.video_id) AS videos_count
FROM channels c
         JOIN videos v ON c.channel_id = v.channel_id
GROUP BY c.channel_id, c.name
HAVING COUNT(v.video_id) > 3
ORDER BY videos_count DESC;