# -*- coding: utf-8 -*-
"""Breastcancer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LJnGzT4GGYf4AmB3UQNKiLSzOlLSpEQv
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
# %matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report,confusion_matrix,classification_report,f1_score,roc_curve,ConfusionMatrixDisplay,precision_score,recall_score

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score,roc_curve
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import AdaBoostClassifier

df = pd.read_csv("/content/drive/MyDrive/cancer (1).csv")
df.head()

df.columns

df.shape

df.info()

df.isnull().sum()

df.describe()

df.shape

df=df.drop([ 'id'], axis=1)

df=df.drop([ 'Unnamed: 32'], axis=1)

df

df['diagnosis'].unique()

df['diagnosis'].value_counts()

df['diagnosis'].value_counts().plot(kind='pie',autopct='%0.2F%%',figsize=[5,5],colors=['#228B22','#EE2C2C'],shadow=True)
plt.show()

label_encode=LabelEncoder()
labels=label_encode.fit_transform(df['diagnosis'])
df['t_diagnosis']=labels

df['t_diagnosis'].value_counts()

df['t_diagnosis'].head()

df.drop(columns='diagnosis',axis=1,inplace=True)

df

corr=df.corr()
kot=corr[corr>=.7]
plt.figure(figsize=[15,20])
sns.heatmap(kot,annot=True,cmap='gist_rainbow_r',fmt="0.2f")
plt.show()

plt.figure(figsize=(30,10))
df_corr = df.corr()
res = df_corr['t_diagnosis'][1:]
res1 = res.reset_index()
res1.rename(columns={'index':'parameter','t_diagnosis':'correlation_value'}, inplace = True)
res2 = res1.sort_values(by = 'correlation_value',ascending = True)
colors = ['red' if val < 0 else 'lime' for val in res2['correlation_value']]
ax = sns.barplot(data=res2, x='parameter', y='correlation_value', palette=colors)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha='right')
plt.show()

X=df.drop(columns='t_diagnosis',axis=1)
Y=df['t_diagnosis']

X_train, X_test, Y_train, Y_test = train_test_split( X, Y, test_size=0.20, random_state=4)
print(X.shape,X_train.shape,X_test.shape)

model=SVC(kernel='linear')
model.fit(X_train,Y_train)

test_prediction=model.predict(X_test)
accuracy=accuracy_score(Y_test,test_prediction)
print('Accuracy score of the ', model,'',accuracy)

X_train_prediction=model.predict(X_train)
training_data_accu=accuracy_score(Y_train,X_train_prediction)
print(training_data_accu)

print('Accuracy on Training data:',round(training_data_accu*100,2))

X_test_prediction=model.predict(X_test)
test_data_accu=accuracy_score(Y_test,X_test_prediction)
print(test_data_accu)

confua_matrix=confusion_matrix(Y_test,X_test_prediction)
print(confua_matrix)

tn,fp,fn,tp=confua_matrix.ravel()
print(tn,fp,fn,tp)

plt.figure(figsize=[4,2])
sns.heatmap(confua_matrix,annot=True)
plt.show()

def precision_recall_f1_score(true_labels,pred_labels):
  precision_value= precision_score(true_labels,pred_labels)
  recall_value= recall_score(true_labels,pred_labels)
  f1_score_value=f1_score(true_labels,pred_labels)


  print('precision=',precision_value)
  print('Recall=',recall_value)
  print('F1 Score=',f1_score_value)
precision_recall_f1_score(Y_train,X_train_prediction)

model.fit(X_train,Y_train)
y_pred=model.predict(X_test)
fpr,tpr,thresholds=roc_curve(Y_test,y_pred)
auc=roc_auc_score(Y_test,y_pred)
plt.plot(fpr,tpr,label='RO curve(AU=%0.2f)'%auc)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend(loc='lower right')
plt.show()

X=np.asarray(X)
Y=np.asarray(Y)
model=SVC()
parameters={'kernel':['linear','poly','rbf','sigmoid'],'C':[1,5,10,20]}
classifier=GridSearchCV(model,parameters,cv=5)
classifier.fit(X,Y)
classifier.cv_results_

best_parameters=classifier.best_params_
print(best_parameters)

highest_accu=classifier.best_score_
print(highest_accu)

param_b={'n_estimators':[150,200,250,300],'bootstrap':[True,False],'max_features':[1,2,3,5,10],'max_samples':[15,20,25,30]}
fit_bagging=BaggingClassifier(random_state=1)
cv_bagging=GridSearchCV(fit_bagging,cv=5,param_grid=param_b,n_jobs=-1)
cv_bagging.fit(X_train,Y_train)

cv_bagging.best_params_

bagging=BaggingClassifier(n_estimators=250,max_samples=30,max_features=3)
bagging.fit(X_train,Y_train)
print('Train_accuracy',bagging.score(X_train,Y_train))
print('Test_accuracy',bagging.score(X_test,Y_test))

y_pred_proba=bagging.predict_proba(X_test)[::,1]
model.fit(X_train,Y_train)
y_pred=model.predict(X_test)
fpr,tpr,thresholds=roc_curve(Y_test,y_pred_proba)
auc=roc_auc_score(Y_test,y_pred_proba)
plt.plot(fpr,tpr,label='ROC curve(AUC=%0.2f)'%auc)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend(loc='lower right')
plt.show()

model_report=[]
test_pred_bag=bagging.predict(X_test)
MD=pd.Series({'Model':"Bagging Classifier",
              'ROC Score':metrics.roc_auc_score(Y_test,test_pred_bag),
              'Precision score':metrics.precision_score(Y_test,test_pred_bag),
              'Recall Score':metrics.recall_score(Y_test,test_pred_bag),
              'F1 Score':metrics.f1_score(Y_test,test_pred_bag),
              'Accuracy Score':metrics.accuracy_score(Y_test,test_pred_bag)})
MD

param_ada={'n_estimators':[50,100,150,200],
           'learning_rate':[0.5,0.7,1,1.5,2]}

fit_adaboost=AdaBoostClassifier(random_state=1)
cv_adaboost=GridSearchCV(fit_adaboost,cv=5,param_grid=param_ada,n_jobs=-1)
cv_adaboost.fit(X_test,Y_test)

cv_adaboost.best_params_

ABC=AdaBoostClassifier(n_estimators=150,learning_rate=1.5,random_state=1)
ABC.fit(X_test,Y_test)
print('Train_accuracy',ABC.score(X_train,Y_train))
print('Test_accuracy',ABC.score(X_test,Y_test))

y_pred_proba=ABC.predict_proba(X_test)[::,1]
fpr,tpr,_=metrics.roc_curve(Y_test,y_pred_proba)
auc=metrics.roc_auc_score(Y_test,y_pred_proba)
plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
plt.legend(loc=4)
plt.show()

test_pred_ABC=ABC.predict(X_test)
MD2=pd.Series({'Model':"Adaboost Classifier",
               'ROC Score':metrics.roc_auc_score(Y_test,test_pred_ABC),
               'Precision Score':metrics.precision_score(Y_test,test_pred_ABC),
               'F1 Score':metrics.f1_score(Y_test,test_pred_ABC),
               'Accuracy Score':metrics.accuracy_score(Y_test,test_pred_ABC)})

MD2