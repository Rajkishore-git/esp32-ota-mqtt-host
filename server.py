import http.server
import socketserver
import os

PORT = int(os.environ.get("PORT", 8000))
DIRECTORY = "firmware"

class RangeRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def send_head(self):
        path = self.translate_path(self.path)
        ctype = self.guess_type(path)
        if not os.path.isfile(path):
            self.send_error(404File not found")
            return None

        file = open(path, 'rb')
        fs = os.fstat(file.fileno())
        size = fs.st_size

        # Check for Range header
        range_header = self.headers.get('Range', None)
        if range_header:
            start, end = range_header.replace("bytes=", "").split("-")
            start = int(start)
            end = int(end) if end else size - 1
            length = end - start + 1

            self.send_response(206)
            self.send_header("Content-type", ctype)
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            self.send_header("Content-Length", str(length))
            self.end_headers()
            file.seek(start)
            return file
        else:
            self.send_response(200)
            self.send_header("Content-type", ctype)
            self.send_header("Content-Length", str(size))
            self.end_headers()
            return file

Handler = RangeRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

print(f"Serving at http://localhost:{PORT}")
httpd.serve_forever()
