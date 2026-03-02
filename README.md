# 🌐 Code Switching Translator

A multilingual NLP-based translator that detects and translates **code-switched text** — sentences that mix two or more languages — into a target language. Built using Facebook's M2M100 model, supporting **15+ languages** including major Indian and international languages.

---

## 🚀 What is Code Switching?

Code switching is when a speaker alternates between two or more languages in a single sentence. For example:

> *"Aaj ka weather bohot acha hai, let's go for a walk!"* (Hindi + English)

Most standard translators fail at this. This project handles it.

---

## ✨ Features

- 🔤 Detects mixed-language input automatically
- 🌍 Supports 15+ languages including Hindi, Kannada, Tamil, Telugu, Bengali, Malayalam, Gujarati, Marathi, Urdu, Arabic, French, Spanish, German, Japanese, and English
- 🤖 Powered by Facebook's **M2M100 multilingual model** (supports 100+ languages)
- ⚡ Translates code-switched sentences into any target language
- 🖥️ Runs via terminal — lightweight and easy to use

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| HuggingFace Transformers | M2M100 model loading & inference |
| M2M100 (facebook/m2m100_418M) | Multilingual translation model |
| PyTorch | Deep learning backend |

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/jubaiya12-glitch/code_switching_translator.git
cd code_switching_translator

# Install dependencies
pip install transformers torch sentencepiece

# Run the translator
python main.py
```

> ⚠️ First run will download the M2M100 model (~2GB). This happens only once.

---

## 💻 Usage

```bash
python main.py
```

Example interaction:
```
Enter text: Aaj bahut thanda hai, I forgot my jacket
Source language: hi  
Target language: en

Output: It's very cold today, I forgot my jacket.
```

---

## 🌍 Supported Languages

| Language | Code |
|----------|------|
| English | en |
| Hindi | hi |
| Kannada | kn |
| Tamil | ta |
| Telugu | te |
| Bengali | bn |
| Malayalam | ml |
| Gujarati | gu |
| Marathi | mr |
| Urdu | ur |
| Arabic | ar |
| French | fr |
| Spanish | es |
| German | de |
| Japanese | ja |

---

## 🧠 How It Works

1. User inputs a code-switched sentence
2. The M2M100 model — pre-trained on 100+ languages — processes the mixed input
3. The tokenizer identifies language segments
4. The model generates a fluent translation in the target language

---

## 📁 Project Structure

```
code_switching_translator/
│
├── src/
│   └── translator.py      # Core translation logic
├── Output/                # Sample output screenshots
├── main.py                # Entry point
└── README.md
```

---

## 🎯 Future Improvements

- [ ] Add automatic language detection (no need to specify source language)
- [ ] Build a web UI using Flask or Streamlit
- [ ] Support real-time translation
- [ ] Expand to 50+ languages

---

## 👩‍💻 Author

**Jubaiya** — CS (AI & ML) Student  
GitHub: [@jubaiya12-glitch](https://github.com/jubaiya12-glitch)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
