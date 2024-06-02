import yaml
from pathlib import Path
from utils import get_project_root
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from graph_pattern_visualize import graph_pattern_visualize_iterator
from graph_pattern_reconstruction import graph_pattern_reconstruction_iterator
from graph_pattern_weighting import graph_pattern_iterator
from graph_pattern_scoring import graph_pattern_classification


def do_operations(root, config, dataset='all', mode='concepts', weighting='yes', graph_pattern_reconstruction='yes'):

    if graph_pattern_reconstruction == 'yes':
        print("Reconstructing graph patterns...")
        graph_pattern_reconstruction_iterator(config['ten_newsgroups_classes'], str(root) + '/' + config['ten_newsgroups_data_prefix'], mode)
        # graph_pattern_reconstruction_iterator(config['example_classes'], str(root) + '/' + config['example_data_prefix'], mode)
        # graph_pattern_visualize_iterator(config['example_classes'], str(root) + '/' + config['example_data_prefix'], mode)

        # print("ten newsgroups graph patterns reconstructed.")

    if weighting == 'yes':
        print("Weighting graph patterns...")
        graph_pattern_iterator(config['ten_newsgroups_classes'], str(root) + '/' + config['ten_newsgroups_data_prefix'], 'frequent_subgraphs')
        # graph_pattern_iterator(config['ten_newsgroups_classes'], str(root) + '/' + config['ten_newsgroups_data_prefix'], 'concepts')
        # graph_pattern_iterator(config['ten_newsgroups_classes'], str(root) + '/' + config['ten_newsgroups_data_prefix'], 'concepts')
        # graph_pattern_iterator(config['ten_newsgroups_classes'], str(root) + '/' + config['ten_newsgroups_data_prefix'], 'equivalence_classes')
        # graph_pattern_iterator(config['bbcsport_classes'], str(root) + '/' + config['bbcsport_data_prefix'], 'concepts')

    # graph_pattern_classification(config['bbcsport_classes'], str(root) + '/' + config['bbcsport_data_prefix'], 'concepts')
    # graph_pattern_classification(config['ten_newsgroups_classes'], str(root) + '/' + config['ten_newsgroups_data_prefix'], 'concepts')
    graph_pattern_classification(config['ten_newsgroups_classes'], str(root) + '/' + config['ten_newsgroups_data_prefix'], mode)


if __name__ == '__main__':
    root = get_project_root()

    parser = ArgumentParser(description='Main script', formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('--config', type=Path, default=root/'config/config.yaml',
                        help='Enter the config file path.')

    parser.add_argument('--dataset', type=str, default='all', choices=['all', 'ten_newsgroups', 'bbcsport'],
                        help='Choose the dataset.')

    parser.add_argument('--mode', type=str, default='frequent_subgraphs',
                        choices=['all', 'concepts', 'frequent_subgraphs', 'equivalence_classes'],
                        help='Choose the operation mode.')

    parser.add_argument('--weighting', type=str, default='yes',
                        choices=['yes', 'no'],
                        help='Choose whether to weight graph patterns.')

    parser.add_argument('--graph_pattern_reconstruction', type=str, default='no',
                        choices=['yes', 'no'],
                        help='Choose whether to reconstruct graph patterns.')

    args, unknown = parser.parse_known_args()

    with args.config.open() as y:
        config = yaml.load(y, Loader=yaml.FullLoader)

    do_operations(root=root,
                  config=config,
                  dataset=args.dataset,
                  mode=args.mode,
                  weighting=args.weighting,
                  graph_pattern_reconstruction=args.graph_pattern_reconstruction)
