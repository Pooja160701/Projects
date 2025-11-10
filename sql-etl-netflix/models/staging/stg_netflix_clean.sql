SELECT
    show_id,
    INITCAP(TRIM(title)) AS title,
    LOWER(TRIM(type)) AS type,
    COALESCE(LOWER(TRIM(country)), 'unknown') AS country,
    CAST(release_year AS INTEGER) AS release_year,
    COALESCE(LOWER(TRIM(director)), 'not specified') AS director,
    SPLIT_PART(listed_in, ',', 1) AS main_genre,
    COALESCE(LOWER(TRIM(rating)), 'not rated') AS rating,
    COALESCE(LOWER(TRIM(duration)), 'unknown') AS duration,
    date_added
FROM {{ ref('netflix_titles') }}
WHERE title IS NOT NULL