from konverter.utils.model_attributes import Activations, Layers, watermark
from konverter.utils.konverter_support import KonverterSupport
import numpy as np

support = KonverterSupport()


class Konverter:
  def __init__(self, model, output_file, indent_spaces, verbose=True, use_watermark=True):
    """
    :param model: A preloaded Sequential Keras model
    :param output_file: The desired path and name of the output model files
    :param indent_spaces: The number of spaces to use for indentation
    :param use_watermark: To prepend a watermark comment to model wrapper
    """
    self.model = model
    self.output_file = output_file
    self.indent = ' ' * indent_spaces
    self.verbose = verbose
    self.use_watermark = use_watermark

    self.layers = []
    self.start()

  def start(self):
    self.check_model()
    self.get_layers()
    if self.verbose:
      self.print_model_architecture()
    self.remove_unused_layers()
    self.parse_output_file()
    self.build_konverted_model()

  def build_konverted_model(self):
    self.print('\nNow building pure Python + NumPy model...')

    model_builder = {'imports': ['import numpy as np'],
                     'functions': [],
                     'load_weights': [],
                     'model': ['def predict(x):']}

    # add section to load model weights and biases
    model_builder['load_weights'].append(f'wb = np.load(\'{self.output_file}_weights.npz\', allow_pickle=True)')
    model_builder['load_weights'].append('w, b = wb[\'wb\']')

    # builds the model and adds needed activation functions
    for idx, layer in enumerate(self.layers):
      prev_output = 'x' if idx == 0 else f'l{idx - 1}'

      # work on predict function
      if layer.name == Layers.Dense.name:
        model_line = f'l{idx} = {layer.string.format(prev_output, idx, idx)}'
        model_builder['model'].append(model_line)
        if layer.info.has_activation:
          if layer.info.activation.needs_function:
            activation = f'l{idx} = {layer.info.activation.alias.lower()}(l{idx})'
          else:  # eg. tanh or relu
            activation = f'l{idx} = {layer.info.activation.string.lower().format(f"l{idx}")}'
          model_builder['model'].append(activation)

      elif layer.info.is_recurrent:
        rnn_function = f'l{idx} = {layer.alias.lower()}({prev_output}, {idx})'
        if not layer.info.returns_sequences:
          rnn_function += '[-1]'
        model_builder['model'].append(rnn_function)

      # work on functions: activations/simplernn
      if layer.info.activation.string is not None:
        if support.is_function(layer.info.activation.string):  # don't add tanh as a function
          model_builder['functions'].append(layer.info.activation.string)

        if layer.info.is_recurrent:
          model_builder['functions'].append(layer.string)

    model_builder['functions'] = set(model_builder['functions'])  # remove duplicates
    model_builder['model'].append(f'return l{len(self.layers) - 1}')

    self.save_model(model_builder)
    self.output_file = self.output_file.replace('\\', '/')

    self.print('\nSaved Konverted model!')
    self.print(f'Model wrapper: {self.output_file}.py\nWeights and biases file: {self.output_file}_weights.npz')
    self.print('\nMake sure to change the path inside the wrapper file to your weights if you move the file elsewhere.')
    if Activations.Softmax.name in support.model_activations(self.layers):
      self.print('Important: Since you are using Softmax, make sure that predictions are working correctly!')

  def save_model(self, model_builder):
    wb = list(zip(*[[np.array(layer.info.weights), np.array(layer.info.biases)] for layer in self.layers]))
    np.savez_compressed('{}_weights'.format(self.output_file), wb=wb)

    output = ['\n'.join(model_builder['imports']),  # eg. import numpy as np
              '\n'.join(model_builder['load_weights']),  # loads weights and biases for predict()
              '\n\n'.join(model_builder['functions']),  # houses the model helper functions
              '\n\t'.join(model_builder['model'])]  # builds the predict function
    output = '\n\n'.join(output) + '\n'  # now combine all sections

    if self.use_watermark:
      output = watermark + output

    with open(f'{self.output_file}.py', 'w') as f:
      f.write(output.replace('\t', self.indent))

  def remove_unused_layers(self):
    self.layers = [layer for layer in self.layers if layer.name not in support.attrs_without_activations]

  def parse_output_file(self):
    if self.output_file[-3:] == '.py':
      self.output_file = self.output_file[:-3]

  def print_model_architecture(self):
    print('\nSuccessfully got model architecture!\n')
    print('Layers:\n-----')
    to_print = [[f'name: {layer.alias}'] for layer in self.layers]
    for idx, layer in enumerate(self.layers):
      if not layer.info.is_ignored:
        if layer.info.has_activation:
          to_print[idx].append(f'activation: {layer.info.activation.alias}')
        if layer.info.is_recurrent:
          to_print[idx].append(f'shape: {layer.info.weights[0].shape}')
        else:
          to_print[idx].append(f'shape: {layer.info.weights.shape}')

      to_print[idx] = '  ' + '\n  '.join(to_print[idx])
    print('\n-----\n'.join(to_print))

  def get_layers(self):
    for layer in self.model.layers:
      layer = support.get_layer_info(layer)
      if layer.info.supported:
        self.layers.append(layer)
      else:
        raise Exception('Layer `{}` with activation `{}` not currently supported (check type or activation)'.format(layer.name, layer.info.activation.name))

  def check_model(self):
    if str(type(self.model)) != "<class 'tensorflow.python.keras.engine.sequential.Sequential'>":
      raise Exception('Input for `model` must be a Sequential tf.keras model, not {}'.format(type(self.model)))
    elif not support.in_models(self.model.name):
      raise Exception('Model is `{}`, must be in {}'.format(self.model.name, [mdl.name for mdl in support.models]))

  def print(self, msg):
    if self.verbose:
      print(msg)
