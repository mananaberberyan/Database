#5 is here too
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List
from models import Session
from models import Equipment, Material, ProductSpecification
from pydantic import BaseModel
from datetime import date

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the API. Use /docs to access the Swagger documentation."}

DATABASE_URL = "postgresql://manana:man123@localhost/productspecification"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for request payload
class EquipmentCreate(BaseModel):
    equipment_id: int
    equipment_name: str
    start_explotation: date
    term_explotation: date
    manufacturer: str

class MaterialCreate(BaseModel):
    material_id: int
    material_name: str
    type: str
    price: float
    measurement: int
    alternativa: str

class ProductSpecificationCreate(BaseModel):
    id: int
    equipment_id: int
    material_id: int
    name: str
    duration: int


# Read
def get_equipment(db: Session, equipment_id: int):
    return db.query(Equipment).filter(Equipment.equipment_id == equipment_id).first()

def get_material(db: Session, material_id: int):
    return db.query(Material).filter(Material.material_id == material_id).first()

def get_product_specification(db: Session, product_specification_id: int):
    return db.query(ProductSpecification).filter(ProductSpecification.id == product_specification_id).first()
    
# Create equipment
@app.post("/equipment/", response_model=EquipmentCreate)
def create_equipment(equipment: EquipmentCreate, db: Session = Depends(get_db)):
    return create_equipment(db, equipment)


# Read
@app.get("/equipment/{equipment_id}", response_model=EquipmentCreate)
def read_equipment(equipment_id: int, db: Session = Depends(get_db)):
    db_equipment = get_equipment(db, equipment_id)
    if db_equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return db_equipment

# Update
@app.put("/equipment/{equipment_id}", response_model=EquipmentCreate)
def update_equipment(equipment_id: int, updated_equipment: EquipmentCreate, db: Session = Depends(get_db)):
    db_equipment = update_equipment(db, equipment_id, updated_equipment)
    if db_equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return db_equipment

# Delete
@app.delete("/equipment/{equipment_id}", response_model=dict)
def delete_equipment(equipment_id: int, db: Session = Depends(get_db)):
    db_equipment = delete_equipment(db, equipment_id)
    if db_equipment is None:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return {"message": "Equipment deleted successfully"}    

# Create material
@app.post("/material/", response_model=MaterialCreate)
def create_material(material: MaterialCreate, db: Session = Depends(get_db)):
    return create_material(db, material)

# Read
@app.get("/material/{material_id}", response_model=MaterialCreate)
def read_material(material_id: int, db: Session = Depends(get_db)):
    db_material = get_material(db, material_id)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return db_material

# Update
@app.put("/material/{material_id}", response_model=MaterialCreate)
def update_material(material_id: int, updated_material: MaterialCreate, db: Session = Depends(get_db)):
    db_material = update_material(db, material_id, updated_material)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return db_material

# Delete
@app.delete("/material/{material_id}", response_model=dict)
def delete_material(material_id: int, db: Session = Depends(get_db)):
    db_material = delete_material(db, material_id)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return {"message": "Material deleted successfully"}

#Create productspecification
@app.post("/product_specification/", response_model=ProductSpecificationCreate)
def create_product_specification(product_specification: ProductSpecificationCreate, db: Session = Depends(get_db)):
    return create_product_specification(db, product_specification)

#Read
@app.get("/product_specification/{product_specification_id}", response_model=ProductSpecificationCreate)
def read_product_specification(product_specification_id: int, db: Session = Depends(get_db)):
    db_product_specification = get_product_specification(db, product_specification_id)
    if db_product_specification is None:
        raise HTTPException(status_code=404, detail="Product Specification not found")
    return db_product_specification

#Update
@app.put("/product_specification/{product_specification_id}", response_model=ProductSpecificationCreate)
def update_product_specification(product_specification_id: int, updated_product_specification: ProductSpecificationCreate, db: Session = Depends(get_db)):
    db_product_specification = update_product_specification(db, product_specification_id, updated_product_specification)
    if db_product_specification is None:
        raise HTTPException(status_code=404, detail="Product Specification not found")
    return db_product_specification

#Delete
@app.delete("/product_specification/{product_specification_id}", response_model=dict)
def delete_product_specification(product_specification_id: int, db: Session = Depends(get_db)):
    db_product_specification = delete_product_specification(db, product_specification_id)
    if db_product_specification is None:
        raise HTTPException(status_code=404, detail="Product Specification not found")
    return {"message": "Product Specification deleted successfully"}



# 1. SELECT ... WHERE 
@app.get("/equipment/filter/", response_model=List[EquipmentCreate])
def filter_equipment(manufacturer: str, start_explotation: date, db: Session = Depends(get_db)):
    equipment = db.query(Equipment).filter(
        Equipment.manufacturer == manufacturer,
        Equipment.start_explotation >= start_explotation
    ).all()
    return equipment

# 2. JOIN
@app.get("/product_specifications/join/", response_model=List[ProductSpecificationCreate])
def get_product_specifications_join(db: Session = Depends(get_db)):
    product_specifications = db.query(ProductSpecification).options(
        joinedload(ProductSpecification.equipment),
        joinedload(ProductSpecification.material)
    ).all()
    return product_specifications

# 3. UPDATE with a non-trivial condition
@app.put("/equipment/update/", response_model=EquipmentCreate)
def update_equipment_by_condition(threshold_equipment_id: int, updated_equipment: EquipmentCreate, db: Session = Depends(get_db)):
    updated_rows = db.query(Equipment).filter(
        Equipment.equipment_id > threshold_equipment_id
    ).update(updated_equipment.dict(), synchronize_session=False)
    db.commit()
    if updated_rows == 0:
        raise HTTPException(status_code=404, detail="No matching equipment found for update")
    return updated_equipment

# 4. GROUP BY
@app.get("/equipment/count_by_manufacturer/", response_model=List[dict])
def count_equipment_by_manufacturer(db: Session = Depends(get_db)):
    result = db.query(Equipment.manufacturer, func.count(Equipment.equipment_id)).group_by(Equipment.manufacturer).all()
    return [{"manufacturer": manufacturer, "equipment_count": count} for manufacturer, count in result]

# 5. Add sorting of results by one of the fields to the request parameters in the API
@app.get("/equipment/sorted/", response_model=List[EquipmentCreate])
def get_sorted_equipment(sort_by: str = Query("start_explotation", description="Field to sort by"), db: Session = Depends(get_db)):
    equipment = db.query(Equipment).order_by(sort_by).all()
    return equipment
