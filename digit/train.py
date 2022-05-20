
from tensorflow import keras

def model_construct():
    model = keras.models.load_model('digit/30-epoch-val-acc-9589-lr-1e-3-two-dropout-2e-1-batch-32-adam.h5')
    return model
