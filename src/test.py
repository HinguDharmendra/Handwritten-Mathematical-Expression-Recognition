from inkml import *

file = 'E:/RIT/PR/Project3/TrainINKML/HAMEX/formulaire001-equation009.inkml'
inkml_obj = marshal_inkml(file)
lgfile = file.split('/')[-1].replace('.inkml', '.lg')
lgfile = '../TrainINKML/pd.to_numeric(/'+lgfile
marshal_objects_relations(lgfile, inkml_obj)

print('qkj')