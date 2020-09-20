from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import dependency_injector.providers as providers
from sqlalchemy.orm import Session

Base = declarative_base()

class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    employees = relationship("Employee", back_populates="company")
    def __init__(self, name):
        self.name = name
    def put(self, sess):
        print("Put")
        SQL(sess).save(self)

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    type = Column(String(50))
    company_id = Column(ForeignKey('company.id'))
    company = relationship("Company", back_populates="employees")

    __mapper_args__ = {
        'polymorphic_identity':'employee',
        'polymorphic_on':type
    }
    def __init__(self, name, type, company_id):
        self.name = name
        self.type = type
        self.company_id = company_id
    def put(self, sess):
        print("Put")
        SQL(sess).save(self)

class Engineer(Employee):
    __tablename__ = 'engineer'
    id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
    engineer_name = Column(String(30))

    __mapper_args__ = {
        'polymorphic_identity':'engineer',
    }
    def __init__(self, name, company_id, engineer_name):
        super().__init__(name, self.__mapper_args__['polymorphic_identity'], 1)
        self.engineer_name = engineer_name

    def put(self, sess):
        print("Put")
        SQL(sess).save(self)

class Manager(Employee):
    __tablename__ = 'manager'
    id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
    manager_name = Column(String(30))

    __mapper_args__ = {
        'polymorphic_identity':'manager',
    }
    def __init__(self, name, company_id, manager_name):
        super().__init__(name, self.__mapper_args__['polymorphic_identity'], company_id)
        self.manager_name = manager_name
    def put(self, sess):
        print("Put")
        SQL(sess).save(self)

class SQL():

    def __init__(self, sess):
        self.sess = sess
    def save(self, _obj):
        print("save")
        self.sess.add(_obj)
        self.sess.commit()
        self.sess.refresh(_obj)
        print("Saved")

if __name__ == "__main__":
    engine = create_engine("mysql+pymysql://root:1234@localhost/sample")
    # try:
    print("Connecting.....")    
    connection = engine.connect()
    Session = sessionmaker(engine)
    session = Session()
    # cpmy_obj = Company("Pramata")
    # res = session.query(Employee).all()
    # print(res[1].engineer_name, res[1].type)
    # print(res[0][0])
    emp_obj = Manager("Bharath", 1, "Bharath")
    emp_obj.put(session)
    print("Connected")