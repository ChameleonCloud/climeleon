"""Commandline wrapper to set envs for Chameleon."""
import argparse
import json
import subprocess
from os import getenv, path
from sys import exec_prefix
from typing import Dict, Text


class Commands:
    def get_env_vars(self, cloud, env_dir) -> Dict:
        env_cmd = ["bash", "clouds2rc", cloud]

        result = subprocess.run(env_cmd, cwd=env_dir, capture_output=True, text=True)
        env_dict = {}
        env_dict["PATH"] = path.join(exec_prefix, "bin")
        env_dict["OS_CLOUD"] = cloud
        env_dict["OS_USERNAME"] = self.get_username(cloud)
        env_dict["OS_PASSWORD"] = self.get_password(cloud)

        for line in result.stdout.splitlines():
            data = json.loads(line)
            env_var, value = data.split("=")
            env_dict[env_var] = value

        return env_dict

    def get_username(self, cloud):
        return getenv("CHAMELEON_USER")

    def get_password(self, cloud):

        path_string = getenv("PATH")
        result = subprocess.run(
            ["/usr/bin/env", "-P", path_string, "chameleon_password", cloud],
            capture_output=True,
            text=True,
        )
        text = result.stdout.strip()
        return text


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("cloud", help="select cloud to run commands against")
    parser.add_argument("command")
    parser.add_argument(
        "args",
        nargs=argparse.REMAINDER,
        help="arguments to pass to command",
    )
    args = parser.parse_args()

    env_dir = path.join(path.dirname(__file__), "os_env")
    env_vars = Commands().get_env_vars(args.cloud, env_dir)

    cmd_arr = ["/usr/bin/env", "-P", env_vars.get("PATH")]
    cmd_arr.append(args.command)
    cmd_arr.extend(args.args)

    print(f"Executing {args.command} with args {args.args}")
    proc = subprocess.Popen(cmd_arr, env=env_vars, cwd=env_dir)
    try:
        outs, errs = proc.communicate(timeout=15)
    except Exception:
        proc.kill()
        outs, errs = proc.communicate()
