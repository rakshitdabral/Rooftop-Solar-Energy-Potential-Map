import splitfolders

input_folder='data\external'
splitfolders.ratio(input_folder,output="data/processed_border",ratio=(0.8,0.1,0.1), seed=2023)