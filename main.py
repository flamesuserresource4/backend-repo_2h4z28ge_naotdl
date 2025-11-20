import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Farmhouse, Booking

app = FastAPI(title="Farmhouse Booking API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Farmhouse Booking API is running"}

@app.get("/api/farmhouses")
def list_farmhouses():
    try:
        docs = get_documents("farmhouse", {}, limit=50)
        # Normalize _id and drop internal fields
        for d in docs:
            d["id"] = str(d.get("_id"))
            d.pop("_id", None)
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class BookingRequest(Booking):
    pass

@app.post("/api/bookings")
def create_booking(payload: BookingRequest):
    try:
        # basic validation for farmhouse exists
        fh = db["farmhouse"].find_one({"_id": ObjectId(payload.farmhouse_id)})
        if not fh:
            raise HTTPException(status_code=404, detail="Farmhouse not found")
        booking_id = create_document("booking", payload)
        return {"id": booking_id, "status": "confirmed"}
    except Exception as e:
        # if invalid ObjectId or db error
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
