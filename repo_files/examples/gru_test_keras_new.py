import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from repo_utils.BASEDIR import BASEDIR
import os
from tensorflow.python.keras import backend as K

os.chdir(BASEDIR)
model = load_model('{}/repo_files/examples/gru_model.h5'.format(BASEDIR))


def tanh(x):
  return np.tanh(x)

def sigmoid(x):
  return 1 / (1 + np.exp(-x))


dense_w = np.array(model.layers[1].get_weights()[0])
dense_b = np.array(model.layers[1].get_weights()[1])

input_kernel = np.array(model.layers[0].get_weights()[0])
recurrent_kernel = np.array(model.layers[0].get_weights()[1])
bias = np.array(model.layers[0].get_weights()[2])
input_bias, recurrent_bias = tf.unstack(tf.convert_to_tensor(bias))

sample = np.array([[4, 4], [2.5, 1], [2, 2], [4, 4]])
x_e = sample
units = 4
reset_after = True

Hts = [np.zeros(4)]
outputs = []
for t in range(len(sample)):
  print(t)
  matrix_x = np.dot(sample[t], input_kernel)
  matrix_x += input_bias

  x_z, x_r, x_h = np.split(matrix_x, 3, axis=-1)

  matrix_inner = np.dot(Hts[-1], recurrent_kernel)
  matrix_inner += recurrent_bias

  # if reset_after:
  #   matrix_inner = np.dot(Hts[-1], recurrent_kernel)
  #   matrix_inner = matrix_inner + recurrent_bias
  # else:
  #   matrix_inner = np.dot(Hts[-1], recurrent_kernel[:, :2 * units])

  recurrent_z, recurrent_r, recurrent_h = np.split(matrix_inner.numpy(), 3, axis=-1)

  z = sigmoid(x_z + recurrent_z)
  r = sigmoid(x_r + recurrent_r)
  hh = tanh(x_h + r * recurrent_h)

  h = z * Hts[-1] + (1 - z) * hh
  # Y = np.dot(h, W_hq) + b_q
  Hts.append(h)
  # Y = np.dot(h, W_hq) + b_q
  # l0 = np.dot(h.numpy(), dense_w) + dense_b
  # print(l0.tolist())


l0 = np.dot(Hts[-1], dense_w) + dense_b
print(l0.tolist())


# l0 = np.dot(outputs, dense_w) + dense_b
# print(l0.tolist())



# for t in range(len(sample)):
#   print(t)
#   Rt = np.dot(sample[t], input_kernel)
#   Rt += np.dot(Hts[-1], recurrent_kernel[0])
#   Rt += bias[0]
#   print(Rt.shape)
#
#   Zt = np.dot(sample[t], input_kernel)
#   Zt += np.dot(Hts[-1], recurrent_kernel[1])
#   Zt += bias[1]
#
#   Ht = np.dot(sample[t], input_kernel)
#   Ht += np.dot(Ht * Rt, recurrent_kernel[t]) + bias[0]
#   Ht = tanh(Ht)
#   print(Ht.shape)
#   Ht = Zt * Ht + (1 - Zt) * Ht
#   Y = np.dot(Ht, recurrent_kernel[t]) + bias
#   Hts.append(Ht)
#
#   # add = mulw + mulu + bias
#   # z = np.dot(sample[0], input_kernel)  #  + np.dot(Uz, h) + bz)




# def forward_prop_step(x_t, s_t1_prev):
#   z_t1 = sigmoid(recurrent_kernel[0].dot(x_e) + input_kernel[0].dot(s_t1_prev) + bias[0])
#   r_t1 = sigmoid(recurrent_kernel[1].dot(x_e) + input_kernel[1].dot(s_t1_prev) + bias[1])
#   c_t1 = tanh(recurrent_kernel[2].dot(x_e) + input_kernel[2].dot(s_t1_prev * r_t1) + bias[2])
#   s_t1 = (np.ones_like(z_t1) - z_t1) * c_t1 + z_t1 * s_t1_prev
#
#   # o_t = T.nnet.softmax(V.dot(s_t1) + c)[0]
#
# forward_prop_step(1, np.zeros(4))


# timesteps = sample.shape[0]
# prev_s = np.zeros(4)
# for step in range(timesteps):
#   mulu = np.dot(sample[step], kernel)
#   mulw = np.dot(prev_s, recurrent_kernel)
#   add = mulw + mulu + bias
#   s = np.tanh(add)
#   mulv = np.dot(recurrent_kernel, s)
#   prev_s = np.array(s)
#
# l0 = np.dot(s, dense_w) + dense_b
# print(l0.tolist())


#
# weights = np.transpose(np.concatenate([np.transpose(input_matrix), recurrent_matrix], 1))
#
# gate_inputs = np.concatenate([sample, np.zeros(16)], 1)
# gate_inputs = np.matmul(gate_inputs, weights)
#
#
# gate_inputs = np.bias_add(gate_inputs, bias)
#
# output = tanh(gate_inputs)
# print(output)