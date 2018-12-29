from Line_of_Sight import *
from inkml import *


def find_nodes_to_add_edges(this_tg, inkml_obj, this_index):
    if len(inkml_obj.trace_groups) == 1:
        return []
    elif len(inkml_obj.trace_groups) <= 3:
        return [i.id for i in inkml_obj.trace_groups if i.id != this_tg.id]
    this_tg_tr = trace()
    for t in inkml_obj.get_traces_in_group(this_tg.id):
        this_tg_tr.x.extend(t.x)
        this_tg_tr.y.extend(t.y)
    this_tg_tr.calculate_centroids()
    this_tg_tr.id = "this"
    dist = {}
    for tg in range(len(inkml_obj.trace_groups)):
        if inkml_obj.trace_groups[tg].id != this_tg.id:
            other_tg_tr = trace()
            for t in inkml_obj.get_traces_in_group(inkml_obj.trace_groups[tg].id):
                other_tg_tr.x.extend(t.x)
                other_tg_tr.y.extend(t.y)
            other_tg_tr.calculate_centroids()
            other_tg_tr.id = "Other"
            # if this_tg_tr.bb_center_x <= other_tg_tr.bb_center_x:
            this_dist = this_tg_tr.get_distance_bb_center(other_tg_tr)
            dist[inkml_obj.trace_groups[tg].id] = this_dist
    dist = sorted(dist.items(), key=lambda x: x[1])
    if len(dist) >= 2:
        return [dist[0][0], dist[1][0]]
    elif len(dist) == 1:
        return [dist[0][0]]
    return []


def build_graph_of_relations(inkml_obj, model):
    g = Graph(len(inkml_obj.trace_groups))
    inkml_obj.compute_all_tg_bb()
    # inkml_obj.trace_groups.sort(key=lambda x: x.bbx)
    for tg in inkml_obj.trace_groups:
        g.add_node(tg.id)
    tr_index = 0
    for tg in inkml_obj.trace_groups:
        this_trs = inkml_obj.get_traces_in_group(tg.id)
        eds = find_nodes_to_add_edges(tg, inkml_obj, tr_index)
        for edge in eds:
            trs = inkml_obj.get_traces_in_group(edge)
            ob1_label = tg.annotation_mml
            ob2_label = inkml_obj.get_trace_group(edge).annotation_mml
            features = pfe.get_features(this_trs, trs)
            [r, w] = model.score_for_trace([features])
            if r != 'None':
                g.add_edge(tg.id, edge, -1 * w, label=r, directed=True)
        tr_index += 1
    return g


def write_lg_file(mst, in_to_id, rgraph, file, inkml_obj):
    filename = file.replace('.inkml', '.lg')
    with open(filename, 'w') as f:
        for tg in inkml_obj.trace_groups:
            line = "O, " + str(tg.id) + ", " + \
                   tg.annotation_mml.replace(",", "COMMA") + ", 1.0, "
            line += str(tg.trace_list).replace("[", "").replace("]",
                                                                "").replace("'", "")
            line += '\n'
            f.write(line)

        for row in range(len(mst)):
            for col in range(len(mst[row])):
                if mst[row][col] < 0:
                    o1 = in_to_id[row]
                    o2 = in_to_id[col]
                    label = rgraph.get_node(o1).edge_l[o2]
                    line = "R, " + o1 + ", " + o2 + ", " + label + ", " + "1.0"
                    line += '\n'
                    f.write(line)


def main(filename):
    parsing_model = Detector(training_features='features/training_set_features_for_parser_wlab.txt',
                             training_gt='features/training_set_GT_for_parser_wlab.txt')

    parsing_model.deserialize_model_parameters(
        'training_parameters/parser_training_params_wlab.ds')

    with open(filename, 'r') as file_pointer:
        file_list = json.load(file_pointer)

    for file_index in range(len(file_list)):
        # if file_index > 11:
        #     break
        file = file_list[file_index]  # "E:/RIT/PR/Project3/3.inkml"#
        print('Processing: ', file_index + 1, file)

        inkml_obj = marshal_inkml(file)
        # relation_graph = build_graph_of_relations(inkml_obj, parsing_model)
        los = get_line_of_sight_graph(inkml_obj.trace_groups, inkml_obj,
                                      parsing_model)
        g, in_to_id = los.get_adjacency_list()
        e_mst = edmonds_mst(g, True)
        write_lg_file(e_mst, in_to_id, los, file, inkml_obj)


if __name__ == '__main__':
    main('testing_files.txt')
