"""
ESTE CÓDIGO SERVIU APENAS PARA TESTES. O CÓDIGO FINAL ESTÁ NO ARQUIVO 'main.py'
"""
# Importando as bibliotecas e módulos necessários
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from math import factorial


# Combinação entre o valor resposta e o valor previsto pelo modelo
def combinacao(n, p):
    comb = (factorial(n))/(factorial(p)*factorial(abs(n-p)))
    return comb


# Importando o dataset
df = pd.read_csv("../CSVs/fetal_health.csv")

# Entendendo o dataframe
print(f'{df.head()}\n')
print(f'{df.shape}\n')
print(f'{df.dtypes}\n')
print(f'{list(df.columns)}\n')

# Removendo coluna com valores praticamente constantes
print(df['severe_decelerations'].value_counts())
df.drop('severe_decelerations', axis=1, inplace=True)

# Lidando com dados faltantes
print(f'{df.isna().any()}\n')

# Checando dados duplicados
print(df.duplicated().sum())
df.drop_duplicates(inplace=True)
print(f'{df.duplicated().sum()}\n')

# Exportando o dataframe alterado
df.to_csv("CSVs/fetal_health_manipulated.csv", index=False)

# Verificando a correlação entre as variávies do dataset
corr = df.corr()
sns.set_context("notebook", font_scale=1.0, rc={"lines.linewidth": 2.0})
plt.figure(figsize=(13, 7))
mask = np.zeros_like(corr)
mask[np.triu_indices_from(mask, 1)] = True
a = sns.heatmap(corr, mask=mask, annot=True, fmt='.2f')
rotx = a.set_xticklabels(a.get_xticklabels(), rotation=90)
roty = a.set_yticklabels(a.get_yticklabels(), rotation=30)

# Reunindo colunas com alta correlação
df.drop(columns=['histogram_mode', 'histogram_median'], axis=1, inplace=True)

# Passando as colunas que serão usadas de entrada no modelo (conjunto de features)
X = df.drop("fetal_health", axis=1)

# Passando a coluna que será usada de resposta do modelo (conjunto de labels)
y = df.fetal_health

# Dividindo os conjuntos de treino e de teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Normalizando os dados
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)

# Treinando o modelo
logit = LogisticRegression(verbose=1, max_iter=1000)
logit.fit(X_train, np.ravel(y_train, order='C'))
y_pred = logit.predict(X_test)
print(logit.score(X_test, y_test))
print('\n')

# Matriz de confusão
cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
print(f'Matriz de confusão:\n{cnf_matrix}\n')

# Acurácia
'''
acc = acurácia
fpos = número de falsos positivos
vneg = número de verdadeiros negativos
vpos = número de verdadeiros positivos

soma dos verdadeiros dividida pelo 3 da soma de todos os elementos da matriz (3 vezes pois são 3 classes).
'''
fpos = 0
vneg = 0
vpos = 0

for i in range(3):
    for j in range(3):
        fpos += cnf_matrix[j][i]
    fpos -= cnf_matrix[i][i]
    vneg += sum(sum(cnf_matrix)) - sum(cnf_matrix[i]) - fpos
    fpos = 0
    vpos += cnf_matrix[i][i]

acc = (vpos + vneg)/(3*sum(sum(cnf_matrix)))
print(f'Acurácia: {acc}')

# Sensibilidade
'''
snes = lista com sensibilidade de cada classe
ssens = soma de falsos negativos e verdadeiros positivos

verdadeiros positivos divididos pela soma dos verdadeiros positivos e falsos negativos
'''
sens = []

for i in range(3):
    ssens = sum(cnf_matrix[i])
    sens.append(cnf_matrix[i][i]/ssens)
    print(f'Sensibilidade (recall) de {i+1}: {sens[i]}')

# Especificidade
'''
espec = lista com especificidade de cada classe
fpos = numero de falsos positivos
vneg = numero de verdadeiros negativos

verdadeiros negativos divididos pela soma de verdadeiros negativos e falsos positivos
'''
espec = []
fpos = 0
vneg = 0

for i in range(3):
    for j in range(3):
        fpos += cnf_matrix[j][i]
    fpos -= cnf_matrix[i][i]
    vneg = sum(sum(cnf_matrix)) - sum(cnf_matrix[i]) - fpos
    espec.append(vneg/(vneg+fpos))
    print(f'Especificidade de {i+1}: {espec[i]}')
    fpos = 0

# Precisão (para medir o f1_score)

'''
prec = lista com precisão de cada classe
fpos = numero de falsos positivos
vpos = numero de verdadeiros positivos

verdadeiros positivos dividido pela soma dos positivos
'''
prec = []
fpos = 0

for i in range(3):
    for j in range(3):
        fpos += cnf_matrix[j][i]
    fpos -= cnf_matrix[i][i]
    vpos = cnf_matrix[i][i]
    prec.append(vpos/(vpos+fpos))
    fpos = 0

# f1_score

'''
dobro do produto da precisão com a sensibilidade divido pela soma da precisão com a sensibilidade
'''
f1_score = []

for i in range(3):
    f1_score.append((2*prec[i]*sens[i])/(prec[i]+sens[i]))
    print(f'f1_score de {i + 1}: {f1_score[i]}')

# Matriz de confusão 2
'''
vetor_test = recebe os valores do conjunto de teste como um vetor unidimensional
pred = lista com quantidade de predições pra cada classe
test = lista com quantidade de labels pra cada classe
função 'combinacao' = faz a combinação entre pred e test pra formar a matriz de confusão

tá dando errado. verificar depois.
'''

vetor_test = y_test.values

pred, test = [0, 0, 0], [0, 0, 0]

for i in range(len(y_pred)):
    if y_pred[i] == 1:
        pred[0] += 1
    elif y_pred[i] == 2:
        pred[1] += 1
    elif y_pred[i] == 3:
        pred[2] += 1

for i in range(len(vetor_test)):
    if vetor_test[i] == 1:
        test[0] += 1
    elif vetor_test[i] == 2:
        test[1] += 1
    elif vetor_test[i] == 3:
        test[2] += 1

confusion_matrix = [[], [], []]

for i in range(3):
    for j in range(3):
        confusion_matrix[j].append(combinacao(test[i], pred[j]))

print(confusion_matrix)
print(test)
print(pred)
