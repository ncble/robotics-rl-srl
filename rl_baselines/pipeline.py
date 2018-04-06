"""
baseline benchmark script for openAI RL Baselines
"""
import os
import argparse
import subprocess

from srl_priors.utils import printGreen, printRed

SEEDS = [0, 2, 4, 6]  # the seeds used in trainning the baseline.


def main():
    parser = argparse.ArgumentParser(description="OpenAI RL Baselines Benchmark")
    parser.add_argument('--algo', default='ppo2',
                        choices=['acer', 'deepq', 'a2c', 'ppo2', 'random_agent', 'ddpg'],
                        help='OpenAI baseline to use', type=str)
    parser.add_argument('--env', type=str, help='environment ID', default='all',
                        choices=["all", "KukaButtonGymEnv-v0"])
    parser.add_argument('--srl-model', type=str, default='all',
                        choices=['all', "autoencoder", "ground_truth", "srl_priors", "supervised", "pca", "vae",
                                 "joints", "joints_position", "raw_pixels"],
                        help='SRL model to use')
    parser.add_argument('--num-timesteps', type=int, default=int(1e6 * 1.1), 
                        help='number of timesteps the baseline should run')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Display baseline STDOUT')

    # returns the parsed arguments, and the rest are assumed to be arguments for rl_baselines.train
    args, train_args = parser.parse_known_args()

    if args.srl_model == "all":
        models = ["autoencoder", "ground_truth", "srl_priors", "supervised", "pca", "vae", "joints", "joints_position",
                  "raw_pixels"]
    else:
        models = [args.srl_model]

    if args.env == "all":
        envs = ["KukaButtonGymEnv-v0"]
    else:
        envs = [args.env]

    if args.verbose:
        # None here means stdout of terminal for subprocess.call
        stdout = None
    else:
        stdout = open(os.devnull, 'w')

    printGreen("\nRunning {} benchmarks...".format(args.algo))
    print("\nSRL-Models:\t{}".format(models))
    print("environments:\t{}".format(envs))
    print("verbose:\t{}".format(args.verbose))
    print("timesteps:\t{}".format(args.num_timesteps))
    for model in models:
        for env in envs:
            for seed_idx in range(len(SEEDS)):

                printGreen("\nIteration_num={}, Environment='{}', SRL-Model='{}'".format(seed_idx, env, model))

                # redefine the parsed args for rl_baselines.train
                if model != "raw_pixels":
                    # raw_pixels is when --srl-model is left as default
                    train_args.extend(['--srl-model', model])
                train_args.extend(['--seed', str(SEEDS[seed_idx]), '--algo', args.algo, '--env', env, '--num-timesteps',
                                   str(args.num_timesteps)])

                ok = subprocess.call(['python', '-m', 'rl_baselines.train'] + train_args, stdout=stdout)

                if ok != 0:
                    printRed("An error occured, error code: {}".format(ok))
                    # throw the error down to the terminal
                    return ok


if __name__ == '__main__':
    main()