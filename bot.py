import openai
import chatgpt
from chatgpt import ChatGpt as Chat
import os

requests = {
    "baslikIstek": "{sehir} şehrinde gezilecek yerler ve yapılması gerekenler hakkında makale yazıyorum. Bana {sehir} şehrinde en az 15 gezilecek yeri sıralı başlıklar halinde yazmanı istiyorum. ",
    "baslikYaz": "{sehir} şehrindeki {mekan} hakkında 50 kelimelik seo uyumlu bir makale yaz",
    "baslikBul": "Birazdan yazacağım makale için seo uyumlu, 60 karakterden oluşan bir başlık yaz. {makale}",
    "metaDescription": "Birazdan yazacağım makale için seo uyumlu 160 karakterden oluşan bir meta description yaz. {makale}"
}
places = { # her bir eleman için request içerisindeki baslikIstek çalıştırılacaktır ve {sehir}, item ile değiştirilecektir.
    "Adıyaman",
    "Afyonkarahisar",
    "Ağrı",
    "Amasya",
    "Ankara",
    "Antalya",
    "Artvin",
    "Aydın",
    "Balıkesir",
    "Bilecik",
    "Bingöl",
    "Bitlis",
    "Bolu",
    "Burdur",
    "Bursa",
    "Çanakkale",
    "Çankırı",
    "Çorum",
    "Denizli",
    "Diyarbakır",
    "Elazığ",
    "Erzincan",
    "Erzurum",
    "Eskişehir",
    "Gaziantep",
    "Giresun",
    "Gümüşhane",
    "Hakkari",
    "Hatay",
    "Isparta",
    "Mersin",
    "İstanbul",
    "Kars",
    "Kastamonu",
    "Kayseri",
    "Kırşehir",
    "Kocaeli",
    "Konya",
    "Kütahya",
    "Malatya",
    "Manisa",
    "Kahramanmaraş",
    "Mardin",
    "Muğla",
    "Muş",
    "Nevşehir",
    "Niğde",
    "Ordu",
    "Rize",
    "Sakarya",
    "Samsun",
    "Siirt",
    "Sinop",
    "Sivas",
    "Tokat",
    "Trabzon",
    "Tunceli",
    "Uşak",
    "Van",
    "Yozgat",
    "Zonguldak",
    "Aksaray",
    "Bayburt",
    "Karaman",
    "Kırıkkale",
    "Batman",
    "Şırnak",
    "Bartın",
    "Ardahan",
    "Iğdır",
    "Yalova",
    "Karabük",
    "Kilis",
    "Osmaniye",
    "Düzce"
}

# basliklar dizinine baslik'daki değerin isminde bir dizin daha oluşturacaktır.
# bu dizinin içerisine de altBaslik isimli bir txt dosyası oluşturup içerisine makale'yi kaydedecektir.
def saveAltBaslik(baslik, altBaslik, makale):
    try:
        dpath = "./basliklar/" + baslik
        isExist = os.path.exists(dpath)
        if not isExist:
            os.makedirs(dpath)
        path = "./basliklar/" + baslik + "/" + altBaslik
        with open(path + ".txt", 'w') as f:
            f.write(makale)
    except:
        print(altBaslik + " Başlığı Dosya Yolunda Bir Hata Meydana Geldi")

def saveMakale(anaBaslik, makale):
    try:
        saveHtml(anaBaslik, makale)
        path = "./makaleler/" + anaBaslik
        with open(path + ".txt", 'w') as f:
            f.write(makale)

    except:
        print(anaBaslik + " Ana Başlığı Dosya Yolunda Bir Hata Meydana Geldi")

def saveHtml(anaBaslik, makale):
    try:
        tempMakale = makale.split("\n")
        htmlMakale = ""
        for satir in tempMakale:
            satir = str(satir)
            if satir.startswith("1.") or satir.startswith("2.") or satir.startswith("3.") or satir.startswith("4.") or satir.startswith("5.") or satir.startswith("6.") or satir.startswith("7.") or satir.startswith("8.") or satir.startswith("9.") or satir.startswith("10.") or satir.startswith("11.") or satir.startswith("12.") or satir.startswith("13.") or satir.startswith("14.") or satir.startswith("15."):
                htmlMakale += '<hr class="wp-block-separator has-alpha-channel-opacity"/><br><h2>' + satir + "</h2><br>"
            elif "MAKALE BAŞLIK :" in satir or "MAKALE META :" in satir:
                htmlMakale += satir
            else:
                htmlMakale += "<p>" + satir + "</p>"
        path = "./html/" + anaBaslik
        with open(path + ".txt", 'w') as f:
            f.write(htmlMakale)
    except:
        print(anaBaslik + " Ana Başlığı Dosya Yolunda Bir Hata Meydana Geldi")


if __name__ == "__main__":
    GPT = Chat()
    for place in places:
        try:
            prompt = requests['baslikIstek'].replace("{sehir}", place)
            print("YOU : " + prompt)
            basliklar = GPT.question(prompt)
            baslikList = basliklar.split('\n')
            print("AI : " + str(baslikList))
            makale = ""
            for baslik in baslikList:
                promptBaslik = ""
                try:
                    promptBaslik = requests['baslikYaz'].replace("{sehir}", place).replace("{mekan}", baslik.split(". ")[1])
                    print("YOU : " + promptBaslik)
                    makale += baslik + "\n"
                    baslikMakale = GPT.question(promptBaslik) + "\n"
                    makale += baslikMakale
                    saveAltBaslik(place, baslik.split(". ")[1].replace(' ', '-'), baslikMakale)
                    print("AI : " + baslikMakale)
                except:
                    continue

            makaleBaslik = ""
            makaleMeta = ""
            try:
                if len(makale) > 1000:
                    first500Chars = makale[0:1000]
                    makaleBaslikPrompt = requests['baslikBul'].replace("{makale}", first500Chars)
                    makaleMetaPrompt = requests['metaDescription'].replace("{makale}", first500Chars)
                    makaleBaslik = GPT.question(makaleBaslikPrompt)
                    makaleMeta = GPT.question(makaleMetaPrompt)
            except:
                print("ERROR : META VE BAŞLIK SORGUSUNDA HATA")
            print("MAKALE META : " + makaleMeta)
            print("MAKALE BAŞLIK : " + makaleBaslik)
            print("MAKALE : " + makale)
            makaleBaslikMeta = "MAKALE BAŞLIK : " + makaleBaslik + "\nMAKALE META : " + makaleMeta + "\n" + makale
            saveMakale(place.replace(' ', '-'), makaleBaslikMeta)
        except:
            continue


