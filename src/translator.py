import os
os.environ['HF_HUB_DISABLE_SSL_VERIFICATION'] = '1'
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''

import httpx
import ssl
_ctx = ssl.create_default_context()
_ctx.check_hostname = False
_ctx.verify_mode = ssl.CERT_NONE

from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

class Translator:
    def __init__(self):
        """Initialize the translator with M2M100 model (supports 100+ languages)"""
        print("Loading multilingual translation model (this may take a few minutes)...")
        self.model_name = "facebook/m2m100_418M"
        self.model = None
        self.tokenizer = None
        
    def load_model(self):
        """Load the M2M100 model"""
        if self.model is None:
            print("Downloading model... (first time only, ~2GB)")
            self.tokenizer = M2M100Tokenizer.from_pretrained(self.model_name)
            self.model = M2M100ForConditionalGeneration.from_pretrained(self.model_name)
            print("✓ Model loaded successfully!")
        return True
    
    def translate(self, text, source_lang, target_lang):
        """
        Translate text from source language to target language
        Supports 100+ languages including:
        - Indian: hi (Hindi), bn (Bengali), ta (Tamil), te (Telugu), mr (Marathi), 
                 kn (Kannada), gu (Gujarati), ml (Malayalam), ur (Urdu)
        - European: en, es, fr, de, it, pt, nl, etc.
        - Asian: zh, ja, ko, th, vi, id, etc.
        """
        if not self.model:
            self.load_model()
        
        try:
            # Set source language
            self.tokenizer.src_lang = source_lang
            
            # Encode the text
            encoded = self.tokenizer(text, return_tensors="pt")
            
            # Generate translation
            generated_tokens = self.model.generate(
                **encoded,
                forced_bos_token_id=self.tokenizer.get_lang_id(target_lang)
            )
            
            # Decode the translation
            result = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
            
            return result
        except Exception as e:
            print(f"Translation error: {e}")
            return text