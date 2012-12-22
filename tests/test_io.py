from sketchrec import imageio
from sketchrec.pagedata import PageData, load_all_page_data

label_dir = 'tests/testlabels/'

temp_file = 'tests/testlabels/Pen005/Homework6-Problem1-text.iv'
grp_file = 'tests/testlabels/Pen005/Homework6-Problem1-text.grp'
lbl_file = 'tests/testlabels/Pen005/Homework6-Problem1-text.lbl'

temps = imageio.single_stroke_unlabeled_file(temp_file)
groups = imageio.load_group_file(grp_file)
labels = imageio.load_label_file(lbl_file)

def basic_tests():
    assert len(temps) == 223
    assert len(groups) == 161
    assert len(labels) == 223

def page_data_labeled_load_tests():
    all_files = imageio.get_labeled_filenames(label_dir)
    assert len(all_files) == 4

    pages = load_all_page_data(label_dir)
    assert len(pages) == 4
    assert len(pages[0].templates) == 223
    assert len(pages[0].groups) == 161
    assert len(pages[0].labels) == 223

    assert pages[0].pen == 'Pen005'
    assert pages[0].filename == 'tests/testlabels/Pen005/Homework6-Problem1-text'

    pages[0].compute_recognition_data()
    for temp, label in zip(pages[0].templates, pages[0].labels):
        assert temp.name == label
    

def page_data_unlabeled_load_tests():
    page = PageData(temp_file, labeled=False)
    assert len(page.templates) == 223
    for i in range(len(page.templates)):
        assert page.labels[i] == 'NO LABEL'
    assert page.pen == 'Pen005'
    
     
