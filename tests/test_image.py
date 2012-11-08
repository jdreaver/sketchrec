from sketchrec.imagerec import image_template

def test_inheritance():
    single = [[[1,2]]]
    dubs = [[[1,2],[3,4]], [[5,6],[7,8]]]
    
    
    temp_s = image_template.ImageTemplate(single, dim=6)
    assert temp_s.is_single_stroke() == True
    
    temp_d = image_template.ImageTemplate(dubs, dim=5)
    assert temp_d.is_single_stroke() == False




