from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_model(data):
    X = data[['sku', 'discount']]
    y = data['priority']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    joblib.dump(model, 'deal_priority_model.pkl')
    print("Model trained and saved.")

if __name__ == "__main__":
    sample_data = [{'sku': '12345', 'discount': 50, 'priority': 1}, {'sku': '67890', 'discount': 30, 'priority': 0}]
    train_model(sample_data)
