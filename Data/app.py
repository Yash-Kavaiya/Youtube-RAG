import yt_dlp
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_audio_with_selenium(video_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(video_url)
        
        # Wait for the video player to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "movie_player"))
        )
        
        # Simulate human-like behavior
        time.sleep(random.uniform(2, 5))
        
        # Get the page source after JavaScript has loaded
        page_source = driver.page_source
        
        # Use yt-dlp to extract audio URL from the page source
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'audio.%(ext)s',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            audio_url = info['url']
        
        return audio_url
    
    finally:
        driver.quit()

def main():
    video_url = input("Enter the YouTube video URL: ")
    
    try:
        audio_url = get_audio_with_selenium(video_url)
        print(f"Audio URL: {audio_url}")
        # You can now download the audio using this URL
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()