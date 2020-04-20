import numpy as np
import time

def tanh(x):
  return np.tanh(x)


dense_w = np.array([[4.4533796310424805], [3.904163122177124], [-4.157683372497559], [-4.126044750213623]], dtype=np.float32)
dense_b = np.array([3.1906535625457764], dtype=np.float32)

input_matrix1 = np.array([[0.3503837287425995, -0.6090512275695801, 0.5120230913162231, 0.618511438369751, 0.34506383538246155, 0.23916944861412048, -0.07810785621404648, -0.5678746700286865]], dtype=np.float32)
recurrent_matrix1 = np.array([[-0.3745907247066498, -0.5406574606895447, 0.6244067549705505, 0.9300629496574402, -0.2923195958137512, 0.3483703136444092, -0.8992422819137573, 0.31768566370010376], [0.29596951603889465, -0.10573689639568329, -0.7591146230697632, -0.01308444980531931, 1.1678930521011353, 0.06139689311385155, 0.5248716473579407, -1.0621553659439087], [0.24065515398979187, -0.8029423952102661, 0.39852994680404663, 0.5287620425224304, -0.9726812243461609, -0.430145263671875, -0.11637792736291885, 0.8627297878265381], [0.5485591292381287, -0.3551076650619507, 0.15364575386047363, 0.21012282371520996, -0.5168384313583374, 0.13495934009552002, -0.8835782408714294, 1.5462497472763062], [-0.2856665253639221, 0.37245044112205505, 0.21260793507099152, -0.3344860076904297, 0.1565718799829483, 0.36164578795433044, 0.05231143534183502, -0.4039258658885956], [0.12475862354040146, 0.1951674371957779, -0.38808175921440125, 0.2826586663722992, 0.04580866917967796, -0.1489139348268509, -0.42163556814193726, 0.004179258830845356], [-0.21753013134002686, 0.7318369746208191, -0.3762476146221161, -0.41087496280670166, -0.07026743143796921, 0.6826944351196289, 0.36899399757385254, -0.878793478012085], [-0.12458813190460205, -0.24330154061317444, -0.6546486616134644, -0.34079673886299133, 0.1608840376138687, 0.2018812894821167, 0.23624727129936218, -0.3515665531158447]], dtype=np.float32)
bias1 = np.array([0.05364954099059105, -0.2579916715621948, 0.06247323751449585, 0.6673364043235779, -0.7193581461906433, -0.1874137967824936, -0.4030403196811676, 1.2123667001724243], dtype=np.float32)

input_matrix2 = np.array([[0.4873669147491455, 0.41480952501296997, -0.8977516889572144, -0.8705614805221558], [0.3373301029205322, 0.48836269974708557, -0.25056594610214233, 0.16897304356098175], [0.32809025049209595, 0.8274158835411072, -0.3582465946674347, 0.06990647315979004], [-0.21945013105869293, 0.576094925403595, -0.46845805644989014, -0.14289359748363495], [0.2582559883594513, 0.3844425678253174, 0.2517955005168915, -1.1658083200454712], [0.8531469106674194, 0.9179336428642273, -0.7450319528579712, -0.22708064317703247], [-0.020663416013121605, -0.028180036693811417, 0.44087332487106323, 0.08955733478069305], [-1.2382841110229492, -0.8017340898513794, -0.017240477725863457, 0.8461002111434937]], dtype=np.float32)
recurrent_matrix2 = np.array([[-0.32943886518478394, 0.1107330471277237, -0.35135456919670105, -0.31046533584594727], [0.34380581974983215, -0.09856705367565155, 0.14202503859996796, 0.12441567331552505], [-0.6463932991027832, -0.27018052339553833, 1.2152642011642456, 0.586061418056488], [-0.12334558367729187, 0.05459415912628174, 0.42127448320388794, -0.30222004652023315]], dtype=np.float32)
bias2 = np.array([0.19217738509178162, 0.1740526258945465, -0.3403782248497009, -0.3945063352584839], dtype=np.float32)

sample = np.array([[10], [10], [10], [10], [2]], dtype=np.float32)

t = time.time()

states = [np.zeros(input_matrix1.shape[1], dtype=np.float32)]
for step in range(sample.shape[0]):
  states.append(np.tanh(np.dot(sample[step], input_matrix1) + np.dot(states[-1], recurrent_matrix1) + bias1))
states = states[1:]  # remove first zero state

new_states = [np.zeros(input_matrix2.shape[1], dtype=np.float32)]
for step in range(sample.shape[0]):
  new_states.append(np.tanh(np.dot(new_states[-1], recurrent_matrix2) + np.dot(states[step], input_matrix2) + bias2))


l0 = np.dot(new_states[-1], dense_w) + dense_b
print(f'time: {time.time() - t}s')
print(f'prediction: {l0.tolist()[0]}')
