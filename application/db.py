from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Создание файла базы данных SQLite и установление соединения
engine = create_engine('sqlite:///soliuz.db')

class SalesPoint(Base):
    __tablename__ = 'sales_points'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    coordinates = Column(String)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    expiry_date = Column(DateTime)
    volume = Column(Float)
    weight = Column(Float)

class DeliveryRoute(Base):
    __tablename__ = 'delivery_routes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    origin_id = Column(Integer, ForeignKey('sales_points.id'))
    destination_id = Column(Integer, ForeignKey('sales_points.id'))
    estimated_time = Column(Float)
    distance = Column(Float)
    
    origin = relationship("SalesPoint", foreign_keys=[origin_id])
    destination = relationship("SalesPoint", foreign_keys=[destination_id])

class DeliverySchedule(Base):
    __tablename__ = 'delivery_schedules'
    id = Column(Integer, primary_key=True, autoincrement=True)
    route_id = Column(Integer, ForeignKey('delivery_routes.id'))
    delivery_datetime = Column(DateTime)
    
    route = relationship("DeliveryRoute")

class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    expiry_date = Column(DateTime)
    optimal_stock_levels = Column(String)
    
    product = relationship("Product")

class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    sales_point_id = Column(Integer, ForeignKey('sales_points.id'))
    sale_date = Column(DateTime)
    quantity_sold = Column(Integer)
    
    product = relationship("Product")
    sales_point = relationship("SalesPoint")

class SalesHistory(Base):
    __tablename__ = 'sales_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    sale_date = Column(DateTime)
    quantity_sold = Column(Integer)
    
    product = relationship("Product")


# Связь many-to-many таблиц
class SalesForecast(Base):
    __tablename__ = 'sales_forecasts'
    id = Column(Integer, primary_key=True)
    sales_point_id = Column(Integer, ForeignKey('sales_points.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    forecasted_demand = Column(Integer)
    avg_order_period = Column(Integer)
    
    product = relationship("Product")
    sales_point = relationship("SalesPoint")

class SeasonalFactors(Base):
    __tablename__ = 'seasonal_factors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    month = Column(Integer)
    seasonality_coefficient = Column(Float)

class MarketTrends(Base):
    __tablename__ = 'market_trends'
    id = Column(Integer, primary_key=True, autoincrement=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    trend_coefficient = Column(Float)

Base.metadata.create_all(engine)

# Создание сессии для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
session = Session()