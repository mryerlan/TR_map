from sqlalchemy import create_engine, Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import URL_DB

Base = declarative_base()

engine = create_engine(URL_DB, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class TransmissionTypes(Base):
    __tablename__ = 'tr_types'

    id = Column(Integer, primary_key=True)
    site = Column('SITE ID', String)
    tr_type_lm = Column('TR TYPE LM', String)
    tr_type = Column('TR TYPE', String)

    def __init__(self, site: str, tr_type_lm: str, tr_type: str):
        super().__init__()
        self.site = site
        self.tr_type_lm = tr_type_lm
        self.tr_type = tr_type

    def __repr__(self) -> str:
        info: str = f'{self.site} {self.tr_type_lm} {self.tr_type}'
        return info


class QuantitySites(Base):
    __tablename__ = 'quantity_sites'

    id = Column(Integer, primary_key=True)
    site = Column('SITE ID', String)
    quantity = Column('QUANTITY', Integer)
    quantity_list = Column('QUANTITY LIST', Text)

    def __init__(self, site: str, quantity: int, quantity_list: tuple):
        super().__init__()
        self.site = site
        self.quantity = quantity
        self.quantity_list = quantity_list

    def __repr__(self) -> str:
        return f'{self.site} {self.quantity} {self.quantity_list}'


class TrMap(Base):
    __tablename__ = 'tr map'

    id = Column(Integer, primary_key=True)
    site = Column('SITE ID', String)
    chain = Column('CHAIN', Integer)
    fe = Column('FE', Text)
    uplink = Column('UPLINK', Text)

    def __init__(self, site: str, chain: int, fe: str, uplink: str):
        super().__init__()
        self.site = site
        self.chain = chain
        self.fe = fe
        self.uplink = uplink

    def __repr__(self) -> str:
        return f'{self.site} {self.chain} {self.fe}{self.uplink}'
