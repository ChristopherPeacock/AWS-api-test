from typing import Union, Optional, List
from fastapi import FastAPI, Header, HTTPException
from API.Services.automationSearch import main
from API.Services.hashTags import get_instagram_hashtags
import os
import pathlib
from dotenv import load_dotenv

app = FastAPI(
    title="OptiCultivate API",
    version="1.0.0",
    description="Private API for targeted service discovery in the UK.",
)

@app.get("/")
def test():
    return {"API Running": True}

@app.post("/search&retrieveurls")
def read_root(
    keyword: Optional[str] = Header(None),
    location: Optional[str] = Header(None),
    engine: Optional[str] = Header(None),
    apiKey: Optional[str] = Header(None),
):
    if not keyword or not location or not engine:
        raise HTTPException(status_code=400, detail="Missing headers")

    if apiKey is None:
        try:
            load_dotenv(dotenv_path=pathlib.Path(__file__).resolve().parents[1] / '.env')
            apiKey = os.getenv("SERPAPIKEY")

        except FileNotFoundError:
            raise HTTPException(status_code=401, detail="Missing API key")

    result = main(keyword, location, engine)

    return {
        "info": {
            "title": app.title,
            "description": app.description,
            "version": app.version,
        },
        "paths": {
            "/search&retrieveurls": {
                "get": {
                    "summary": "Returns an array of URLS from the key search term that was provided in the request",
                    "response": {
                        200: {
                            "description": "Array of urls that was retrieved",
                            "content": {
                                "application/json": {
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "payload": result,
                                    },
                                }
                            },
                        }
                    },
                }
            }
        },
    }


@app.post("/retrieveemails")
def scrapeEmail(
    urls: Optional[List[str]] = Header(None),
):
    if not urls:
        raise HTTPException(status_code=400, detail="Missing urls header")
    return {"received_urls": urls}

@app.post("/hashtags")
def scrapeHashTags(
    Keyword: Optional[str] = Header(None),
):
    if not Keyword:
        raise HTTPException(status_code=400, details='Missing headers')
    
    result = get_instagram_hashtags(Keyword)
    
    return {
        "info": {
            "title": app.title,
            "description": app.description,
            "version": app.version,
        },
        "paths": {
            "/hashTags": {
                "get":{
                    "summary": "Returns an array of hash tags from the key word that was provided in the request",
                    "response": {
                        200: {
                            "description": "Array of urls that was retrieved",
                            "content": {
                                "application/json": {
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "payload": result,
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }