[app]
title = Presenter Toolkit
project_dir = .
input_file = src/prtools/__main__.py
exec_directory = dist
project_file =
icon =

[python]
python_path =
packages = Nuitka==4.0
android_packages =

[qt]
qml_files =
excluded_qml_plugins = QtQuick,QtQuick3D,QtCharts,QtWebEngine,QtTest,QtSensors
modules = Core,Gui,Svg,Widgets
plugins = iconengines,imageformats,platforms,styles

[android]
wheel_pyside =
wheel_shiboken =
plugins =

[nuitka]
macos.permissions = NSInputMonitoringUsageDescription:Display presentation keystrokes
mode = onefile
extra_args = --quiet --noinclude-qt-translations --include-package=prtools --include-package=pynput

[buildozer]
mode = debug
recipe_dir =
jars_dir =
ndk_path =
sdk_path =
local_libs =
arch =
