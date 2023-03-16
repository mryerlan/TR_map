from sqlalchemy import create_engine, Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

engine = create_engine('mssql+pymssql://sa:Gdheuec37{52T3@10.250.14.42/TR_MAP', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class TrMap(Base):
    __tablename__ = 'tr map'

    id = Column(Integer, primary_key=True)
    site = Column('SITE ID', String)
    chain = Column('CHAIN', Integer)
    fe = Column('FE', Text)

    def __init__(self, site: str, chain: int, fe: list):
        super().__init__()
        self.site = site
        self.chain = chain
        self.fe = fe

    def __repr__(self) -> str:
        return f'{self.site} {self.chain} {self.fe}'


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    temp = TrMap(site='AL7777', chain=3, fe=str(['AL7777', 'AL5555', 'AL4444']))
    session.add(temp)
    session.commit()
    session.close()
