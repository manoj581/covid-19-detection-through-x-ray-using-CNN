# covid-19-detection-through-x-ray-using-CNN


• train_covid19.py – Used to train the model with the provided dataset. It also performs 
validation and creates the model with the required plot showing various metrics of the 
model

• sample_kaggle_dataset.py- To extract the dataset required.

• build_covid_dataset.py- To build the dataset required in the local machine with the 
dataset extracted.

• tornado_api.py- Used to implement the model on a localhost to make sure its available 
to everyone.



Epochs

The number of epochs is a hyperparameter that defines the number times that the learning 
algorithm will work through the entire training dataset. One epoch means that each sample in 
the training dataset has had an opportunity to update the internal model parameters. An epoch is 
comprised of one or more batches. In this model we are implementing 25 Epochs with a batch 
size of 25.
