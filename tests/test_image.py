from sketchrec import image_template, template, pagedata
import numpy as np

degen1 = [[[1,-1]]]
nowidth = [[[1,1], [0,1]]]
single = [[[1,2], [5,6]]]
dubs = [[[1,2],[3,3]], [[5,6],[10,10]]]

temp_d1 = image_template.ImageTemplate(degen1, dim=47)
temp_nw = image_template.ImageTemplate(nowidth, dim=48)
temp_s = image_template.ImageTemplate(single, dim=6)
temp_s.name = "temp_s"
temp_d = image_template.ImageTemplate(dubs, dim=6)

temp_dim = image_template.ImageTemplate(dubs, dim=5)

page_path = 'tests/testlabels/Pen005/Homework6-Problem1-text'
page = pagedata.PageData(page_path, labeled=True)
page.compute_recognition_data()
    

def inheritance_tests():
    assert temp_s.is_single_stroke() == True
    assert temp_d.is_single_stroke() == False
    assert np.array_equal(temp_s.timestamps, np.array(None))

def upsample_tests():
    test_points = np.array(([1,1], [3,4], [0, 4], [-3, -3]))
    assert np.array_equal(image_template.full_upsample(test_points),
                          [[ 1, 1], [1, 2], [2, 3], [3, 4], [2, 4],
                           [1, 4], [0, 4], [0, 3], [0, 2], [0, 1],
                           [0, 0], [-1, -1], [-2, -2], [-3, -3]])

def conversion_tests():
    t = template.Template(dubs)
    t_img = image_template.convert_to_image(t)
    other_img = image_template.ImageTemplate(dubs)
    assert all([np.array_equal(a, b) 
                for a, b in zip(t_img.strokes, other_img.strokes)])

def basics_tests():
    assert temp_dim.dimension != temp_s.dimension
    assert temp_s.name == "temp_s"
    temp_d.name = "TEST NAME"
    assert temp_d.name == "TEST NAME"
    assert np.array_equal(temp_d.points,[[1,2], [3,3], [5,6], [10,10]])
    assert np.array_equal(temp_s.points, [[1,2], [5,6]])
    assert np.array_equal([1.6, 1.8], image_template.group_centroid(
        [temp_d1, temp_nw, temp_s]))
    

def distances_tests():
    HAUS_S_D = 0.0673441488
    haus = image_template.modified_hausdorff_distance
    assert abs(haus(temp_s, temp_d) - HAUS_S_D) < 0.0001
    assert image_template.list_classification(temp_s, [temp_d, temp_s])[0] == "temp_s"
    test = page.image_templates[0]
    train = page.image_templates[1:50]
    assert image_template.list_classification_vec(test, train) == \
           image_template.list_classification(test, train)

    dist_matrix = image_template.distance_matrix([temp_s, temp_d, temp_s])
    assert np.allclose(dist_matrix, np.array([[ 0.      , HAUS_S_D, 0.      ],
                                              [ HAUS_S_D, 0.      , HAUS_S_D],
                                              [ 0.      , HAUS_S_D, 0.      ]]))
    
