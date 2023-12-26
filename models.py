from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, DECIMAL, text
from sqlalchemy.orm import relationship, declarative_base, Session, sessionmaker

Base = declarative_base()

class Equipment(Base):
    __tablename__ = 'equipment'
    equipment_id = Column(Integer, primary_key=True, autoincrement=True)
    equipment_name = Column(String(50))
    start_explotation = Column(Date)
    term_explotation = Column(Date)
    manufacturer = Column(String(50))

class Material(Base):
    __tablename__ = 'material'
    material_id = Column(Integer, primary_key=True, autoincrement=True)
    material_name = Column(String(50))
    type = Column(String(50))
    price = Column(DECIMAL(10, 2))
    measurement = Column(Integer)
    alternativa = Column(String(50))

class ProductSpecification(Base):
    __tablename__ = 'product_specification'
    id = Column(Integer, primary_key=True, autoincrement=True)
    equipment_id = Column(Integer, ForeignKey('equipment.equipment_id'), primary_key=True)
    material_id = Column(Integer, ForeignKey('material.material_id'), primary_key=True)
    name = Column(String(50))
    duration = Column(Integer)
    equipment = relationship('Equipment', back_populates='specifications')
    material = relationship('Material', back_populates='specifications')

DATABASE_URL = "postgresql://postgres:man123@localhost:5432/productspecification"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

session.commit()