try:
    from moviepy.editor import VideoFileClip, ImageClip
    print("MoviePy导入成功！")
    
    # 测试创建一个简单的图片剪辑
    image_clip = ImageClip("input/images/speaker1.png")
    print("图片加载成功！")
    
except Exception as e:
    print(f"发生错误: {str(e)}") 