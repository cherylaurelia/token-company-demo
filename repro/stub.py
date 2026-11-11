"""Local OpenAI- and Anthropic-compatible stub LLM: counts requests that reach it."""
import json, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
HITS = {"openai": 0, "anthropic": 0}
class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        self._send(200, HITS)
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("content-length", 0))) or b"{}")
        if self.path.endswith("/chat/completions"):
            HITS["openai"] += 1
            self._send(200, {"id": "c1", "object": "chat.completion", "created": 0, "model": body.get("model"),
                "choices": [{"index": 0, "finish_reason": "stop", "message": {"role": "assistant", "content": "stub answer"}}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 2, "total_tokens": 12}})
        elif self.path.endswith("/messages"):
            HITS["anthropic"] += 1
            self._send(200, {"id": "m1", "type": "message", "role": "assistant", "model": body.get("model"),
                "content": [{"type": "text", "text": "stub answer"}], "stop_reason": "end_turn", "stop_sequence": None,
                "usage": {"input_tokens": 10, "output_tokens": 2}})
        else:
            self._send(404, {})
    def _send(self, code, obj):
        b = json.dumps(obj).encode(); self.send_response(code)
        self.send_header("content-type", "application/json"); self.send_header("content-length", str(len(b)))
        self.end_headers(); self.wfile.write(b)
ThreadingHTTPServer(("127.0.0.1", int(sys.argv[1])), H).serve_forever()
