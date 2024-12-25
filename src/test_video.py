from moviepy.editor import AudioFileClip
from video_generator import VideoGenerator

def get_audio_duration(audio_path):
    """获取音频文件的精确时长"""
    audio = AudioFileClip(audio_path)
    duration = audio.duration
    audio.close()
    return duration

def test_video_generation():
    # 图片路径（说话人0和说话人1的图片）
    image_paths = [
        "input/images/speaker1.png",
        "input/images/speaker2.png"
    ]
    
    # 音频文件路径
    audio_path = "input/audio/面包店.mp3"
    
    # 输出视频路径
    output_path = "output/output.mp4"
    
    # 说话人片段时间点（精确到毫秒）
    segments = [
        (0.000, 3.400, 1),    # "Good morning. What's fresh today?"
        (3.400, 7.800, 0),    # "Morning, Lily. Our blueberry muffins just came out of the oven. They're still warm."
        (7.800, 13.000, 1),   # "Yum, I'll take two. And do you have any croissants left?"
        (13.000, 18.000, 0),  # "Absolutely. We've got plain and almond. Which would you prefer?"
        (18.000, 22.900, 1),  # "I'll go with an almond one. Thanks."
        (22.900, 27.000, 0),  # "Sure thing. Would you like that extra hot?"
        (27.000, 31.000, 1),  # "No, just regular is fine. Thanks, Mike."
        (31.000, 34.500, 0),  # "You're welcome."
    ]
    
    # 加载音频并获取实际时长
    audio_duration = get_audio_duration(audio_path)
    print(f"音频加载成功：时长 {audio_duration}秒\n")
    
    # 打印说话片段信息
    print("说话片段信息：")
    for i, (start, end, speaker_id) in enumerate(segments):
        duration = end - start
        print(f"片段 {i+1}: 说话者{speaker_id}, 开始:{start:.3f}秒, 结束:{end:.3f}秒, 持续:{duration:.3f}秒")
    
    # 创建视频生成器并生成视频
    generator = VideoGenerator(image_paths, audio_path, output_path)
    generator.create_video(segments)

if __name__ == "__main__":
    test_video_generation() 