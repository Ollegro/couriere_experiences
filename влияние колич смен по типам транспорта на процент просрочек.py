import matplotlib
import pandas as pd

matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.tools.tools import add_constant

# Группируем по courier_dtype и строим отдельную модель для каждой группы
df = pd.read_csv('results/courier_score.csv')
df_reset = df.reset_index()
courier_types = df_reset['courier_dtype'].unique()

plt.figure(figsize=(12, 8))

for i, dtype in enumerate(courier_types):
    df_group = df_reset[df_reset['courier_dtype'] == dtype]
    X = df_group['total_shifts']
    y = df_group['pct_timer_up_expired']

    if len(X) < 2:
        continue  # пропускаем группы с малым числом наблюдений
    X = add_constant(X)

    model = sm.OLS(y, X).fit()

    print(f"\n[courier_dtype = {dtype}]")
    print("Коэффициент total_shifts:", model.params['total_shifts'])
    print("P-значение:", model.pvalues['total_shifts'])



    # Визуализация
    plt.subplot(2, 2, i+1)
    sns.regplot(x='total_shifts', y='pct_timer_up_expired', data=df_group,
                scatter_kws={'alpha': 0.6}, line_kws={'color': 'red'})
    plt.title(f'{dtype}\n(slope={model.params["total_shifts"]:.6f})')
    plt.xlabel('Число смен')
    plt.ylabel('pct_timer_up_expired')
    plt.grid(True)

plt.tight_layout()
plt.show()

print('\n','Выводы \n'
           'Коэффициент показывает, на сколько процентов снижается доля просроченных заказов (pct_timer_up_expired) при увеличении числа смен на 1 .\n'
           'Например:\n'
           'Для велокурьеров :\n'
           'с каждой новой сменой доля просрочек падает на 2.9%\n'
           'Для электровелокурьеров :\n'
           'с каждой новой сменой доля просрочек падает на 1.3%\n'
           'Для автокурьеров :\n'
           'падает на 1.2%\n'
           'Для пеших курьеров :\n'
           'влияния нет — p > 0.05 → статистически незначимо \n' )