import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
matplotlib.use('TkAgg')


# Проверим гипотезу - с увеличением опыта курьера (experience_category) улучшается отношение факта к плану.
# median_time_ratio снижается — курьер прибывает вовремя.


# Выбираем данные
df_reset = pd.read_csv('results/courier_score.csv').reset_index()

X = df_reset['total_shifts']  # Предиктор (опыт)
y = df_reset['median_time_ratio']  # Целевая переменная (эффективность)

# Добавляем константу для intercept
X = sm.add_constant(X)

# Обучаем модель
model = sm.OLS(y, X).fit()
print('C УВЕЛИЧЕНИЕМ ОПЫТА КУРЬЕРА (EXPERIENCE_CATEGORY) УЛУЧШАЕТСЯ ОТНОШЕНИЕ ФАКТА К ПЛАНУ ','\n',model.summary(), '\n')

print(' Вывод:\n' +
      'С увеличением числа смен (total_shifts) курьеры становятся более пунктуальными (отношение факта к плану '
      'снижается).\n' +
      'Эффект маленький, но стабильный и значимый .\n' +
      'Это может говорить о том, что курьеры учатся на опыте , лучше оценивают время пути, избегают пробок и т.п.\n\n')

# Рисуем график
# Данные
x = df_reset['total_shifts']
y = df_reset['median_time_ratio']
# Построение графика
plt.figure(figsize=(10, 6))
plt.scatter(x, y, alpha=0.5, color='steelblue', label='Курьеры', s=30)
# Регрессионная прямая: y = const + coef * x
const = 0.5729
coef = -0.0004
x_line = np.array([x.min(), x.max()])
y_line = const + coef * x_line
# Рисуем линию регрессии
plt.plot(x_line, y_line, color='red', linewidth=2, label='Регрессионная линия')
# Подписи
plt.title('Зависимость median_time_ratio от числа смен (total_shifts)')
plt.xlabel('Число смен (total_shifts)')
plt.ylabel('median_time_ratio')
plt.legend()
plt.grid(True)
plt.tight_layout()
# Отображаем
plt.show()


# Теперь сделаем анализ влияния количества смен на процент просрочек по времени
# Убедимся, что индекс не мешает

X = df_reset['total_shifts']
y = df_reset['pct_timer_up_expired']
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
print('ВЛИЯНИЯ КОЛИЧЕСТВА СМЕН НА ПРОЦЕНТ ПРОСРОЧЕК ПО ВРЕМЕНИ','\n',model.summary(),'\n'+

'1. Коэффициент total_shifts = -0.0133\n'+
'Это означает, что с каждой дополнительной сменой процент просроченных доставок (pct_timer_up_expired) уменьшается на 0.0133% .\n'+

'То есть:\n'+
'Курьер становится всё более пунктуальным по мере увеличения опыта.\n'
'Пример:\n'
'На 10-й смене:\n'
'pct_timer_up_expired = 4.2158 + (-0.0133 × 10) = 4.0828%\n'
'На 50-й смене:\n'
'pct_timer_up_expired = 4.2158 + (-0.0133 × 50) = 3.5498%\n'
'С каждыми 10 сменами курьер теряет ~0.133% просрочек — заметное улучшение!\n'
'P-значение = 0.000\n'
'Это говорит о том, что связь между total_shifts и pct_timer_up_expired — статистически значима .\n'
'То есть, зависимость реальна , а не случайна.\n'
'Const = 4.2158\n'
'Это значение pct_timer_up_expired у курьера с 0 смен.\n'
'Иными словами — новички в среднем имеют около 4.2% просроченных заказов .\n'
'Общий вывод:\n'
'С увеличением количества смен (total_shifts) курьеры становятся более пунктуальными , и процент просроченных заказов снижается линейно .\n'
'Эффект статистически значимый и довольно стабильный .\n'
'Это может говорить о том, что курьеры учатся лучше планировать время , избегать пробок, выбирать лучшие маршруты и т.п.\n\n' )

# Визуализация зависимости ВЛИЯНИЯ КОЛИЧЕСТВА СМЕН НА ПРОЦЕНТ ПРОСРОЧЕК ПО ВРЕМЕНИ
x = df_reset['total_shifts']
y = df_reset['pct_timer_up_expired']
# Построение графика
plt.figure(figsize=(10, 6))
plt.scatter(x, y, alpha=0.5, color='steelblue', label='Курьеры', s=30)
# Регрессионная прямая: y = const + coef * x
const = 4.2158
coef = -0.0133
x_line = np.array([x.min(), x.max()])
y_line = const + coef * x_line
# Рисуем линию регрессии
plt.plot(x_line, y_line, color='red', linewidth=2, label='Регрессионная линия')
# Подписи
plt.title('Зависимость pct_timer_up_expired от числа смен (total_shifts)')
plt.xlabel('Число смен (total_shifts)')
plt.ylabel('pct_timer_up_expired')
plt.legend()
plt.grid(True)
plt.tight_layout()
# Отображаем
plt.show()