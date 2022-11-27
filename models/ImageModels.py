# Author: David Harwath, Wei-Ning Hsu
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as imagemodels
import torch.utils.model_zoo as model_zoo


class Resnet50(imagemodels.ResNet):
    def __init__(self, embedding_dim=1024, pretrained=False):
        super(Resnet50, self).__init__(imagemodels.resnet.Bottleneck, [3, 4, 6, 3])
        if pretrained:
            model_url = imagemodels.resnet.model_urls['resnet50']
            self.load_state_dict(model_zoo.load_url(model_url))
        self.avgpool = None
        self.fc = None
        self.embedder = nn.Conv2d(2048, embedding_dim, kernel_size=1, stride=1, padding=0)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.embedder(x)
        return x

class Resnet18(imagemodels.ResNet):
    def __init__(self, embedding_dim=1024, pretrained= False):
        super(Resnet18, self).__init__(imagemodels.resnet.BasicBlock, [2,2,2,2])
        if pretrained:
            model_url = imagemodels.resnet.model_urls['resnet18']
            self.load_state_dict(model_zoo.load_url(model_url))
        self.avgpool = None
        self.fc = None
        self.embedder = nn.Conv2d(512, embedding_dim, kernel_size=1, stride=1, padding=0)
    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = self.embedder(x)
        return x

class SqueezeNet(imagemodels.SqueezeNet):
    def __init__(self, embedding_dim=1024, pretrained= False):
        super(SqueezeNet, self).__init__(version="1_1")
        if pretrained:
            model_url = imagemodels.squeezenet.model_urls['squeezenet1_1']
            self.load_state_dict(model_zoo.load_url(model_url))
        self.classifier = None
        self.embedder = nn.Conv2d(512, embedding_dim, kernel_size=1, stride=1, padding=0)
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = self.embedder(x)
        return x

class ViT(imagemodels.VisionTransformer):
    def __init__(self, embedding_dim=1024, pretrained= False):

        super(ViT, self).__init__(image_size=224, patch_size=16, num_layers=12, num_heads=12, hidden_dim=768, mlp_dim=3072)
        if pretrained:
            weights = imagemodels.ViT_B_16_Weights(imagemodels.ViT_B_16_Weights.DEFAULT)
            self.load_state_dict(weights.get_state_dict(progress=True))
        self.embedder = nn.Linear(768, embedding_dim)
    def forward(self, x: torch.Tensor):
        x = self._process_input(x)
        n = x.shape[0]

        batch_class_token = self.class_token.expand(n, -1, -1)
        x = torch.cat([batch_class_token, x], dim=1)

        x = self.encoder(x)

        x = x[:, 0]

        x = self.embedder(x)

        return x.view(x.shape[0], 1024, 1, -1)