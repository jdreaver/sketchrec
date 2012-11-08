from sketchrec.imagerec import image_template

single = [[[1,2], [5,6]]]
dubs = [[[1,2],[3,4]], [[5,6],[7,8]]]

temp_s = image_template.ImageTemplate(single, dim=6)
temp_d = image_template.ImageTemplate(dubs, dim=6)

temp_dim = image_template.ImageTemplate(dubs, dim=5)
    

def inheritance_tests():
    assert temp_s.is_single_stroke() == True
    assert temp_d.is_single_stroke() == False

def basics_tests():
    assert temp_dim.dimension != temp_s.dimension
    assert temp_s.name == "NO LABEL"
    temp_d.name = "TEST NAME"
    assert temp_d.name == "TEST NAME"
    assert temp_d.points == [[1,2], [3,4], [5,6], [7,8]]
    assert temp_s.points == [[1,2], [5,6]]
    

def distances_tests():
    hauss = image_template.mod_hauss_distance
    assert abs(hauss(temp_s, temp_d) - 0.125) < 0.0001
    
    
