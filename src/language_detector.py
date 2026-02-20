from langdetect import detect_langs, LangDetectException
import re

ENGLISH_WORDS = {
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'shall', 'can', 'not', 'no', 'yes', 'ok',
    'okay', 'this', 'that', 'these', 'those', 'it', 'its', 'i', 'you',
    'he', 'she', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my',
    'your', 'his', 'our', 'their', 'what', 'when', 'where', 'who', 'how',
    'why', 'which', 'and', 'or', 'but', 'if', 'so', 'because', 'then',
    'than', 'too', 'also', 'just', 'very', 'really', 'much', 'more',
    'most', 'some', 'any', 'all', 'both', 'each', 'few', 'many', 'with',
    'about', 'from', 'into', 'through', 'for', 'on', 'at', 'by', 'up',
    'out', 'in', 'of', 'to', 'as', 'like', 'food', 'tasty', 'spicy',
    'good', 'bad', 'nice', 'great', 'awesome', 'love', 'hate', 'today',
    'tomorrow', 'yesterday', 'now', 'here', 'there', 'still', 'again',
    'already', 'always', 'never', 'sometimes', 'maybe', 'please', 'sorry',
    'thanks', 'thank', 'welcome', 'hello', 'hi', 'hey', 'bye', 'food',
    'eat', 'drink', 'go', 'come', 'see', 'look', 'know', 'think', 'want',
    'need', 'get', 'give', 'take', 'make', 'say', 'tell', 'ask', 'work',
    'feel', 'seem', 'put', 'keep', 'let', 'begin', 'show', 'hear', 'play'
}

class LanguageDetector:
    def __init__(self):
        self.script_map = {
            'hi': r'[\u0900-\u097F]',
            'bn': r'[\u0980-\u09FF]',
            'pa': r'[\u0A00-\u0A7F]',
            'gu': r'[\u0A80-\u0AFF]',
            'ta': r'[\u0B80-\u0BFF]',
            'te': r'[\u0C00-\u0C7F]',
            'kn': r'[\u0C80-\u0CFF]',
            'ml': r'[\u0D00-\u0D7F]',
            'ur': r'[\u0600-\u06FF]',
        }

        self.hindi_patterns = set(['hai', 'hain', 'hoon', 'tha', 'thi', 'ke', 'ka', 'ki', 'main', 'mujhe', 'kya', 'kaise', 'bohot', 'bahut', 'acha', 'thik', 'yaar', 'nahin', 'karo', 'karna', 'nhi', 'accha', 'bhai', 'yrr', 'lag', 'rha', 'rhi', 'gaya', 'aaja', 'aacha', 'nahi', 'hua', 'hui', 'hoga', 'hogi', 'wala', 'wali', 'abhi', 'phir', 'toh', 'bhi', 'sirf', 'bas', 'agar', 'lekin', 'aur', 'par', 'mera', 'tera', 'apna', 'sab', 'kuch', 'mat', 'aao', 'jao', 'dekho', 'suno', 'bolo', 'bol', 'kar', 'haan', 'naa', 'woh', 'yeh', 'koi', 'kaafi', 'zyada', 'thoda', 'bilkul'])
        self.bengali_patterns = set(['ami', 'tumi', 'tomar', 'amar', 'khub', 'bhalo', 'kemon', 'achi', 'korchi', 'khushi', 'kharap', 'ekta', 'keno', 'ebar', 'abar', 'kintu', 'tai', 'hobe', 'nai', 'nei', 'boro', 'choto', 'jabo', 're', 'emon'])
        self.tamil_patterns = set(['naan', 'nee', 'unakku', 'enakku', 'enna', 'romba', 'nalla', 'irukku', 'panren', 'vara', 'poga', 'veetla', 'inga', 'illai', 'aamaa', 'seri', 'konjam', 'theriyum', 'sollu', 'paarunga'])
        self.telugu_patterns = set(['nenu', 'neenu', 'chala', 'bagundi', 'ela', 'unnaru', 'chesanu', 'emi', 'ekkada', 'eppudu', 'enduku', 'enti', 'anni', 'ledu', 'undi', 'cheyu', 'vasta', 'podham', 'ayindi'])
        self.marathi_patterns = set(['maze', 'tujhe', 'kay', 'kase', 'bara', 'ahe', 'karto', 'karun', 'kuthe', 'kiti', 'asa', 'tasa', 'mala', 'tula', 'amhi', 'tumhi', 'jar', 'tar'])
        self.punjabi_patterns = set(['tenu', 'kiven', 'ohda', 'sahi', 'theek', 'haal', 'chal', 'dasso', 'oye', 'kiddan', 'tussi', 'saada', 'taada', 'changa', 'munda', 'kuri'])
        self.gujarati_patterns = set(['hu', 'tame', 'mane', 'tamane', 'kevi', 'bahu', 'che', 'karvu', 'kyare', 'kem', 'chho', 'nathi', 'chhe', 'joie', 'male', 'hatu', 'hata'])
        self.kannada_patterns = set(['naanu', 'neenu', 'tumba', 'chennagi', 'hegide', 'idvi', 'madidini', 'yaake', 'ellide', 'yaavaga', 'enu', 'illa', 'bidi', 'bekhu', 'barthini', 'hogthini', 'nimage', 'nanage'])
        self.malayalam_patterns = set(['njan', 'enikku', 'ninakku', 'enthu', 'engane', 'nannaayi', 'unde', 'cheyyunnu', 'evide', 'enth', 'ano', 'alle', 'aanu', 'ille', 'varu', 'poku', 'parayuu'])
        self.urdu_patterns = set(['aap', 'tumhara', 'shukriya', 'meherbani', 'zaroor', 'matlab', 'waise', 'hamesha', 'kabhi', 'shayad', 'chahiye', 'milenge'])

        self.spanish_patterns = set(['pero', 'muy', 'donde', 'cuando', 'porque', 'esta', 'bien', 'gracias', 'hola', 'esto', 'ese', 'una', 'los', 'las', 'del'])
        self.french_patterns = set(['mais', 'comme', 'tres', 'quand', 'pourquoi', 'oui', 'pour', 'avec', 'merci', 'bonjour', 'aussi', 'pas', 'plus', 'une', 'les', 'des', 'dans', 'sur'])
        self.german_patterns = set(['das', 'und', 'aber', 'sehr', 'wann', 'warum', 'nein', 'mit', 'gut', 'danke', 'hallo', 'ich', 'sie', 'wir', 'ein', 'eine', 'nicht', 'auch'])
        self.portuguese_patterns = set(['mas', 'muito', 'onde', 'quando', 'porque', 'sim', 'nao', 'com', 'bem', 'obrigado', 'ola', 'uma', 'isso', 'aqui', 'ainda', 'agora'])
        self.italian_patterns = set(['molto', 'dove', 'quando', 'perche', 'bene', 'grazie', 'ciao', 'sono', 'anche', 'una', 'non', 'questo', 'qui', 'ora'])

        self.japanese_patterns = set(['desu', 'kara', 'demo', 'totemo', 'doko', 'itsu', 'naze', 'iie', 'arigatou', 'konnichiwa', 'sugoi', 'kawaii', 'suki', 'dame', 'chotto', 'matte'])
        self.korean_patterns = set(['geot', 'geunde', 'eotteoke', 'eodi', 'eonje', 'wae', 'anio', 'gamsahamnida', 'annyeong', 'daebak', 'jinjja', 'aigoo', 'oppa', 'unni'])
        self.chinese_patterns = set(['zai', 'hen', 'zeme', 'weishenme', 'duoshao', 'nihao', 'xie', 'women', 'zenme', 'meiyou', 'zhidao'])
        self.thai_patterns = set(['chai', 'mak', 'arai', 'khrap', 'sawatdee', 'khob', 'khun', 'dee', 'pen', 'gin', 'pai'])
        self.indonesian_patterns = set(['yang', 'saya', 'kamu', 'apa', 'untuk', 'dengan', 'sangat', 'baik', 'terima', 'kasih', 'tidak', 'bisa', 'mau', 'sudah', 'belum', 'karena'])
        self.vietnamese_patterns = set(['cua', 'rat', 'tot', 'cam', 'xin', 'chao', 'ban', 'toi', 'khong', 'duoc', 'roi', 'vay'])

    def detect_script(self, text):
        for lang, pattern in self.script_map.items():
            if re.search(pattern, text):
                return lang
        return None

    def split_by_script(self, text):
        all_script_pattern = (
            r'([\u0900-\u097F]+|'
            r'[\u0980-\u09FF]+|'
            r'[\u0A00-\u0A7F]+|'
            r'[\u0A80-\u0AFF]+|'
            r'[\u0B80-\u0BFF]+|'
            r'[\u0C00-\u0C7F]+|'
            r'[\u0C80-\u0CFF]+|'
            r'[\u0D00-\u0D7F]+|'
            r'[\u0600-\u06FF]+|'
            r'[a-zA-Z0-9][a-zA-Z0-9\s,\.\!\?\']*)'
        )
        chunks = re.findall(all_script_pattern, text)
        return [c.strip() for c in chunks if c.strip()]

    def detect_romanized_language(self, text):
        text_lower = text.lower()
        words = set(text_lower.split())

        scores = {
            'hi': sum(1 for w in words if w in self.hindi_patterns),
            'bn': sum(1 for w in words if w in self.bengali_patterns),
            'ta': sum(1 for w in words if w in self.tamil_patterns),
            'te': sum(1 for w in words if w in self.telugu_patterns),
            'mr': sum(1 for w in words if w in self.marathi_patterns),
            'pa': sum(1 for w in words if w in self.punjabi_patterns),
            'gu': sum(1 for w in words if w in self.gujarati_patterns),
            'kn': sum(1 for w in words if w in self.kannada_patterns),
            'ml': sum(1 for w in words if w in self.malayalam_patterns),
            'ur': sum(1 for w in words if w in self.urdu_patterns),
            'es': sum(1 for w in words if w in self.spanish_patterns),
            'fr': sum(1 for w in words if w in self.french_patterns),
            'de': sum(1 for w in words if w in self.german_patterns),
            'pt': sum(1 for w in words if w in self.portuguese_patterns),
            'it': sum(1 for w in words if w in self.italian_patterns),
            'ja': sum(1 for w in words if w in self.japanese_patterns),
            'ko': sum(1 for w in words if w in self.korean_patterns),
            'zh': sum(1 for w in words if w in self.chinese_patterns),
            'th': sum(1 for w in words if w in self.thai_patterns),
            'id': sum(1 for w in words if w in self.indonesian_patterns),
            'vi': sum(1 for w in words if w in self.vietnamese_patterns),
        }

        max_lang = max(scores, key=scores.get)
        return max_lang if scores[max_lang] > 0 else None

    def detect_language(self, text):
        # Step 1: non-Roman script (बहुत, বাংলা, etc.)
        script_lang = self.detect_script(text)
        if script_lang:
            return script_lang

        # Step 2: short chunks — check English word list before langdetect
        # prevents "tasty" → Finnish, "spicy" → Polish
        words = set(text.lower().split())
        if len(words) <= 4:
            english_hits = sum(1 for w in words if w in ENGLISH_WORDS)
            if english_hits >= 1:
                return 'en'

        # Step 3: romanized pattern matching
        romanized_lang = self.detect_romanized_language(text)
        if romanized_lang:
            return romanized_lang

        # Step 4: fallback to langdetect
        try:
            result = detect_langs(text)
            return result[0].lang if result else 'en'
        except LangDetectException:
            return 'en'

    def split_by_language(self, text):
        chunks = self.split_by_script(text)
        segments = []
        for chunk in chunks:
            lang = self.detect_language(chunk)
            segments.append((chunk, lang))
        return segments