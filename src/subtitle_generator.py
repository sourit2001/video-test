import whisper

class SubtitleGenerator:
    def __init__(self):
        print("加载语音识别模型...")
        self.model = whisper.load_model("base")
    
    def generate_subtitles(self, audio_path):
        print("开始识别音频...")
        result = self.model.transcribe(
            audio_path,
            language="en",
            task="transcribe",
            fp16=False,
            condition_on_previous_text=True,
            temperature=0.0,
            best_of=1,
            initial_prompt="This is a conversation in English between a customer and a barista."
        )
        
        segments = []
        for segment in result["segments"]:
            segments.append({
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"].strip()
            })
            
        print("\n识别到的字幕段落：")
        for i, segment in enumerate(segments):
            print(f"段落 {i+1}: [{segment['start']:.1f}s - {segment['end']:.1f}s]: {segment['text']}")
        
        return segments 