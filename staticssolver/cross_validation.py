from imagerec.imageio import load_all_label_files as load
import imagrec.image_template

def cross_validation(template_base, label_base):
    files = load(template_base, label_base)

    


if __name__ == '__main__':
    template_base = '../../Data/PencaseDataFix/'
    label_base = '../../Data/PenCaseLabels/'
    cross_validation(raw_base, label_base)
    
