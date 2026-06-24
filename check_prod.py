import urllib.request
import re

url = "https://prisme-yh16.onrender.com/"
try:
    html = urllib.request.urlopen(url).read().decode("utf-8")
    imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', html)
    print("\n".join(imgs))
except Exception as e:
    print("Error:", e)
