#!/usr/bin/env python
# coding: utf-8

# # TP Règles d'associations et motifs fréquents (correction)

# In[11]:


import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules


# ## Exercice 2. Titanic

# Le RMS Titanic est un paquebot transatlantique britannique qui fait naufrage dans l’océan Atlantique
# Nord en 1912 à la suite d’une collision avec un iceberg, lors de son voyage inaugural de Southampton
# à New York. C’est l’une des plus grandes catastrophes maritimes survenues en temps de paix et la plus
# grande pour l’époque. (Source : Wikipédia)
# 
# Nous disposons de données sur les passagers (âge, sexe, . . .) et leur devenir (survivant ou non au
# naufrage). Le fichier "titanic3.xls" est à télécharger sur la page AMeTICE du cours.
# 
# Vous allez utiliser les règles d’association pour caractériser les deux classes (survivant et non-survivant)
# en fonction des autres attributs.

# ### 1. Chargement des données

# In[12]:


df = pd.read_excel('titanic3.xls')


# In[13]:


#vérification des données chargées
print(df.shape)
print(df.columns)
print(df.dtypes)


# In[14]:


print(df.head())


# ### 2. Préparation des données

# Pour préparer les données, nous allons sélectionner certains attributs ("pclass", "survived", "sex"
# et "age"), ignorer les exemples ayant une ou plusieurs valeurs manquantes, discrétiser l’âge (en
# deux), renommer des valeurs et changer le type des colonnes (en "category"). Enfin, nous mettrons lehs données préparées au bon format pour MLxtend.

# In[17]:


#on enleve les attributs non voulus
df1 = df.drop(columns = ['name', 'ticket', 'home.dest', 'cabin', 'boat', 'body', 'sibsp', 'parch', 'fare', 'embarked'])


# In[18]:


print(df1.shape)
print(df1.head())
print(df1.dtypes)
print(df1.columns)


# In[19]:


#ignorer les exemples ou l'age est inconnu
#print(df1['age'])
print(df1['age'].isnull().sum())

df2 = df1.dropna()

#print(df2.shape)
#print(df2.head())

# reste-t-il des valeurs manquantes?
print(df2.isnull().values.any())


# In[20]:


#discrétisation de l'age
data = df2['age']
agemin = data.min()
agemax = data.max()
datad = pd.cut(data, bins=[agemin, 18, agemax], labels=['child', 'adult'], include_lowest = True)
print(datad.value_counts())
#ici, au lieu d’indiquer le nombre d’intervalles (par exemple, "bins=2"), 
#on donne une liste de valeurs. Afin d’inclure le minimum, on ajoute "include_lowest=True"


# In[21]:


df2.insert(4, "aged", datad, True)
print(df2.head())
df2 = df2.drop(columns = ['age'])
df2 = df2.rename(columns={'aged': 'age'})
print(df2.head())


# In[22]:


#renommage de valeurs
df2['pclass'] = df2['pclass'].map({1:'class=1st', 2:'class=2nd', 3:'class=3rd'})
df2['survived'] = df2['survived'].map({1:'survived=yes', 0:'survived=no'})
df2['sex'] = df2['sex'].map({'female':'sex=female', 'male':'sex=male'})
df2['age'] = df2['age'].map({'adult':'age=adult', 'child':'age=child'})


# In[23]:


#changement de types
print(df2.dtypes)
df2['pclass'] = df2['pclass'].astype('category')
df2['survived'] = df2['survived'].astype('category')
df2['sex'] = df2['sex'].astype('category')
#df2['age'] = df2['age'].astype('category')
print(df2.dtypes)


# In[24]:


#pour enregistrer les donnees preparees dans un fichier
#df2.to_csv('titanic.csv', header=True, index=False)


# In[25]:


dataset = df2.values
te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
dataset = pd.DataFrame(te_ary, columns=te.columns_)


# ### 3. Découverte des règles d'association

# In[26]:


#extraction des motifs frequents
frequent_itemsets = apriori(dataset, min_support=0.50, use_colnames=True, verbose=0)
print(frequent_itemsets)


# In[27]:


#génération des règles d'association
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.8)
print(rules)


# ### 4. Post-traitement et interprétation des résultats

# In[28]:


myRules = rules.loc[:,['antecedents','consequents', 'support', 'confidence', 'lift']]
print(myRules)


# La 1re regle est peu interessante.
# 
# (sex=male) -> (age=adult)  supp=0.533  lift=1.038
# 
# Il y a 1046 passagers au total.
# 
# A partir des données, on voit que :
# 
# 658 sont des hommes ; support(sex=male) = P(sex=male) = 0,629.
# 
# 853 sont des adultes ; support(age=adult) = P(age=adult) = 0,815.
# 
# support = P(sex=male et age=adult) = 0,533 (558/1046)
# 
# confiance = P(sex=male et age=adult) / P(sex=male) = 0,847 (0,5333/0,629)
# 
# lift = confiance / support(age=adult) = 1,039 (0,847/0,815)
# 
# Cette règle concerne 558 passagers sur 1046, soit un support de 53,3%. Comme il y a 658 personnes de sexe masculin dont 558 sont adultes, la confiance est de 84,7%.
# Le lift est seulement de 1,039. La confiance dépasse de peu la probabilité d'avoir une personne adulte (qui est de 81,5%).
# 
# Cette règle est donc peu intéressante.
# 
# 
# La 2e regle l'est un peu plus.
# 
# (survived=no) -> (sex=male)  supp=0.500  lift=1.343

# ### 5. A vous de jouer

# Refaire l'extraction des motifs et la génration des règles en faisant varier le minsup et minconf
# 
# Remarque : si le minsup n'est pas assez bas, on ne verra pas les enfants 
# (age=child) dans les regles produites par la suite
# 
# Une bonne premiere approche est : faible minsup (si calculs possibles) et minconf eleve, ensuite ajustement/essai

# In[29]:


# extraction des motifs frequents et des regles d'association
frequent_itemsets = apriori(dataset, min_support=0.01, use_colnames=True, verbose=0)
print(frequent_itemsets)


# In[37]:


rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.8)
print(rules.shape)
#print(rules)


# In[39]:


myRules = rules.loc[:,['antecedents','consequents', 'support', 'confidence', 'lift']]
print(rules.shape)
#print(myRules)


# In[40]:


#filtrer les regles avec 'survived=yes' dans consequent
survivants = myRules[myRules['consequents'].eq({'survived=yes'})]
print(survivants.sort_values(by='lift', ascending=False))


# In[41]:


#filtrer les regles avec 'survived=no' dans consequent
nonsurvivants = myRules[myRules['consequents'].eq({'survived=no'})]
print(nonsurvivants.sort_values(by='lift', ascending=False))


# **Nous observons que les hommes de 2e et 3e classe n'ont en général pas survécu. 
# Les femmes de 1re et 2e classe ont en général survécu, tout comme les enfants de 1re et 2e classe.**

# **Remarque : attention au (très) faible support de certaines règles qui concernent donc peu de passagers. Il faut être prudent dans les conclusions...**

# In[ ]:




