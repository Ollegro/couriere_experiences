import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
matplotlib.use('TkAgg')
# вычислить датафрейм и нарисовать именно гистограмму в pandas - влияние количества смен на объем исполненных заказов
# в смену Создание DataFrame с группами

df_reset = pd.read_csv('courier_score.csv').reset_index()


# Определим бины для total_shifts
bins = [20, 50, 100, 200, 500]
labels = ['20-50', '51-100', '101-200', '201-500']

# Добавляем столбец с категорией смен
df_reset['shift_group'] = pd.cut(df_reset['total_shifts'], bins=bins, labels=labels)

# Группируем по группам смен и считаем среднее число заказов в смену
grouped = df_reset.groupby('shift_group', observed=True).agg(
    avg_orders=('avg_orders_per_shift', 'mean'),
    courier_count=('id_driver', 'count')
).round(2)
print('влияние количества смен на объем исполненных заказов в смену','\n',grouped,'\n' )

# Визуализация зависимости
# Построение столбчатого графика
ax = grouped['avg_orders'].plot(kind='bar', figsize=(10, 6), color='skyblue')
plt.title('Среднее количество заказов в смену в зависимости от общего числа смен')
plt.xlabel('Число смен (total_shifts)')
plt.ylabel('Среднее число заказов в смену')
plt.xticks(rotation=45)

# Подписываем значения avg_orders и courier_count на графике
for i, (index, row) in enumerate(grouped.iterrows()):
    # Среднее число заказов
    ax.text(i, row['avg_orders'] + 0.1, f'{row["avg_orders"]:.2f}',
            ha='center', fontsize=11, fontweight='bold')
    # Количество курьеров (n)
    ax.text(i, row['avg_orders'] - 0.15, f'n={row["courier_count"]}',
            ha='center', fontsize=9, color='dimgray')

# Подпись внизу графика
plt.figtext(0.5, 0.01, 'n = количество курьеров в группе',
            ha='center', fontsize=10, color='gray', style='italic')

plt.ylim(grouped['avg_orders'].min() - 0.3, grouped['avg_orders'].max() + 0.2)

plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()