# Bug Report: Prefab does not include prebuilt shared libraries in .aar

## Summary

When using an `IMPORTED` shared library in CMake with `prefabPublishing` enabled, the generated `.aar` package is missing the `.so` files under `prefab/modules/<module>/libs/`. The native libraries end up only in `jni/<abi>/`, not in the prefab layout.

This affects projects that distribute prebuilt native libraries via AAR and rely on prefab for downstream consumption.

## Environment

| Component    | Version   |
|-------------|-----------|
| Android Gradle Plugin | 9.0.1 |
| Gradle      | 9.2.1    |
| NDK         | 28.1.13356709 |
| CMake       | 3.22.1   |

## Steps to Reproduce

1. Clone this repository.

2. Build the prebuilt shared library (normally, it would use a build system, but to keep it as simple as possible, let's just directly use clang):
   ```bash
   python CPP_module/src/main/cpp/build_shared_library.py --ndk-path "PATH_TO_NDK" --abi-version 24
   ```

3. In Android Studio: select the `CPP_module` module → **Build** → **Assemble Module MyApplication.CPP_module**  
   *(Note: Running the app directly may fail (I don't know why); assemble the module explicitly.)*

## Expected Behavior

The `.aar` should contain the shared library under both `jni/<abi>/` and `prefab/modules/CPP_module/libs/`:

```
├── AndroidManifest.xml
├── classes.jar
├── jni
│   ├── arm64-v8a
│   │   └── libCPP_module.so
│   ├── armeabi-v7a
│   │   └── libCPP_module.so
│   ├── x86
│   │   └── libCPP_module.so
│   └── x86_64
│       └── libCPP_module.so
├── META-INF
│   └── com
│       └── android
│           └── build
│               └── gradle
│                   └── aar-metadata.properties
├── prefab
│   ├── modules
│   │   └── CPP_module
│   │       ├── include
│   │       │   └── c_file.h
│   │       ├── libs
│   │       │   ├── android.arm64-v8a
│   │       │   │   ├── abi.json
│   │       │   │   └── libCPP_module.so
│   │       │   ├── android.armeabi-v7a
│   │       │   │   ├── abi.json
│   │       │   │   └── libCPP_module.so
│   │       │   ├── android.x86
│   │       │   │   ├── abi.json
│   │       │   │   └── libCPP_module.so
│   │       │   └── android.x86_64
│   │       │       ├── abi.json
│   │       │       └── libCPP_module.so
│   │       └── module.json
│   └── prefab.json
└── R.txt
```

## Actual Behavior

With an `IMPORTED` shared library in CMake, the prefab layout lacks the `libs` folder:

```
├── AndroidManifest.xml
├── classes.jar
├── jni
│   ├── arm64-v8a
│   │   └── libCPP_module.so
│   ├── armeabi-v7a
│   │   └── libCPP_module.so
│   ├── x86
│   │   └── libCPP_module.so
│   └── x86_64
│       └── libCPP_module.so
├── META-INF
│   └── com
│       └── android
│           └── build
│               └── gradle
│                   └── aar-metadata.properties
├── prefab
│   ├── modules
│   │   └── CPP_module
│   │       ├── include
│   │       │   └── c_file.h
│   │       └── module.json
│   └── prefab.json
└── R.txt
```

The `.so` files appear only under `jni/<abi>/`, not in `prefab/modules/CPP_module/libs/`.

## Minimal Reproducer: CMakeLists.txt (Current / Failing)

```cmake
cmake_minimum_required(VERSION 3.22.1)
project("CPP_module")

add_library(${CMAKE_PROJECT_NAME} SHARED IMPORTED)
set_target_properties(${CMAKE_PROJECT_NAME} PROPERTIES
    IMPORTED_LOCATION ${CMAKE_CURRENT_SOURCE_DIR}/../jniLibs/${ANDROID_ABI}/libCPP_module.so)
```

## Workaround (really hacky)

Create a stub shared library and replace it with the prebuilt `.so` in a post-build step:

```cmake
cmake_minimum_required(VERSION 3.22.1)
project("CPP_module")

set(SO_FILE ${CMAKE_CURRENT_SOURCE_DIR}/../jniLibs/${ANDROID_ABI}/libCPP_module.so)

add_library(${CMAKE_PROJECT_NAME} SHARED stub.c)

set_target_properties(${CMAKE_PROJECT_NAME} PROPERTIES
    OUTPUT_NAME ${CMAKE_PROJECT_NAME}
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_LIBRARY_OUTPUT_DIRECTORY})

add_custom_command(TARGET ${CMAKE_PROJECT_NAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different ${SO_FILE} $<TARGET_FILE:${CMAKE_PROJECT_NAME}>
    COMMENT "Replacing with prebuilt libCPP_module.so")
```

With this approach, the `.aar` correctly contains `prefab/modules/CPP_module/libs/android.<abi>/libCPP_module.so` along with the `abi.json` files.

PS: This bug is currently been tracked here: https://issuetracker.google.com/issues/491158080
