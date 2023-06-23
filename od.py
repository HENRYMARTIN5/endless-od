import http.server
import socketserver
import os

# Define the custom handler
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        moviecount = len(os.listdir("movies"))
        musiccount = len(os.listdir("music"))
        bookcount = len(os.listdir("books"))
        tvcount = len(os.listdir("tv"))
        audiobookcount = len(os.listdir("audiobooks"))
        allowed_dl_paths = ["/movies/", "/music/", "/books/", "/tv/", "/audiobooks/"]
        for path in allowed_dl_paths:
            if self.path.startswith(path):
                return http.server.SimpleHTTPRequestHandler.do_GET(self)
        allowed_paths = ["/", "/movies/", "/music/", "/books/", "/tv/", "/audiobooks/"]
        if self.path in allowed_paths:
            if self.path == "/":
                with open("index.html", "r") as f:
                    file = f.read()
                    file = file.replace("{{ moviecount }}", str(moviecount))
                    file = file.replace("{{ musiccount }}", str(musiccount))
                    file = file.replace("{{ bookcount }}", str(bookcount))
                    file = file.replace("{{ tvcount }}", str(tvcount))
                    file = file.replace("{{ audiobookcount }}", str(audiobookcount))
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(bytes(file, "utf-8"))
                    return
            else:
                return http.server.SimpleHTTPRequestHandler.do_GET(self)
        else:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"403 - Forbidden")

# Set the server configuration
port = 8092
handler = CustomHandler

# Create the server
with socketserver.TCPServer(("", port), handler) as httpd:
    print(f"Serving at port {port}")
    httpd.serve_forever()
