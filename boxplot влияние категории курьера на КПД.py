import matplotlib
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
matplotlib.use('TkAgg')
pd.set_option('display.width', None)  # Автоматически подбирает ширину под консоль



# СТРОИМ ЯШИК С УСАМИ ПО КАТЕГОРИЯМ ОПЫТА ДЛЯ ЗНАЧЕНИЯ COURIER_SCORE
# Группируем данные по experience_category, указываем observed=True

df = pd.read_csv('courier_score.csv')


groups = df.groupby('experience_category', observed=True)['courier_score'].apply(list)

# Подготавливаем данные для boxplot
data = [np.array(groups[cat]) for cat in groups.index]

# Строим boxplot
plt.figure(figsize=(10, 6))
plt.boxplot(data, tick_labels=groups.index, patch_artist=True)  # <-- labels → tick_labels

# Оформление графика
colors = ['lightblue', 'lightgreen', 'salmon']
bplots = plt.boxplot(data, tick_labels=groups.index, patch_artist=True)

for patch, color in zip(bplots['boxes'], colors):
    patch.set_facecolor(color)

plt.title('Распределение courier_score по категориям опыта', fontsize=14)
plt.xlabel('Категория опыта', fontsize=12)
plt.ylabel('courier_score', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(rotation=0)
plt.tight_layout()

# Показываем график
plt.show()
