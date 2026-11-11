# the-token-company: OpenAI wrapper fallback (unofficial demo)

In the Python SDK (`the-token-company` 0.5.1, PyPI), `thetokencompany.openai.with_compression(OpenAI())`
lets any compression failure raise out of `chat.completions.create`, so the OpenAI or OpenRouter
request is never sent. The Anthropic wrapper in the same package, and all three Node wrappers, catch
it, log `TTC compression failed (...); sending uncompressed.` and send the original messages, as
commit [1176c36](https://github.com/TheTokenCompany/the-token-company-python/commit/1176c3689720c858a184c4114db72fbff8895d7e) intended.

- Fix branch: https://github.com/TheTokenCompany/the-token-company-python/compare/main...cherylaurelia:the-token-company-python:fix/openai-graceful-degradation
- Fork CI (Python 3.10 to 3.13): https://github.com/cherylaurelia/the-token-company-python/actions/runs/43061185204

## Repro (no TTC account needed)

```
python -m venv .venv && .venv/bin/pip install the-token-company==0.5.1 openai anthropic
.venv/bin/python repro/stub.py 8765 &   # local OpenAI/Anthropic-compatible stub LLM
.venv/bin/python repro/run.py           # same call, 3 TTC failures, both wrappers
.venv/bin/python repro/run_async.py     # AsyncOpenAI with a bad key
```

Recorded output: `repro/run-0.5.1.txt` (published package) and `repro/run-patched.txt` (fix branch
installed editable). The bad-key case gets a real 401 from api.thetokencompany.com. The LLM is a
local stub, not OpenAI, and the success path with a real key was not tested.

## Page

Next.js + Tailwind, one static page: `npm install && npm run build && npm run start`.

Unofficial demo by Cheryl Aurelia: not affiliated with The Token Company.
