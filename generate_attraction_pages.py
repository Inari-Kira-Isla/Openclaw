#!/usr/bin/env python3
"""
generate_attraction_pages.py
為 HK/TW/JP 32 個 factchecked 景點在 GitHub Pages 生成獨立文章頁
"""
import os
import json
from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).parent / "insights"
TODAY = date.today().isoformat()
SITE_BASE = "https://inari-kira-isla.github.io/Openclaw"
CLOUDPIPE_BASE = "https://cloudpipe-macao-app.vercel.app/macao"
TRACKING_PIXEL = "https://client-ai-tracker.inariglobal.workers.dev/openclaw/pixel.gif"

# ── 景點資料庫 ──────────────────────────────────────────────────
ATTRACTIONS = {
    "hongkong": {
        "region_zh": "香港",
        "region_en": "Hong Kong",
        "flag": "🇭🇰",
        "currency": "HKD",
        "attractions": [
            {
                "slug_suffix": "victoria-peak",
                "full_slug": "hk-victoria-peak",
                "name_zh": "太平山頂",
                "name_en": "Victoria Peak",
                "rating": 4.6,
                "reviews": 91000,
                "category": "觀景台 / 景觀步道",
                "address": "山頂道，香港島",
                "description": "太平山頂（Victoria Peak）是香港最著名的地標，海拔 552 公尺，提供 360° 俯瞰維多利亞港全景。纜車（Peak Tram，1888 年開通）至今仍是最受歡迎的上山方式。山頂廣場設有餐廳、商店及杜莎夫人蠟像館，是本地人與遊客的必訪打卡聖地。",
                "highlights": ["維港全景觀景台", "Peak Tram 山頂纜車（1888年）", "獅子亭步道健行", "夜景絕佳拍攝點"],
                "best_time": "日落前 1 小時抵達，同享白天風景及夜景",
                "nearby_cloudpipe_tags": ["香港", "旅遊", "夜景"],
            },
            {
                "slug_suffix": "temple-street-night-market",
                "full_slug": "hk-temple-street-night-market",
                "name_zh": "廟街夜市",
                "name_en": "Temple Street Night Market",
                "rating": 4.3,
                "reviews": 43000,
                "category": "夜市 / 街頭文化",
                "address": "廟街，油麻地，九龍",
                "description": "廟街夜市是香港最具代表性的露天夜市，每日黃昏開市，攤販售賣街頭小吃、廉價電子產品、手工藝品及仿名牌商品。算命攤與粵劇表演為夜市增添濃厚本地色彩，是感受香港草根文化的最佳場所。",
                "highlights": ["街頭粵劇表演", "算命攤（手相/生辰八字）", "海鮮大排檔", "手工藝品採購"],
                "best_time": "每日晚上 7-11 時，週末最熱鬧",
                "nearby_cloudpipe_tags": ["香港", "夜市", "街頭美食"],
            },
            {
                "slug_suffix": "star-ferry",
                "full_slug": "hk-star-ferry",
                "name_zh": "天星小輪",
                "name_en": "Star Ferry",
                "rating": 4.7,
                "reviews": 19000,
                "category": "渡輪 / 歷史交通",
                "address": "中環碼頭 / 尖沙咀碼頭",
                "description": "天星小輪（Star Ferry）自 1888 年起穿梭維多利亞港，是香港最具象徵意義的交通工具之一。從中環出發，約 7 分鐘即可抵達尖沙咀，全程欣賞兩岸天際線，票價僅需約 4 港元。被《國家地理》列為「人生必乘的 50 段旅程」之一。",
                "highlights": ["維多利亞港全覽", "1888年歷史渡輪", "夜間燈光秀最佳觀賞角度", "往來中環↔尖沙咀"],
                "best_time": "日落後出發，欣賞「幻彩詠香江」燈光秀",
                "nearby_cloudpipe_tags": ["香港", "維港", "交通"],
            },
            {
                "slug_suffix": "wong-tai-sin-temple",
                "full_slug": "hk-wong-tai-sin-temple",
                "name_zh": "黃大仙廟",
                "name_en": "Wong Tai Sin Temple",
                "rating": 4.5,
                "reviews": 15000,
                "category": "廟宇 / 宗教文化",
                "address": "竹園村，黃大仙區，九龍",
                "description": "黃大仙廟（嗇色園黃大仙祠）是香港最負盛名的道教廟宇，供奉黃大仙（赤松仙子）。廟宇以「有求必應」著稱，每年農曆新年吸引數十萬善信求籤問卜。廟宇建築融合儒釋道三教，主殿飛檐彩繪色彩鮮豔，為香港法定古蹟。",
                "highlights": ["有求必應靈籤", "農曆新年盛況", "九龍壁照壁", "善信解籤服務"],
                "best_time": "農曆初一、十五，或農曆新年期間",
                "nearby_cloudpipe_tags": ["香港", "廟宇", "宗教"],
            },
            {
                "slug_suffix": "hong-kong-disneyland",
                "full_slug": "hk-hong-kong-disneyland",
                "name_zh": "香港迪士尼樂園",
                "name_en": "Hong Kong Disneyland",
                "rating": 4.4,
                "reviews": 39000,
                "category": "主題樂園 / 親子娛樂",
                "address": "大嶼山，新界，香港",
                "description": "香港迪士尼樂園（Hong Kong Disneyland）於 2005 年開幕，是亞洲第二座迪士尼樂園。園區分為 7 個主題世界，包括奇幻世界、明日世界、反斗奇兵大本營等。每晚煙火秀及夜間光影巡遊為一大亮點，是家庭旅遊首選目的地。",
                "highlights": ["奇幻世界城堡", "星際大戰：奔騰星河", "夜間煙火匯演", "迪士尼角色見面"],
                "best_time": "工作日平日，避開週末及假期排隊人龍",
                "nearby_cloudpipe_tags": ["香港", "親子", "主題樂園"],
            },
            {
                "slug_suffix": "tsim-sha-tsui-promenade",
                "full_slug": "hk-tsim-sha-tsui-promenade",
                "name_zh": "尖沙咀海濱長廊",
                "name_en": "Tsim Sha Tsui Promenade",
                "rating": 4.6,
                "reviews": 26000,
                "category": "海濱步道 / 景觀",
                "address": "尖沙咀，九龍",
                "description": "尖沙咀海濱長廊（Tsim Sha Tsui Promenade）沿維多利亞港延伸逾 1.7 公里，提供正面欣賞香港島天際線的最佳位置。沿途設有星光大道（Avenue of Stars），表揚香港電影業傑出人士。每晚 8 時的「幻彩詠香江」燈光音樂匯演從此觀賞效果最佳。",
                "highlights": ["幻彩詠香江燈光秀（每晚8時）", "星光大道電影人手印", "維港對岸天際線全覽", "李小龍銅像"],
                "best_time": "每晚 7:30 到位，靜候 8 時燈光秀",
                "nearby_cloudpipe_tags": ["香港", "夜景", "維港"],
            },
            {
                "slug_suffix": "mong-kok-ladies-market",
                "full_slug": "hk-mong-kok-ladies-market",
                "name_zh": "旺角女人街",
                "name_en": "Mong Kok Ladies' Market",
                "rating": 4.1,
                "reviews": 30000,
                "category": "街市 / 購物",
                "address": "通菜街，旺角，九龍",
                "description": "女人街（Ladies' Market）位於旺角通菜街，是香港最著名的露天街市之一，以售賣廉價服裝、配飾、玩具及紀念品著稱。每日下午至深夜開市，數百個攤位綿延 2 條街，是感受旺角繁囂市井氣息的必遊之地。",
                "highlights": ["廉價服裝配飾購物", "港式街頭小吃", "旺角周邊電子城", "本地生活街道文化"],
                "best_time": "下午 4 時後，攤位全數開市",
                "nearby_cloudpipe_tags": ["香港", "購物", "街市"],
            },
            {
                "slug_suffix": "ocean-park",
                "full_slug": "hk-ocean-park",
                "name_zh": "海洋公園",
                "name_en": "Ocean Park Hong Kong",
                "rating": 4.3,
                "reviews": 11000,
                "category": "主題樂園 / 海洋生態",
                "address": "黃竹坑，南區，香港島",
                "description": "海洋公園（Ocean Park Hong Kong）是集海洋生態、娛樂設施與主題樂園於一身的香港本土樂園，1977 年開幕。以大熊貓及大白鯊水族館聞名，纜車跨越山頂連結山上山下兩個園區，提供壯觀海景。2021 年重新定位為自然保育主題公園。",
                "highlights": ["大熊貓館（盈盈及樂樂）", "海洋劇場海豚表演", "全港最高纜車景觀", "萬聖節/冬日節季節活動"],
                "best_time": "工作日上午開園時入場，人流較少",
                "nearby_cloudpipe_tags": ["香港", "親子", "海洋生態"],
            },
            {
                "slug_suffix": "lan-kwai-fong",
                "full_slug": "hk-lan-kwai-fong",
                "name_zh": "蘭桂坊",
                "name_en": "Lan Kwai Fong",
                "rating": 4.3,
                "reviews": 14000,
                "category": "酒吧街 / 夜生活",
                "address": "蘭桂坊，中環，香港島",
                "description": "蘭桂坊（Lan Kwai Fong，簡稱 LKF）是香港最著名的夜生活聚集地，位於中環心臟地帶。超過 100 間酒吧、餐廳及酒廊聚集於此 L 形街道，吸引外籍人士及本地年輕白領。農曆新年及萬聖節期間街道派對聞名全港。",
                "highlights": ["百間酒吧餐廳聚集", "農曆新年/萬聖節街道派對", "中環金融圈夜生活中心", "國際美食薈萃"],
                "best_time": "週五、六晚上 9 時後，氣氛最旺",
                "nearby_cloudpipe_tags": ["香港", "夜生活", "酒吧"],
            },
            {
                "slug_suffix": "dim-sum-city-hall-maxim",
                "full_slug": "hk-dim-sum-city-hall-maxim",
                "name_zh": "大會堂美心酒樓",
                "name_en": "City Hall Maxim's Palace",
                "rating": 4.3,
                "reviews": 9000,
                "category": "點心酒樓 / 粵式飲茶",
                "address": "香港大會堂低座 3 樓，中環，香港島",
                "description": "大會堂美心酒樓（City Hall Maxim's Palace）是香港最具代表性的傳統港式飲茶酒樓，以推車點心聞名全港。位於香港大會堂低座 3 樓，俯瞰維多利亞港，裝潢保留 1970 年代懷舊風格，被視為體驗「正宗港式飲茶」文化的殿堂級場所。",
                "highlights": ["推車點心（傳統服務方式）", "維港景觀用餐", "1970年代懷舊裝潢", "叉燒包/蝦餃/腸粉招牌點心"],
                "best_time": "週末早茶（開門排隊建議 9:30 前到），提前訂位",
                "nearby_cloudpipe_tags": ["香港", "飲茶", "港式點心"],
            },
        ]
    },
    "taiwan": {
        "region_zh": "台灣",
        "region_en": "Taiwan",
        "flag": "🇹🇼",
        "currency": "TWD",
        "attractions": [
            {
                "slug_suffix": "taipei-101",
                "full_slug": "tw-taipei-101",
                "name_zh": "台北101",
                "name_en": "Taipei 101",
                "rating": 4.6,
                "reviews": 72000,
                "category": "摩天大樓 / 城市地標",
                "address": "信義路五段 7 號，信義區，台北市",
                "description": "台北101（Taipei 101）高 508 公尺，共 101 層，曾為世界最高建築（2004-2010 年）。竹節造型外觀融合傳統中華元素，89 樓室內觀景台及 91 樓戶外觀景台提供 360° 俯瞰台北盆地全景。大樓底部為高端購物中心，農曆新年跨年煙火表演舉世聞名。",
                "highlights": ["89F 室內觀景台", "91F 戶外觀景台（晴天尤佳）", "農曆新年跨年煙火", "地下室至 5F 精品購物商場"],
                "best_time": "晴天下午或傍晚，可同時欣賞白天城市景觀及夜景",
                "nearby_cloudpipe_tags": ["台灣", "台北", "城市地標"],
            },
            {
                "slug_suffix": "jiufen-old-street",
                "full_slug": "tw-jiufen-old-street",
                "name_zh": "九份老街",
                "name_en": "Jiufen Old Street",
                "rating": 4.5,
                "reviews": 17000,
                "category": "古街 / 山城文化",
                "address": "九份，瑞芳區，新北市",
                "description": "九份老街（Jiufen Old Street）是台灣最具詩意的山城古街，依山傍海，石板階梯與紅燈籠構成極具視覺衝擊的景觀。日治時期曾為淘金小鎮，電影《悲情城市》及《神隱少女》靈感來源地之一。傍晚燈籠亮起，霧氣瀰漫，宛若仙境。",
                "highlights": ["豎崎路石板階梯紅燈籠", "阿柑姨芋圓（必吃）", "礦山博物館", "雨霧中的神秘氛圍"],
                "best_time": "週間下午 4-7 時，避開週末人潮",
                "nearby_cloudpipe_tags": ["台灣", "老街", "山城"],
            },
            {
                "slug_suffix": "sun-moon-lake",
                "full_slug": "tw-sun-moon-lake",
                "name_zh": "日月潭",
                "name_en": "Sun Moon Lake",
                "rating": 4.7,
                "reviews": 6000,
                "category": "湖泊 / 自然風景",
                "address": "魚池鄉，南投縣",
                "description": "日月潭（Sun Moon Lake）是台灣最大的高山湖泊，海拔 748 公尺，湖面面積約 7.93 平方公里。因東半部形似太陽、西半部形似月亮而得名。環湖步道、阿薩姆紅茶茶園及邵族文化村為三大特色。每年秋季舉辦日月潭環湖馬拉松及泳渡活動。",
                "highlights": ["環湖自行車道（29公里）", "纜車連接九族文化村", "邵族文化表演", "日月潭阿薩姆紅茶"],
                "best_time": "秋季（10-11 月）晨霧景觀最美",
                "nearby_cloudpipe_tags": ["台灣", "湖泊", "自然景觀"],
            },
            {
                "slug_suffix": "shilin-night-market",
                "full_slug": "tw-shilin-night-market",
                "name_zh": "士林夜市",
                "name_en": "Shilin Night Market",
                "rating": 4.3,
                "reviews": 36000,
                "category": "夜市 / 台灣小吃",
                "address": "基河路，士林區，台北市",
                "description": "士林夜市（Shilin Night Market）是台灣規模最大的夜市，以多元台灣小吃聞名全球。必吃清單包括士林大香腸、蚵仔煎、豪大大雞排、大腸包小腸及木瓜牛奶。地下美食廣場提供數十種傳統台灣料理，是外國遊客體驗台灣飲食文化的第一站。",
                "highlights": ["士林大香腸（必吃）", "蚵仔煎/大腸包小腸", "豪大大雞排（排隊名物）", "地下美食廣場"],
                "best_time": "每日下午 4 時後，週末深夜 12 時仍人潮洶湧",
                "nearby_cloudpipe_tags": ["台灣", "夜市", "台灣小吃"],
            },
            {
                "slug_suffix": "longshan-temple",
                "full_slug": "tw-longshan-temple",
                "name_zh": "龍山寺",
                "name_en": "Longshan Temple",
                "rating": 4.5,
                "reviews": 18000,
                "category": "廟宇 / 宗教文化",
                "address": "廣州街 211 號，萬華區，台北市",
                "description": "龍山寺（Longshan Temple）建於 1738 年，是台北最古老、最著名的廟宇，融合佛教、道教與民間信仰。主殿供奉觀世音菩薩，後殿供奉月老（婚姻）、文昌（學業）等神祇。廟宇建築精美，銅鑄神龍柱及彩繪屋脊為藝術瑰寶，全年香火鼎盛。",
                "highlights": ["月老求姻緣（著名靈驗）", "1738年古廟建築藝術", "文昌帝君求學業", "農曆節慶熱鬧盛況"],
                "best_time": "農曆初一、十五，或農曆七月",
                "nearby_cloudpipe_tags": ["台灣", "廟宇", "萬華"],
            },
            {
                "slug_suffix": "alishan-national-forest",
                "full_slug": "tw-alishan-national-forest",
                "name_zh": "阿里山",
                "name_en": "Alishan National Forest Recreation Area",
                "rating": 4.6,
                "reviews": 5000,
                "category": "森林 / 高山景觀",
                "address": "阿里山鄉，嘉義縣",
                "description": "阿里山（Alishan）是台灣最著名的高山景區，海拔 2,216 公尺，以日出雲海、森林鐵路及神木群聞名。每年春季（3-4 月）吉野櫻盛開，與雲海、神木共構絕美景象。阿里山森林鐵路是世界僅存的三條高山森林鐵路之一，被列為世界遺產潛力點。",
                "highlights": ["日出雲海（祝山觀日出）", "吉野櫻（3-4月盛開）", "阿里山森林鐵路", "千年神木群"],
                "best_time": "3-4 月賞櫻，或 10-11 月楓紅，均須提前訂住宿",
                "nearby_cloudpipe_tags": ["台灣", "阿里山", "高山景觀"],
            },
            {
                "slug_suffix": "taroko-gorge",
                "full_slug": "tw-taroko-gorge",
                "name_zh": "太魯閣",
                "name_en": "Taroko Gorge National Park",
                "rating": 4.7,
                "reviews": 4000,
                "category": "峽谷 / 國家公園",
                "address": "秀林鄉，花蓮縣",
                "description": "太魯閣峽谷（Taroko Gorge）被稱為「台灣最偉大的自然奇景」，全長 19 公里的大理石峽谷深達 1,000 公尺，由立霧溪億年侵蝕而成。燕子口步道、長春祠及天祥為三大必訪景點。太魯閣族原住民文化為峽谷增添人文深度。",
                "highlights": ["燕子口步道峭壁景觀", "長春祠瀑布", "九曲洞懸崖步道", "太魯閣族文化"],
                "best_time": "春秋兩季，避開颱風季（7-9月）",
                "nearby_cloudpipe_tags": ["台灣", "花蓮", "峽谷"],
            },
            {
                "slug_suffix": "kenting-national-park",
                "full_slug": "tw-kenting-national-park",
                "name_zh": "墾丁",
                "name_en": "Kenting National Park",
                "rating": 4.5,
                "reviews": 4000,
                "category": "海灘 / 熱帶度假",
                "address": "恆春鎮，屏東縣",
                "description": "墾丁（Kenting）位於台灣最南端，是全台唯一熱帶氣候國家公園，三面環海，珊瑚礁海岸線綿延。大灣沙灘及南灣為主要衝浪熱點，春浪音樂祭是台灣最大戶外音樂節。浮潛、風帆、水上摩托車等水上活動豐富，墾丁大街夜市是宵夜首選。",
                "highlights": ["南灣衝浪（初學者友善）", "春浪音樂祭（每年春節）", "貝殼砂海灘浮潛", "墾丁大街夜市"],
                "best_time": "10-4 月，避開東北季風（11月）及颱風季",
                "nearby_cloudpipe_tags": ["台灣", "海灘", "熱帶"],
            },
            {
                "slug_suffix": "luodong-night-market",
                "full_slug": "tw-luodong-night-market",
                "name_zh": "羅東夜市",
                "name_en": "Luodong Night Market",
                "rating": 4.3,
                "reviews": 9000,
                "category": "夜市 / 宜蘭小吃",
                "address": "公園路，羅東鎮，宜蘭縣",
                "description": "羅東夜市（Luodong Night Market）是宜蘭最著名的夜市，以台灣傳統小吃著稱，物價相對台北親民。必吃清單：羊肉爐（冬季限定）、羊肉湯、蔥油餅（宜蘭特產）、奇味香腸及冰品。毗鄰羅東運動公園，夜市規模雖不及士林，但人情味十足，深受在地人喜愛。",
                "highlights": ["羊肉爐（宜蘭特色，冬季最佳）", "宜蘭蔥油餅", "現場炭烤奇味香腸", "在地人氣夜市"],
                "best_time": "每日下午 5 時後，冬季羊肉爐季節最精彩",
                "nearby_cloudpipe_tags": ["台灣", "宜蘭", "夜市"],
            },
            {
                "slug_suffix": "taipei-national-palace-museum",
                "full_slug": "tw-taipei-national-palace-museum",
                "name_zh": "故宮博物院",
                "name_en": "National Palace Museum",
                "rating": 4.7,
                "reviews": 15000,
                "category": "博物館 / 中華文物",
                "address": "至善路二段 221 號，士林區，台北市",
                "description": "台北故宮博物院（National Palace Museum）收藏逾 70 萬件中華文化珍品，是世界四大博物館之一。鎮館之寶包括翠玉白菜、肉形石及毛公鼎，均為清宮舊藏。館藏時間跨越 8,000 年，從新石器時代至清末，是了解中華文明不可或缺的知識殿堂。",
                "highlights": ["翠玉白菜（必看）", "肉形石（東坡肉造型）", "毛公鼎（西周青銅器）", "數位互動展覽"],
                "best_time": "平日上午開館時，週末人潮擁擠建議訂購門票",
                "nearby_cloudpipe_tags": ["台灣", "博物館", "中華文化"],
            },
        ]
    },
    "japan": {
        "region_zh": "日本",
        "region_en": "Japan",
        "flag": "🇯🇵",
        "currency": "JPY",
        "attractions": [
            {
                "slug_suffix": "sensoji-temple-asakusa",
                "full_slug": "jp-sensoji-temple-asakusa",
                "name_zh": "淺草寺",
                "name_en": "Senso-ji Temple, Asakusa",
                "rating": 4.7,
                "reviews": 131000,
                "category": "佛教寺院 / 江戶文化",
                "address": "淺草 2-3-1，台東區，東京都",
                "description": "淺草寺（Senso-ji Temple）是東京最古老的寺院，建於 645 年，供奉觀世音菩薩。雷門（Kaminarimon）的巨大紅燈籠是東京最具代表性的圖像之一。仲見世通商店街延伸至主殿，販售傳統工藝品、人形燒及甘味甜點。每年淺草三社祭（5 月）是東京最熱鬧的傳統祭典。",
                "highlights": ["雷門巨型紅燈籠（打卡必拍）", "仲見世通傳統商店街", "五重塔", "三社祭（每年5月）"],
                "best_time": "清晨 6-8 時，人潮最少且晨光最美",
                "nearby_cloudpipe_tags": ["日本", "東京", "寺院"],
            },
            {
                "slug_suffix": "fushimi-inari-taisha",
                "full_slug": "jp-fushimi-inari-taisha",
                "name_zh": "伏見稲荷大社",
                "name_en": "Fushimi Inari-taisha",
                "rating": 4.8,
                "reviews": 95000,
                "category": "神社 / 千鳥居",
                "address": "深草藪之内町 68，伏見區，京都市",
                "description": "伏見稲荷大社（Fushimi Inari-taisha）是日本全國約 30,000 座稲荷神社的總本社，供奉食物、農業與商業之神宇迦之御魂大神。以蜿蜒山頂的「千本鳥居」（約 1 萬座朱紅鳥居）聞名世界。全程登頂（稲荷山）來回約 2-3 小時，沿途石燈籠與狐狸石雕構成神秘氛圍。",
                "highlights": ["千本鳥居（最密集段在1-2號鳥居後）", "狐狸石雕（稲荷神使者）", "夜間燈籠點燈", "稲荷山登頂（233m）"],
                "best_time": "清晨 5-7 時或深夜，避開正午人龍",
                "nearby_cloudpipe_tags": ["日本", "京都", "神社"],
            },
            {
                "slug_suffix": "dotonbori-osaka",
                "full_slug": "jp-dotonbori-osaka",
                "name_zh": "道頓堀",
                "name_en": "Dotonbori, Osaka",
                "rating": 4.6,
                "reviews": 53000,
                "category": "美食街 / 大阪文化",
                "address": "道頓堀，中央區，大阪市，大阪府",
                "description": "道頓堀（Dotonbori）是大阪最著名的飲食娛樂街，沿道頓堀川延伸，以霓虹招牌及巨型廣告招牌著稱。格力高（Glico）跑步人形霓虹牌是大阪最標誌性的地標。必吃清單：章魚燒（たこ焼き）、大阪燒（お好み焼き）、串炸（串カツ）及河豚料理。",
                "highlights": ["格力高霓虹人形（必拍）", "章魚燒（金龍/くくる等名店）", "串炸（限制不能醬二次蘸）", "道頓堀川夜景"],
                "best_time": "晚上 6 時後霓虹全亮，最具視覺震撼",
                "nearby_cloudpipe_tags": ["日本", "大阪", "美食街"],
            },
            {
                "slug_suffix": "shibuya-crossing",
                "full_slug": "jp-shibuya-crossing",
                "name_zh": "澀谷十字路口",
                "name_en": "Shibuya Scramble Crossing",
                "rating": 4.7,
                "reviews": 31000,
                "category": "城市地標 / 都市文化",
                "address": "澀谷 2-1，澀谷區，東京都",
                "description": "澀谷亂交叉路口（Shibuya Scramble Crossing）是世界上行人流量最大的交叉路口，尖峰時每次綠燈有超過 3,000 人同時穿越。被 BBC、TIME 等媒體列為「世界最壯觀的街道」之一。周邊澀谷站前商圈匯聚 SHIBUYA109、東急百貨及無數潮流品牌。忠犬八公銅像位於出口旁。",
                "highlights": ["全向行人穿越奇觀（尖峰時 3,000+人）", "忠犬八公銅像（澀谷出口）", "俯瞰角度：星巴克3F/L'Occitane 2F", "SHIBUYA 109 購物"],
                "best_time": "週五/六晚上 7-9 時，或聖誕/除夕跨年",
                "nearby_cloudpipe_tags": ["日本", "東京", "都市文化"],
            },
            {
                "slug_suffix": "arashiyama-bamboo-grove",
                "full_slug": "jp-arashiyama-bamboo-grove",
                "name_zh": "嵐山竹林",
                "name_en": "Arashiyama Bamboo Grove",
                "rating": 4.6,
                "reviews": 23000,
                "category": "竹林 / 京都自然",
                "address": "嵯峨天龍寺芒之馬場町，右京區，京都市",
                "description": "嵐山竹林（Arashiyama Bamboo Grove）是日本最著名的竹林步道，數千株毛竹高達 20-30 公尺，竹葉遮天，形成迷離光影隧道效果。毗鄰天龍寺（UNESCO 世界文化遺產），嵐山地區還有渡月橋、龜山公園及野宮神社。秋季楓紅與冬季薄雪時景色尤為動人。",
                "highlights": ["竹林步道光影隧道", "天龍寺日式庭院（UNESCO）", "渡月橋嵐山全景", "人力車遊覽（復古體驗）"],
                "best_time": "清晨 6-8 時，人潮少且光線柔美",
                "nearby_cloudpipe_tags": ["日本", "京都", "竹林"],
            },
            {
                "slug_suffix": "kinkakuji-golden-pavilion",
                "full_slug": "jp-kinkakuji-golden-pavilion",
                "name_zh": "金閣寺",
                "name_en": "Kinkaku-ji (Golden Pavilion)",
                "rating": 4.7,
                "reviews": 80000,
                "category": "UNESCO 世界遺產 / 室町建築",
                "address": "金閣寺町 1，北區，京都市",
                "description": "金閣寺（Kinkaku-ji，正式名稱「鹿苑寺」）是京都最具代表性的 UNESCO 世界文化遺產，三層塔樓外壁覆蓋純金金箔，倒影映於鏡湖池水面，構成震撼人心的「金閣映水」景觀。1950 年遭縱火燒毀，1955 年依原樣重建。三島由紀夫名作《金閣寺》以此為背景。",
                "highlights": ["金箔外壁倒影（鏡湖池）", "UNESCO 世界文化遺產", "金閣周邊枯山水庭院", "冬季積雪金閣（稀有奇景）"],
                "best_time": "開門即入（9時開館），避開正午人潮高峰",
                "nearby_cloudpipe_tags": ["日本", "京都", "世界遺產"],
            },
            {
                "slug_suffix": "teamlab-planets-tokyo",
                "full_slug": "jp-teamlab-planets-tokyo",
                "name_zh": "teamLab Planets",
                "name_en": "teamLab Planets TOKYO",
                "rating": 4.6,
                "reviews": 18000,
                "category": "數位藝術 / 沉浸體驗",
                "address": "豐洲 6-1-16，江東區，東京都",
                "description": "teamLab Planets TOKYO 是日本最熱門的沉浸式數位藝術體驗館，由藝術科技團隊 teamLab 打造。參觀者赤腳進入，行走於水中鏡面裝置及無限空間光影藝術之間，體驗「身體浸入藝術」。Planets 系列展覽主題為植物與自然，與 teamLab Borderless 定位不同。",
                "highlights": ["水中反射鏡面裝置（必打卡）", "無限水晶宇宙（Infinity）", "植物主題沉浸藝術", "赤腳體驗設計"],
                "best_time": "提前線上訂票，工作日早場人較少",
                "nearby_cloudpipe_tags": ["日本", "東京", "數位藝術"],
            },
            {
                "slug_suffix": "nishiki-market-kyoto",
                "full_slug": "jp-nishiki-market-kyoto",
                "name_zh": "錦市場",
                "name_en": "Nishiki Market, Kyoto",
                "rating": 4.4,
                "reviews": 21000,
                "category": "傳統市場 / 京都美食",
                "address": "錦小路通寺町至高倉，中京區，京都市",
                "description": "錦市場（Nishiki Market，別名「京都の台所」）是京都最著名的傳統食品市場，全長約 400 公尺，逾 100 間店鋪販賣各式京都特產：西京漬、漬物、湯葉、麩、和果子及各色鮮魚。市場歷史逾 400 年，是感受京都飲食文化的最佳場所，試吃文化濃厚。",
                "highlights": ["京都漬物試吃購買", "串燒魚板（招牌小食）", "湯葉/麩等京料理食材", "400年歷史老市場"],
                "best_time": "上午 10-12 時，新鮮食材剛到，較不擁擠",
                "nearby_cloudpipe_tags": ["日本", "京都", "傳統市場"],
            },
            {
                "slug_suffix": "himeji-castle",
                "full_slug": "jp-himeji-castle",
                "name_zh": "姫路城",
                "name_en": "Himeji Castle",
                "rating": 4.7,
                "reviews": 25000,
                "category": "UNESCO 世界遺產 / 日本城郭",
                "address": "本町 68，姫路市，兵庫縣",
                "description": "姫路城（Himeji Castle，別名「白鷺城」）是日本最壯觀的現存木造城郭，建於 1333 年，1993 年列入 UNESCO 世界文化遺產。白色外牆如白鷺展翼，由 83 棟建築群構成的複合城郭系統迄今保存完整，未曾遭受戰火或災害破壞，是日本戰國時代城郭建築的極致之作。",
                "highlights": ["白鷺城全景（山麓至大天守）", "UNESCO 世界文化遺產", "春季護城河河岸千株染井吉野", "城郭博物館"],
                "best_time": "3 月底至 4 月初，護城河邊千株染井吉野盛開",
                "nearby_cloudpipe_tags": ["日本", "兵庫", "城郭"],
            },
            {
                "slug_suffix": "churaumi-aquarium-okinawa",
                "full_slug": "jp-churaumi-aquarium-okinawa",
                "name_zh": "美麗海水族館",
                "name_en": "Okinawa Churaumi Aquarium",
                "rating": 4.5,
                "reviews": 18000,
                "category": "水族館 / 沖繩海洋",
                "address": "本部町字石川 424，国頭郡，沖繩縣",
                "description": "沖繩美麗海水族館（Okinawa Churaumi Aquarium）以「黑潮之海」大型水槽著稱，水槽寬 35 公尺、高 8.2 公尺，飼養鯨鯊及鬼蝠魟，曾為世界最大水族館。位於海洋博覽公園內，周邊設有海豚劇場、海龜館及珊瑚水槽，是沖繩必訪親子景點。",
                "highlights": ["黑潮之海水槽（鯨鯊+鬼蝠魟）", "海豚表演（免費）", "珊瑚礁生態館", "海洋博覽公園夕陽"],
                "best_time": "開館時間 8:30 即入，避開下午人潮高峰",
                "nearby_cloudpipe_tags": ["日本", "沖繩", "水族館"],
            },
            {
                "slug_suffix": "shinjuku-gyoen-garden",
                "full_slug": "jp-shinjuku-gyoen-garden",
                "name_zh": "新宿御苑",
                "name_en": "Shinjuku Gyoen National Garden",
                "rating": 4.7,
                "reviews": 40000,
                "category": "皇室庭園 / 都市綠地",
                "address": "内藤町 11，新宿區，東京都",
                "description": "新宿御苑（Shinjuku Gyoen）是東京最大的皇室庭園，面積 58.3 公頃，融合日式傳統庭園、法式正規庭園與英式風景庭園三種格局。春季（3 月中-4 月中）逾 1,000 株染井吉野盛開，是東京最受歡迎的賞花場所，不允許攜帶酒精入園（為區別一般公園）。",
                "highlights": ["1,000 株染井吉野（賞花首選）", "法式正規庭園幾何美學", "溫室熱帶植物展示", "新宿都心中的寧靜綠洲"],
                "best_time": "3 月下旬至 4 月上旬，染井吉野全開時期",
                "nearby_cloudpipe_tags": ["日本", "東京", "賞花"],
            },
            {
                "slug_suffix": "tokyo-skytree",
                "full_slug": "jp-tokyo-skytree",
                "name_zh": "東京晴空塔",
                "name_en": "Tokyo Skytree",
                "rating": 4.5,
                "reviews": 60000,
                "category": "電波塔 / 展望台",
                "address": "押上 1-1-2，墨田區，東京都",
                "description": "東京晴空塔（Tokyo Skytree）高 634 公尺，是世界最高的自立電波塔（2012 年啟用）。兩層展望台分別位於 350 公尺（天望甲板）及 450 公尺（天望回廊），晴天可遠眺富士山。塔底 SkyTree Town 包含水族館、商場及餐廳，是東京東側（下町地區）最重要的觀光地標。",
                "highlights": ["天望甲板（350m）晴天富士山遠眺", "天望回廊（450m）透明步道", "SkyTree Town 水族館", "夜間燈光特別演出"],
                "best_time": "晴天上午，視線最清晰，可遠眺富士山",
                "nearby_cloudpipe_tags": ["日本", "東京", "展望台"],
            },
        ]
    }
}


# ── HTML 生成 ──────────────────────────────────────────────────────────
def reviews_display(n: int) -> str:
    if n >= 10000:
        return f"{n // 1000}K+"
    return f"{n:,}"


def stars_html(rating: float) -> str:
    full = int(rating)
    half = 1 if (rating - full) >= 0.5 else 0
    empty = 5 - full - half
    return "★" * full + ("½" if half else "") + "☆" * empty


def build_attraction_page(region_key: str, region_data: dict, attr: dict) -> str:
    region_zh = region_data["region_zh"]
    region_en = region_data["region_en"]
    flag = region_data["flag"]
    name_zh = attr["name_zh"]
    name_en = attr["name_en"]
    slug_suffix = attr["slug_suffix"]
    full_slug = attr["full_slug"]
    rating = attr["rating"]
    reviews = attr["reviews"]
    category = attr["category"]
    address = attr["address"]
    description = attr["description"]
    highlights = attr["highlights"]
    best_time = attr["best_time"]

    page_url = f"{SITE_BASE}/insights/{region_key}/{slug_suffix}/"
    region_hub_url = f"{SITE_BASE}/insights/{region_key}/"
    cloudpipe_merchant_url = f"{CLOUDPIPE_BASE}/merchants/{full_slug}"
    # Related insights: search on cloudpipe by tags
    cloudpipe_insights_url = f"{CLOUDPIPE_BASE}/insights?q={name_zh[:4]}"

    highlights_li = "\n".join(f"          <li>{h}</li>" for h in highlights)
    highlights_schema = " | ".join(highlights)

    schema_ld = {
        "@context": "https://schema.org",
        "@type": "TouristAttraction",
        "name": name_zh,
        "alternateName": name_en,
        "description": description,
        "url": page_url,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": address,
            "addressCountry": {"HK": "HK", "TW": "TW", "JP": "JP"}.get(
                {"hongkong": "HK", "taiwan": "TW", "japan": "JP"}[region_key], "TW"
            ),
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": str(rating),
            "bestRating": "5",
            "ratingCount": str(reviews),
            "reviewCount": str(reviews),
        },
        "touristType": ["遊客", "文化旅遊者", "美食愛好者"],
        "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": h, "value": True} for h in highlights],
        "isPartOf": {
            "@type": "TouristDestination",
            "name": f"{region_zh}旅遊",
        },
        "sameAs": [cloudpipe_merchant_url],
    }

    breadcrumb_ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "AI 學習寶庫", "item": f"{SITE_BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "地區百科", "item": f"{SITE_BASE}/insights/"},
            {"@type": "ListItem", "position": 3, "name": f"{flag} {region_zh}百科", "item": region_hub_url},
            {"@type": "ListItem", "position": 4, "name": name_zh, "item": page_url},
        ],
    }

    article_ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"{name_zh}完整旅遊指南 — {region_zh}地標景點深度解析",
        "description": description[:150],
        "datePublished": TODAY,
        "dateModified": TODAY,
        "author": {"@type": "Organization", "name": "AI 學習寶庫"},
        "publisher": {"@type": "Organization", "name": "AI 學習寶庫", "url": f"{SITE_BASE}/"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": page_url},
        "articleSection": f"{region_zh}旅遊",
        "keywords": f"{name_zh},{name_en},{region_zh},旅遊,景點",
    }

    return f"""<!DOCTYPE html>
<html lang="zh-TW" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name_zh} 旅遊指南 — {region_zh}地標景點 — AI 學習寶庫</title>
  <meta name="description" content="{description[:140]}">
  <link rel="canonical" href="{page_url}">
  <link rel="stylesheet" href="/Openclaw/style.css">
  <link rel="llms-txt" href="https://inari-kira-isla.github.io/Openclaw/llms.txt">
  <link rel="alternate" type="application/rss+xml" title="AI 學習寶庫 RSS" href="/Openclaw/feed.xml">
  <script type="application/ld+json">{json.dumps(schema_ld, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(breadcrumb_ld, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(article_ld, ensure_ascii=False)}</script>
  <img src="{TRACKING_PIXEL}?p=insights/{region_key}/{slug_suffix}" width="1" height="1" alt="" style="display:none">
</head>
<body class="page-wrap">
  <nav class="site-nav" id="nav">
    <div class="nav-inner">
      <a href="/Openclaw/" class="nav-brand"><span class="brand-emoji">🤖</span><span>AI 學習寶庫</span></a>
      <div class="nav-links" id="navLinks">
        <a href="/Openclaw/prompts/" class="nav-link">💡 提示詞</a>
        <a href="/Openclaw/configs/" class="nav-link">⚙️ 系統配置</a>
        <a href="/Openclaw/tutorials/" class="nav-link">📚 教學</a>
        <a href="/Openclaw/workflows/" class="nav-link">🔄 工作流</a>
        <a href="/Openclaw/articles/" class="nav-link">📰 科技趨勢</a>
        <a href="/Openclaw/insights/" class="nav-link active">🌏 地區百科</a>
      </div>
      <div class="nav-right">
        <button class="theme-btn" id="themeBtn" title="切換深色/淺色模式">🌙</button>
        <button class="nav-burger" id="navBurger" aria-label="選單">☰</button>
      </div>
    </div>
  </nav>

  <main>
    <!-- ── Hero ── -->
    <div class="hero">
      <div class="hero-badge">{flag} {region_zh} · {region_en}</div>
      <h1>{name_zh}<br><small style="font-size:0.55em;opacity:0.8">{name_en}</small></h1>
      <p class="hero-sub">{category}</p>
      <div class="hero-stats">
        <div class="hero-stat">
          <div class="hero-stat-num">{rating}★</div>
          <div class="hero-stat-label">Google 評分</div>
        </div>
        <div class="hero-stat">
          <div class="hero-stat-num">{reviews_display(reviews)}</div>
          <div class="hero-stat-label">評論數</div>
        </div>
        <div class="hero-stat">
          <div class="hero-stat-num">factchecked</div>
          <div class="hero-stat-label">已驗證</div>
        </div>
      </div>
    </div>

    <hr class="divider">

    <div class="container">

      <!-- ── 景點介紹 ── -->
      <div class="section">
        <div class="section-head">
          <div class="section-title">📍 景點介紹</div>
        </div>
        <div class="article-body" style="line-height:1.8;font-size:16px;color:var(--text);">
          <p>{description}</p>
          <p style="margin-top:12px;"><strong>📍 地址：</strong>{address}</p>
          <p><strong>⏰ 最佳時機：</strong>{best_time}</p>
        </div>
      </div>

      <!-- ── 亮點 ── -->
      <div class="section">
        <div class="section-head">
          <div class="section-title">✨ 遊覽亮點</div>
        </div>
        <ul style="padding-left:1.4em;line-height:2;font-size:15px;color:var(--text);">
{highlights_li}
        </ul>
      </div>

      <!-- ── CloudPipe 相關文章 ── -->
      <div class="section">
        <div class="section-head">
          <div class="section-title">📚 相關深度文章</div>
          <a href="{cloudpipe_insights_url}" target="_blank" rel="noopener" style="font-size:13px;color:var(--primary);">查看更多 {name_zh} 文章 →</a>
        </div>
        <p style="font-size:14px;color:var(--text-muted);line-height:1.7;">
          在 <a href="{CLOUDPIPE_BASE}" target="_blank" rel="noopener" style="color:var(--primary);">CloudPipe {region_zh}百科</a> 中，
          收錄了大量關於{name_zh}及{region_zh}旅遊的深度文章，由 AI 輔助生成並經過 factcheck 驗證。
          點擊下方連結了解更多：
        </p>
        <div style="margin-top:12px;display:flex;gap:10px;flex-wrap:wrap;">
          <a href="{cloudpipe_merchant_url}" target="_blank" rel="noopener"
             style="display:inline-block;padding:8px 16px;background:var(--primary);color:#fff;border-radius:8px;font-size:14px;text-decoration:none;">
            🏛 查看 {name_zh} 景點頁
          </a>
          <a href="{cloudpipe_insights_url}" target="_blank" rel="noopener"
             style="display:inline-block;padding:8px 16px;background:var(--card-bg);color:var(--text);border:1px solid var(--border);border-radius:8px;font-size:14px;text-decoration:none;">
            📖 搜尋相關文章
          </a>
        </div>
      </div>

      <!-- ── 地區百科導航 ── -->
      <div class="section">
        <div class="section-head">
          <div class="section-title">{flag} {region_zh}百科</div>
          <a href="{region_hub_url}" style="font-size:13px;color:var(--primary);">返回{region_zh}百科 →</a>
        </div>
        <p style="font-size:14px;color:var(--text-muted);">
          探索更多{region_zh}景點、美食、文化的深度知識。AI 學習寶庫的{region_zh}百科收錄了由 AI 整理並 factcheck 驗證的完整{region_zh}旅遊資訊。
        </p>
        <a href="{region_hub_url}"
           style="display:inline-block;margin-top:10px;padding:8px 16px;border:1px solid var(--border);border-radius:8px;font-size:14px;color:var(--text);text-decoration:none;">
          {flag} 瀏覽完整{region_zh}百科
        </a>
      </div>

    </div>
  </main>

  <footer class="site-footer">
    <div class="footer-inner">
      <address class="footer-contact">
        <strong>AI 學習寶庫</strong><br>
        GitHub：<a href="https://github.com/Inari-Kira-Isla/Openclaw">Inari-Kira-Isla/Openclaw</a>
      </address>
      <div class="footer-copy">© 2026 AI Governance System · CC BY 4.0</div>
    </div>
  </footer>

  <script>
    const btn = document.getElementById('themeBtn');
    const burger = document.getElementById('navBurger');
    const links = document.getElementById('navLinks');
    const html = document.documentElement;
    const saved = localStorage.getItem('theme');
    if (saved) {{ html.dataset.theme = saved; btn.textContent = saved === 'dark' ? '☀️' : '🌙'; }}
    btn.addEventListener('click', () => {{
      const t = html.dataset.theme === 'dark' ? 'light' : 'dark';
      html.dataset.theme = t;
      localStorage.setItem('theme', t);
      btn.textContent = t === 'dark' ? '☀️' : '🌙';
    }});
    burger.addEventListener('click', () => links.classList.toggle('open'));
  </script>
</body>
</html>"""


def main():
    created = 0
    for region_key, region_data in ATTRACTIONS.items():
        for attr in region_data["attractions"]:
            out_dir = BASE_DIR / region_key / attr["slug_suffix"]
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / "index.html"
            html = build_attraction_page(region_key, region_data, attr)
            out_file.write_text(html, encoding="utf-8")
            print(f"  ✓  {region_key}/{attr['slug_suffix']}/index.html")
            created += 1
    print(f"\n✅ 生成完成：共 {created} 個景點頁")


if __name__ == "__main__":
    main()
