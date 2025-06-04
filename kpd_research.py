import matplotlib
import pandas as pd

from data import df
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')
pd.set_option('display.width', None)  # Автоматически подбирает ширину под консоль

# Основные факторы для расчёта КПД:
# avg_orders_per_shift  Среднее число заказов за смену  ↑ больше = ↑ эффективность
# days_active  Дней активности  ↑ больше = ↑ надежность
# total_shifts  Общее количество смен  ↑ больше = ↑ опытность
# median_time_ratio - медиана факта времени к плану. <1 - работает быстрее планового, >1 - наоборот
# avg_time_ratio - среднее факта времени к плану. Не учитывает выбросы
# pct_timer_up_expired  Процент просроченных доставок  ↓ меньше = ↑ качество
# stddev_up_ratio , iqr_up_ratio  Мера нестабильности доставок  ↓ меньше = ↑ предсказуемость Не используем !!!!!!!
print('*' * 200)

# Метрики для оценки КПД
metrics = [
    'avg_orders_per_shift',
    'median_time_ratio',
    'pct_timer_up_expired',
    'stddev_up_ratio',
    'days_active'
]

# Нормализация
scaler = MinMaxScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df[metrics]), columns=metrics, index=df.index)

# Веса
weights = {
    'avg_orders_per_shift': 0.5,
    'median_time_ratio': -0.1,  # обратная метрика
    'pct_timer_up_expired': -0.1,
    'stddev_up_ratio': -0.1,
    'days_active': 0.1  # стабильность
}

# Расчёт courier_score
df['courier_score'] = (
        df_scaled['avg_orders_per_shift'] * weights['avg_orders_per_shift'] +
        (1 - df_scaled['median_time_ratio']) * weights['median_time_ratio'] +
        (1 - df_scaled['pct_timer_up_expired']) * weights['pct_timer_up_expired'] +
        (1 - df_scaled['stddev_up_ratio']) * weights['stddev_up_ratio'] +
        df_scaled['days_active'] * weights['days_active']
)

# Нормализуем courier_score от 0 до 1
df['courier_score'] = MinMaxScaler().fit_transform(df[['courier_score']])

# Переставляем колонки так, чтобы courier_score был первой колонкой после индекса
cols = ['courier_score'] + [col for col in df.columns if col != 'courier_score']
df = df[cols]

# Сортируем и выводим
print(df.sort_values('courier_score', ascending=False))


if __name__ == "__main__":


    # Топ N самых эффективных курьеров
    top_n = 10
    top_couriers = df['courier_score'].sort_values(ascending=False).head(top_n)

    plt.figure(figsize=(10, 6))
    top_couriers.plot(kind='bar', color='skyblue')
    plt.title('Топ 10 курьеров по КПД')
    plt.xlabel('ID курьера')
    plt.ylabel('КПД (courier_score)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Распределение КПД
    plt.figure(figsize=(8, 5))
    plt.hist(df['courier_score'], bins=30, color='teal', edgecolor='black')
    plt.title('Распределение КПД курьеров')
    plt.xlabel('courier_score')
    plt.ylabel('Частота')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Зависимость между заказами в смену и КПД
    plt.figure(figsize=(8, 6))
    plt.scatter(
        df['avg_orders_per_shift'],
        df['courier_score'],
        alpha=0.6,
        c='green'
    )
    plt.title('Зависимость КПД от среднего числа заказов в смену')
    plt.xlabel('Среднее число заказов в смену')
    plt.ylabel('courier_score')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


