select title, rating from movies join ratings where year = 2010 and movie_id = id order by rating desc, title asc;