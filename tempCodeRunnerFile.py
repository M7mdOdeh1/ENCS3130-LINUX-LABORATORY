# Import the necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from sklearn import tree
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('https://www.dropbox.com/s/ltoc6c32xjhy5kl/DiabetesData.csv?dl=1')

# Print the main statistics of each attribute
print(df.describe())

# Print the distribution of the target class
print(df['Diabetic'].value_counts(normalize=True))

# Split the dataset into 70% training and 30% test data
X = df.drop('Diabetic', axis=1)
y = df['Diabetic']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

# Train the model
clf = DecisionTreeClassifier()
clf = clf.fit(X_train, y_train)

# Predict on test data
y_pred = clf.predict(X_test)

# Print the accuracy of the test set
print("Accuracy of model M1:", metrics.accuracy_score(y_test, y_pred))

# Split the data again with a 50-50 split
X_train2, X_test2, y_train2, y_test2 = train_test_split(X, y, test_size=0.5, random_state=1)

# Train a new model on this split
clf2 = DecisionTreeClassifier()
clf2 = clf2.fit(X_train2, y_train2)

# Predict on new test data
y_pred2 = clf2.predict(X_test2)

# Print the accuracy of the new test set
print("Accuracy of model M2:", metrics.accuracy_score(y_test2, y_pred2))

# Plot the decision tree of model M1
fig = plt.figure(figsize=(15,10))
_ = tree.plot_tree(clf, 
                   feature_names=df.columns[:-1],  
                   class_names=['Negative','Positive'],
                   filled=True)

# Plot the decision tree of model M2
fig2 = plt.figure(figsize=(15,10))
_ = tree.plot_tree(clf2, 
                   feature_names=df.columns[:-1],  
                   class_names=['Negative','Positive'],
                   filled=True)
plt.show()


