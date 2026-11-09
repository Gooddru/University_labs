SELECT c.name AS channel_name,
       v.title,
       v.upload_date,
       COUNT(v.video_id) OVER (
           PARTITION BY v.channel_id
           ORDER BY v.upload_date
           )  AS total
FROM videos v
         JOIN channels c ON v.channel_id = c.channel_id
ORDER BY c.name, v.upload_date;