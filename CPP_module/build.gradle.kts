plugins {
    alias(libs.plugins.android.library)
}

android {
    namespace = "com.example.cpp_module"
    compileSdk = 36
    ndkVersion = "28.1.13356709"

    defaultConfig {
        minSdk = 24
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"

        externalNativeBuild {
            cmake {
                arguments += "-DANDROID_STL=none"
            }
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    externalNativeBuild {
        cmake {
            path = file("src/main/cpp/CMakeLists.txt")
            version = "3.22.1"
        }
    }

    buildFeatures {
        prefabPublishing = true
    }

    prefab {
        create("CPP_module") {
            headers = "src/main/cpp/include"
        }
    }
}

dependencies {
    // C++ only module - no Java/Kotlin dependencies
}