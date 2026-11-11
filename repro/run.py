"""Same chat call through each documented Python wrapper while TTC fails three ways."""
import json, logging, sys, httpx
from openai import OpenAI
from anthropic import Anthropic
from thetokencompany.openai import with_compression as wrap_openai
from thetokencompany.anthropic import with_compression as wrap_anthropic
import thetokencompany
logging.basicConfig(level=logging.WARNING, format="    log: %(message)s")
STUB = "http://127.0.0.1:8765"
MSGS = [{"role": "user", "content": "Summarize: the quarterly report shows revenue grew while costs stayed flat."}]

def failures():
    # 1. real TTC API, key revoked/typo'd -> real HTTP 401 from api.thetokencompany.com
    yield "real API, invalid key (401)", "ttc-invalid", None
    # 2. TTC API returns 503 (outage), via a caller-supplied httpx client
    t = httpx.MockTransport(lambda r: httpx.Response(503, json={"detail": "Service Unavailable"}))
    yield "TTC 503 (outage)", "ttc-x", t
    # 3. TTC unreachable (DNS/network), via a dead proxy
    yield "TTC unreachable", "ttc-x", httpx.HTTPTransport(proxy="http://127.0.0.1:9")

print("the-token-company", thetokencompany.__version__ if hasattr(thetokencompany, "__version__") else "?")
for name, key, transport in failures():
    print(f"\n== {name}")
    for label in ("openai", "anthropic"):
        hc = httpx.Client(transport=transport) if transport else None
        try:
            if label == "openai":
                c = wrap_openai(OpenAI(base_url=STUB + "/v1", api_key="sk-stub"), compression_api_key=key, http_client=hc)
                r = c.chat.completions.create(model="gpt-4o-mini", messages=MSGS)
                out = r.choices[0].message.content
            else:
                c = wrap_anthropic(Anthropic(base_url=STUB, api_key="sk-stub"), compression_api_key=key, http_client=hc)
                r = c.messages.create(model="claude-sonnet-4-6", max_tokens=50, messages=MSGS)
                out = r.content[0].text
            print(f"  {label:9s} OK    -> {out!r}")
        except Exception as e:
            print(f"  {label:9s} RAISED {type(e).__module__}.{type(e).__name__}: {str(e)[:90]}")
print("\nLLM requests that reached the stub:", httpx.get(STUB).json())
