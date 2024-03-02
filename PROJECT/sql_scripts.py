INIT_DB = '''
    CREATE TABLE IF NOT EXISTS employee(
        employee_id TEXT not null PRIMARY KEY UNIQUE, 
        employee_name text NOT NULL, 
        employee_vacan text NOT NULL, 
        employee_phone text NOT NULL, 
        employee_mail text UNIQUE NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS visit(
        employee_id TEXT NOT NULL, 
        visit_day DATE, 
        visit_time TIME,
        status text, 
        FOREIGN KEY(employee_id) REFERENCES employee(employee_id)
    );
    
    CREATE TABLE IF NOT EXISTS temp(
        visitor_id TEXT PRIMARY KEY NOT NULL,
        name_visitor text, 
        goal text,
        phone text, 
        email text,
        temp_date DATE
    );
    
    CREATE TABLE IF NOT EXISTS visit_temp(
        visitor_id TEXT NOT NULL, 
        visit_time TIME, 
        status text, 
        FOREIGN KEY(visitor_id) REFERENCES temp(visitor_id)
    );
'''

INSERT_EMPLOYEE = '''
    INSERT INTO employee(
        employee_id,
        employee_name, 
        employee_vacan, 
        employee_phone, 
        employee_mail
        ) 
    VALUES (?,?,?,?,?)
'''

INSERT_VISITOR = '''
INSERT INTO temp(
    visitor_id,
    name_visitor,
    goal,
    phone,
    email,
    temp_date
) VALUES (?,?,?,?,?,?)
'''

COUNT_EMPLOYEES = '''
SELECT count(employee_id) FROM visit WHERE employee_id = ? AND visit_day = ?;
'''

COUNT_VISITORS = '''
SELECT count(visit_temp.visitor_id) 
FROM visit_temp JOIN temp on visit_temp.visitor_id = temp.visitor_id 
where temp_date = ? and visit_temp.visitor_id=?;
'''

INSERT_VISIT = '''INSERT INTO visit(employee_id, visit_day, visit_time, status) VALUES (?,?,?,?)'''

INSERT_TEMP = '''INSERT INTO visit_temp(visitor_id, visit_time, status) VALUES (?,?,?)'''

CHECK_EMPL = '''SELECT * FROM employee where employee_id = ?'''

CHECK_TEMP = '''SELECT * FROM temp where visitor_id = ?'''

EMPLOYEE_CUR_DATE = '''
    SELECT employee_name, employee_vacan, employee_phone, visit_time, status 
    FROM visit join employee on visit.employee_id=employee.employee_id where visit_day = ?;
'''

VISITOR_CUR_DATE = '''
    SELECT name_visitor, goal, phone, visit_time, status 
    FROM visit_temp join temp on visit_temp.visitor_id = temp.visitor_id where temp_date = ?;
'''

EMPLOYEE_LIST = '''SELECT employee_name, employee_vacan, employee_phone FROM employee;'''
