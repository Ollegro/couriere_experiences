import matplotlib
import pandas as pd
from matplotlib import pyplot as plt
matplotlib.use('TkAgg')
df = pd.read_csv('results/courier_score.csv')


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

# *********************************************************************************************************
# Записываем в эксель
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

from openpyxl.drawing.image import Image as XLImage
from io import BytesIO
from PIL import Image

# Шаг 1: Загрузка данных
df = pd.read_csv('courier_score.csv')

# Шаг 2: Группировка данных
grouped = df.groupby('experience_category', observed=True).agg(
    avg_orders=('avg_orders_per_shift', 'mean'),
    median_orders=('avg_orders_per_shift', 'median'),
    courier_count=('id_driver', 'count')
).round(2).sort_values(by='avg_orders', ascending=False)

# Шаг 3: Построение графика
plt.figure(figsize=(10, 6))

for category in df['experience_category'].unique():
    subset = df[df['experience_category'] == category]
    plt.scatter(subset['avg_orders_per_shift'], subset['courier_score'], label=category, alpha=0.7, edgecolor='k')

plt.title('courier_score по категориям опыта')
plt.xlabel('Среднее число заказов в смену')
plt.ylabel('courier_score (КПД)')
plt.legend(title='Категория опыта')
plt.grid(True)
plt.tight_layout()

# Сохраняем график в буфер
buf = BytesIO()
plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
buf.seek(0)
plt.close()

# Шаг 4: Сохранение в Excel
output_path = 'results/courier_analysis.xlsx'
sheet_name = 'опыт_vs_заказы'

with pd.ExcelWriter(output_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    # Записываем таблицу начиная с A1
    grouped.to_excel(writer, sheet_name=sheet_name, startrow=1)

    worksheet = writer.sheets[sheet_name]

    # Добавляем заголовок
    worksheet.cell(row=1, column=1, value='Среднее и медиана avg_orders_per_shift по категориям опыта')

    # Автоподбор ширины столбцов
    for idx, col in enumerate(grouped.columns):
        max_length = max(grouped[col].astype(str).map(len).max(), len(col)) + 2
        worksheet.column_dimensions[worksheet.cell(row=1, column=idx+1).column_letter].width = max_length

    # Добавляем изображение на ячейку A10
    img = XLImage(buf)
    worksheet.add_image(img, 'A10')

print(f"Результаты успешно сохранены в {output_path}, лист '{sheet_name}'")