import urllib.request
import socket
import os
import requests
import speedtest
import webbrowser
from dotenv import load_dotenv
from urllib.parse import quote_plus
import pywhatkit as kit

load_dotenv()

class Network: 
    def check_connection(self, input_text=""):
        """
        Testing internet connection
        """
        try:
            urllib.request.urlopen("http://www.google.com", timeout=5)
            return f"The internet connection is currently active, {os.getenv("USER_TITLE")}."
        except (urllib.error.URLError, socket.timeout):
            return f"The internet connection is not available, {os.getenv("USER_TITLE")}."

    def execute_speedtest(self, input_text=""):
        """
        playing speedtest after check internet connection
        """
        if self.check_connection():
            try: 
                st = speedtest.Speedtest()
                
                # download
                download_speed = st.download() / 1_000_000  
                
                # upload
                upload_speed = st.upload() / 1_000_000 

                result = f"Speed test completed. Download speed: {download_speed:.2f} Mbps, Upload speed: {upload_speed:.2f} Mbps."
                return result
            except Exception as e:
                return f"Error during speedtest {os.getenv("USER_TITLE")}."
        else:
            return f"I don't have access to the internet {os.getenv("USER_TITLE")}."

    def play_music(self, query):
        """
        Plays music on YouTube based on search query
        """
        if self.check_connection():
            try:
                kit.playonyt(query)
                return f"Playing {query} on YouTube {os.getenv("USER_TITLE")}."
            
            except Exception as e:
                return f"Error during playback: {str(e)}"
        else:
            return f"I don't have access to the internet {os.getenv("USER_TITLE")}."

    def search(self, query):
        """
        Execute a Google search
        """
        if self.check_connection():
            try:
                kit.search(query)
                return f"Search for '{query}' completed successfully {os.getenv("USER_TITLE")}."
            except Exception as e:
                return f"Search {query} failed {os.getenv("USER_TITLE")}."
        else:
            return f"I don't have access to the internet {os.getenv("USER_TITLE")}."