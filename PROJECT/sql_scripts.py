INIT_DB = '''
    CREATE TABLE IF NOT EXISTS user_type(
        type_id INTEGER PRIMARY KEY AUTOINCREMENT,
        type_name text
    );
    
    CREATE TABLE IF NOT EXISTS user(
        user_id TEXT not null PRIMARY KEY UNIQUE, 
        user_name text NOT NULL, 
        user_type_id int NOT NULL, 
        user_phone text NOT NULL, 
        user_mail text UNIQUE NOT NULL,
        user_is_active BOOLEAN NOT NULL DEFAULT TRUE,
        FOREIGN KEY(user_type_id) REFERENCES user_type(type_id)
    );

    CREATE TABLE IF NOT EXISTS visit(
        user_id TEXT NOT NULL, 
        visit_day DATE, 
        visit_time TIME,
        status boolean, 
        FOREIGN KEY(user_id) REFERENCES user(user_id)
    );
'''

INSERT_USER = '''
    INSERT INTO user(
        user_id, 
        user_name, 
        user_type_id, 
        user_phone, 
        user_mail
        ) 
    VALUES (?,?,?,?,?)
'''

INSERT_VISIT = '''INSERT INTO visit(user_id, visit_day, visit_time, status) VALUES (?,?,?,?)'''

GET_STATUS = '''
    SELECT v.status FROM 
    visit v join user u on v.user_id = u.user_id
    where v.user_id = ? and v.visit_day = ?
    ORDER BY visit_day, visit_time DESC 
    LIMIT 1
 '''

CHECK_TEMP = '''SELECT * FROM user where user_id = ? and user_type_id = 2'''

USER_TYPE = '''
    SELECT DISTINCT u.user_id, u.user_name, u.user_phone, u.user_mail, LAST_VALUE (v.status) OVER (
        PARTITION BY v.user_id
        ORDER BY v.user_id DESC 
        RANGE BETWEEN UNBOUNDED PRECEDING AND 
        UNBOUNDED FOLLOWING
    )
    FROM user u inner join visit v on u.user_id = v.user_id 
    where user_type_id = ?;
'''
