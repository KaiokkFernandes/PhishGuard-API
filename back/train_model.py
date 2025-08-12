import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import pickle
from pathlib import Path

def create_sample_dataset():
    """Cria um dataset de exemplo para treinamento"""
    np.random.seed(42)
    
    # Gerar dados sintéticos para demonstração
    n_samples = 5000
    
    # URLs legítimas (label = 0)
    legitimate_data = []
    for i in range(n_samples // 2):
        url_length = np.random.normal(30, 10)
        num_dots = np.random.poisson(2)
        num_subdomains = np.random.poisson(1)
        has_ip = 0 if np.random.random() > 0.05 else 1
        has_suspicious_words = np.random.exponential(0.1)
        num_suspicious_chars = np.random.exponential(0.1)
        domain_age = np.random.uniform(0.5, 1.0)
        has_https = 1 if np.random.random() > 0.3 else 0
        url_depth = np.random.poisson(2)
        num_params = np.random.poisson(1)
        
        legitimate_data.append([
            max(10, url_length), min(5, num_dots), min(3, num_subdomains),
            has_ip, min(1, has_suspicious_words), min(1, num_suspicious_chars),
            domain_age, has_https, min(10, url_depth), min(10, num_params), 0
        ])
    
    # URLs de phishing (label = 1)
    phishing_data = []
    for i in range(n_samples // 2):
        url_length = np.random.normal(80, 20)
        num_dots = np.random.poisson(4)
        num_subdomains = np.random.poisson(3)
        has_ip = 1 if np.random.random() > 0.3 else 0
        has_suspicious_words = np.random.uniform(0.3, 1.0)
        num_suspicious_chars = np.random.uniform(0.4, 1.0)
        domain_age = np.random.uniform(0.0, 0.3)
        has_https = 0 if np.random.random() > 0.7 else 1
        url_depth = np.random.poisson(5)
        num_params = np.random.poisson(3)
        
        phishing_data.append([
            max(20, url_length), min(10, num_dots), min(8, num_subdomains),
            has_ip, min(1, has_suspicious_words), min(1, num_suspicious_chars),
            domain_age, has_https, min(15, url_depth), min(15, num_params), 1
        ])
    
    # Combinar dados
    all_data = legitimate_data + phishing_data
    
    # Criar DataFrame
    columns = [
        'url_length', 'num_dots', 'num_subdomains', 'has_ip',
        'has_suspicious_words', 'num_suspicious_chars', 'domain_age',
        'has_https', 'url_depth', 'num_params', 'is_phishing'
    ]
    
    df = pd.DataFrame(all_data, columns=columns)
    return df

def train_model():
    """Treina o modelo de detecção de phishing"""
    print("Criando dataset de exemplo...")
    df = create_sample_dataset()
    
    # Separar features e target
    feature_columns = [
        'url_length', 'num_dots', 'num_subdomains', 'has_ip',
        'has_suspicious_words', 'num_suspicious_chars', 'domain_age',
        'has_https', 'url_depth', 'num_params'
    ]
    
    X = df[feature_columns]
    y = df['is_phishing']
    
    # Dividir em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("Treinando modelo Random Forest...")
    # Treinar modelo
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight='balanced'
    )
    
    model.fit(X_train, y_train)
    
    # Avaliar modelo
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Acurácia do modelo: {accuracy:.4f}")
    print("\nRelatório de classificação:")
    print(classification_report(y_test, y_pred))
    
    # Salvar modelo
    model_dir = Path(__file__).parent / "ml_model"
    model_dir.mkdir(exist_ok=True)
    
    model_path = model_dir / "phishing_classifier_model.pkl"
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"Modelo salvo em: {model_path}")
    
    # Importâncias das features
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nImportância das features:")
    print(feature_importance)
    
    return model

if __name__ == "__main__":
    train_model()
