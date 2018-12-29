import parsing_feature_extractor as pfe
from inkml import *
from segmentor_using_binary_detector import *

__author__ = ['Dharmendra Hingu', 'Sanjay Khatwani']


def find_nodes_to_add_edges(this_obj, inkml_obj):
    if len(inkml_obj.objects) == 1:
        return []
    elif len(inkml_obj.objects) <= 3:
        return [i.id for i in inkml_obj.objects if i.id != this_obj.id]
    this_ob_tr = trace()
    for t in inkml_obj.get_traces_in_object(this_obj.id):
        this_ob_tr.x.extend(t.x)
        this_ob_tr.y.extend(t.y)
    this_ob_tr.calculate_centroids()
    this_ob_tr.id = "this"
    dist = {}
    for o in range(len(inkml_obj.objects)):
        if inkml_obj.objects[o].id != this_obj.id:
            other_ob_tr = trace()
            for t in inkml_obj.get_traces_in_object(inkml_obj.objects[o].id):
                other_ob_tr.x.extend(t.x)
                other_ob_tr.y.extend(t.y)
            other_ob_tr.calculate_centroids()
            other_ob_tr.id = "Other"
            # if this_ob_tr.bb_center_x <= other_ob_tr.bb_center_x:
            this_dist = this_ob_tr.get_distance_bb_center(other_ob_tr)
            dist[inkml_obj.objects[o].id] = this_dist
    dist = sorted(dist.items(), key=lambda x: x[1])
    if len(dist) >= 2:
        return [dist[0][0], dist[1][0]]
    elif len(dist) >= 1:
        return [dist[0][0]]
    return []


def build_graph_of_relations(inkml_obj, model):
    g = Graph(len(inkml_obj.objects))
    inkml_obj.compute_all_obj_bb()
    # inkml_obj.objects.sort(key=lambda x: x.bbx)
    for o in inkml_obj.objects:
        g.add_node(o.id)
    tr_index = 0
    for o in inkml_obj.objects:
        this_trs = inkml_obj.get_traces_in_object(o.id)
        eds = find_nodes_to_add_edges(o, inkml_obj)
        for edge in eds:
            trs = inkml_obj.get_traces_in_object(edge)
            features = pfe.get_features(this_trs, trs)
            [r, w] = model.score_for_trace([features])
            if r != 'None':
                g.add_edge(o.id, edge, -1 * w, label=r, directed=True)
        tr_index += 1
    return g


def write_lg_file(mst, in_to_id, rgraph, file):
    filename = file.replace('.inkml', '.lg')
    with open(filename, 'a') as f:
        f.write("\n")

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
    parsing_model = Detector(training_features='features/parser_bonus_features.txt',
                             training_gt='features/parser_bonus_GT.txt')
    parsing_model.deserialize_model_parameters('training_parameters/parser_bonus.ds')

    detector = Detector(training_features='features/binary_detector_bonus_features.txt',
                        training_gt='features/binary_detector_bonus_GT.txt')
    detector.deserialize_model_parameters('training_parameters/binary_detector_bonus.ds')

    classifier = Detector(training_features='features/classifier_bonus_features.txt',
                          training_gt='features/classifier_bonus_GT.txt')
    classifier.deserialize_model_parameters('training_parameters/classifier_bonus.ds')

    with open(filename, 'r') as file_pointer:
        file_list = json.load(file_pointer)

    for file_index in range(len(file_list)):
        # if file_index > 10:
        #     break
        file = file_list[file_index]
        print('Processing: ', file_index + 1, file)

        inkml_obj = generate_lg_file_for_inkml(file, classifier, detector)
        lg_file_name = file.replace(".inkml", ".lg")
        marshal_objects_relations(lg_file_name, inkml_obj)

        relation_graph = build_graph_of_relations(inkml_obj, parsing_model)
        g, in_to_id = relation_graph.get_adjacency_list()
        e_mst = edmonds_mst(g, True)
        write_lg_file(e_mst, in_to_id, relation_graph, file)


if __name__ == '__main__':
    main('bonus_set.txt')
