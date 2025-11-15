# DCT Стеганография
Теория этого проекта находится в report файле этого репозитория.

Использование:
```bash
git clone https://github.com/inno1314/DCT-stegano.git
cd DCT-stegano
rm -rf .git/
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Пример вставки данных:
```py
python3 app.py embed pepper.jpeg stego_pepper.jpeg "hidden data"
```

Пример извлечения данных:
```py
python3 app.py extract stego_pepper.jpeg
```

"zigzag.py" location source: https://github.com/amzhang1/simple-JPEG-compression/blob/master/zigzag.py
