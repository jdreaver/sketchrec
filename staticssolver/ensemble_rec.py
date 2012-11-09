from sketchrec.imagerec.imageio import load_all_label_files as load
from sketchrec.imagerec.image_template import convert_to_image
import numpy as np
#import sketchrec.imagrec.image_template

def ensemble_rec(template_base, label_base):
    files = load(template_base, label_base)
    for f in files:
        labels = f[4]
        for i, temp in enumerate(f[2]):
            temp.name = labels[i]

    k = len(files)
    accuracies = np.zeros(k)

    for i in range(k):
        test = files[0]
        train = files[1:]

        test_images = [convert_to_image(t) for t in test[2]]
        train_images = [convert_to_image(t) for group in train for t in group[2]]

        

if __name__ == '__main__':
    #template_base = '../../Data/PencaseDataFix/'
    #label_base = '../../Data/PenCaseLabels/'
    template_base = './Data/PencaseDataFix/'
    label_base = './Data/PenCaseLabels/'
    ensemble_rec(template_base, label_base)
    


