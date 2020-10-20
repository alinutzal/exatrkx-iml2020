import os
import yaml
import pprint

import pytorch_lightning as pl

from exatrkx import FeatureStore

from exatrkx import LayerlessEmbedding
from exatrkx import EmbeddingInferenceCallback

from exatrkx import VanillaFilter
from exatrkx import FilterInferenceCallback

def build(config, args):
    preprocess_dm = FeatureStore(config)
    preprocess_dm.prepare_data()

def embedding(config, args):
    model = LayerlessEmbedding(config)
    callback_list = [EmbeddingInferenceCallback()]
    trainer = pl.Trainer.from_argparse_args(args, callbacks=callback_list)
    trainer.fit(model)

def filtering(config, args):
    model = LayerlessEmbedding(config)
    callback_list = [EmbeddingInferenceCallback()]
    trainer = pl.Trainer.from_argparse_args(args, callbacks=callback_list)
    trainer.fit(model)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="build a feature storage")
    parser = pl.Trainer.add_argparse_args(parser)

    add_arg = parser.add_argument
    add_arg('--action', help='which action you want to take', choices=['build', 'embedding', 'filtering'], required=True)
    add_arg("--config", help="configuration file", default=None)
    add_arg("--input-dir", help="input directory", default=None)
    add_arg("--output-dir", help='output directory', default=None)
    add_arg("--detector-path", help='detector file path', default=None)
    add_arg("--n-files", help='number of files to process', default=None, type=int)
    add_arg('--n-workers', help='number of workers/threads', default=None, type=int)
    add_arg("--pt-min", help='minimum pT', default=None, type=float)

    args = parser.parse_args()
    config_dict = {
        "build": 'prepare_feature_store.yaml',
        'embedding': 'train_embedding.yaml', 
        'filtering': 'train_filter.yaml',
    }

    if args.config is None or not os.path.exists(args.config):
        print("missing configuration, using default")
        import pkg_resources
        config_file = pkg_resources.resource_filename("exatrkx", os.path.join('configs', config_dict[args.action]))
    else:
        config_file = args.config

    pp = pprint.PrettyPrinter(indent=4, sort_dicts=False)

    with open(config_file) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    for key,value in args.__dict__.items():
        if key in config and value is not None:
            config[key] = value

    pp.pprint(config)
    ctn = input("Continue? [y/n]: ")
    print(ctn)
    if ctn.lower() == "y":
        eval(args.action)(config, args)
    else:
        parser.print_help()
        print("nothing is done. bye.")