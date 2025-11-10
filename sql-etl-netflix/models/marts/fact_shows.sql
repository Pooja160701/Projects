SELECT
    show_id,
    title,
    release_year,
    rating,
    duration,
    main_genre,
    country
FROM {{ ref('stg_netflix_clean') }}
WHERE type = 'tv show'