from utilities.slim_network import Network
from utilities.cleaner import clear_temp_folder

clear_temp_folder()

slim_net = Network('vgg_16') #InceptionV1 or vgg_16
#slim_net.predict()
#slim_net.print_layers()
slim_net.deep_taylor()
