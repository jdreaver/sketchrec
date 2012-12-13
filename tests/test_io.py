from sketchrec import imageio

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
