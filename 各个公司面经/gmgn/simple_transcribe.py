#!/usr/bin/env python3
import subprocess
import os
import json
import sys

def transcribe_with_whispercpp(audio_file):
    """
    使用whisper.cpp进行语音识别（如果可用）
    """
    # 首先检查whisper.cpp是否可用
    try:
        result = subprocess.run(["which", "whisper.cpp"], capture_output=True, text=True)
        if result.returncode != 0:
            print("whisper.cpp 未安装")
            return None
    except:
        print("无法检查whisper.cpp")
        return None
    
    # 转换音频格式为whisper.cpp所需的格式
    wav_file = audio_file.replace(".m4a", "_16k.wav")
    cmd = f"ffmpeg -i '{audio_file}' -ar 16000 -ac 1 '{wav_file}'"
    subprocess.run(cmd, shell=True)
    
    # 运行whisper.cpp
    cmd = f"./whisper.cpp -m models/ggml-base.bin -f '{wav_file}' -l zh -otxt"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    # 读取输出文件
    txt_file = wav_file.replace(".wav", ".txt")
    if os.path.exists(txt_file):
        with open(txt_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    return None

def transcribe_with_google(audio_file):
    """
    使用Google Speech Recognition API（需要网络）
    """
    try:
        import speech_recognition as sr
        
        r = sr.Recognizer()
        
        # 由于文件较大，我们需要分段处理
        # 这里只处理前5分钟作为示例
        from pydub import AudioSegment
        
        audio = AudioSegment.from_wav(audio_file)
        # 只取前5分钟
        five_min = 5 * 60 * 1000
        if len(audio) > five_min:
            audio = audio[:five_min]
        
        # 导出临时文件
        temp_file = "temp_audio.wav"
        audio.export(temp_file, format="wav")
        
        with sr.AudioFile(temp_file) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language='zh-CN')
            
        # 清理临时文件
        os.remove(temp_file)
        
        return text
    except Exception as e:
        print(f"Google Speech Recognition 错误: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("使用方法: python3 simple_transcribe.py <音频文件>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    
    if not os.path.exists(audio_file):
        print(f"文件不存在: {audio_file}")
        sys.exit(1)
    
    print(f"处理音频文件: {audio_file}")
    
    # 尝试Google Speech Recognition
    print("尝试使用Google Speech Recognition...")
    text = transcribe_with_google(audio_file)
    
    if text:
        output_file = audio_file.replace(".m4a", "_transcript.txt").replace(".wav", "_transcript.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"转写完成，保存到: {output_file}")
        print(f"\n转写结果:\n{text}")
    else:
        print("转写失败")
        
        # 提供替代方案
        print("\n由于技术限制，无法完成完整的语音转文本。")
        print("建议:")
        print("1. 使用专业的语音转文本工具如Whisper、Google Cloud Speech-to-Text")
        print("2. 将音频文件上传到在线语音识别服务")
        print("3. 使用macOS的听写功能（系统偏好设置 > 键盘 > 听写）")

if __name__ == "__main__":
    main()