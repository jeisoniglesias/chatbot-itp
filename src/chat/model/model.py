import torch
import torch.nn as nn
import torch.nn.functional as F


class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes, dropout_rate=0.2):
        super(NeuralNet, self).__init__()
        self.dropout = nn.Dropout(dropout_rate)

        # Definir la arquitectura de la red utilizando nn.Sequential
        self.layers = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.BatchNorm1d(hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.BatchNorm1d(hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, num_classes),
        )

        # Inicialización de pesos usando Kaiming
        for m in self.layers:
            if isinstance(m, nn.Linear):
                nn.init.kaiming_normal_(m.weight, nonlinearity="relu")
                m.bias.data.fill_(0.01)

    def forward(self, x):
        x = self.dropout(x)
        x = self.layers(x)
        return x


"""

# Ejemplo de uso
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = NeuralNet(input_size=784, hidden_size=128, num_classes=10).to(device)

# Establecer semillas para reproducibilidad
torch.manual_seed(42)
torch.cuda.manual_seed_all(42)

# Datos de ejemplo
data = torch.randn(64, 784).to(device)
output = model(data)
print(output.shape)  # Salida: torch.Size([64, 10])
"""
