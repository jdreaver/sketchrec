from sketchrec.imagerec.imageio import load_all_label_files as load
from sketchrec.imagerec.image_template import convert_to_image, multiple_to_image
from sketchrec.imagerec.grouping import compute_features_equation
from sketchrec.imagerec.grouping import groups_to_join_graph
from sketchrec.imagerec.grouping import features_to_classifier_input
import numpy as np
from sklearn import tree
from collections import namedtuple
#import sketchrec.imagrec.image_template

FileInfo = namedtuple('fileinfo', ['pen', 'filename', 'templates', 'groups', 
                                   'labels', 'join_graph', 'imagetemps',    
                                   'grouping_features', 'grouping_labels'])
                                   

def ensemble_rec(template_base, label_base):
    raw_files = load(template_base, label_base)
    pages = build_data(raw_files)
    
    for i in range(len(pages)):
        test = pages[0]
        train = pages[1:]

        group_clf = grouping_classifier(train, tree.DecisionTreeClassifier)
        grouped_templates = group_classify(test, group_clf)
                                                  
        files = files[1:] + files[0]

def group_image_templates(templates, groups):
    grouped = []
    for group in groups:
        t_group = [templates[i] for i in group]
        grouped.append(multiple_to_image(t_group))

    return grouped
                        

def build_data(raw_files):
    """ 
    Takes the raw files and computes image templates, join_graphs, features.
    """
    pages = []
    for f in raw_files:
        labels = f[4]
        for i, temp in enumerate(f[2]):
            temp.name = labels[i]
        join_graph = groups_to_join_graph(f[3])
        image_temps = group_image_templates(f[2], f[3])
        raw_features = compute_features_equation(f[2])
        (g_features, g_labels) = features_to_classifier_input(raw_features, 
                                                              join_graph)
        tup = f + (join_graph, image_temps, g_features, g_labels)
        pages.append(FileInfo(*tup))
    return pages
    

def grouping_classifier(train, clf_type):
    X, y = [],[]

    for f in train:
        this_features = compute_features_equation(f[2])
        join_graph = groups_to_join_graph(f[3])
        (feats, labels) = features_to_classifier_input(this_features, join_graph)
        X.extend(feats)
        y.extend(labels)
    print X, y

    clf = clf_type()
    clf = clf.fit(np.array(X), np.array(y))
    return clf

def group_class(templates, clf):
    features = compute_features_equation(templates)
    
    

if __name__ == '__main__':
    #template_base = '../../Data/PencaseDataFix/'
    #label_base = '../../Data/PenCaseLabels/'
    template_base = './Data/PencaseDataFix/'
    label_base = './Data/PenCaseLabels/'
    ensemble_rec(template_base, label_base)
    


