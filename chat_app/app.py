from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, Request, status, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from auth.auth import router, verify_jwt
from fastapi.middleware.cors import CORSMiddleware

template = Jinja2Templates(directory="templates")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

class Connection_Manager:
    def __init__(self):
        self.active_connections = set()

    async def connect(self, websocket:WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    async def send_personal_message(self, message:str, websocket:WebSocket):
        await websocket.send_text(message)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message:str, websocket:WebSocket):
        for conn in self.active_connections:
            if conn != websocket:
                await conn.send_text(message)

manager = Connection_Manager()

@app.get("/")
async def home(request:Request):
    return template.TemplateResponse("index.html", {"request":request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, username: str = Query(...), token: str = Query(...)):
    try:
        user = verify_jwt(token)
        if user.username != username:
            print("token verified in websocket")
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
    
        await manager.connect(websocket)
        await manager.send_personal_message("You have joined the chat", websocket)
        await manager.broadcast(f"{username} joined the chat", websocket)
        while True:
            try:
                data = await websocket.receive_text()
                await manager.send_personal_message(f"{username} : {data}", websocket)
                await manager.broadcast(f"🔹{username} : {data}", websocket)
            except WebSocketDisconnect:
                await manager.broadcast(f"🔸{username} left the chat.", websocket)
                await manager.disconnect(websocket)
                return RedirectResponse("/")
    except HTTPException:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
