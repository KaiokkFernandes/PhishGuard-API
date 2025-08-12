import re
import pickle
import numpy as np
import pandas as pd
from urllib.parse import urlparse
import whois
import requests
from typing import Dict, Tuple
import os
from pathlib import Path

class PhishingPredictor:
    def __init__(self):
        self.model = None
        self.feature_names = [
            'url_length', 'num_dots', 'num_subdomains', 'has_ip',
            'has_suspicious_words', 'num_suspicious_chars', 'domain_age',
            'has_https', 'url_depth', 'num_params'
        ]
        self.load_model()
    
    def load_model(self):
        """Carrega o modelo de machine learning"""
        try:
            model_path = Path(__file__).parent.parent.parent / "ml_model" / "phishing_classifier_model.pkl"
            if model_path.exists():
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                print("Modelo carregado com sucesso!")
            else:
                print("Modelo não encontrado. Usando modelo mock para demonstração.")
                self.model = self._create_mock_model()
        except Exception as e:
            print(f"Erro ao carregar modelo: {e}")
            self.model = self._create_mock_model()
    
    def _create_mock_model(self):
        """Cria um modelo mock para demonstração"""
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        # Dados dummy para treinar o modelo mock
        X_dummy = np.random.rand(1000, len(self.feature_names))
        y_dummy = np.random.randint(0, 2, 1000)
        model.fit(X_dummy, y_dummy)
        return model
    
    def extract_features(self, url: str) -> Dict[str, float]:
        """Extrai características da URL para análise"""
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            
            features = {
                'url_length': len(url),
                'num_dots': url.count('.'),
                'num_subdomains': len(domain.split('.')) - 2 if domain else 0,
                'has_ip': self._has_ip_address(domain),
                'has_suspicious_words': self._has_suspicious_words(url),
                'num_suspicious_chars': self._count_suspicious_chars(url),
                'domain_age': self._get_domain_age(domain),
                'has_https': 1 if parsed_url.scheme == 'https' else 0,
                'url_depth': len([x for x in parsed_url.path.split('/') if x]),
                'num_params': len(parsed_url.query.split('&')) if parsed_url.query else 0
            }
            
            return features
            
        except Exception as e:
            print(f"Erro ao extrair características: {e}")
            return {feature: 0 for feature in self.feature_names}
    
    def _has_ip_address(self, domain: str) -> float:
        """Verifica se o domínio contém endereço IP"""
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        return 1.0 if re.search(ip_pattern, domain) else 0.0
    
    def _has_suspicious_words(self, url: str) -> float:
        """Verifica palavras suspeitas na URL"""
        suspicious_words = [
            'login', 'secure', 'account', 'update', 'verify', 'bank',
            'paypal', 'amazon', 'microsoft', 'apple', 'google',
            'facebook', 'instagram', 'twitter', 'linkedin'
        ]
        url_lower = url.lower()
        count = sum(1 for word in suspicious_words if word in url_lower)
        return min(count / 3.0, 1.0)  # Normaliza para 0-1
    
    def _count_suspicious_chars(self, url: str) -> float:
        """Conta caracteres suspeitos na URL"""
        suspicious_chars = ['-', '_', '?', '=', '&', '%']
        count = sum(url.count(char) for char in suspicious_chars)
        return min(count / 10.0, 1.0)  # Normaliza para 0-1
    
    def _get_domain_age(self, domain: str) -> float:
        """Obtém a idade do domínio (simplificado)"""
        try:
            # Em produção, você usaria whois para obter a idade real
            # Por enquanto, retorna um valor mock baseado no comprimento do domínio
            return min(len(domain) / 20.0, 1.0)
        except:
            return 0.5  # Valor neutro se não conseguir obter
    
    def predict(self, url: str) -> Tuple[bool, float, str, Dict]:
        """Faz a predição se a URL é phishing"""
        try:
            # Extrai características
            features = self.extract_features(url)
            
            # Prepara dados para o modelo
            feature_vector = np.array([features[name] for name in self.feature_names]).reshape(1, -1)
            
            # Faz a predição
            if self.model is not None:
                prediction = self.model.predict(feature_vector)[0]
                confidence = self.model.predict_proba(feature_vector)[0].max()
            else:
                # Fallback: análise baseada em regras simples
                prediction, confidence = self._rule_based_prediction(features)
            
            is_phishing = bool(prediction)
            
            # Determina nível de risco
            if confidence >= 0.8:
                risk_level = "Alto" if is_phishing else "Baixo"
            elif confidence >= 0.6:
                risk_level = "Médio"
            else:
                risk_level = "Incerto"
            
            return is_phishing, float(confidence), risk_level, features
            
        except Exception as e:
            print(f"Erro na predição: {e}")
            return False, 0.5, "Incerto", {}
    
    def _rule_based_prediction(self, features: Dict) -> Tuple[int, float]:
        """Predição baseada em regras quando modelo não está disponível"""
        score = 0
        
        # Regras simples
        if features.get('has_ip', 0) > 0:
            score += 0.3
        if features.get('has_suspicious_words', 0) > 0.5:
            score += 0.2
        if features.get('url_length', 0) > 100:
            score += 0.1
        if features.get('has_https', 0) == 0:
            score += 0.1
        if features.get('num_suspicious_chars', 0) > 0.5:
            score += 0.2
        
        prediction = 1 if score > 0.5 else 0
        confidence = min(abs(score - 0.5) * 2, 0.95)
        
        return prediction, confidence