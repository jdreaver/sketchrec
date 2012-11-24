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

def group_convert_test():
    groups = [[1], [2,3,4], [5], [6,8,9], [7]]
    join_graph = grouping.groups_to_join_graph(groups)
    assert  join_graph == {1:[1], 2:[2, 3, 4], 3:[2, 3, 4],
                           4:[2, 3, 4], 5:[5], 6:[6, 8, 9],
                           7:[7], 8:[6, 8, 9], 9:[6, 8, 9]}
    new_groups = grouping.join_graph_to_groups(join_graph)
    assert len(new_groups) == len(groups)
    for g1, g2 in zip(new_groups, groups):
        assert g1 == g2

    sparse_groups = [[2,3], [5, 7, 10], [8,11], [12, 13]]
    all_groups = grouping.sparse_groups_to_groups(sparse_groups, 14)
    real_all_groups = [[0], [1], [2, 3], [4], [5, 7, 10], [6], [8,11],
                       [9], [12, 13]]
    for g1, g2 in zip(all_groups, real_all_groups):
        assert g1 == g2
    
