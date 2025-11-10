SELECT
    country,
    COUNT(show_id) AS total_titles,
    COUNT(CASE WHEN type = 'movie' THEN 1 END) AS total_movies,
    COUNT(CASE WHEN type = 'tv show' THEN 1 END) AS total_shows
FROM {{ ref('stg_netflix_clean') }}
GROUP BY country
ORDER BY total_titles DESC