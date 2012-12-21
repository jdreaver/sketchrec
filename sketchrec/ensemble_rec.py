import numpy as np
from sklearn import tree
from collections import namedtuple
#from multiprocessing import Pool

from sketchrec.image_template import multiple_to_image
from sketchrec.image_template import list_classification
from sketchrec.grouping import (compute_features_equation,
                                groups_to_join_graph,
                                features_to_classifier_input,
                                clf_results_to_join_graph,
                                group_image_templates)
from sketchrec.pagedata import load_all_page_data

base_directory = '/home/david/Dropbox/Research/Data/PenCaseLabels/'
                             
# Ensemble schemes

def ensemble_rec():
    print "Building data"
    pages = load_pages(base_directory)
    
    accuracies = []
    for i in range(len(pages)):
        test = pages[0]
        train = pages[1:]

        print i, "Grouping"
        group_clf = grouping_classifier(train, tree.DecisionTreeClassifier)
        (g_acc, grouped_test) = group_classify(test, group_clf)
                                                  
        print i, "Classifiying"
        train_images = [image for page in train 
                        for image in page.image_templates
                        if image.name != "NO LABEL"]
        grouped_labels = [list_classification(t, train_images)
                          for t in grouped_test]

        predicted_labels = distribute_labels(test.groups,
                                             grouped_labels,
                                             test.num_temps)
        
        real_labels = test.labels

        num_right = np.sum([1.0 if predicted_labels[i] == real_labels[i]
                            else 0.0
                            for i in range(len(real_labels))])
        accuracies.append([num_right/test.num_temps, g_acc])
        pages = pages[1:] + pages[:1]

    return accuracies

def character_rec(dim):
    print "Building data"
    pages = load_pages(base_directory)
    
    accuracies = []
    for i in range(len(pages)):
        test = pages[0]
        train = pages[1:]
        
        print i, "Classifiying"
        train_images = [image for page in train 
                        for image in page.image_templates
                        if image.name != "NO LABEL"]
        grouped_labels = [list_classification(t, train_images)
                          for t in test.image_templates]
        
        predicted_labels = distribute_labels(test.groups,
                                             grouped_labels,
                                             test.num_temps)
        
        real_labels = test.labels
        
        num_right = np.sum([1.0 if predicted_labels[i] == real_labels[i]
                            else 0.0
                            for i in range(len(real_labels))])
        accuracies.append(num_right/test.num_temps)
        pages = pages[1:] + pages[:1]
        
    return accuracies

# Utilites
def distribute_labels(groups, labels, num_temps):
    dist_labels = ['dummy' for i in range(num_temps)]
    for group, label in zip(groups, labels):
        for i in group:
            dist_labels[i] = label
    return dist_labels
        
def load_pages(base_dir, dim=48):
    """ 
    Takes the raw files and computes image templates, join_graphs, features.
    """
    pages = load_all_page_data(base_directory)
    [page.compute_recognition_data(dim) for page in pages]
    return pages
    
def grouping_classifier(train, clf_type):
    X = [f for page in train 
         for f in page.group_features]
    y = [f for page in train 
         for f in page.group_labels]

    clf = clf_type()
    clf = clf.fit(np.array(X), np.array(y))
    return clf

def group_classify(page, clf):
    features = page.group_features
    
    y = clf.predict(features)
    real = page.group_labels
    accuracy = sum([1.0 if r == p else 0.0
                    for r,p in zip(real, y)])/len(y)
    groups = clf_results_to_join_graph(page.raw_features,
                                       y, 
                                       page.num_temps)
    return (accuracy, group_image_templates(page.templates,
                                            groups))
    

if __name__ == '__main__':

    ensemble_rec()
