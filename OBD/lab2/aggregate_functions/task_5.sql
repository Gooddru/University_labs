SELECT
    v.title,
    (SELECT COUNT(*) FROM video_likes WHERE video_id = v.video_id) AS likes_count,
    (SELECT COUNT(*) FROM comments WHERE video_id = v.video_id) AS comments_count
FROM videos v
ORDER BY likes_count DESC, comments_count DESC;