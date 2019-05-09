import json
import uuid
import datetime

from sqlalchemy import create_engine
from conf.settings import db_settings as dbs
from models import Employee

database_url = "{0}://{1}:{2}@{3}:{4}/{5}".format(dbs['db_driver'],
                                                  dbs['user'],
                                                  dbs['password'],
                                                  dbs['host'],
                                                  dbs['port'],
                                                  dbs['database'])

engine = create_engine(database_url)


def create_employee_table():
    try:
        if not engine.dialect.has_table(engine,
                                        Employee.__tablename__):
            employee_obj = Employee()
            employee_obj.metadata.create_all(engine)

    except Exception as err:
        print err.message


def save_employee_data(data):
    try:
        conn = engine.connect()
        current_time = str(datetime.datetime.now())
        data = json.loads(data)
        checkin_id = str(uuid.uuid4())
        sql_string = "insert into {0} values('{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(Employee.__tablename__,
                                                                                               checkin_id,
                                                                                               data['name'],
                                                                                               data['designation'],
                                                                                               data['in_out'],
                                                                                               data['department'],
                                                                                               current_time)
        conn.execute(sql_string)
        return {"checkin_id": checkin_id,
                "name": data['name'],
                "designation": data['designation'],
                "in_out": data['in_out'],
                "department": data['department'],
                "checkin_time": current_time}
    except Exception as err:
        print err.message
