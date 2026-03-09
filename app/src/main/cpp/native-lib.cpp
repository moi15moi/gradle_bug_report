#include <jni.h>
#include <string>
#include "c_file.h"

extern "C" JNIEXPORT jstring JNICALL
Java_com_example_myapplication_MainActivity_stringFromJNI(
        JNIEnv* env,
        jobject /* this */) {
    std::string hello = std::string(get_hello_world_string());
    return env->NewStringUTF(hello.c_str());
}