import random
from db import Inventory, Sale, SalesPoint, Product, DeliveryRoute, DeliverySchedule, SalesForecast, SalesHistory, SeasonalFactors, MarketTrends
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

# Создание файла базы данных SQLite и установление соединения
engine = create_engine('sqlite:///soliuz.db')

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
    ]

    for data in products_data:
        product = Product(**data)
        session.add(product)

    # Добавление маршрутов доставки
    delivery_routes_data = [
        {"origin_id": 1, "destination_id": 2, "estimated_time": 2.5, "distance": 10},
        {"origin_id": 2, "destination_id": 3, "estimated_time": 3.5, "distance": 15},
        {"origin_id": 3, "destination_id": 4, "estimated_time": 4.5, "distance": 20},
        {"origin_id": 4, "destination_id": 5, "estimated_time": 5.5, "distance": 25},
        {"origin_id": 5, "destination_id": 1, "estimated_time": 6.5, "distance": 30},
    ]

    for data in delivery_routes_data:
        delivery_route = DeliveryRoute(**data)
        session.add(delivery_route)

    # Добавление расписания доставки
    delivery_schedules_data = [
        {"route_id": 1, "delivery_datetime": random_date(datetime.now(), datetime.now() + timedelta(days=30))},
        {"route_id": 2, "delivery_datetime": random_date(datetime.now(), datetime.now() + timedelta(days=60))},
        {"route_id": 3, "delivery_datetime": random_date(datetime.now(), datetime.now() + timedelta(days=90))},
        {"route_id": 4, "delivery_datetime": random_date(datetime.now(), datetime.now() + timedelta(days=120))},
        {"route_id": 5, "delivery_datetime": random_date(datetime.now(), datetime.now() + timedelta(days=150))},
    ]

    for data in delivery_schedules_data:
        delivery_schedule = DeliverySchedule(**data)
        session.add(delivery_schedule)

    # Добавление инвентаря
    inventory_data = [
        {"product_id": 1, "quantity": 100, "expiry_date": datetime.now() + timedelta(days=30), "optimal_stock_levels": "High"},
        {"product_id": 2, "quantity": 200, "expiry_date": datetime.now() + timedelta(days=60), "optimal_stock_levels": "Medium"},
        {"product_id": 3, "quantity": 300, "expiry_date": datetime.now() + timedelta(days=90), "optimal_stock_levels": "Low"},
        {"product_id": 4, "quantity": 400, "expiry_date": datetime.now() + timedelta(days=120), "optimal_stock_levels": "Medium"},
        {"product_id": 5, "quantity": 500, "expiry_date": datetime.now() + timedelta(days=150), "optimal_stock_levels": "High"},
    ]

    for data in inventory_data:
        inventory = Inventory(**data)
        session.add(inventory)

    # Добавление продаж
    sales_data = [
        {"product_id": 1, "sales_point_id": 1, "sale_date": random_date(datetime.now(), datetime.now() + timedelta(days=30)), "quantity_sold": 20},
        {"product_id": 2, "sales_point_id": 2, "sale_date": random_date(datetime.now(), datetime.now() + timedelta(days=60)), "quantity_sold": 40},
        {"product_id": 3, "sales_point_id": 3, "sale_date": random_date(datetime.now(), datetime.now() + timedelta(days=90)), "quantity_sold": 60},
        {"product_id": 4, "sales_point_id": 4, "sale_date": random_date(datetime.now(), datetime.now() + timedelta(days=120)), "quantity_sold": 80},
        {"product_id": 5, "sales_point_id": 5, "sale_date": random_date(datetime.now(), datetime.now() + timedelta(days=150)), "quantity_sold": 100},
    ]

    for data in sales_data:
        sale = Sale(**data)
        session.add(sale)

    # Добавление прогнозов продаж
    sales_forecasts_data = [
        {"sales_point_id": 1, "product_id": 1, "forecasted_demand": 50, "avg_order_period": 5},
        {"sales_point_id": 2, "product_id": 2, "forecasted_demand": 70, "avg_order_period": 7},
        {"sales_point_id": 3, "product_id": 3, "forecasted_demand": 90, "avg_order_period": 9},
        {"sales_point_id": 4, "product_id": 4, "forecasted_demand": 110, "avg_order_period": 11},
        {"sales_point_id": 5, "product_id": 5, "forecasted_demand": 130, "avg_order_period": 13},
    ]

    for data in sales_forecasts_data:
        sales_forecast = SalesForecast(**data)
        session.add(sales_forecast)

    # Добавление сезонных коэффициентов
    seasonal_factors_data = [
        {"month": 1, "seasonality_coefficient": 1.2},
        {"month": 2, "seasonality_coefficient": 1.1},
        {"month": 3, "seasonality_coefficient": 1.0},
        {"month": 4, "seasonality_coefficient": 0.9},
        {"month": 5, "seasonality_coefficient": 0.8},
    ]

    for data in seasonal_factors_data:
        seasonal_factor = SeasonalFactors(**data)
        session.add(seasonal_factor)

    # Добавление трендов рынка
    market_trends_data = [
        {"start_date": datetime.now(), "end_date": datetime.now() + timedelta(days=30), "trend_coefficient": 1.1},
        {"start_date": datetime.now(), "end_date": datetime.now() + timedelta(days=60), "trend_coefficient": 1.2},
        {"start_date": datetime.now(), "end_date": datetime.now() + timedelta(days=90), "trend_coefficient": 1.3},
        {"start_date": datetime.now(), "end_date": datetime.now() + timedelta(days=120), "trend_coefficient": 1.4},
        {"start_date": datetime.now(), "end_date": datetime.now() + timedelta(days=150), "trend_coefficient": 1.5},
    ]

    for data in market_trends_data:
        market_trend = MarketTrends(**data)
        session.add(market_trend)

    # Сохранение изменений в базе данных
    session.commit()

def update_sales_data():
    # Получить все продажи
    sales = session.query(Sale).all()
    sale_dict = []
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
            print(inventory.quantity)
        point_dict = {
                    'product_id': sale.product_id,
                    'sales_point_id': sale.sales_point_id,
                    'quantity_sold': sale.quantity_sold
                }
        sale_dict.append(point_dict)

    # Сохранить изменения в базе данных
    session.commit()

    return sale_dict

# populate_database()
# update_sales_data()


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

    # Сохранить изменения в базе данных
    session.commit()

    return int(optimal_stock_level)

# 2. Проверка и управление сроками годности:
def check_expiry_dates():
    # Получить все продукты с просроченными сроками годности
    expired_products = session.query(Inventory).filter(Inventory.expiry_date <= func.now()).all()

    # Обновить информацию в инвентаре о просроченных продуктах
    for product in expired_products:
        product.quantity = 0  # Установить количество просроченного продукта в 0

        # Вывести информацию о просроченном продукте
        print(f"Product ID: {product.product_id}, Quantity Updated to: {product.quantity}")

    # Сохранить изменения в базе данных
    session.commit()

    return "Информация о просроченных продуктах успешно обновлена."


# 3. Обновление запасов на основе продаж:
def update_inventory_from_sales():
    # Получить все продажи
    sales = session.query(Sale).all()
    sale_dict = []
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
            print(inventory.quantity)
        point_dict = {
                    'product_id': sale.product_id,
                    'sales_point_id': sale.sales_point_id,
                    'quantity_sold': sale.quantity_sold
                }
        sale_dict.append(point_dict)

    # Сохранить изменения в базе данных
    session.commit()

    return sale_dict


# Рассчет и обновление оптимальных уровней запасов
for product_id in range(1, 6):
    for sales_point_id in range(1, 6):
        optimal_stock = calculate_optimal_stock_levels(product_id, sales_point_id)
        print(f"Optimal Stock for Product {product_id} at Sales Point {sales_point_id}: {optimal_stock}")

# Проверка и управление сроками годности
expired_info = check_expiry_dates()
print(expired_info)

# Обновление запасов на основе продаж
updated_inventory = update_inventory_from_sales()
print(updated_inventory)
