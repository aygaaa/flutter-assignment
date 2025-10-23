import subprocess
import os
from .constants import ROOTPATH
from mutagen.mp3 import MP3

def split_audio_ffmpeg(input_file, chunk_duration=300, output_dir=None, ffmpeg_path=None):
    """
    Efficiently split an audio file using FFmpeg with optional custom FFmpeg path.
    
    :param input_file: Path to the input audio file
    :param chunk_duration: Duration of each chunk in seconds (default: 300 = 5 minutes)
    :param output_dir: Directory to save chunks (if None, creates a directory based on input filename)
    :param ffmpeg_path: Custom path to FFmpeg executable (optional)
    """
    # Determine FFmpeg executable
    if ffmpeg_path:
        # Use custom FFmpeg path
        ffmpeg_executable = os.path.join(ffmpeg_path, 'ffmpeg')
        # Add the custom path to system PATH temporarily
        os.environ['PATH'] = f"{ffmpeg_path}:{os.environ.get('PATH', '')}"
    else:
        # Use system FFmpeg
        ffmpeg_executable = 'ffmpeg'
    
    # Determine output directory
    if output_dir is None:
        base_filename = os.path.splitext(os.path.basename(input_file))[0]
        output_dir = f"{base_filename}_chunks"
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Construct FFmpeg command
    output_pattern = os.path.join(output_dir, '%d.mp3')
    
    ffmpeg_command = [
        ffmpeg_executable,
        '-i', input_file,        # Input file
        '-f', 'segment',         # Use segment muxer
        '-segment_time', str(chunk_duration),  # Duration of each segment
        '-c', 'copy',            # Copy codec to avoid re-encoding
        output_pattern           # Output filename pattern
    ]
    
    try:
        # Execute FFmpeg command
        result = subprocess.run(ffmpeg_command, check=True, stderr=subprocess.PIPE, text=True)
        print(f"Successfully split {input_file} into {chunk_duration}-second chunks in {output_dir}")
    
    except subprocess.CalledProcessError as e:
        print(f"Error splitting audio file: {e}")
        print(f"FFmpeg error output: {e.stderr}")
    except FileNotFoundError:
        print(f"FFmpeg not found. Please check the path: {ffmpeg_executable}")
        # Helpful debug information
        print("Current PATH:", os.environ.get('PATH', 'No PATH set'))
        print("Specified FFmpeg path:", ffmpeg_path or "Not specified")

def five_min_splitter(file, folder): # find the ffmpeg file
    custom_ffmpeg_path = None#f"{ROOTPATH}/models/ffmpeg" #/flet-reader\assets
    split_audio_ffmpeg(file, ffmpeg_path=custom_ffmpeg_path, output_dir= folder)

def get_duration(file):
    audio = MP3(file)
    return audio.info.length
