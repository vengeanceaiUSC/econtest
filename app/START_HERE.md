# Open Practice Test 1 (works on your computer)

## Option A — One command (easiest)

```bash
cd app
npm install
npm run build
python3 open_practice_test.py
```

Your browser opens automatically at **http://localhost:8765**

## Option B — Download zip

1. Download [Practice_Test_App.zip](https://github.com/vengeanceaiUSC/econtest/releases/download/exam-prep-download/Practice_Test_App.zip)
2. Unzip it
3. In the unzipped folder, run:
   ```bash
   python3 -m http.server 8765
   ```
4. Open **http://localhost:8765** in your browser

## Option C — GitHub Pages (permanent link)

1. Go to https://github.com/vengeanceaiUSC/econtest/settings/pages
2. Under **Build and deployment**, set Source to **Deploy from branch**
3. Branch: **gh-pages** / **(root)**
4. Click Save
5. Wait ~2 minutes, then open: **https://vengeanceaiUSC.github.io/econtest/**
