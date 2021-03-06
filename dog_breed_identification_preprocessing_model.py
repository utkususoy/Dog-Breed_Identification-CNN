# -*- coding: utf-8 -*-
"""newModel.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1I48iKLxMaJBzFFGvQtWCTcvtfaRpaMGO
"""

import tensorflow.keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout, Flatten, Conv2D, MaxPooling2D, BatchNormalization
import numpy as np
from keras.layers import GlobalAveragePooling2D, Dense, Dropout, BatchNormalization, Flatten, MaxPooling2D, Activation
from keras.optimizers import Adam, SGD, RMSprop, adadelta
from keras.models import Sequential, Model
from keras.applications.xception import Xception
from keras.applications.inception_v3 import InceptionV3
from keras.utils import np_utils
from keras.models import model_from_json

train_inception_v3 = np.load('../stanford_dataSet/data/train_inception_v3_300.npy')

valid_inception_v3 = np.load('../stanford_dataSet/data/valid_inception_v3_300.npy')

from keras.preprocessing.image import ImageDataGenerator
print(train_inception_v3.shape)
valid_inception_v3.shape

input_size = 300
batch_size = 16

train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        rotation_range=30,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True)

valid_datagen = ImageDataGenerator(rescale=1./255)

test_datagen = ImageDataGenerator(rescale=1./255)

train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        rotation_range=30,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True)


train_generator = train_datagen.flow_from_directory(
    directory="../stanford_dataSet/data/train/breed/",
    target_size=(input_size, input_size),
    color_mode="rgb",
    batch_size=batch_size,
    class_mode="categorical",
    shuffle=False,
    seed=42
)

valid_generator = valid_datagen.flow_from_directory(
    directory="../stanford_dataSet/data/valid/breed/",
    target_size=(input_size, input_size),
    color_mode="rgb",
    batch_size=batch_size,
    class_mode="categorical",
    shuffle=False,
    seed=42
)

test_generator = test_datagen.flow_from_directory(
    directory="../stanford_dataSet/data/test2/",
    target_size=(input_size, input_size),
    color_mode="rgb",
    batch_size=batch_size,
    class_mode="categorical",
    shuffle=False,
    seed=42
)

y_train = train_generator.classes
y_valid = valid_generator.classes
y_train = np_utils.to_categorical(y_train)
y_valid = np_utils.to_categorical(y_valid)

model = Sequential()
model.add(GlobalAveragePooling2D(input_shape=train_inception_v3.shape[1:]))
model.add(Dense(256))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(120, activation = 'softmax'))

from keras.models import model_from_json
json_file = open('../stanford_dataSet/data/model_inception_v3.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

loaded_model.load_weights("../stanford_dataSet/data/model_inception_v3.h5")
print("Loaded model from disk")

optimizer = RMSprop(lr = 0.0001, rho = 0.99)
model.compile(optimizer = optimizer, loss = 'categorical_crossentropy', metrics = ['accuracy'])

# Fit model with images

history = model.fit(train_inception_v3, y_train, epochs=20, batch_size=batch_size, validation_data = (valid_inception_v3, y_valid))

from sklearn.datasets import load_files       
from keras.utils import np_utils
import numpy as np
from glob import glob
import pandas as pd
import shutil, os, glob

# define function to load train, test, and validation datasets
def load_dataset(path):
    data = load_files(path)
    dog_files = np.array(data['filenames'])
    dog_targets = np_utils.to_categorical(np.array(data['target']), 133)
    return dog_files, dog_targets

# load train, test, and validation datasets
train_files, train_targets = load_dataset('../stanford_dataSet/data/train/breed')
valid_files, valid_targets = load_dataset('../stanford_dataSet/data/valid/breed')
test_files, test_targets = load_dataset('../stanford_dataSet/data/test2')

# print statistics about the dataset

print('There are %s total dog images.\n' % len(np.hstack([train_files, valid_files, test_files])))
print('There are %d training dog images.' % len(train_files))
print('There are %d validation dog images.' % len(valid_files))
print('There are %d test dog images.'% len(test_files))

test_inception = np.load('../stanford_dataSet/data/test_inception_v3_300.npy')

# get index of predicted dog breed for each image in test set
InceptionV3_predictions = [np.argmax(loaded_model.predict(np.expand_dims(feature, axis=0))) for feature in train_inception_v3]

# report test accuracy
test_accuracy = 100*np.sum(np.array(InceptionV3_predictions)==np.argmax(train_targets, axis=1))/len(InceptionV3_predictions)
print('Test accuracy: %.4f%%' % test_accuracy)

score = model.evaluate(valid_inception_v3, y_valid, verbose=0)
print('\nKeras CNN #2 - accuracy:', score[1], '\n')

prediction = loaded_model.predict(test_inception, verbose=1)

# Commented out IPython magic to ensure Python compatibility.
from sklearn.metrics import classification_report
# %matplotlib inline
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
from itertools import product

map_characters = {0:'none',1:'affenpinscher',2:'afghan_hound',3:'african_hunting_dog',
4:'airedale',5:'american_staffordshire_terrier',6:'appenzeller',7:'australian_terrier',
8:'basenji',9:'basset',10:'beagle',11:'bedlington_terrier',12:'bernese_mountain_dog',
13:'black-and-tan_coonhound',14:'blenheim_spaniel',15:'bloodhound',16:'bluetick',
17:'border_collie',18:'border_terrier',19:'borzoi',20:'boston_bull',21:'bouvier_des_flandres',
22:'boxer',23:'brabancon_griffon',24:'briard',25:'brittany_spaniel',26:'bull_mastiff',
27:'cairn',28:'cardigan',29:'chesapeake_bay_retriever',30:'chihuahua',31:'chow',
32:'clumber',33:'cocker_spaniel',34:'collie',35:'curly-coated_retriever',36:'dandie_dinmont',
37:'dhole',38:'dingo',39:'doberman',40:'english_foxhound',41:'english_setter',
42:'english_springer',43:'entlebucher',44:'eskimo_dog',45:'flat-coated_retriever',
46:'french_bulldog',47:'german_shepherd',48:'german_short-haired_pointer',49:'giant_schnauzer',
50:'golden_retriever',51:'gordon_setter',52:'great_dane',53:'great_pyrenees',
54:'greater_swiss_mountain_dog',55:'groenendael',56:'ibizan_hound',57:'irish_setter',
58:'irish_terrier',59:'irish_water_spaniel',60:'irish_wolfhound',61:'italian_greyhound',
62:'japanese_spaniel',63:'keeshond',64:'kelpie',65:'kerry_blue_terrier',66:'komondor',
67:'kuvasz',68:'labrador_retriever',69:'lakeland_terrier',70:'leonberg',71:'lhasa',72:'malamute',
73:'malinois',74:'maltese_dog',75:'mexican_hairless',76:'miniature_pinscher',77:'miniature_poodle',
78:'miniature_schnauzer',79:'newfoundland',80:'norfolk_terrier',81:'norwegian_elkhound',
82:'norwich_terrier',83:'old_english_sheepdog',84:'otterhound',85:'papillon',86:'pekinese',
87:'pembroke',88:'pomeranian',89:'pug',90:'redbone',91:'rhodesian_ridgeback',92:'rottweiler',
93:'saint_bernard',94:'saluki',95:'samoyed',96:'schipperke',97:'scotch_terrier',98:'scottish_deerhound',
99:'sealyham_terrier',100:'shetland_sheepdog',101:'shih-tzu',102:'siberian_husky',103:'silky_terrier',
104:'soft-coated_wheaten_terrier',105:'staffordshire_bullterrier',106:'standard_poodle',
107:'standard_schnauzer',108:'sussex_spaniel',109:'tibetan_mastiff',110:'tibetan_terrier',111:'toy_poodle',
112:'toy_terrier',113:'vizsla',114:'walker_hound',115:'weimaraner',116:'welsh_springer_spaniel',
117:'west_highland_white_terrier',118:'whippet',119:'wire-haired_fox_terrier',120:'yorkshire_terrier'}

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.figure(figsize = (30,30))
    #plt.figure(figsize = (15,15))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=90)
    plt.yticks(tick_marks, classes)
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    thresh = cm.max() / 2.
    for i, j in product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def plotKerasLearningCurve():
    plt.figure(figsize=(20,10))
    metrics = history.history
    filt = ['acc'] # try to add 'loss' to see the loss learning curve
    for k in filter(lambda x : np.any([kk in x for kk in filt]), metrics.keys()):
        l = np.array(metrics[k])
        plt.plot(l, c= 'r' if 'val' not in k else 'b', label='val' if 'val' in k else 'train')
        x = np.argmin(l) if 'loss' in k else np.argmax(l)
        y = l[x]
        plt.scatter(x,y, lw=0, alpha=0.25, s=100, c='r' if 'val' not in k else 'b')
        plt.text(x, y, '{} = {:.4f}'.format(x,y), size='15', color= 'r' if 'val' not in k else 'b')   
    plt.legend(loc=4)
    plt.axis([0, None, None, None]);
    plt.xlabel('Number of epochs')
    plt.grid()
    
    plt.show()
    
y_pred = model.predict(valid_inception_v3)
print('\n', classification_report(np.where(y_valid > 0)[1], np.argmax(y_pred, axis=1), target_names=list(map_characters.values())), sep='') 
Y_pred_classes = np.argmax(y_pred,axis = 1) 
Y_true = np.argmax(y_pred,axis = 1) 
confusion_mtx = confusion_matrix(Y_true, Y_pred_classes) 
plotKerasLearningCurve()

plot_confusion_matrix(confusion_mtx, classes = list(map_characters.values()))
plt.show()

import matplotlib.pyplot as plt
import numpy

print(history.history.keys())

# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()