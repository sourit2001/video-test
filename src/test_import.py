import sys
print("Python路径:", sys.path)
print("\n尝试导入moviepy...")

try:
    import moviepy
    print("moviepy已安装在:", moviepy.__file__)
    from moviepy.editor import *
    print("成功导入moviepy.editor!")
except Exception as e:
    print("导入错误:", str(e)) 