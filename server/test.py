from utilities.slim_network import Network
from utilities.cleaner import clear_temp_folder

clear_temp_folder()

slim_net = Network('InceptionV1')
#slim_net.predict()
#slim_net.print_layers()
slim_net.deep_taylor()
