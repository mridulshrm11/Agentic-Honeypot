from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from detector import is_scam
from agent_loop import run_honeypot

app = FastAPI(title="Agentic Honeypot API")

API_KEY = "honeypot-cyber_sorcers-123"


class Message(BaseModel):
    message: str


@app.get("/")
def home():
    return {"status": "Agentic Honeypot Running"}


def mock_scammer_api(msg):
    return "Send money to UPI abc@upi and account 123456789012 IFSC SBIN0001234 https://fake-link.com"


from fastapi import Request

@app.post("/honeypot")
async def honeypot(
    request: Request,
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Try to read JSON first
    try:
        data = await request.json()
        message = data.get("message", "")
    except:
        # If not JSON, read raw body
        message = (await request.body()).decode("utf-8")

    if not is_scam(message):
        return {"is_scam": False}

    result = run_honeypot(message, mock_scammer_api)

    return {
        "is_scam": True,
        "persona_used": "confused_upi_user",
        **result
    }

