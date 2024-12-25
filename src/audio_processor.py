from pydub import AudioSegment
import numpy as np

class AudioProcessor:
    def __init__(self, audio_path):
        self.audio = AudioSegment.from_mp3(audio_path)
        print(f"音频加载成功：时长 {self.audio.duration_seconds}秒")

    def get_speaker_segments(self):
        # 将音频转换为numpy数组
        samples = np.array(self.audio.get_array_of_samples())
        
        # 预定义的关键时间点（根据实际对话调整）
        key_points = [
            0.0,    # 开始
            3.4,    # 第一次切换
            8.4,    # 第二次切换
            13.8,   # 第三次切换（调整这里）
            19.5,   # 第四次切换
            22.9,   # 第五次切换
            27.0,   # 第六次切换
            31.0,   # 第七次切换
            34.5,   # 第八次切换
            37.6,   # 第九次切换
            41.0,   # 第十次切换
            45.4,   # 第十一次切换
            52.4,   # 第十二次切换
            59.0,   # 第十三次切换
            self.audio.duration_seconds  # 结束
        ]
        
        # 生成说话片段
        segments = []
        current_speaker = 1  # 从speaker1开始
        
        for i in range(len(key_points) - 1):
            start_time = key_points[i]
            end_time = key_points[i + 1]
            
            if end_time - start_time >= 2.0:  # 最小2秒
                segments.append((start_time, end_time, current_speaker))
                current_speaker = 1 - current_speaker
        
        # 打印分段信息
        print("\n说话片段信息：")
        for i, (start, end, speaker) in enumerate(segments):
            duration = end - start
            print(f"片段 {i+1}: 说话者{speaker}, 开始:{start:.1f}秒, 结束:{end:.1f}秒, 持续:{duration:.1f}秒")
        
        return segments
