"""
Run the FastAPI server for BloodFlow AI.
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "bloodflow_ai.api_server:app",  # ← Updated import
        host="0.0.0.0",
        port=8000,
        reload=True
    )