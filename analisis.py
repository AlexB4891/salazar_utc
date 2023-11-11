import pandas as pd
from IPython.display import display
import scipy.stats as stats
import seaborn as sns
import textwrap
import matplotlib.pyplot as plt

df = pd.read_excel('datos_encuestas_empresas.xlsx',sheet_name='Respuestas de formulario 1')

# transformar todas las columnas a texto
df = df.astype(str)

def count_frecuency(compare):
    
    new_df = df.groupby([df.columns[2], df.columns[compare]]).size().reset_index(name='count')

    new_df['Porcentaje'] = (new_df['count'] / new_df['count'].sum()) * 100
    
    new_df.columns = [df.columns[2], df.columns[compare], 'Frecuencia', 'Porcentaje']

    return new_df

def collapse_responeses(count_df):
    top_n = 3
    
    grouped = count_df.groupby(count_df.columns[0]).apply(lambda x: x.nlargest(top_n, count_df.columns[3])).reset_index(drop=True)
    # ordenar de mayor a menor de acuerdo a la columna porcentaje
    grouped = grouped.sort_values(by=[grouped.columns[0],grouped.columns[3]], ascending=False)

    return grouped

def contingency_table_analysis(df, column1, column2):
    contingency_table = pd.crosstab(df[column1], df[column2])
    contingency_table['Total'] = contingency_table.sum(axis=1)
    contingency_table.loc['Total'] = contingency_table.sum() 
    return contingency_table

def print_contingency_table(contingency_table):
    chi2, p, dof, expected = stats.chi2_contingency(contingency_table)
    print(f"Chi-cuadrado: {chi2}")
    print(f"p-valor: {p}")
    print(f"Grados de libertad: {dof}")
    return(p)

def solo_p(contingency_table):
    chi2, p, dof, expected = stats.chi2_contingency(contingency_table)
    return p




# p = print_contingency_table(contingency_table)

def heat_plot(df, column1, column2):

    contingency_table = contingency_table_analysis(df, column1, column2)
    # Luego, crea el mapa de calor con seaborn
    plt.figure(figsize=(10, 7))
    sns.heatmap(contingency_table, annot=True, fmt="d", cmap="YlGnBu")


    # Configura los títulos de los ejes con wrap
    plt.xlabel('\n'.join(textwrap.wrap(column1, 50)))
    plt.ylabel('\n'.join(textwrap.wrap(column2, 50)))

    # Muestra el gráfico
    plt.show()

# heat_plot(df, df.columns[3], df.columns[4])

# heat_plot(contingency_table, df.columns[3], df.columns[4])

# Encontrar a los significativos:
# for i in range(2, 15):
#     for j in range(2, 15):
#         contingency_table = contingency_table_analysis(df, df.columns[i], df.columns[j])
#         p = solo_p(contingency_table)
#         if p < 0.05:
#             print(i,j)