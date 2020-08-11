import requests
import random
import shutil
import bs4
import ssl
import cv2
import time
import csv
import imghdr

ssl._create_default_https_context = ssl._create_unverified_context
def get_images(keyword, num):
    Res = requests.get("https://www.google.com/search?hl=jp&q=" + keyword + "&btnG=Google+Search&tbs=0&safe=off&tbm=isch")
    Html = Res.text
    Soup = bs4.BeautifulSoup(Html,'lxml')
    images = random.sample(Soup.find_all("img"), num)
    return images

def download_img(url, imgpath):
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(imgpath, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
                return True
        return False
    except Exception:
        print("画像のダウンロードに失敗しました。url：" + url)
        return False

def put_converted_img(img, converted_imgpath):
    converted_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    converted_img = cv2.rotate(converted_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv2.imwrite(converted_imgpath, converted_img)

def get_size(img):
    height, width = img.shape[:2]
    return str(width) + "×" + str(height)

def put_csv(data, keyword):
    with open('./csv/' + keyword + '_data.csv', 'w') as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerows(data)

keyword = input("検索ワードを入力してください:")
# keyword = "犬" # 画像項目固定の場合

# csvの行情報を定義
csv_rows = []
csv_rows.append(["ファイル名", "サイズ", "フォーマット"])

# インターネット上から画像を取得
images = get_images(keyword, 10)
for i,image in enumerate(images):
    filename = keyword + "_" + str(i)
    imgpath = "./img/" + filename + ".png"
    # サーバーの負荷を考慮して1秒間待つ
    time.sleep(1)
    # 課題1 画像のダウンロード
    if download_img(image["src"], imgpath) == True:
        ext = imghdr.what(imgpath)
        img = cv2.imread(imgpath)
        # csvの行情報を追加。ファイル名,サイズ,フォーマット
        csv_rows.append([imgpath, get_size(img), ext])
        # 課題３ 画像の変換
        put_converted_img(img, "./img_converted/" + filename + "." + ext)

# 課題２ csvの保存
put_csv(csv_rows, keyword)

print("画像の保存、変換が完了しました。")
