from sketchrec import imageio
from sketchrec.pagedata import PageData, load_all_page_data 

label_dir = 'tests/testlabels/'

temp_file = 'tests/test_page.iv'
grp_file = 'tests/test_page.grp'
lbl_file = 'tests/test_page.lbl'

temps = imageio.single_stroke_unlabeled_file(temp_file)
groups = imageio.load_group_file(grp_file)
labels = imageio.load_label_file(lbl_file)

def basic_tests():
    assert len(temps) == 223
    assert len(groups) == 161
    assert len(labels) == 223

def page_data_tests():
    all_files = imageio.get_labeled_filenames(label_dir)
    assert len(all_files) == 4

    pages = load_all_page_data(label_dir)
    assert len(pages) == 4
