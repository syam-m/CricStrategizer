import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from keras.models import Sequential
from keras.layers import Embedding, Dense, Flatten
from keras.optimizers import Adam
from keras.utils import to_categorical

def train_test_split_data(player_df):
    player_df1 = player_df.loc[:, ['pitchtype', 'bowlerhand', 'bowlertype', 'balllength', 'ballline', 'ballspeed', 'ballswing/spin', 'stageofgame', 'boundary_size', 'result_n']]
    X = player_df1.drop('result_n', axis=1)
    y = player_df1['result_n']
    encoder = OrdinalEncoder()
    X_encoded = encoder.fit_transform(X)
    return train_test_split(X_encoded, y, test_size=0.2, random_state=42)

def train_random_forest(X_train, X_test, y_train, y_test):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model.predict(X_test)

def train_svm(X_train, X_test, y_train, y_test):
    clf = SVC(kernel='rbf', C=1, gamma='auto')
    clf.fit(X_train, y_train)
    return clf.predict(X_test)

def train_neural_network(X_train, X_test, y_train, y_test):
    model = Sequential()
    model.add(Embedding(input_dim=X_train.shape[1], output_dim=10, input_length=X_train.shape[1]))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(len(set(y_train)), activation='softmax'))  # assuming y_train contains integer labels
    model.compile(optimizer=Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.1, verbose=0)
    return model.predict(X_test)

def evaluate_model(y_true, y_pred):
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='weighted')
    recall = recall_score(y_true, y_pred, average='weighted')
    f1 = f1_score(y_true, y_pred, average='weighted')
    return accuracy, precision, recall, f1

def main():
    player_df = pd.read_csv("~/golddata.csv")

    # Random Forest
    X_train_rf, X_test_rf, y_train_rf, y_test_rf = train_test_split_data(player_df)
    y_pred_rf = train_random_forest(X_train_rf, X_test_rf, y_train_rf, y_test_rf)
    accuracy_rf, precision_rf, recall_rf, f1_rf = evaluate_model(y_test_rf, y_pred_rf)
    print("Random Forest Metrics:")
    print("Accuracy:", accuracy_rf)
    print("Precision:", precision_rf)
    print("Recall:", recall_rf)
    print("F1-score:", f1_rf)

    # SVM
    X_train_svm, X_test_svm, y_train_svm, y_test_svm = train_test_split_data(player_df)
    y_pred_svm = train_svm(X_train_svm, X_test_svm, y_train_svm, y_test_svm)
    accuracy_svm, precision_svm, recall_svm, f1_svm = evaluate_model(y_test_svm, y_pred_svm)
    print("\nSVM Metrics:")
    print("Accuracy:", accuracy_svm)
    print("Precision:", precision_svm)
    print("Recall:", recall_svm)
    print("F1-score:", f1_svm)

    # Neural Network
    X_train_nn, X_test_nn, y_train_nn, y_test_nn = train_test_split_data(player_df)
    y_pred_nn = train_neural_network(X_train_nn, X_test_nn, y_train_nn, y_test_nn)
    accuracy_nn, precision_nn, recall_nn, f1_nn = evaluate_model(y_test_nn, y_pred_nn.argmax(axis=-1))
    print("\nNeural Network Metrics:")
    print("Accuracy:", accuracy_nn)
    print("Precision:", precision_nn)
    print("Recall:", recall_nn)
    print("F1-score:", f1_nn)

if __name__ == "__main__":
    main()
