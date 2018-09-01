#! /usr/bin/env python
import os
import sys
from colorfulPrint import generate

home = os.environ['HOME']
if home[len(home)-1:len(home)] == "/":
    home = home[0:len(home)-1]

# 检查环境
# java
if not os.system("java -version") == 0:
    print(generate("没有检测到 Java 环境。请安装。", 31))
    sys.exit(0)
else:
    print(generate("检测到 Java 环境。", 32))
# Android sdk
android_sdk = input("请输入 Android Sdk 路径：\n")
if not os.path.exists(android_sdk):
    print(generate("路径不存在", 31))
    if os.path.exists(os.environ["ANDROID_HOME"]):
        print(generate("已从环境变量中读取", 32))
        android_sdk = os.environ["ANDROID_HOME"]
    else:
        sys.exit(0)
else:
    print(generate("路径存在", 32))
# git
if not os.system("which git") == 0:
    print(generate("没有安装 git，请安装。", 31))
    sys.exit(0)

os.chdir(home)
# 克隆源码
if os.path.exists(home+"/Mindustry"):
    print(generate("家目录下已存在 Mindustry 文件夹，将直接使用此目录", 32))
else:
    print(generate("开始克隆源码，时间可能较长，请耐心等待。\n网速太慢可以尝试科学上网。", 32))
    if os.system("git clone https://github.com/Anuken/Mindustry.git") == 0:
        print(generate("克隆完成", 32))
    else:
        print(generate("失败，可能需要科学上网。", 31))
        sys.exit(0)

os.chdir("Mindustry")

# 进行配置
print("添加 local.properties")
f = open("local.properties", "w")
f.write("sdk.dir="+android_sdk)
f.close()


def key():
    if ".keystore" not in os.popen("ls android").read() or "RELEASE" in open("android/build.gradle", "r").read():
        print(generate("将使用keytool工具生成签名", 33))
        store_password = input("密钥库密码")
        key_password = input("私钥密码")
        command = """keytool -genkey -alias android.keystore -storepass %s -keypass %s -dname CN=cn -keyalg RSA -validity 20000 -keystore android/android.keystore""" % (store_password, key_password)
        print(command)
        os.system(command)
        print(generate("正在更改 build.gradle", 32))
        build = open("android/build.gradle", "r")
        build_content = build.read()
        build.close()
        build_content = build_content.replace("""project.hasProperty("RELEASE_STORE_FILE")""", "true")
        build_content = build_content.replace("""RELEASE_STORE_FILE""", "\"android.keystore\"")
        build_content = build_content.replace("""RELEASE_STORE_PASSWORD""", "\"" + store_password + "\"")
        build_content = build_content.replace("""RELEASE_KEY_PASSWORD""", "\"" + key_password + "\"")
        build_content = build_content.replace("""RELEASE_KEY_ALIAS""", "\"android.keystore\"")
        build = open("android/build.gradle", "w")
        build.write(build_content)
        build.close()
        print(generate("更改完成", 32))


def run_client():
    print(generate("请输入 root 用户密码", 33))
    command = "sudo ./gradlew desktop:run"
    os.system(command)


def build_client():
    print(generate("请输入 root 用户密码", 33))
    command = "sudo ./gradlew desktop:dist"
    if os.system(command) == 0:
        print(generate("构建完成", 32))
        if os.system("cp desktop/build/libs/desktop-release.jar .") == 0:
            print(generate("已将 jar 复制到 "+home+"/Mindustry/desktop-release.jar", 32))


def run_android():
    key()
    input("请打开手机的USB调试，并连接到电脑，按任意键继续...")
    print(generate("请输入 root 用户密码", 33))
    command = "sudo ./gradlew android:run"
    os.system(command)


def build_android():
    key()
    print(generate("请输入 root 用户密码", 33))
    command = "sudo ./gradlew android:deploy"
    os.system(command)
    print(generate("安装包在 deploy/ 下", 32))


op = int(input("请输入对应的序号：\n1.运行 PC 版客户端\n2.编译 PC 版客户端\n3.运行安卓版客户端\n4.编译安卓版客户端\n->"))
if op in range(0, 5):
    if op == 1:
        run_client()
    elif op == 2:
        build_client()
    elif op == 3:
        run_android()
    elif op == 4:
        build_android()
else:
    print(generate("无效的输入",31))
    sys.exit(0)
