try:
    import moviepy
    from moviepy.editor import *
    print("MoviePy版本:", moviepy.__version__)
    print("MoviePy导入成功!")
except Exception as e:
    print("错误:", str(e)) 