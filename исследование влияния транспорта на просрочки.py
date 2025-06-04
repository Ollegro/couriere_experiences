import matplotlib
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

matplotlib.use('TkAgg')


df= pd.read_csv('results/courier_score.csv').reset_index()
# ГРУППИРУЕМ ПО ТИПУ ТРАНСПОРТА И СЧИТАЕМ ПОКАЗАТЕЛИ ПО ПОЛЮ SCORE.
# Уникальные типы транспорта
transport_types = df['courier_dtype'].unique()
# Настройки графика
plt.figure(figsize=(10, 6))

# Для каждого типа транспорта строим гистограмму
for transport in transport_types:
    subset = df[df['courier_dtype'] == transport]['pct_timer_up_expired']
    # Веса: каждый элемент — доля в процентах от общего числа курьеров
    weights = np.ones_like(subset) / len(subset) * 100
    # Строим гистограмму как контур (без заливки)
    plt.hist(subset, bins=20,
             weights=weights,
             histtype='step',  # только контур
             linewidth=2,  # толщина линии
             label=transport)
# Оформление графика
plt.title('Процент курьеров по уровню просроченных заказов')
plt.xlabel('Процент просроченных заказов')
plt.ylabel('Процент курьеров (%)')
plt.legend(title='Тип транспорта')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
# Отображаем график
plt.show()
