select name from people join movies, stars where year = 2004 and movies.id = stars.movie_id and stars.person_id = people.id order by birth;