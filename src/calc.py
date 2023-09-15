from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from collections import deque
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

class Calc:
    def __init__(self):
        self.data = deque(maxlen=20)
        # Adicionando hiperparâmetros iniciais para modelos
        self.models = {
            'random_forest': RandomForestClassifier(n_estimators=50),
            'logistic_regression': LogisticRegression(),
            'svm': SVC(probability=True, kernel='linear')  # Usando um kernel linear
        }
        self.is_trained = {}  # Inicializado como um dicionário vazio
        self.mean_cv_scores = {}

    def add_data(self, line):
        try:
            decoded_line = line
            cor, data, hora, numero = [item.split(":")[1].strip() for item in decoded_line.split(",")]
            new_data = {
                'Cor_do_Evento': cor,
                'Data_do_Evento': data,
                'Hora_do_Evento': hora,
                'Numero_do_Evento': numero
            }
            self.data.append(new_data)
        except Exception as e:
            logging.error(f"Erro ao adicionar dados: {e}")

    def prepare_data(self):
        logging.info("Preparando dados...")
        if len(self.data) < 20:
            return None, None
        df = pd.DataFrame(self.data)
        df['Cor_do_Evento'] = df['Cor_do_Evento'].astype('category').cat.codes
        df['Data_do_Evento'] = pd.to_datetime(df['Data_do_Evento'], dayfirst=True).astype('int64') // 10**9
        
        # Normalizando os dados
        scaler = StandardScaler()
        X = scaler.fit_transform(df.drop('Cor_do_Evento', axis=1))
        
        y = df['Cor_do_Evento']
        return X, y
    
    def train_models(self):
        X, y = self.prepare_data()
        if X is None or y is None:
            logging.warning("Dados insuficientes para treinar os modelos.")
            return

        for name, model in self.models.items():
            cv_scores = cross_val_score(model, X, y, cv=5)
            mean_cv_score = cv_scores.mean()
            self.mean_cv_scores[name] = mean_cv_score
            logging.info(f"Precisão média durante a validação cruzada do {name}: {mean_cv_score * 100:.2f}%")
            
            # Alterando o limite para 80%
            if mean_cv_score > 0.7:
                model.fit(X, y)
                self.is_trained[name] = True
                logging.info(f"Modelo {name} treinado com sucesso.")
            else:
                self.is_trained[name] = False
                logging.info(f"Modelo {name} não alcançou a precisão mínima para ser treinado.")


    def predict_color(self):
        X, _ = self.prepare_data()
        
        # Verificar se os dados estão disponíveis
        if X is None:
            logging.warning("No data available for prediction.")
            return None
        
        last_X = X[-1, :].reshape(1, -1)
         
        votes = {}
        
        # Realizar previsões com todos os modelos treinados
        for name, model in self.models.items():
            if hasattr(model, "classes_"):
                prediction = model.predict(last_X)
                votes[prediction[0]] = votes.get(prediction[0], 0) + 1
            else:
                logging.warning(f"The model {name} is not fitted and will be skipped.")
        
        # Verificar se houve votos
        if not votes:
            logging.warning("No votes from the models.")
            return None
        
        try:
            # Encontrar a classe com a maioria dos votos
            final_prediction = max(votes, key=votes.get)
            
            # Mapear a classe para a cor correspondente
            color_map = {0: 'green', 1: 'red', 2: 'white'}
            
            return {
                'final_color': color_map[final_prediction],
                'votes': votes
            }
        except KeyError:
            logging.error("KeyError: The predicted class is not in color_map.")
            return None
