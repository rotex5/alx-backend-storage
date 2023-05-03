-- script that lists all bands with Glam rock as
-- their main style, ranked by their longevity
-- Column names must be: band_name and lifespan (in years)
-- You should use attributes formed and split for computing the lifespan

SELECT origin AS origin, SUM(fans) AS nb_fans FROM metal_bands
GROUP BY origin ORDER BY nb_fans DESC;
