"""AsyncOpenAI through the wrapper with a real 401 from api.thetokencompany.com."""
import asyncio, logging
from openai import AsyncOpenAI
from thetokencompany.openai import with_compression
logging.basicConfig(level=logging.WARNING, format="    log: %(message)s")
async def main():
    c = with_compression(AsyncOpenAI(base_url="http://127.0.0.1:8765/v1", api_key="sk-stub"), compression_api_key="ttc-invalid")
    try:
        r = await c.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": "hi there, summarize this"}])
        print("  async openai OK    ->", repr(r.choices[0].message.content))
    except Exception as e:
        print(f"  async openai RAISED {type(e).__name__}: {e}")
asyncio.run(main())
