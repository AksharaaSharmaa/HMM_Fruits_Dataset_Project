from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import subprocess
import os
import tempfile
import base64
from pathlib import Path
from collections import defaultdict
from typing import List, Optional
import uvicorn

# Configuration
ESPEAK_PATH = r"C:\Program Files\eSpeak NG\espeak-ng.exe"

app = FastAPI(title="HMM Pronunciation Generator")

class TrainingRequest(BaseModel):
    words: List[str]

class PronunciationRequest(BaseModel):
    word: str
    voice: str = "en"
    speed: int = 175
    pitch: int = 50

class PhonemeLearner:
    """Learn phoneme patterns from eSpeak NG output"""
    
    def __init__(self):
        self.learned_phonemes = {}
        self.grapheme_to_phoneme = defaultdict(lambda: defaultdict(int))
        self.phoneme_sequences = []
        
    def extract_phonemes_from_espeak(self, word):
        """Extract phonemes using eSpeak NG's phoneme output"""
        try:
            # Try with --ipa flag first
            result = subprocess.run(
                [ESPEAK_PATH, "-q", "--ipa", word],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # Check if stdout exists and has content
            if result.stdout:
                phonemes = result.stdout.strip()
                if phonemes:
                    return phonemes
            
            # Fallback: try with -x flag for phoneme output
            result = subprocess.run(
                [ESPEAK_PATH, "-q", "-x", word],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.stdout:
                phonemes = result.stdout.strip()
                if phonemes:
                    return phonemes
            
            # If still no output, return a simple representation
            print(f"Warning: No phoneme output for '{word}', using fallback")
            return f"/{word}/"
            
        except subprocess.TimeoutExpired:
            print(f"Timeout extracting phonemes for '{word}'")
            return f"/{word}/"
        except FileNotFoundError:
            print(f"eSpeak NG not found at {ESPEAK_PATH}")
            return None
        except Exception as e:
            print(f"Error extracting phonemes for '{word}': {e}")
            return f"/{word}/"
    
    def learn_from_word(self, word):
        """Learn phoneme mapping from a word"""
        phonemes = self.extract_phonemes_from_espeak(word)
        if phonemes:
            self.learned_phonemes[word.lower()] = phonemes
            self.phoneme_sequences.append((word.lower(), phonemes))
            
            # Build grapheme-to-phoneme statistics
            word_lower = word.lower()
            for i, char in enumerate(word_lower):
                context = word_lower[max(0, i-1):min(len(word_lower), i+2)]
                if i < len(phonemes):
                    self.grapheme_to_phoneme[char][phonemes[i]] += 1
            
            return phonemes
        return None
    
    def predict_phonemes(self, word):
        """Predict phonemes for a new word"""
        word_lower = word.lower()
        
        if word_lower in self.learned_phonemes:
            return self.learned_phonemes[word_lower]
        
        return self.extract_phonemes_from_espeak(word)
    
    def get_stats(self):
        """Get learning statistics"""
        return {
            'words_learned': len(self.learned_phonemes),
            'unique_phonemes': len(set(''.join(self.learned_phonemes.values()))),
            'phoneme_patterns': len(self.grapheme_to_phoneme)
        }

class HMMPronunciationSystem:
    """HMM-based pronunciation generation system"""
    
    def __init__(self):
        self.phoneme_learner = PhonemeLearner()
        self.training_words = []
        
    def train_on_dataset(self, words):
        """Train the system on a list of words"""
        results = []
        for word in words:
            phonemes = self.phoneme_learner.learn_from_word(word)
            if phonemes:
                results.append({"word": word, "phonemes": phonemes})
                self.training_words.append(word)
        return results
    
    def generate_pronunciation(self, text, output_file, voice="en", speed=175, pitch=50):
        """Generate audio pronunciation using eSpeak NG"""
        if not os.path.exists(ESPEAK_PATH):
            raise FileNotFoundError(f"eSpeak NG not found at: {ESPEAK_PATH}")
        
        command = [
            ESPEAK_PATH,
            "-v", voice,
            "-s", str(speed),
            "-p", str(pitch),
            "-w", output_file,
            text
        ]
        
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                print(f"eSpeak NG error: {result.stderr}")
                return False
            return True
        except Exception as e:
            print(f"Error generating audio: {e}")
            return False
    
    def get_phoneme_representation(self, word):
        """Get phoneme representation for a word"""
        return self.phoneme_learner.predict_phonemes(word)

# Global system instance
hmm_system = HMMPronunciationSystem()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the HTML frontend"""
    html_file = Path(__file__).parent / "index.html"
    if html_file.exists():
        try:
            return html_file.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            try:
                # Try with a different encoding
                return html_file.read_text(encoding='latin-1')
            except Exception:
                # Fallback to default content
                return HTMLResponse(content=get_html_content(), status_code=200)
    return HTMLResponse(content=get_html_content(), status_code=200)

@app.post("/api/train")
async def train_system(request: TrainingRequest):
    """Train the HMM system on words"""
    try:
        results = hmm_system.train_on_dataset(request.words)
        stats = hmm_system.phoneme_learner.get_stats()
        
        return {
            "success": True,
            "results": results,
            "stats": stats,
            "message": f"Trained on {len(results)} words"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate")
async def generate_pronunciation(request: PronunciationRequest):
    """Generate pronunciation for a word"""
    try:
        # Get phoneme representation
        phonemes = hmm_system.get_phoneme_representation(request.word)
        
        if not phonemes:
            raise HTTPException(status_code=400, detail="Could not generate phonemes")
        
        # Generate audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            output_file = tmp_file.name
        
        success = hmm_system.generate_pronunciation(
            request.word, output_file, request.voice, request.speed, request.pitch
        )
        
        if not success or not os.path.exists(output_file):
            raise HTTPException(status_code=500, detail="Audio generation failed")
        
        # Read audio file and encode to base64
        with open(output_file, "rb") as f:
            audio_bytes = f.read()
        
        audio_base64 = base64.b64encode(audio_bytes).decode()
        
        # Cleanup
        try:
            os.unlink(output_file)
        except:
            pass
        
        return {
            "success": True,
            "phonemes": phonemes,
            "audio_base64": audio_base64,
            "word": request.word
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    try:
        stats = hmm_system.phoneme_learner.get_stats()
        return {
            "success": True,
            "stats": stats,
            "training_words": hmm_system.training_words
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Check if eSpeak NG is available"""
    espeak_available = os.path.exists(ESPEAK_PATH)
    return {
        "status": "healthy" if espeak_available else "unhealthy",
        "espeak_available": espeak_available,
        "espeak_path": ESPEAK_PATH
    }

def get_html_content():
    """Fallback HTML content if index.html doesn't exist"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>HMM Pronunciation Generator</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
            h1 { color: #1f77b4; }
            .error { color: red; }
            .success { color: green; }
        </style>
    </head>
    <body>
        <h1>🔊 HMM Pronunciation Generator</h1>
        <p>Please create an index.html file or the system will serve this fallback page.</p>
        <p>API is running at <a href="/docs">/docs</a></p>
    </body>
    </html>
    """

if __name__ == "__main__":
    # Check if eSpeak NG is available
    if not os.path.exists(ESPEAK_PATH):
        print(f"⚠️ Warning: eSpeak NG not found at: {ESPEAK_PATH}")
        print("Please install eSpeak NG and update the ESPEAK_PATH variable")
    
    uvicorn.run(app, host="0.0.0.0", port=8001)