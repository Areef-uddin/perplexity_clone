import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from pydantic_models.chat_body import ChatBody
from services.llm_service import LLMService
from services.sort_source_service import SortSourceService
from services.search_service import SearchService


app = FastAPI()


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://perplexityclone-ae6ac.web.app",
        "https://perplexityclone-ae6ac.firebaseapp.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


search_service = SearchService()
sort_source_service = SortSourceService()
llm_service = LLMService()


# Chat WebSocket
@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        await asyncio.sleep(0.1)

        data = await websocket.receive_json()
        query = data.get("query")

        if not query:
            await websocket.send_json({
                "type": "error",
                "data": "Query is required"
            })
            return

        search_results = search_service.web_search(query)

        sorted_results = sort_source_service.sort_sources(
            query,
            search_results
        )

        await websocket.send_json({
            "type": "search_result",
            "data": sorted_results
        })

        for chunk in llm_service.generate_response(
            query,
            sorted_results
        ):
            await websocket.send_json({
                "type": "content",
                "data": chunk
            })

    except WebSocketDisconnect:
        print("WebSocket client disconnected")

    except Exception as e:
        print(f"WebSocket error: {e}")

        try:
            await websocket.send_json({
                "type": "error",
                "data": "An unexpected server error occurred"
            })
        except Exception:
            pass


# Chat HTTP endpoint
@app.post("/chat")
def chat_endpoint(body: ChatBody):
    search_results = search_service.web_search(body.query)

    sorted_results = sort_source_service.sort_sources(
        body.query,
        search_results
    )

    response = llm_service.generate_response(
        body.query,
        sorted_results
    )

    return response
