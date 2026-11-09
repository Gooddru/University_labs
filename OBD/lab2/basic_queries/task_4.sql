SELECT
    s.subscriber_channel_id AS subscriber_id,
    subscriber.name AS subscriber_name,
    target.name AS subscribed_to
FROM subscriptions s
JOIN channels target ON s.target_channel_id = target.channel_id
JOIN channels subscriber ON s.subscriber_channel_id = subscriber.channel_id
WHERE s.subscriber_channel_id = 5;