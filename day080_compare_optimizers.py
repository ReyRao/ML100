# -*- coding: utf-8 -*-
"""Day080_HW.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zgGGNm0mIk2-rGfTLxsgEX3a4qVbzlOR

# 請結合前面的知識與程式碼，比較不同的 optimizer 與 learning rate 組合對訓練的結果與影響
### 常見的 optimizer 包含
* SGD
* RMSprop
* AdaGrad
* Adam
"""

import os
import keras

# Disable GPU
# os.environ["CUDA_VISIBLE_DEVICES"] = ""

(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()

## 資料前處理
def preproc_x(x, flatten=True):
    x = x / 255.
    if flatten:
        x = x.reshape((len(x), -1))
    return x

def preproc_y(y, num_classes=10):
    if y.shape[-1] == 1:
        y = keras.utils.to_categorical(y, num_classes)
    return y

# Preproc the inputs
x_train = preproc_x(x_train)
x_test = preproc_x(x_test)

# Preprc the outputs
y_train = preproc_y(y_train)
y_test = preproc_y(y_test)

def build_mlp(input_data, output_data, n_neurons=[512, 256, 256, 256, 256, 128]):
    """
    Build your own model
    """
    input_layer = keras.layers.Input([input_data.shape[-1]], name='input_layer')
    for i, n_unit in enumerate(n_neurons):
        if i == 0:
            x = keras.layers.Dense(units=n_unit, activation='relu', name='hidden_layer'+str(i+1))(input_layer)
        else:
            x = keras.layers.Dense(units=n_unit, activation='relu', name='hidden_layer'+str(i+1))(x)
            
    output_layer = keras.layers.Dense(units=output_data.shape[-1], activation='softmax', name='output_layer')(x)
    model = keras.models.Model(inputs=input_layer, outputs=output_layer)
    return model
model = build_mlp(x_train, y_train)
model.summary()

## 超參數設定
"""
Set your required experiment parameters
"""
EPOCHS = 50
BATCH_SIZE = 1024
LR = 0.005
optimizer = keras.optimizers.adam()

results = {}
"""
建立你的訓練與實驗迴圈並蒐集資料
"""
optimizer_type = ['SGD', 'adam', 'adagrad']

for name_optimizer in optimizer_type:
    keras.backend.clear_session()
    print(f'optimizer: {name_optimizer}')
    model = build_mlp(x_train, y_train)
    model.summary()
    optimizer = eval(f'keras.optimizers.{name_optimizer}(lr={LR})')
    print(optimizer)
    model.compile(optimizer=optimizer, loss="categorical_crossentropy", metrics=['accuracy'])
    model.fit(x_train, y_train,
             epochs=EPOCHS,
             batch_size=BATCH_SIZE,
             validation_data=(x_test, y_test),
             shuffle=True)
    
    train_loss = model.history.history['loss']
    valid_loss = model.history.history['val_loss']
    train_acc = model.history.history['acc']
    valid_acc = model.history.history['val_acc']
    
    condition_tag = f'optimizer: {name_optimizer}'
    
    results[condition_tag] = {'train-loss': train_loss,
                              'valid-loss': valid_loss,
                              'train-acc': train_acc,
                              'valid-acc': valid_acc}

import matplotlib.pyplot as plt
# %matplotlib inline

"""
將實驗結果繪出
"""
color_bar = ['r', 'g', 'b', 'y', 'm', 'k']
plt.figure(figsize=(10, 8))
for i, condition in enumerate(results.keys()):
    plt.plot(range(len(results[condition]['train-loss'])), results[condition]['train-loss'], '-', label=condition, color=color_bar[i])
    plt.plot(range(len(results[condition]['valid-loss'])), results[condition]['valid-loss'], '--', label=condition, color=color_bar[i])
plt.title('Loss')
plt.legend()
plt.show()

plt.figure(figsize=(10, 8))
for i, condition in enumerate(results.keys()):
    plt.plot(range(len(results[condition]['train-acc'])), results[condition]['train-acc'], '-', label=condition, color=color_bar[i])
    plt.plot(range(len(results[condition]['valid-acc'])), results[condition]['valid-acc'], '--', label=condition, color=color_bar[i])
plt.title('Accuracy')
plt.legend()
plt.show()