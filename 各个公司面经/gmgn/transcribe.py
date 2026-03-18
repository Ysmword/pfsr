#!/usr/bin/env python3
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import sys

def transcribe_audio(file_path):
    """
    将音频文件转换为文本
    """
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"错误：文件 {file_path} 不存在")
        return None
    
    print(f"开始处理音频文件: {file_path}")
    
    # 初始化识别器
    r = sr.Recognizer()
    
    # 加载音频文件
    try:
        audio = AudioSegment.from_wav(file_path)
    except Exception as e:
        print(f"加载音频文件失败: {e}")
        # 尝试其他格式
        try:
            audio = AudioSegment.from_file(file_path)
        except Exception as e2:
            print(f"无法加载音频文件: {e2}")
            return None
    
    print(f"音频时长: {len(audio) / 1000:.2f} 秒")
    
    # 分割音频，避免内存问题
    # 每5分钟分割一次
    chunk_length_ms = 5 * 60 * 1000  # 5分钟
    chunks = []
    
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i + chunk_length_ms]
        chunks.append(chunk)
    
    print(f"音频分割为 {len(chunks)} 个片段")
    
    full_text = ""
    
    # 处理每个片段
    for i, chunk in enumerate(chunks):
        print(f"处理片段 {i+1}/{len(chunks)}...")
        
        # 导出为临时wav文件
        chunk.export(f"temp_chunk_{i}.wav", format="wav")
        
        # 使用speech_recognition处理
        with sr.AudioFile(f"temp_chunk_{i}.wav") as source:
            # 调整环境噪声
            r.adjust_for_ambient_noise(source)
            audio_data = r.record(source)
            
            try:
                # 使用Google Web Speech API
                text = r.recognize_google(audio_data, language='zh-CN')
                full_text += text + "\n"
                print(f"片段 {i+1} 转写完成")
            except sr.UnknownValueError:
                print(f"片段 {i+1}: Google Speech Recognition 无法理解音频")
                full_text += f"[片段 {i+1}: 无法识别]\n"
            except sr.RequestError as e:
                print(f"片段 {i+1}: Google Speech Recognition 服务错误; {e}")
                full_text += f"[片段 {i+1}: 服务错误]\n"
            except Exception as e:
                print(f"片段 {i+1}: 其他错误: {e}")
                full_text += f"[片段 {i+1}: 处理错误]\n"
        
        # 清理临时文件
        try:
            os.remove(f"temp_chunk_{i}.wav")
        except:
            pass
    
    return full_text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python3 transcribe.py <音频文件路径>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    text = transcribe_audio(audio_file)
    
    if text:
        output_file = os.path.splitext(audio_file)[0] + "_transcript.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"转写完成，结果已保存到: {output_file}")
        
        # 也打印前1000个字符预览
        print("\n=== 转写结果预览（前1000字符）===")
        print(text[:1000] + "..." if len(text) > 1000 else text)
    else:
        print("转写失败")