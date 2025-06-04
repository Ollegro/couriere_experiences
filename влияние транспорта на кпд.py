import matplotlib
import pandas as pd
from matplotlib import pyplot as plt
matplotlib.use('TkAgg')

# Сброс индекса, чтобы включить id_driver в дальнейшую обработку
df_reset = pd.read_csv('courier_score.csv').reset_index()


# Группировка по courier_dtype
grouped = df_reset.groupby('courier_dtype').agg(
    avg_courier_score=('courier_score', 'mean'),
    courier_count=('id_driver', 'count'),
    avg_orders_per_shift=('avg_orders_per_shift', 'mean'),
    avg_median_time_ratio=('median_time_ratio', 'mean'),
    avg_pct_timer_up_expired=('pct_timer_up_expired', 'mean'),
    avg_stddev_up_ratio=('stddev_up_ratio', 'mean'),
    avg_days_active=('days_active', 'mean')
).round(2)
print(grouped.sort_values('avg_courier_score'), '\n')

# Сравнение среднего КПД по типам курьеров
plt.figure(figsize=(10, 6))
grouped['avg_courier_score'].plot(kind='bar', color='skyblue')
plt.title('Средний КПД курьеров по типу доставки')
plt.xlabel('Тип курьера (courier_dtype)')
plt.ylabel('avg_courier_score')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

