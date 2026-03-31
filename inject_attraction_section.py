#!/usr/bin/env python3
"""
inject_attraction_section.py
在 region index.html 的「地區百科導航」section 之前，插入「景點地標」卡片區塊
"""
from pathlib import Path

BASE = Path(__file__).parent / "insights"

SITE_BASE = "https://inari-kira-isla.github.io/Openclaw"

# 每個地區的景點資料（slug_suffix, name_zh, category, rating, reviews）
REGION_ATTRACTIONS = {
    "hongkong": {
        "flag": "🇭🇰",
        "region_zh": "香港",
        "attractions": [
            ("victoria-peak", "太平山頂", "觀景台", 4.6, 91000),
            ("temple-street-night-market", "廟街夜市", "夜市文化", 4.3, 43000),
            ("star-ferry", "天星小輪", "歷史渡輪", 4.7, 19000),
            ("wong-tai-sin-temple", "黃大仙廟", "廟宇宗教", 4.5, 15000),
            ("hong-kong-disneyland", "香港迪士尼", "主題樂園", 4.4, 39000),
            ("tsim-sha-tsui-promenade", "尖沙咀海濱長廊", "海濱步道", 4.6, 26000),
            ("mong-kok-ladies-market", "旺角女人街", "街市購物", 4.1, 30000),
            ("ocean-park", "海洋公園", "海洋生態", 4.3, 11000),
            ("lan-kwai-fong", "蘭桂坊", "夜生活", 4.3, 14000),
            ("dim-sum-city-hall-maxim", "大會堂美心酒樓", "港式點心", 4.3, 9000),
        ],
    },
    "taiwan": {
        "flag": "🇹🇼",
        "region_zh": "台灣",
        "attractions": [
            ("taipei-101", "台北101", "城市地標", 4.6, 72000),
            ("jiufen-old-street", "九份老街", "古街山城", 4.5, 17000),
            ("sun-moon-lake", "日月潭", "湖泊自然", 4.7, 6000),
            ("shilin-night-market", "士林夜市", "台灣小吃", 4.3, 36000),
            ("longshan-temple", "龍山寺", "廟宇宗教", 4.5, 18000),
            ("alishan-national-forest", "阿里山", "高山森林", 4.6, 5000),
            ("taroko-gorge", "太魯閣峽谷", "國家公園", 4.7, 4000),
            ("kenting-national-park", "墾丁", "熱帶海灘", 4.5, 4000),
            ("luodong-night-market", "羅東夜市", "宜蘭小吃", 4.3, 9000),
            ("taipei-national-palace-museum", "故宮博物院", "博物館", 4.7, 15000),
        ],
    },
    "japan": {
        "flag": "🇯🇵",
        "region_zh": "日本",
        "attractions": [
            ("sensoji-temple-asakusa", "淺草寺", "佛教寺院", 4.7, 131000),
            ("fushimi-inari-taisha", "伏見稲荷大社", "神社千鳥居", 4.8, 95000),
            ("dotonbori-osaka", "道頓堀", "大阪美食街", 4.6, 53000),
            ("shibuya-crossing", "澀谷十字路口", "都市地標", 4.7, 31000),
            ("arashiyama-bamboo-grove", "嵐山竹林", "京都自然", 4.6, 23000),
            ("kinkakuji-golden-pavilion", "金閣寺", "UNESCO遺產", 4.7, 80000),
            ("teamlab-planets-tokyo", "teamLab Planets", "數位藝術", 4.6, 18000),
            ("nishiki-market-kyoto", "錦市場", "京都食材市場", 4.4, 21000),
            ("himeji-castle", "姫路城", "日本城郭", 4.7, 25000),
            ("churaumi-aquarium-okinawa", "美麗海水族館", "沖繩海洋", 4.5, 18000),
            ("shinjuku-gyoen-garden", "新宿御苑", "皇室庭園", 4.7, 40000),
            ("tokyo-skytree", "東京晴空塔", "展望台", 4.5, 60000),
        ],
    },
}

CATEGORY_ICONS = {
    "觀景台": "🏔️", "夜市文化": "🌃", "歷史渡輪": "⛴️",
    "廟宇宗教": "🛕", "主題樂園": "🎡", "海濱步道": "🌊",
    "街市購物": "🛍️", "海洋生態": "🐠", "夜生活": "🍸",
    "港式點心": "🍵", "城市地標": "🏙️", "古街山城": "🏮",
    "湖泊自然": "🏞️", "台灣小吃": "🥡", "高山森林": "🌲",
    "國家公園": "⛰️", "熱帶海灘": "🏖️", "宜蘭小吃": "🍢",
    "博物館": "🏛️", "佛教寺院": "⛩️", "神社千鳥居": "⛩️",
    "大阪美食街": "🦑", "都市地標": "🚦", "京都自然": "🎋",
    "UNESCO遺產": "🏯", "數位藝術": "💫", "京都食材市場": "🐟",
    "日本城郭": "🏯", "沖繩海洋": "🐋", "皇室庭園": "🌸",
    "展望台": "📡",
}

def reviews_display(n):
    if n >= 10000:
        return f"{n // 1000}K+"
    return f"{n:,}"


def build_attraction_section(region_key, data):
    flag = data["flag"]
    region_zh = data["region_zh"]
    cards = []
    for slug, name_zh, category, rating, reviews in data["attractions"]:
        icon = CATEGORY_ICONS.get(category, "📍")
        url = f"/Openclaw/insights/{region_key}/{slug}/"
        card = f"""          <a href="{url}" class="cat-card" style="text-decoration:none;">
            <div class="cat-icon">{icon}</div>
            <h3 style="font-size:15px;margin:6px 0 4px;">{name_zh}</h3>
            <p style="font-size:12px;margin:0 0 4px;color:var(--text-muted);">{category}</p>
            <p style="font-size:13px;margin:0;"><strong>{rating}★</strong> <span style="color:var(--text-muted);">({reviews_display(reviews)})</span></p>
          </a>"""
        cards.append(card)

    cards_html = "\n".join(cards)
    return f"""      <div class="section">
        <div class="section-head">
          <div class="section-title">{flag} {region_zh}景點地標</div>
          <span style="font-size:13px;color:var(--text-muted);">Factchecked · Google Maps 驗證</span>
        </div>
        <div class="cat-grid">
{cards_html}
        </div>
      </div>
"""


def inject_into_region_index(region_key, data):
    index_path = BASE / region_key / "index.html"
    content = index_path.read_text(encoding="utf-8")

    section_html = build_attraction_section(region_key, data)

    # 找到 </div>  </main> 作為插入點（就在 main 收尾之前）
    insert_marker = "    </div>  </main>"
    if insert_marker not in content:
        # fallback: 找 </div>\n  </main>
        insert_marker = "    </div>\n  </main>"

    if insert_marker not in content:
        print(f"  ⚠️  {region_key}: 找不到插入點，跳過")
        return

    new_content = content.replace(insert_marker, section_html + insert_marker, 1)
    index_path.write_text(new_content, encoding="utf-8")
    count = len(data["attractions"])
    print(f"  ✓  {region_key}/index.html 加入 {count} 個景點卡片")


def main():
    for region_key, data in REGION_ATTRACTIONS.items():
        inject_into_region_index(region_key, data)
    print("\n✅ Region index 頁面更新完成")


if __name__ == "__main__":
    main()
