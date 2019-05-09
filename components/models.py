from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()


class Employee(Base):
    __tablename__ = "employee"

    id = Column(String(256), primary_key=True)
    name = Column(String(40))
    designation = Column(String(60))
    in_out = Column(String(10))
    department = Column(String(60))
    checkin_timestamp = Column(DateTime)

    def __repr__(self):
        return "employee : {} - {}".format(self.id,
                                           self.name)
