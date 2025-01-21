import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


# Wczytanie danych z pliku CSV
def load_data(file_path):
    """Wczytuje dane z pliku CSV"""
    return pd.read_csv(file_path)


# Wczytanie zakresów referencyjnych
def load_reference_ranges(file_path):
    """Wczytuje zakresy referencyjne z pliku CSV"""
    try:
        ref_ranges = pd.read_csv(file_path)
        print("Zakresy referencyjne wczytane pomyślnie:")
        print(ref_ranges)
        return ref_ranges
    except FileNotFoundError:
        print(f"Plik {file_path} nie został znaleziony. Upewnij się, że ścieżka jest poprawna.")
        return None


# Przygotowanie danych do modelu
def prepare_data(df, target_column):
    """Przygotowuje dane do modelu LML"""
    X = df.drop(columns=[target_column])
    y = df[target_column]
    return train_test_split(X, y, test_size=0.2, random_state=42)


# Trening modelu LML
def train_model(X_train, y_train):
    """Trenuje model regresji liniowej"""
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


# Ewaluacja modelu
def evaluate_model(model, X_test, y_test):
    """Ewaluacja modelu za pomocą danych testowych"""
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R^2 Score: {r2:.2f}")
    return y_pred


# Wizualizacja wyników
def plot_results(y_test, y_pred):
    """Generuje wykres porównujący wartości rzeczywiste i przewidywane"""
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.7)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], '--r', linewidth=2)
    plt.title("Porównanie wartości rzeczywistych i przewidywanych")
    plt.xlabel("Wartości rzeczywiste")
    plt.ylabel("Wartości przewidywane")
    plt.show()


# Główna funkcja
def main():
    # Ścieżki do plików
    file_path = "morfologia_5diff.csv"  # Zmień na właściwą ścieżkę
    ref_ranges_path = "zakresy_referencyjne.csv"  # Ścieżka do zakresów referencyjnych

    try:
        # Wczytywanie danych
        df = load_data(file_path)

        # Wczytywanie zakresów referencyjnych
        ref_ranges = load_reference_ranges(ref_ranges_path)

        # Wyświetlenie kilku pierwszych wierszy danych
        print("\nPierwsze wiersze danych:")
        print(df.head())

        # Przygotowanie danych (przewidujemy np. WBC)
        target_column = "WBC"  # Zmień na kolumnę, którą chcesz przewidywać
        X_train, X_test, y_train, y_test = prepare_data(df, target_column)

        # Trening modelu
        model = train_model(X_train, y_train)

        # Ewaluacja modelu
        y_pred = evaluate_model(model, X_test, y_test)

        # Wizualizacja wyników
        plot_results(y_test, y_pred)

    except FileNotFoundError:
        print(f"Plik {file_path} nie został znaleziony. Upewnij się, że ścieżka jest poprawna.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")


if __name__ == "__main__":
    main()
