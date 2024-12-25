from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, TextClip, ColorClip
from PIL import Image
from subtitle_generator import SubtitleGenerator

class VideoGenerator:
    def __init__(self, image_paths, audio_path, output_path):
        self.image_paths = image_paths
        self.audio_path = audio_path
        self.output_path = output_path
        self.subtitle_generator = SubtitleGenerator()
        
        with Image.open(image_paths[0]) as img:
            self.size = img.size
            print(f"视频尺寸将设置为：{self.size[0]}x{self.size[1]}")

    def create_subtitle_clip(self, text, duration, start, video_size):
        txt_clip = TextClip(
            text,
            fontsize=45,
            font='Arial-Bold',
            color='black',
            bg_color='yellow',
            size=(video_size[0] - 80, None),
            method='caption',
            align='center'
        )
        
        txt_clip = txt_clip.set_duration(duration).set_start(start)
        txt_clip = txt_clip.set_position(('center', video_size[1] - txt_clip.h - 80))
        return txt_clip

    def split_subtitle_at_time(self, sub, split_time):
        """在指定时间点分割字幕，考虑对话的自然切换点"""
        if split_time <= sub["start"] or split_time >= sub["end"]:
            return [sub]
            
        # 计算时间比例
        total_duration = sub["end"] - sub["start"]
        split_ratio = (split_time - sub["start"]) / total_duration
        text = sub["text"]
        
        # 定义对话切换标记
        dialogue_markers = ['. ', '? ', '! ', '... ']
        greeting_markers = ['Good morning', 'Morning', 'Hello', 'Hi']
        response_markers = ['Thanks', 'Thank you', 'Sure', 'Okay', 'Yes', 'No']
        
        # 尝试在对话自然切换点分割
        for marker in dialogue_markers:
            parts = text.split(marker)
            if len(parts) > 1:
                # 找到最接近时间分割点的切换点
                accumulated_length = 0
                target_length = len(text) * split_ratio
                
                for i in range(len(parts) - 1):
                    part_length = len(parts[i] + marker)
                    if accumulated_length + part_length >= target_length:
                        # 在这里分割
                        first_part = marker.join(parts[:i+1])
                        second_part = marker.join(parts[i+1:])
                        
                        # 检查是否包含问候语或回应语
                        for g_marker in greeting_markers:
                            if g_marker in second_part and g_marker not in first_part:
                                # 调整分割点到问候语开始
                                split_index = second_part.index(g_marker)
                                first_part = text[:text.rindex(second_part) + split_index].strip()
                                second_part = text[text.rindex(second_part) + split_index:].strip()
                                
                        for r_marker in response_markers:
                            if r_marker in second_part and r_marker not in first_part:
                                # 调整分割点到回应语开始
                                split_index = second_part.index(r_marker)
                                first_part = text[:text.rindex(second_part) + split_index].strip()
                                second_part = text[text.rindex(second_part) + split_index:].strip()
                        
                        # 计算实际的时间分割点
                        time_ratio = len(first_part) / len(text)
                        actual_split_time = sub["start"] + (total_duration * time_ratio)
                        
                        return [
                            {
                                "text": first_part,
                                "start": sub["start"],
                                "end": actual_split_time
                            },
                            {
                                "text": second_part,
                                "start": actual_split_time,
                                "end": sub["end"]
                            }
                        ]
                    accumulated_length += part_length
        
        # 如果没有找到自然切换点，使用简单的时间比例分割
        words = text.split()
        split_index = int(len(words) * split_ratio)
        
        # 确保不会在问候语或回应语中间分割
        for i in range(split_index - 2, split_index + 3):
            if 0 <= i < len(words):
                combined_words = ' '.join(words[max(0, i-1):min(len(words), i+2)])
                for marker in greeting_markers + response_markers:
                    if marker in combined_words:
                        # 调整分割点到标记词之前或之后
                        if i < split_index:
                            split_index = max(0, i-1)
                        else:
                            split_index = min(len(words), i+2)
        
        first_part = ' '.join(words[:split_index])
        second_part = ' '.join(words[split_index:])
        
        return [
            {
                "text": first_part,
                "start": sub["start"],
                "end": split_time
            },
            {
                "text": second_part,
                "start": split_time,
                "end": sub["end"]
            }
        ]

    def create_video(self, speaker_segments):
        try:
            audio = AudioFileClip(self.audio_path)
            audio_duration = audio.duration
            print(f"音频实际时长: {audio_duration:.3f}秒")
            
            # 调整说话人片段，确保精确的时间点
            adjusted_segments = []
            for start, end, speaker_id in speaker_segments:
                if start >= audio_duration:
                    continue
                # 精确到毫秒
                start = round(start, 3)
                end = min(round(end, 3), audio_duration)
                if end > start:
                    adjusted_segments.append((start, end, speaker_id))
            
            # 创建基础视频片段，确保精确的切换时间
            base_clips = []
            for i, (start, end, speaker_id) in enumerate(adjusted_segments):
                duration = round(end - start, 3)
                
                print(f"创建图片片段 {i+1}: 说话者{speaker_id}")
                print(f"开始:{start:.3f}秒, 结束:{end:.3f}秒, 持续:{duration:.3f}秒")
                
                # 创建图片片段，确保精确的时间控制
                image_path = self.image_paths[1 - speaker_id]
                clip = (ImageClip(image_path)
                       .set_start(start)
                       .set_duration(duration))
                base_clips.append(clip)
            
            # 获取字幕
            print("识别字幕...")
            subtitles = self.subtitle_generator.generate_subtitles(self.audio_path)
            subtitle_clips = []
            
            # 调试信息
            print("\n处理字幕段落:")
            
            # 处理每个字幕
            for sub_index, sub in enumerate(subtitles):
                if sub["start"] >= audio_duration:
                    continue
                    
                sub_end = min(sub["end"], audio_duration)
                if sub_end <= sub["start"]:
                    continue
                
                print(f"\n处理字幕 {sub_index + 1}:")
                print(f"原始文本: {sub['text']}")
                print(f"时间: {sub['start']:.1f}s - {sub['end']:.1f}s")
                
                # 找到这个字幕对应的所有说话人片段
                relevant_segments = []
                for seg_start, seg_end, speaker_id in adjusted_segments:
                    if (seg_start <= sub_end and seg_end >= sub["start"]):
                        relevant_segments.append((seg_start, seg_end, speaker_id))
                
                # 如果字幕跨越了说话人切换点
                if len(relevant_segments) > 1:
                    print(f"字幕跨越了 {len(relevant_segments)} 个说话人片段")
                    current_text = sub["text"]
                    current_start = sub["start"]
                    
                    for i, (seg_start, seg_end, speaker_id) in enumerate(relevant_segments):
                        # 计算这个片段的结束时间
                        if i < len(relevant_segments) - 1:
                            end_time = relevant_segments[i + 1][0]
                        else:
                            end_time = min(sub_end, seg_end)
                        
                        # 确保时间点有效
                        if end_time <= current_start:
                            continue
                        
                        # 创建字幕片段
                        segment_duration = end_time - current_start
                        if segment_duration > 0:
                            print(f"创建字幕片段: {current_text}")
                            print(f"时间: {current_start:.1f}s - {end_time:.1f}s")
                            
                            subtitle_clip = self.create_subtitle_clip(
                                current_text,
                                segment_duration,
                                current_start,
                                self.size
                            )
                            subtitle_clips.append(subtitle_clip)
                        
                        current_start = end_time
                else:
                    # 单个说话人的字幕
                    print("单个说话人字幕")
                    for seg_start, seg_end, speaker_id in adjusted_segments:
                        if seg_start <= sub["start"] < seg_end:
                            sub_duration = min(sub_end, seg_end) - sub["start"]
                            if sub_duration > 0:
                                print(f"创建字幕: {sub['text']}")
                                print(f"时间: {sub['start']:.1f}s - {min(sub_end, seg_end):.1f}s")
                                
                                subtitle_clip = self.create_subtitle_clip(
                                    sub["text"],
                                    sub_duration,
                                    sub["start"],
                                    self.size
                                )
                                subtitle_clips.append(subtitle_clip)
                            break
            
            print("\n合并所有片段...")
            base_video = CompositeVideoClip(base_clips, size=self.size)
            
            if subtitle_clips:
                final_clip = CompositeVideoClip([base_video] + subtitle_clips)
            else:
                final_clip = base_video
            
            print("添加音频...")
            final_clip = final_clip.set_audio(audio)
            final_clip = final_clip.set_duration(audio_duration)
            
            print("正在生成视频...")
            final_clip.write_videofile(
                self.output_path,
                fps=30,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile="temp-audio.m4a",
                remove_temp=True,
                audio=True,
                threads=8,
                preset='ultrafast',
                bitrate='3000k'
            )
            
            final_clip.close()
            audio.close()
            
            print(f"视频已成功生成：{self.output_path}")
            
        except Exception as e:
            print(f"视频生成失败：{str(e)}")
            raise

