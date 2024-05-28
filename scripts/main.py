import yaml
from pathlib import Path
from utils import get_project_root
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from graph_pattern_reconstruction import frequent_subgraphs_builder, concepts_builder, equivalence_classes_builder


def do_operations(root, config, dataset='all', mode='all', weighting='yes', graph_pattern_reconstruction='yes'):
    # print(config)
    print(dataset)
    print(mode)
    print(weighting)
    print(graph_pattern_reconstruction)
    print(root)

    if graph_pattern_reconstruction == 'yes':
        print("Reconstructing graph patterns...")

        for class_name in config['ten_newsgroups_classes']:
            frequent_subgraphs_builder(class_name, str(root) + '/' + config['ten_newsgroups_data_prefix'])
            concepts_builder(class_name, str(root) + '/' + config['ten_newsgroups_data_prefix'])
            equivalence_classes_builder(class_name, str(root) + '/' + config['ten_newsgroups_data_prefix'])


if __name__ == '__main__':
    root = get_project_root()

    parser = ArgumentParser(description='Main script', formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('--config', type=Path, default=root/'config/config.yaml',
                        help='Enter the config file path.')

    parser.add_argument('--dataset', type=str, default='all', choices=['all', 'ten_newsgroups', 'bbcsport'],
                        help='Choose the dataset.')

    parser.add_argument('--mode', type=str, default='all',
                        choices=['all', 'concepts', 'frequent_subgraphs', 'equivalence_classes'],
                        help='Choose the operation mode.')

    parser.add_argument('--weighting', type=str, default='yes',
                        choices=['yes', 'no'],
                        help='Choose whether to weight graph patterns.')

    parser.add_argument('--graph_pattern_reconstruction', type=str, default='yes',
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
