from sketchrec.imagerec.imageio import load_all_label_files as load
#import sketchrec.imagrec.image_template

def ensemble_rec(template_base, label_base):
    files = load(template_base, label_base)
    for f in files:
        labels = f[4]
        for i, temp in enumerate(f[2]):
            temp.name = labels[i]

    print len(files)
    print "so far so good"
    

if __name__ == '__main__':
    #template_base = '../../Data/PencaseDataFix/'
    #label_base = '../../Data/PenCaseLabels/'
    template_base = './Data/PencaseDataFix/'
    label_base = './Data/PenCaseLabels/'
    ensemble_rec(template_base, label_base)
    


