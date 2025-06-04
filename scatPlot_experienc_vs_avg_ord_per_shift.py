import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('TkAgg')
from kpd_research import df


# СТРОИМ СКАТТЕР ПЛОТ  - СРЕДНЕЕ ЧИСЛО ЗАКАЗОВ В СМЕНУ В ЗАВИС ОТ КАТЕГОРИИ ОПЫТА
# Уникальные категории (на случай, если появятся новые)
categories = df['experience_category'].unique()

# Цвета для категорий — добавили 'эксперт'
colors = {
    'новичок': 'red',
    'средний': 'blue',
    'опытный': 'green',
    'эксперт': 'purple',  # ← новый цвет
    'обычный': 'brown'
}

plt.figure(figsize=(10, 6))

# Рисуем точки по категориям
for category in categories:
    subset = df[df['experience_category'] == category]
    plt.scatter(
        subset['avg_orders_per_shift'],
        subset['courier_score'],
        label=category,
        color=colors[category],  # Теперь KeyError не будет
        alpha=0.7,
        edgecolor='k'
    )

# Подписи и легенда
plt.title('courier_score по категориям опыта', fontsize=14)
plt.xlabel('Среднее число заказов в смену', fontsize=12)
plt.ylabel('courier_score (КПД)', fontsize=12)
plt.legend(title='Категория опыта')
plt.grid(True)
plt.tight_layout()
plt.show()


