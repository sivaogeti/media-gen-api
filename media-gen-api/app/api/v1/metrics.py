# app/api/v1/metrics.py
from fastapi import APIRouter, HTTPException, Query, Depends, Request
from typing import List
from sklearn.metrics import accuracy_score
from nltk.translate.bleu_score import sentence_bleu
from sentence_transformers import SentenceTransformer, util
from app.auth.auth import verify_token

router = APIRouter()
model = SentenceTransformer("clip-ViT-B-32")  # for CLIP-like semantic score

@router.post("/evaluate/bleu", dependencies=[Depends(verify_token)])
def compute_bleu(reference: str, candidate: str):
    ref_tokens = [reference.split()]
    cand_tokens = candidate.split()
    score = sentence_bleu(ref_tokens, cand_tokens)
    return {"metric": "BLEU", "score": score}

@router.post("/evaluate/clipscore")
def compute_clip_score(reference: str, candidate: str):
    ref_emb = model.encode(reference, convert_to_tensor=True)
    cand_emb = model.encode(candidate, convert_to_tensor=True)
    score = util.cos_sim(ref_emb, cand_emb).item()
    return {"metric": "CLIPScore", "score": score}
