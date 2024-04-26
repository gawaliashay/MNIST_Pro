# %matplotlib inline
import warnings
warnings.filterwarnings("ignore")

import numpy as np                   # advanced math library
import keras
import matplotlib.pyplot as plt      # MATLAB like plotting routines

from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D, GlobalAveragePooling2D, Flatten
from keras.layers import BatchNormalization

from keras.datasets import mnist     # MNIST dataset is included in Keras
from keras.models import Sequential  # Model type to be used
from keras.layers import Dense, Dropout, Activation # Types of layers to be used in our model
from keras.utils import to_categorical

# The MNIST data is split between 60,000 28 x 28 pixel training images and 10,000 28 x 28 pixel images
(X_train, y_train), (X_test, y_test) = mnist.load_data()

print("X_train shape", X_train.shape)
print("y_train shape", y_train.shape)
print("X_test shape", X_test.shape)
print("y_test shape", y_test.shape)

plt.imshow(X_train[2], cmap='gray')

y_train[2]

# Again, do some formatting
# Except we do not flatten each image into a 784-length vector because we want to perform convolutions first

X_train = X_train.reshape(60000, 28, 28, 1) #add an additional dimension to represent the single-channel
X_test = X_test.reshape(10000, 28, 28, 1)

X_train = X_train.astype('float32')         # change integers to 32-bit floating point numbers
X_test = X_test.astype('float32')

X_train /= 255                              # normalize each value for each pixel for the entire vector for each input
X_test /= 255

print("Training matrix shape", X_train.shape)
print("Testing matrix shape", X_test.shape)

# one-hot format classes

nb_classes = 10 # number of unique digits

y_train = to_categorical(y_train, nb_classes)
y_test = to_categorical(y_test, nb_classes)
print(y_train.shape)
print(y_test.shape)

model = Sequential()                                 # Linear stacking of layers

# Convolution Layer 1
model.add(Conv2D(32, (3, 3), input_shape=(28,28,1))) # 32 different 3x3 kernels -- so 32 feature maps
model.add(BatchNormalization(axis=-1))               # normalize each feature map before activation
convLayer01 = Activation('relu')                     # activation
model.add(convLayer01)

# Convolution Layer 2
model.add(Conv2D(32, (3, 3)))                        # 32 different 3x3 kernels -- so 32 feature maps
model.add(BatchNormalization(axis=-1))               # normalize each feature map before activation
model.add(Activation('relu'))                        # activation
convLayer02 = MaxPooling2D(pool_size=(2,2))          # Pool the max values over a 2x2 kernel
model.add(convLayer02)

# Convolution Layer 3
model.add(Conv2D(64,(3, 3)))                         # 64 different 3x3 kernels -- so 64 feature maps
model.add(BatchNormalization(axis=-1))               # normalize each feature map before activation
convLayer03 = Activation('relu')                     # activation
model.add(convLayer03)

# Convolution Layer 4
model.add(Conv2D(64, (3, 3)))                        # 64 different 3x3 kernels -- so 64 feature maps
model.add(BatchNormalization(axis=-1))               # normalize each feature map before activation
model.add(Activation('relu'))                        # activation
convLayer04 = MaxPooling2D(pool_size=(2,2))          # Pool the max values over a 2x2 kernel
model.add(convLayer04)
model.add(Flatten())                                 # Flatten final 4x4x64 output matrix into a 1024-length vector

# Fully Connected Layer 5
model.add(Dense(512))                                # 512 FCN nodes
model.add(BatchNormalization())                      # normalization
model.add(Activation('relu'))                        # activation

# Fully Connected Layer 6
model.add(Dropout(0.2))                              # 20% dropout of randomly selected nodes
model.add(Dense(10))                                 # final 10 FCN nodes
model.add(Activation('softmax'))                     # softmax activation

model.summary()

# we'll use the same optimizer

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(X_train, y_train,
          steps_per_epoch=60000//120,
          epochs=5,
          verbose=1,
          validation_split=0.2,  # Add validation split here
          validation_steps=10000//120)

plt.imshow(X_train[2], cmap='gray')

(y_train[2])

score = model.evaluate(X_test, y_test)
print('Test score:', score[0])
print('Test accuracy:', score[1])

sample_index = 6  # Change this index to select a different sample
input_image = np.expand_dims(X_test[sample_index], axis=0)  # Adding a batch dimension

# Perform inference
predictions = model.predict(input_image)

# Convert the predicted probabilities to class labels
predicted_class = np.argmax(predictions)

# Print the predicted class
print("Predicted class:", predicted_class)

plt.imshow(X_test[6], cmap='gray')

model.save('mnist_model.keras')

m1 = keras.models.load_model('mnist_model.keras')

sample_index = 6  # Change this index to select a different sample
input_image = np.expand_dims(X_test[sample_index], axis=0)  # Adding a batch dimension

# Perform inference
predictions = m1.predict(input_image)

# Convert the predicted probabilities to class labels
predicted_class = np.argmax(predictions)

# Print the predicted class
print("Predicted class:", predicted_class)

plt.imshow(X_test[11], cmap='gray')