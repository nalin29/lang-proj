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
        self.embedder = nn.Conv2d(64, embedding_dim, kernel_size=1, stride=1, padding=0)
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = self.embedder(x)
        return x

