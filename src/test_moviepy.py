# 测试moviepy导入
try:
    from moviepy.editor import VideoFileClip
    print("moviepy导入成功！")
except Exception as e:
    print(f"导入错误: {str(e)}") 