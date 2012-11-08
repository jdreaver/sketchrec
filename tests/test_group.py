from sketchrec.imagerec import grouping, imageio
import numpy as np

temp_file = 'tests/test_page.iv'
#grp_file = 'tests/test_page.grp'
#lbl_file = 'tests/test_page.lbl'

temps = imageio.single_stroke_unlabeled_file(temp_file)
#groups = imageio.load_group_file(grp_file)
#labels = imageio.load_label_file(lbl_file)

def basic_tests():
    lines = grouping.equation_lines(temps)
    assert (np.max([v for line in lines for v in line]) + 1) == len(temps)

