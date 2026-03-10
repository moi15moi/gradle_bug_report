
1. Run `python CPP_module/src/main/cpp/build_shared_library.py --ndk-path "PATH_TO_NDK" --abi-version 24
2. In Android Studio, select the `CPP_module` and select `Build` --> `Assemble Module MyApplication.CPP_module` (don't know why, but otherwise, the build will fail if directly clicking the Run button.)