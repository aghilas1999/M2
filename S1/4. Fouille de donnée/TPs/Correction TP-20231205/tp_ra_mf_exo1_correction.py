#!/usr/bin/env python
# coding: utf-8

# # TP Règles d'associations et motifs fréquents (correction)

# In[1]:


import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules


# ## Exercice 1. Analyse du ticket de caisse

# ### 1. Chargement des données

# Les données que nous allons utiliser sont déjà préparées (fichier "market-basket.csv").
# 
# Chaque ligne correspond à une transaction (i.e., un panier/ticket) et chaque colonne à un item (i.e., un produit). Un "1" (ou "True") code la présence d’un item (i.e., produit acheté), un "0" ou "False" son absence (i.e., produit non acheté).

# In[2]:


dataset = pd.read_csv('market_basket.csv', header=0)
print(dataset.shape)
print(dataset.columns)


# In[3]:


# transformation en valeurs booléennes (étape non obligatoire mais recommandée par MLxtend)
for col in dataset.columns:
    dataset[col] = dataset[col].map({1 : True, 0 : False})
    dataset[col].astype("boolean")


# ### 2. Extraction des motifs fréquents

# Pour extraire les motifs fréquents, nous utilisons apriori() sur les données chargées précédemment, avec un support minimum (min_support) fixé à 0,025 (i.e., 2,5%, soit 34 transactions), une cardinalité max (max_len) pour un motif fixée à 4 items et une utilisation des noms d’item (use_colnames) à vrai.
# 
# Nous remarquons que les résultats (l’ensemble des motifs fréquents) sont stockés dans un DataFrame et qu’un motif est stockée dans une Serie. 
# 
# Pour chaque motif, nous avons la valeur de son support en relatif (%) et les items qu’il contient. 
# 
# Notons que les items sont stockés dans un frozenset, i.e., un ensemble non modifiable (non-mutable).

# In[4]:


taillemax = 4
freq_itemsets = apriori(dataset, min_support=0.025, max_len=taillemax, use_colnames=True, verbose=0)


# In[5]:


# type du résultat
type(freq_itemsets)


# In[6]:


# nombre de motifs obtenus
print(freq_itemsets.shape)


# In[7]:


# liste des colonnes
print(freq_itemsets.columns)


# In[8]:


# affichage des 15 premiers motifs
print(freq_itemsets.head(15))


# In[9]:


# type de la colonne ’itemsets’
print(type(freq_itemsets.itemsets))


# In[10]:


# affichage du premier élément
print(freq_itemsets.itemsets[0])


# ### 3. Génération des règles d’association

# Afin de produire les règles d’association, il faut utiliser association_rules(). Nous allons choisir la mesure (metric) de la confiance et fixer le seuil minimal (min_threshold) à 0,75 (i.e., 75%).
# 
# Les règles obtenues sont stockées dans un DataFrame. Pour chaque règle, nous avons l’antécédent, le conséquent, le support de la règle, la confiance, le lift, le leverage et la conviction. Nous avons aussi le support de l’antécédent et celui du conséquent.

# In[11]:


arules = association_rules(freq_itemsets, metric="confidence", min_threshold=0.7)


# In[12]:


# type du résultat
print(type(arules))


# In[13]:


# nombre de règles générées
print(arules.shape)


# In[14]:


# liste des colonnes
print(arules.columns)


# In[15]:


# affichage des 5 premières règles du résultat
print(arules.iloc[:5,:])


# ### 4. Post-traitement des règles découvertes

# A présent, nous allons trier les règles selon une mesure, filtrer les règles selon une mesure, et sélectionner des règles en fonction de la présence de certains items dans l’antécédent et le conséquent.

# In[16]:


# pour un affichage plus lisible
pd.set_option('display.max_columns', 6)
pd.set_option('display.max_rows', 10)
pd.set_option('display.precision', 3)


# In[17]:


# sélection des colonnes à afficher
my_rules = arules.loc[:,['antecedents', 'consequents', 'lift', 'conviction']]
print(my_rules.shape)


# In[19]:


# affichage des 10 premières règles
print(my_rules[:10])


# In[20]:


# affichage des règles avec un lift supérieur ou égal à 7
print(my_rules[my_rules['lift'].ge(7.0)])


# In[21]:


# tri des règles selon le lift (ordre décroissant) et affichage des 10 meilleures règles
print(my_rules.sort_values(by='lift', ascending=False)[:10])


# In[22]:


# affichage des règles contenant 'Eggs' dans le conséquent
print(my_rules[my_rules['consequents'].ge({'Eggs'})])


# In[23]:


# affichage des règles où le conséquent est exactement 'Eggs'
print(my_rules[my_rules['consequents'].eq({'Eggs'})])


# In[24]:


# idem mais en triant selon le lift (ordre décroissant)
print(my_rules[my_rules['consequents'].eq({'Eggs'})].sort_values(by='lift', ascending=False))


# In[25]:


# affichage des règles avec '2pct_Milk' contenu dans l’antécédent et 'Eggs' correspondant au conséquent
print(my_rules[my_rules['antecedents'].ge({'2pct_Milk'}) & my_rules['consequents'].eq({'Eggs'})]
      .sort_values(by='lift', ascending=False))


# ### 5. À vous de jouer

# Les règles que nous avons ne sont pas vraiment très intéressantes. La valeur du support minimum est peut-être trop élevée.
# 
# Déterminez les règles d’association avec cette fois minsup=0,015 et minconf=0,7 (la cardinalité max reste fixée à 4). On a alors 4 759 motifs et 3 265 règles.
# 
# Trouvez quelques règles qui vous semblent intéressantes.

# In[26]:


taillemax = 4
freq_itemsets = apriori(dataset, min_support=0.015, max_len=taillemax, use_colnames=True, verbose=0)
print(freq_itemsets.shape)
print(freq_itemsets.head(15))


# In[30]:


arules = association_rules(freq_itemsets, metric="confidence", min_threshold=0.7)
print(arules.shape)


# Il y a beaucoup de règles, essayons avec minconf=0.9 (90%)

# In[35]:


arules = association_rules(freq_itemsets, metric="confidence", min_threshold=0.9)
print(arules.shape)


# In[36]:


print(arules.iloc[:5,:])


# In[40]:


my_rules = arules.loc[:,['antecedents', 'consequents', 'lift', 'conviction']]
print(my_rules.shape)


# In[41]:


pd.set_option('display.max_columns', 6)
pd.set_option('display.max_rows', 10)
pd.set_option('display.precision', 2)

# affichage des 5 premières règles
print(my_rules[:10])


# In[42]:


# affichage des règles avec un LIFT supérieur ou égal à 7
print(my_rules[my_rules['lift'].ge(7.0)])


# In[43]:


# tri des règles selon le lift (ordre décroissant) et affichage des 10 meilleures règles
print(my_rules.sort_values(by='lift', ascending=False)[:10])


# In[44]:


# filtrage des règles contenant 'Aspirin' dans l'antécédent
print(my_rules[my_rules['antecedents'].ge({'Aspirin'})])
print(my_rules[my_rules['antecedents'].ge({'Hamburger_Buns'})])
print(my_rules[my_rules['antecedents'].ge({'Tissues'})])


# In[45]:


print(my_rules[my_rules['conviction'].ge(100000000)].sort_values(by='lift', ascending=False)[:10])


# In[46]:


# conséquents des regles
c = my_rules['consequents']
mon_set = set()
for i in c:
    mon_set.add(i)
print(mon_set)


# In[47]:


itemsconsequents = ['Pepperoni_Pizza_-_Frozen', 'Eggs', 'Tomatoes', 'Cola', 'White_Bread', 'Onions', 
                    '2pct_Milk', 'Wheat_Bread', 'Toothpaste', 'Toilet_Paper', 'Cola', 'Potato_Chips', 
                    'Sugar_Cookies', 'Bananas', 'Sweet_Relish', 'Aspirin', 'Popcorn_Salt', 'Cream_Cheese', 
                    'Hot_Dogs', '98pct_Fat_Free_Hamburger', 'Ramen_Noodles', 'Potatoes']

for item in itemsconsequents:
    regles_select = my_rules[my_rules['consequents'].ge({item})]
    if regles_select.size > 0:
        print("\n", item)
        print(regles_select)


# **Certains items (2pct_Milk, white_Bread, ...) peuvent "poller" les résultats car ils correspondent à des produits achetés couramment. On pourrait filtrer les règles ou les enlever des données avant la découverte des règles.**

# In[48]:


dataset2 = dataset.copy(deep=True)


# In[49]:


dataset2.drop("2pct_Milk", axis=1, inplace=True)
dataset2.drop("White_Bread", axis=1, inplace=True)
dataset2.drop("Wheat_Bread", axis=1, inplace=True)
dataset2.drop("Eggs", axis=1, inplace=True)


# In[50]:


taillemax = 4
freq_itemsets2 = apriori(dataset2, min_support=0.015, max_len=taillemax, use_colnames=True, verbose=0)
print(freq_itemsets2.shape)


# In[51]:


arules2 = association_rules(freq_itemsets2, metric="confidence", min_threshold=0.8)
print(arules2.shape)


# In[52]:


pd.set_option('display.max_rows', 50)
my_rules2 = arules2.loc[:,['antecedents', 'consequents', 'lift']]
print(my_rules2.sort_values(by='lift', ascending=False))


# **Les données proviennent d'un magasin US et sans surprise on retrouve des produits tels que les hot dogs, popcorn, cola, etc. Avec des règles comme "(Cream_Cheese, Hot_Dog_Buns, Hot_Dogs) -> (Sweet_Relish)", nous pouvons suggérer au gérant du magasin de faire une promotion sur la sauce sweet_relish ou de mettre quelques exemplaires proche de cream_cheese ou de hot_dogs. On pourrait aussi avoir une promo sur l'achat de l'ensemble des items présents dans la règle. L'analyse des résultats peut même amener le gérant à réorganiser certains rayons.**

# Remarque finale : ici on a analysé ce qui se vend bien ensemble, mais on pourrait aussi regarder ce qui ce vend moins bien et donc inciter les clients à les acheter via des promotions, par exemple.

# In[ ]:




