from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
import datetime
import pandas


Base = declarative_base()
username = 'root'
password = 'CFBF5117CBF5A6802F7E2A'
host = '127.0.0.1'
database = '1010gps'
port = '3321'
engine = create_engine('mysql+pymysql://' + username + ':' + password + '@' + \
                       host + ':' + port + '/' + database)

class Counter(Base):
    __tablename__ = 'dev_alarm'

    guid = Column('Guid', String, primary_key = True)
    vehicle = Column('DevIDNo', String)
    alarm_time = Column('ArmTime', DateTime)
    alarm_type = Column('ArmType', Integer)
    alarm_info = Column('ArmInfo', Integer)
    alarm_desc = Column('ArmDesc', String)
    latitude = Column('WeiDu', Integer)
    longitude = Column('JingDu', Integer)


    def __repr__(self):
        return f'<Counter(bus: {self.vehicle}, alarm_time: {self.alarm_time}>)'


def main():
    # Passenger counter is ArmType == 232
    # if ArmInfo == 15, second value of ArmDesc is passenger in
    # passenger out is third value, and 4th value is total people
    Session = sessionmaker(bind=engine)
    session = Session()
    dt = datetime.datetime.now() - datetime.timedelta(hours=5)

    counter = session.query(Counter).filter(and_(Counter.alarm_time > dt, \
                                                    Counter.alarm_type == 232)) \
                                                    .all()

    for i in range(len(counter)):
        
        print(f'{counter[i].alarm_info}, {counter[i].alarm_desc}')

if __name__ == '__main__':
    main()



    
    
