import os
from http.server import BaseHTTPRequestHandler, HTTPServer

# Path to your firmware binary file
FILE_PATH = "latest_firmware.bin"

class RangeHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Check if the requested file is the firmware binary
        if self.path == "/latest_firmware.bin":
            self.serve_file()
        else:
            self.send_error(404, "File not found")

    def serve_file(self):
        # Open the binary file
        try:
            file_size = os.path.getsize(FILE_PATH)
            # Check for Range request
            range_header = self.headers.get('Range')
            if range_header:
                # Parse the range header (e.g., "bytes=0-100")
                range_value = range_header.strip().replace("bytes=", "")
                byte_range = range_value.split("-")
                start_byte = int(byte_range[0])
                end_byte = int(byte_range[1]) if byte_range[1] else file_size - 1

                # Serve the partial file
                with open(FILE_PATH, 'rb') as f:
                    f.seek(start_byte)
                    data = f.read(end_byte - start_byte + 1)
                    self.send_response(206)
                    self.send_header("Content-Type", "application/octet-stream")
                    self.send_header("Content-Range", f"bytes {start_byte}-{end_byte}/{file_size}")
                    self.send_header("Content-Length", len(data))
                    self.end_headers()
                    self.wfile.write(data)
            else:
                # Serve the entire file
                with open(FILE_PATH, 'rb') as f:
                    data = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "application/octet-stream")
                    self.send_header("Content-Length", len(data))
                    self.end_headers()
                    self.wfile.write(data)
        except FileNotFoundError:
            self.send_error(404, "File not found")
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")

# Server setup
def run(server_class=HTTPServer, handler_class=RangeHTTPRequestHandler, port=8080):
    # Bind the server to all interfaces (0.0.0.0) so it's publicly accessible
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving at http://0.0.0.0:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
