import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from data import df

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
print('Датафрейм с посчитанным КПД - courier_score','\n',df.sort_values('courier_score', ascending=False), '\n')

# Записываем датафрейм в новый csv
df.to_csv('courier_score.csv')


df = pd.read_csv('courier_score.csv')
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


# ГРУППИРОВКА ПО КАТЕГОРИИ ОПЫТА

# Убедимся что индекс не мешает
df_reset = df.reset_index()

# Группируем по experience_category и считаем средний courier_score
grouped_by_exp = df_reset.groupby('experience_category', observed=True).agg(
    avg_courier_score=('courier_score', 'mean'),
    courier_count=('id_driver', 'count')
).sort_values(by='avg_courier_score', ascending=False).round(2)
print('Зависимость КПД от опыта', '\n',grouped_by_exp, '\n')

# Визуализация зависимости КПД от категории опыта
plt.figure(figsize=(8, 6))
plt.plot(grouped_by_exp.index, grouped_by_exp['avg_courier_score'], marker='o', color='darkcyan')
plt.title('Зависимость КПД от категории опыта')
plt.xlabel('Категория опыта')
plt.ylabel('avg_courier_score')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# вычислить датафрейм и нарисовать гистограмму зависимость КПД от количества смен
# Восстанавливаем id_driver как столбец для работы
df_reset = df.reset_index()

# Создаём бины и метки для категоризации
bins = [20, 49, 99, 199, float('inf')]
labels = ['20-49', '50-99', '100-199', '200+']

# Добавляем категорию "Количество смен"
df_reset['shifts_category'] = pd.cut(df_reset['total_shifts'], bins=bins, labels=labels)

# Группируем по количеству смен и считаем средний courier_score и количество курьеров
grouped_by_shifts = df_reset.groupby('shifts_category', observed=True).agg(
    avg_courier_score=('courier_score', 'mean'),
    courier_count=('id_driver', 'count')
).round(2)
print('Зависимость КПД от количества смен','\n',grouped_by_shifts, '\n')

# Построение графика зависимости КПД от количества смен. Гистограмма с двумя осями (КПД + количество курьеров)
fig, ax1 = plt.subplots(figsize=(10, 6))

# Столбчатая диаграмма — количество курьеров
ax1.bar(grouped_by_shifts.index.astype(str), grouped_by_shifts['courier_count'],
        color='skyblue', label='Число курьеров', alpha=0.7)

# Линия — средний КПД
ax2 = ax1.twinx()
ax2.plot(grouped_by_shifts.index.astype(str), grouped_by_shifts['avg_courier_score'],
         color='darkorange', marker='o', linestyle='-', linewidth=2, label='Средний КПД')

# Настройки графика
ax1.set_title('Зависимость КПД от количества смен', fontsize=14)
ax1.set_xlabel('Количество смен (интервалы)', fontsize=12)
ax1.set_ylabel('Число курьеров', fontsize=12, color='skyblue')
ax2.set_ylabel('Средний КПД', fontsize=12, color='darkorange')
plt.xticks(rotation=45)

# Легенды
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

plt.tight_layout()
plt.grid(True, axis='x', linestyle='--', alpha=0.5)
plt.show()