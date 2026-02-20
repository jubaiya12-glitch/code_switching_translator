from src.language_detector import LanguageDetector
from src.translator import Translator

class CodeSwitchHandler:
    def __init__(self, target_language='en'):
        self.detector = LanguageDetector()
        self.translator = Translator()
        self.target_language = target_language

    def process_text(self, text):
        print(f"\n--- Processing text ---")
        print(f"Original: {text}")

        segments = self.detector.split_by_language(text)

        print(f"\nDetetcted {len(segments)} segments:")
        for i, (segment, lang) in enumerate (segments):
            print(f" {i+1}. [{lang} {segment.strip()}]")

        translated_segments = []
        for segment, lang in segments:
            if lang != self.target_language and segment.strip():
                 translated = self.translator.translate(
                      segment.strip(),
                      lang,
                      self.target_language
                      )
                 translated_segments.append(translated)   # ✅ FIX

            else:
                translated_segments.append(segment)

        final_text= ' '.join(translated_segments)

        print(f"\nTranslated to {self.target_language}: {final_text}")

        return{
            'original' : text,
            'translated' : final_text,
            'segments':segments,
            'target_language': self.target_language
        }