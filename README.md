# CSE327 Final Project
This is the repository of my final project for CSE 327. It contains the Spikformer and ResNet18 model codes that I've used to conduct my experiments, and my own custom dataset scraped using Google Maps API that is compressed in a .zip file.

## References
**The [Spikformer](https://github.com/ZK-Zhou/spikformer) model was created by Zhaokun Zhou and others. Check the reference below for more information.**  
  
Zhaokun Zhou, Yuesheng Zhu, Chao He, Yaowei Wang, Shuicheng Yan, Yonghong Tian, and Li Yuan.  
Spikformer: When Spiking Neural Network Meets Transformer.  
The Eleventh International Conference on Learning Representations (ICLR), 2023.  
https://openreview.net/forum?id=frE4fUwz_h  

## How to train the Spikformer
1. Unzip the dataset file (my_dataset.zip) into the root folder.
2. Make sure these python libraries are installed:
    - timm==0.5.4
    - cupy==10.3.1
    - pytorch==1.10.0+cu111
    - spikingjelly==0.0.0.0.12
    - pyyaml
3. Go to the /Spikformer directory, then run ```python train.py```

## How to train ResNet18
1. Unzip the dataset file (my_dataset.zip) into the root folder.
2. Make sure these python libraries are installed:
    - pytorch
    - torchvision
3. Go to the /ResNet18 directory, then run ```python train.py```

## How to run the streetview scraper
1. Create a project on Google Cloud Console, then generate an API key and signing secret for Google Maps Street View Static API.
2. Copy the API key and signing secret into the constant variables: ```API_KEY``` and ```SIGNING_SECRET``` respectively.
3. Run ```python scraper.py```
