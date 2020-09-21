import os  
#os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
#os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import tensorflow as tf
from keras import layers
from keras import models
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator
from keras import backend as K

def auc(y_true, y_pred):
    auc = tf.metrics.auc(y_true, y_pred)[1]
    K.get_session().run(tf.local_variables_initializer())
    return auc

plt.switch_backend('agg')  # 目的使命令行界面不报错

train_dir = 'train'
test_dir = 'test'

rf = '46'  # 感受野

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(256, 256, 3)))
model.add(layers.MaxPool2D((2, 2)))

model.add(layers.Conv2D(32, (3, 3), activation='relu'))
model.add(layers.MaxPool2D((2, 2)))

model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPool2D((2, 2)))

model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPool2D((2, 2)))

model.add(layers.Flatten())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc', auc])


train_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    directory=train_dir,
    target_size=(256, 256),
    batch_size=128,
    class_mode='binary')

test_generator = test_datagen.flow_from_directory(
    directory=test_dir,
    target_size=(256, 256),
    batch_size=128,
    class_mode='binary')

history = model.fit_generator(
    train_generator,
    steps_per_epoch=2000,
    epochs=20,
    validation_data=None,
    validation_steps=None)

model.save('tcga_lihc_small_' + rf + '.h5')

acc = history.history['acc']
#val_acc = history.history['val_acc']
loss = history.history['loss']
#val_loss = history.history['val_loss']
auc = history.history['auc']
#val_auc = history.history['val_auc']

print(history.history)

epochs = range(1, len(acc) + 1)
plt.plot(epochs, acc, 'bo', label='Training acc')
#plt.plot(epochs, val_acc, 'b', label='Test acc')
plt.title('Training and test accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.savefig('acc-cnn-' + rf + '.png')

plt.figure()

plt.plot(epochs, loss, 'bo', label='Training loss')
#plt.plot(epochs, val_loss, 'b', label='Test loss')
plt.title('Training and test loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.savefig('loss-cnn-' + rf + '.png')

plt.figure()

plt.plot(epochs, auc, 'bo', label='Training AUC')
#plt.plot(epochs, val_auc, 'b', label='Test AUC')
plt.title('Training and test AUC')
plt.xlabel('Epoch')
plt.ylabel('AUC')
plt.legend()
plt.savefig('auc-cnn-' + rf + '.png')

# plt.show()


