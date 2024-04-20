from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

    # Создание файла базы данных SQLite и установление соединения
engine = create_engine('sqlite:///soliuz.db')


class SalesPoint(Base):
    __tablename__ = 'sales_points'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    coordinates = Column(String)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    expiry_date = Column(DateTime)
    volume = Column(Float)
    weight = Column(Float)

class DeliveryRoute(Base):
    __tablename__ = 'delivery_routes'
    id = Column(Integer, primary_key=True)
    origin_id = Column(Integer)
    destination_id = Column(Integer)
    estimated_time = Column(Float)
    distance = Column(Float)

class DeliverySchedule(Base):
    __tablename__ = 'delivery_schedules'
    id = Column(Integer, primary_key=True)
    route_id = Column(Integer)
    delivery_datetime = Column(DateTime)

class Inventory(Base):
    __tablename__ = 'inventory'
    product_id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    expiry_date = Column(DateTime)

class Sale(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    sales_point_id = Column(Integer)
    sale_date = Column(DateTime)
    quantity_sold = Column(Integer)

class SalesForecast(Base):
    __tablename__ = 'sales_forecasts'
    sales_point_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, primary_key=True)
    forecasted_demand = Column(Integer)
    avg_order_period = Column(Integer)

class SalesHistory(Base):
    __tablename__ = 'sales_history'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer)
    sale_date = Column(DateTime)
    quantity_sold = Column(Integer)

class SeasonalFactors(Base):
    __tablename__ = 'seasonal_factors'
    id = Column(Integer, primary_key=True)
    month = Column(Integer)
    seasonality_coefficient = Column(Float)

class MarketTrends(Base):
    __tablename__ = 'market_trends'
    id = Column(Integer, primary_key=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    trend_coefficient = Column(Float)


Base.metadata.create_all(engine)


# Создание сессии для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
session = Session()