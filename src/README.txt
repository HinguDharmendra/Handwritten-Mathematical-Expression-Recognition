To process one inkml file and obtain predicted label graph (.lg file) for it run main_driver_file.py.
This program takes two arguments. 1st is the location of the inkml file and second is B is file is from Bonus set and T if file is from Testing set.

python main_driver_file <path to inkml file> <B/T>

The output lg file is saved in the same directory with the same name and .lg extension.

All the extracted features are stored in src/features directory.

Training parameters for the two models (Testing set and Bonus set) are present in src/training_parameters directory.

The dataset is split initially using training_testing_split.py and two lists one each for training set and testing set are produced. These lists are saved in text files in the src folder. These files are later used to provide inputs for Detector.py and Segmentor.py.

Detctor.py can be run individually to train Random Forest model in training set. The model is saved in src/training_parameters directory. It is also used by Segmentor.py to obtain scores in the segmentation process.

Segmentor.py can be run individually to obtain predicted outputs for testing set. The output lg files are saved in the same directories as that of the input testing set files. This file is also used my main_driver_file.py to obtain output for a single inkml file.

Detector.py and Segmentor.py if run individually need inkml files to be present in the same directory as src.

The folder structure is as follows:

Project2
...src
......features
......training_parameters
......Detector.py
......Segmentor.py
......main_driver_file.py
...TrainINKML
......expressmatch
......extension
......HAMEX
......KAIST
......MathBrush
......MfrDB