import pandas as pd
from pandas.api.types import CategoricalDtype
pd.set_option('display.width', None)  # Автоматически подбирает ширину под консоль
df = pd.read_csv('row_data/couriers4 08.00.18.csv')
print(df.shape)# Получаем предварительные данные о ДФ
print(df.info(),'\n')
print(df.describe(), '\n')
print(df.isna().sum(), '\n') # Проверяем датафрейм на отсутствие нулевых значений
print(df.duplicated().sum(), '\n') #Check duplicates
# Изменим одно из названий категории
df['experience_category'] = df['experience_category'].replace({'мега-опытный': 'эксперт'})
# Изменим тип анных столбца experience_category на 'category' для улучшения производительности
# Создаём упорядоченный тип.
cat_type = CategoricalDtype(categories=["новичок", "опытный", "эксперт","обычный"], ordered=True)
# Применяем к столбцу
df['experience_category'] = df['experience_category'].astype(cat_type)
# Проверяем уникальность
print(df['experience_category'].unique(), '\n')


# Убедимся, что id_driver будет индексом
df.set_index('id_driver', inplace=True)

# Фильтрация: только курьеры с не менее чем 20 сменами + копия дф
df = df[df['total_shifts'] >= 20]

# Удаляем ненужную колонку
df = df.drop(columns=['iqr_up_ratio'])

print('Датафрейм из файла данных, индексы - id_driver','\n',df.head(15).sort_values('pct_timer_up_expired', ascending=False), '\n')