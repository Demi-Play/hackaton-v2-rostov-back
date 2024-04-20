from filler import calculate_optimal_stock_levels, check_expiry_dates, update_inventory_from_sales


# Рассчитать оптимальные уровни запасов для продукта с ID=1 и точки продажи с ID=1
print(calculate_optimal_stock_levels(1, 1))

# Проверить и обновить информацию о просроченных продуктах
print(check_expiry_dates())

# Обновить запасы в инвентаре на основе продаж
print(update_inventory_from_sales())