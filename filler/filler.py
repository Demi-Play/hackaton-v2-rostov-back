import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import func
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

# Функция для создания случайной даты в диапазоне
def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())))

# Заполнение таблиц данными
def populate_database():
    # Добавление точек продаж
    sales_points_data = [
        {"name": "Store A", "coordinates": "40.7128° N, 74.0060° W"},
        {"name": "Store B", "coordinates": "34.0522° N, 118.2437° W"},
        {"name": "Store C", "coordinates": "51.5074° N, 0.1278° W"},
        {"name": "Store D", "coordinates": "35.6895° N, 139.6917° E"},
        {"name": "Store E", "coordinates": "37.7749° N, 122.4194° W"},
        {"name": "Store F", "coordinates": "52.3667° N, 4.8945° E"},
        {"name": "Store G", "coordinates": "40.4168° N, 3.7038° W"},
        {"name": "Store H", "coordinates": "55.7558° N, 37.6176° E"},
        {"name": "Store I", "coordinates": "52.5200° N, 13.4050° E"},
        {"name": "Store J", "coordinates": "41.9028° N, 12.4964° E"},
    ]

    for data in sales_points_data:
        sales_point = SalesPoint(**data)
        session.add(sales_point)

    # Добавление продуктов
    products_data = [
        {"name": "Product A", "expiry_date": datetime.now() + timedelta(days=30), "volume": 100, "weight": 50},
        {"name": "Product B", "expiry_date": datetime.now() + timedelta(days=60), "volume": 150, "weight": 75},
        {"name": "Product C", "expiry_date": datetime.now() + timedelta(days=90), "volume": 200, "weight": 100},
        {"name": "Product D", "expiry_date": datetime.now() + timedelta(days=120), "volume": 250, "weight": 125},
        {"name": "Product E", "expiry_date": datetime.now() + timedelta(days=150), "volume": 300, "weight": 150},
        {"name": "Product F", "expiry_date": datetime.now() + timedelta(days=180), "volume": 350, "weight": 175},
        {"name": "Product G", "expiry_date": datetime.now() + timedelta(days=210), "volume": 400, "weight": 200},
        {"name": "Product H", "expiry_date": datetime.now() + timedelta(days=240), "volume": 450, "weight": 225},
        {"name": "Product I", "expiry_date": datetime.now() + timedelta(days=270), "volume": 500, "weight": 250},
        {"name": "Product J", "expiry_date": datetime.now() + timedelta(days=300), "volume": 550, "weight": 275},
    ]

    for data in products_data:
        product = Product(**data)
        session.add(product)

    # Добавление маршрутов доставки
    delivery_routes_data = [
        {"origin_id": 1, "destination_id": 2, "estimated_time": 2.5, "distance": 150},
        {"origin_id": 2, "destination_id": 3, "estimated_time": 3.0, "distance": 200},
        {"origin_id": 3, "destination_id": 4, "estimated_time": 2.0, "distance": 120},
        {"origin_id": 4, "destination_id": 5, "estimated_time": 1.5, "distance": 100},
        {"origin_id": 5, "destination_id": 6, "estimated_time": 2.0, "distance": 130},
        {"origin_id": 6, "destination_id": 7, "estimated_time": 2.5, "distance": 160},
        {"origin_id": 7, "destination_id": 8, "estimated_time": 3.0, "distance": 180},
        {"origin_id": 8, "destination_id": 9, "estimated_time": 2.0, "distance": 110},
        {"origin_id": 9, "destination_id": 10, "estimated_time": 1.5, "distance": 90},
        {"origin_id": 10, "destination_id": 1, "estimated_time": 2.0, "distance": 140},
    ]

    for data in delivery_routes_data:
        delivery_route = DeliveryRoute(**data)
        session.add(delivery_route)

    # Добавление продаж
    sales_data = []
    for _ in range(10):
        product_id = random.randint(1, 10)
        sales_point_id = random.randint(1, 10)
        sale_date = random_date(datetime(2023, 1, 1), datetime(2023, 12, 31))
        quantity_sold = random.randint(10, 50)
        sales_data.append({
            "product_id": product_id,
            "sales_point_id": sales_point_id,
            "sale_date": sale_date,
            "quantity_sold": quantity_sold
        })

    for data in sales_data:
        sale = Sale(**data)
        session.add(sale)

    session.commit()


# 1. Расчет оптимальных уровней запасов:
def calculate_optimal_stock_levels(product_id, sales_point_id):
    # Получить прогноз спроса для продукта и точки продажи
    forecast = session.query(SalesForecast).filter_by(product_id=product_id, sales_point_id=sales_point_id).first()
    if not forecast:
        return "Прогноз для данного продукта и точки продажи не найден."

    # Получить текущие остатки продукта в инвентаре
    inventory = session.query(Inventory).filter_by(product_id=product_id).first()
    if not inventory:
        return "Инвентарь для данного продукта не найден."

    # Рассчитать оптимальный уровень запасов
    optimal_stock_level = forecast.forecasted_demand * forecast.avg_order_period + forecast.forecasted_demand * forecast.avg_order_period

    # Обновить информацию об оптимальных уровнях запасов в инвентаре
    inventory.optimal_stock_level = optimal_stock_level
    session.commit()

    return "Оптимальные уровни запасов успешно рассчитаны и обновлены."

# 2. Проверка и управление сроками годности:
def check_expiry_dates():
    # Получить все продукты с просроченными сроками годности
    expired_products = session.query(Inventory).filter(Inventory.expiry_date <= func.now()).all()

    # Обновить информацию в инвентаре о просроченных продуктах
    for product in expired_products:
        product.quantity = 0  # Установить количество просроченного продукта в 0
    session.commit()

    return "Информация о просроченных продуктах успешно обновлена."

# 3. Обновление запасов на основе продаж:
def update_inventory_from_sales():
    # Получить все продажи
    sales = session.query(Sale).all()

    # Обновить количество продуктов в инвентаре на основе продаж
    for sale in sales:
        product_id = sale.product_id
        sales_point_id = sale.sales_point_id
        quantity_sold = sale.quantity_sold

        # Найти соответствующий продукт в инвентаре
        inventory = session.query(Inventory).filter_by(product_id=product_id).first()

        # Уменьшить количество продукта в инвентаре на количество проданных
        if inventory and inventory.quantity >= quantity_sold:
            inventory.quantity -= quantity_sold

    session.commit()

    return "Инвентарь успешно обновлен на основе продаж."





populate_database()