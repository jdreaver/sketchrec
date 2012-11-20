from sketchrec.imagerec.imageio import load_all_label_files as load
from sketchrec.imagerec.image_template import multiple_to_image
from sketchrec.imagerec.image_template import list_classification
from sketchrec.imagerec.grouping import compute_features_equation
from sketchrec.imagerec.grouping import groups_to_join_graph
from sketchrec.imagerec.grouping import features_to_classifier_input
from sketchrec.imagerec.grouping import clf_results_to_join_graph
import numpy as np
from sklearn import tree
from collections import namedtuple
from multiprocessing import Pool

template_base = '/home/david/Dropbox/Research/Data/PencaseDataFix/'
label_base = '/home/david/Dropbox/Research/Data/PenCaseLabels/'

FileInfo = namedtuple('fileinfo', ['pen', 'filename', 'templates', 'groups', 
                                   'labels', 'join_graph', 'imagetemps',    
                                   'raw_grouping_features', 
                                   'grouping_features', 'grouping_labels'])
                                   
# Ensemble schemes

def ensemble_rec():
    raw_files = load(template_base, label_base)
    print "Building data"
    pages = build_data(raw_files)
    
    accuracies = []
    for i in range(len(pages)):
        test = pages[0]
        train = pages[1:]

        num_temps = len(getattr(test, 'templates'))

        print i, "Grouping"
        group_clf = grouping_classifier(train, tree.DecisionTreeClassifier)
        (g_acc, grouped_test) = group_classify(test, group_clf)
                                                  
        print i, "Classifiying"
        train_images = [image for page in train 
                        for image in getattr(page, 'imagetemps')
                        if image.name != "NO LABEL"]
        grouped_labels = [list_classification(t, train_images)
                          for t in grouped_test]

        predicted_labels = distribute_labels(getattr(test, 'groups'),
                                             grouped_labels,
                                             num_temps)
        
        real_labels = getattr(test, 'labels')

        #for a, b, in zip(predicted_labels, real_labels):
        #    print a, b
        #print predicted_labels, grouped_labels
        num_right = np.sum([1.0 if predicted_labels[i] == real_labels[i]
                            else 0.0
                            for i in range(len(real_labels))])
        accuracies.append([num_right/num_temps, g_acc])
        pages = pages[1:] + pages[:1]

    return accuracies

def character_rec(dim):
    raw_files = load(template_base, label_base)
    print "Building data"
    pages = build_data(raw_files, dim)
    
    accuracies = []
    for i in range(len(pages)):
        test = pages[0]
        train = pages[1:]
        
        num_temps = len(getattr(test, 'templates'))               
        print i, "Classifiying"
        train_images = [image for page in train 
                        for image in getattr(page, 'imagetemps')
                        if image.name != "NO LABEL"]
        grouped_labels = [list_classification(t, train_images)
                          for t in getattr(test, 'imagetemps')]
        
        #grouped_labels = map(lambda t: 
        #                     list_classification(t, train_images),
        #                     getattr(test, 'imagetemps'))
        predicted_labels = distribute_labels(getattr(test, 'groups'),
                                             grouped_labels,
                                             num_temps)
        
        real_labels = getattr(test, 'labels')
        
        num_right = np.sum([1.0 if predicted_labels[i] == real_labels[i]
                            else 0.0
                            for i in range(len(real_labels))])
        accuracies.append(num_right/num_temps)
        pages = pages[1:] + pages[:1]
        
    return accuracies

# Utilites
def group_image_templates(templates, groups, dim=48):
    grouped = []
    for group in groups:
        t_group = [templates[i] for i in group]
        grouped.append(multiple_to_image(t_group, dim))
    return grouped
                        
def distribute_labels(groups, labels, num_temps):
    dist_labels = ['dummy' for i in range(num_temps)]
    for group, label in zip(groups, labels):
        for i in group:
            dist_labels[i] = label
    return dist_labels
        

def build_data(raw_files, dim=48):
    """ 
    Takes the raw files and computes image templates, join_graphs, features.
    """
    pages = []
    for f in raw_files:
        labels = f[4]
        for i, temp in enumerate(f[2]):
            temp.name = labels[i]
        #print "Building file ", f[0], f[1], len(f[2])
        join_graph = groups_to_join_graph(f[3])
        image_temps = group_image_templates(f[2], f[3], dim)
        raw_features = compute_features_equation(f[2])
        (g_features, g_labels) = features_to_classifier_input(raw_features, 
                                                              join_graph)
        tup = f + (join_graph, image_temps, raw_features, 
                   g_features, g_labels)
        pages.append(FileInfo(*tup))
    return pages
    

def grouping_classifier(train, clf_type):
    X = [f for page in train 
         for f in getattr(page, 'grouping_features') ]
    y = [f for page in train 
         for f in getattr(page, 'grouping_labels')]

    clf = clf_type()
    clf = clf.fit(np.array(X), np.array(y))
    return clf

def group_classify(page, clf):
    features = getattr(page, 'grouping_features')
    
    y = clf.predict(features)
    real = getattr(page, 'grouping_labels')
    accuracy = sum([1.0 if r == p else 0.0
                    for r,p in zip(real, y)])/len(y)
    groups = clf_results_to_join_graph(getattr(page, 'raw_grouping_features'),
                                       y, 
                                       len(getattr(page, 'templates')))
    return (accuracy, group_image_templates(getattr(page, 'templates'),
                                            groups))
    

if __name__ == '__main__':
    #template_base = '../../Data/PencaseDataFix/'
    #label_base = '../../Data/PenCaseLabels/'
    
    ensemble_rec()
