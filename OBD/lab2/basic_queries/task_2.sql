SELECT v.title, v.upload_date, c.name AS channel_name
FROM videos v
         JOIN channels c ON v.channel_id = c.channel_id
ORDER BY v.upload_date DESC
LIMIT 10;