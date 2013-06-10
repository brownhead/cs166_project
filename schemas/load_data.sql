
COPY users ( user_id , password , first_name , last_name , e_mail , street1 , state , country , zipcode , balance)
FROM 'PROJECT_PATH/dataset/users.data' 
WITH DELIMITER ';';
 
COPY super_user ( super_user_id )
FROM 'PROJECT_PATH/dataset/superusers.data' 
WITH DELIMITER ';';

COPY follow (user_id_to , user_id_from , follow_time)
FROM 'PROJECT_PATH/dataset/followers.data' 
WITH DELIMITER ';';

COPY video ( video_id , title , year, online_price, dvd_price)
FROM 'PROJECT_PATH/dataset/video.data' 
WITH DELIMITER ';';

COPY genre ( genre_id , genre_name )
FROM 'PROJECT_PATH/dataset/genre.data' 
WITH DELIMITER ';';

COPY categorize ( video_id , genre_id )
FROM 'PROJECT_PATH/dataset/categorize.data' 
WITH DELIMITER ';';

COPY director ( director_id , first_name , last_name )
FROM 'PROJECT_PATH/dataset/director.data' 
WITH DELIMITER ';';

COPY star ( star_id , first_name , last_name )
FROM 'PROJECT_PATH/dataset/stars.data' 
WITH DELIMITER ';';

COPY author ( author_id , first_name , last_name )
FROM 'PROJECT_PATH/dataset/authors.data' 
WITH DELIMITER ';';

COPY directed ( video_id , director_id)
FROM 'PROJECT_PATH/dataset/directed.data' 
WITH DELIMITER ';';

COPY played ( video_id, star_id)
FROM 'PROJECT_PATH/dataset/played.data' 
WITH DELIMITER ';';

COPY written ( video_id , author_id )
FROM 'PROJECT_PATH/dataset/written.data' 
WITH DELIMITER ';';

