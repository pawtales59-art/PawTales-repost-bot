import os
import schedule
import time
from instagrapi import Client as InstaClient
import requests
import anthropic

class FullyAutoBot:
    def __init__(self):
        self.claude_client = anthropic.Anthropic()
        self.insta_user = os.getenv("INSTA_USER")
        self.insta_pass = os.getenv("INSTA_PASS")
        self.fb_token = os.getenv("FB_TOKEN")
        self.fb_page_id = os.getenv("FB_PAGE_ID")
    
    def generate_story_claude(self):
        """Claude se story generate karo"""
        message = self.claude_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": """Create a funny 2-3 minute Kutta-Billi 
                    (puppy and kitten) cartoon story. 
                    Include dialogue and actions. 
                    Make it cute and funny for kids."""
                }
            ]
        )
        return message.content[0].text
    
    def generate_captions_claude(self, story):
        """Claude se captions generate karo"""
        message = self.claude_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=200,
            messages=[
                {
                    "role": "user",
                    "content": f"""Create 3 Instagram captions for this 
                    Kutta-Billi story: {story}
                    Include emojis, hashtags."""
                }
            ]
        )
        return message.content[0].text
    
    def post_to_instagram(self, image_path, caption):
        """Instagram par post karo"""
        try:
            cl = InstaClient()
            cl.login(self.insta_user, self.insta_pass)
            cl.photo_upload(image_path, caption=caption)
            print(f"✅ Instagram Posted!")
            cl.logout()
        except Exception as e:
            print(f"❌ Instagram Error: {e}")
    
    def post_to_facebook(self, image_path, caption):
        """Facebook par post karo"""
        try:
            url = f"https://graph.facebook.com/v18.0/{self.fb_page_id}/photos"
            with open(image_path, 'rb') as img:
                files = {'source': img}
                data = {
                    'message': caption,
                    'access_token': self.fb_token
                }
                response = requests.post(url, files=files, data=data)
            if response.status_code == 200:
                print(f"✅ Facebook Posted!")
        except Exception as e:
            print(f"❌ Facebook Error: {e}")
    
    def schedule_posts(self):
        """Posts schedule karo"""
        schedule.every().day.at("09:00").do(
            self.post_to_instagram,
            "content/morning.jpg",
            "🐶 Paw Tales 🐱 #PawTales"
        )
        schedule.every().day.at("18:00").do(
            self.post_to_instagram,
            "content/evening.jpg",
            "🐾 Paw Tales Forever! #Cute"
        )
        schedule.every().day.at("12:00").do(
            self.post_to_facebook,
            "content/facebook.jpg",
            "🐶 Paw Tales 🐱 #PawTales"
        )
        
        print("🤖 Bot Scheduled!")
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    bot = FullyAutoBot()
    print("🤖 Bot Starting...")
    bot.schedule_posts()
    
