from audio_processor import AudioProcessor
import os

def test_audio_processor():
    # 获取当前目录的绝对路径
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 构建音频文件的完整路径
    audio_path = os.path.join(current_dir, "input", "audio", "面包店.mp3")
    
    print(f"尝试打开音频文件: {audio_path}")
    
    try:
        # 创建音频处理器实例
        processor = AudioProcessor(audio_path)
        
        # 获取说话者片段
        segments = processor.get_speaker_segments()
        
        # 打印结果
        print("\n检测到的对话片段：")
        for start, end, speaker_id in segments:
            print(f"说话者 {speaker_id}: {start:.2f}秒 - {end:.2f}秒")
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    test_audio_processor() 