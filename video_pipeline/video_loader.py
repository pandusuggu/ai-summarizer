import yt_dlp
import os
import shutil
from pathlib import Path

class VideoLoader:
    def __init__(self, output_dir="outputs/raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_video(self, source: str) -> str:
        """
        Loads video from a local path or downloads it from YouTube.
        Returns the absolute path to the video file.
        """
        if os.path.exists(source):
            # It's a local file
            dest = self.output_dir / os.path.basename(source)
            if not dest.exists():
                shutil.copy(source, dest)
            return str(dest.absolute())
        
        if source.startswith(("http://", "https://")):
            # It's a URL
            return self.download_youtube(source)
        
        raise ValueError(f"Invalid video source: {source}")

    def download_youtube(self, url: str) -> str:
        """Downloads video from YouTube using yt-dlp."""
        # Use more flexible format selection
        ydl_opts = {
            'outtmpl': str(self.output_dir / '%(id)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'format': 'best[ext=mp4]/best[height<=720]/best',  # More flexible format selection
            'ignoreerrors': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=True)
                if info is None:
                    raise RuntimeError("yt-dlp returned None for video info.")
                
                # Check for various filename locations
                video_path = ydl.prepare_filename(info)
                
                # Some videos might have changed extensions during download (e.g. .mkv to .mp4)
                # Let's verify the file exists on disk
                if not os.path.exists(video_path):
                    stem = Path(video_path).stem
                    possible_files = list(self.output_dir.glob(f"{stem}.*"))
                    if possible_files:
                        video_path = str(possible_files[0])
                    else:
                        # Try to find any file with the video ID
                        video_id = info.get('id', '')
                        if video_id:
                            possible_files = list(self.output_dir.glob(f"{video_id}.*"))
                            if possible_files:
                                video_path = str(possible_files[0])
                            else:
                                raise RuntimeError(f"Downloaded file not found for video {video_id}")
                
                return str(Path(video_path).absolute())
            except Exception as e:
                print(f"yt-dlp error: {e}")
                # Try with even more basic format selection as fallback
                try:
                    fallback_opts = {
                        'outtmpl': str(self.output_dir / '%(id)s.%(ext)s'),
                        'noplaylist': True,
                        'quiet': True,
                        'no_warnings': True,
                        'format': 'worst',  # Fallback to worst quality
                        'ignoreerrors': True,
                    }
                    with yt_dlp.YoutubeDL(fallback_opts) as ydl_fallback:
                        info = ydl_fallback.extract_info(url, download=True)
                        video_path = ydl_fallback.prepare_filename(info)
                        if not os.path.exists(video_path):
                            stem = Path(video_path).stem
                            possible_files = list(self.output_dir.glob(f"{stem}.*"))
                            if possible_files:
                                video_path = str(possible_files[0])
                        return str(Path(video_path).absolute())
                except Exception as fallback_e:
                    raise RuntimeError(f"YouTube Download Error: {str(e)} (Fallback also failed: {str(fallback_e)})")

if __name__ == "__main__":
    # Test
    loader = VideoLoader()
    # Path might need adjustment for testing
    print("Video loader initialized.")
