# Executing: This file execute "clang -fPIC -shared -Wl,-soname,libCPP_module.so -Iinclude c_file.c -o ../jniLibs/ABI/libcfile.so" for all the ABI

import shutil
import subprocess
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from platform import system


@dataclass(frozen=True)
class Target:
    """Android ABI target and cross-compilation metadata.

    Attributes:
        abi: Android ABI name (e.g., "arm64-v8a", "armeabi-v7a"). From https://developer.android.com/ndk/guides/other_build_systems
        triple: LLVM target triple (e.g., "aarch64-linux-android"). From https://developer.android.com/ndk/guides/other_build_systems
    """

    abi: str  
    triple: str


def get_toolchain_path(ndk_path: Path) -> Path:
    """Resolve the NDK LLVM toolchain path for the current host OS.

    Parameters:
        ndk_path: Root path of the Android NDK installation.
            (e.g., .../ndk/27.0.12077973)

    Returns:
        Path to the prebuilt LLVM toolchain (toolchains/llvm/prebuilt/{os}).
        The OS variant is derived from the current platform:
        windows-x86_64, linux-x86_64, or darwin-x86_64.
    """
    system_name = system()

    # See NDK OS Variant in https://developer.android.com/ndk/guides/other_build_systems#overview
    if system_name == "Windows":
        os = "windows-x86_64"
    elif system_name == "Linux":
        os = "linux-x86_64"
    elif system_name == "Darwin":
        os = "darwin-x86_64"
    else:
        raise NotImplementedError(f"The system {system_name} isn't supported.")

    toolchain_path = ndk_path.joinpath("toolchains", "llvm", "prebuilt", os)
    if not toolchain_path.is_dir():
        raise NotADirectoryError(f"The toolchain \"{toolchain_path.absolute()}\" doesn't exist")

    return toolchain_path


def main() -> None:
    parser = ArgumentParser(description="Build libass for android")
    parser.add_argument(
        "--ndk-path",
        type=Path,
        required=True,
        help="""
    The ndk path. Ex: C:\\Users\\moi15moi\\AppData\\Local\\Android\\Sdk\\ndk\\27.0.12077973
    """,
    )

    parser.add_argument(
        "--abi-version",
        type=int,
        required=True,
    )

    args = parser.parse_args()
    ndk_path: Path = args.ndk_path
    abi_version: int = args.abi_version

    if not ndk_path.is_dir():
        raise NotADirectoryError(f"The path you provided \"{ndk_path.absolute()}\" doesn't exist")
    
    toolchain_path = get_toolchain_path(ndk_path)
    python_file_dir = Path(__file__).parent

    target_arm = Target("armeabi-v7a", "armv7a-linux-androideabi")
    target_aarch64 = Target("arm64-v8a", "aarch64-linux-android")
    target_x86 = Target("x86", "i686-linux-android")
    target_x86_64 = Target("x86_64", "x86_64-linux-android")

    targets = [
        target_arm,
        target_aarch64,
        target_x86,
        target_x86_64
    ]

    for target in targets:
        jniLibs = python_file_dir.parent.joinpath("jniLibs", target.abi)

        # Be sure to rebuild
        if jniLibs.is_dir():
            shutil.rmtree(jniLibs)
        jniLibs.mkdir(parents=True)

        clang_path = toolchain_path.joinpath("bin", f'{target.triple}{abi_version}-clang' + (".cmd" if system() == "Windows" else ""))
        build_cmd = [
            str(clang_path),
            "-fPIC", "-shared",
            "-Wl,-soname,libCPP_module.so",
            "-Iinclude", "c_file.c",
            "-o", str(jniLibs.joinpath("libCPP_module.so"))
        ]

        print(f'Executing: {" ".join(build_cmd)}')

        subprocess.run(build_cmd, cwd=python_file_dir, check=True, encoding="utf-8")


if __name__ == "__main__":
    main()
