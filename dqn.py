import torch.nn as nn

class DQN(nn.Module):
    """
    Deep Q-Network
    
    Args:
        state_dim (int): Dimension of the state space
        action_dim (int): Dimension of the action space
        
    Attributes:
        fc (nn.Sequential): Fully connected layers
        
    Methods:
        forward(x): Forward pass
    """
    def __init__(self, state_dim, action_dim):
        super(DQN, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, action_dim)
        )

    def forward(self, x):
        """
        Forward pass
        
        Args:
            x (torch.Tensor): Input tensor
        
        Returns:
            torch.Tensor: Output tensor
        """
        return self.fc(x)