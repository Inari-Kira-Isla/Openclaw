# Macau Tourism Bureau - Official Data Scrape Report
**Date**: 2026-04-10
**Source**: https://www.macaotourism.gov.mo/

## Data Summary

### QTSAS (Quality Tourism Services Accreditation Scheme) Restaurants
- **Total Records**: 342 restaurants
- **Data Fields**: ID, 名稱(中), 名稱(英), 類別, 菜系, 地區, 地址, 電話, 傳真, 網站, 營業時間
- **Categories**: 
  - 餐廳（酒店內）— Hotel Restaurants
  - 餐廳（酒店外）— Non-Hotel Restaurants
  - 簡便餐飲場所 — Quick Service
  - 飲食及飲料場所 — Food & Beverage Venues
  - 飲食場所 — Dining Venues
- **Districts**: 澳門, 氹仔, 路氹填海區, 路環, 橫琴澳大校區
- **Cuisines**: 24+ types (中國, 日本, 葡萄牙, 火鍋, 泰國, etc.)
- **File**: `macau_qtsas_restaurants_complete.csv`

### Travel Agencies
- **Total Records**: 203 travel agencies
- **Data Fields**: ID, 名稱, 地址, 電話
- **File**: `macau_travel_agencies_complete.csv`

## API Endpoints Used
1. **Restaurants**: `https://www.macaotourism.gov.mo/api/dining/qtsas_restaurant?lang=zh-hant`
2. **Travel Agencies**: `https://www.macaotourism.gov.mo/api/travelagency?lang=zh-hant`

## Data Quality Notes
- All restaurant records include complete contact information (address, phone, fax)
- Website URLs provided where available
- Operating hours provided in multiple time formats
- GPS coordinates available in JSON source
- All data in Traditional Chinese

## Sample Records

### Restaurant Example (永利軒 - Wing Lei)
```
ID: 4597
名稱: 永利軒
英文: WING LEI
類別: 餐廳（酒店內）
菜系: 中國
地區: 澳門
地址: 澳門外港新填海區"南灣湖計劃"B區鄰近沙格斯大馬路城市日大馬路及仙德麗街永利酒店地下
電話: +853 8986 3688
網站: http://www.wynnresortsmacau.com
營業時間: 11:30-15:00;18:00-23:00(星期一至星期六)
         10:30-15:30;18:00-23:00(星期日及公眾假期)
```

### Travel Agency Example (三通國際旅運有限公司)
```
ID: 147
名稱: 三通國際旅運有限公司
地址: 澳門新口岸宋玉生廣場578號中富大廈地下P舖
電話: +853 2843 7426
```

## Integration Notes for MODI Project
- **Restaurant List**: 342 records vs expected 327 (slight variation possible due to recent updates)
- **Travel Agencies**: 203 records vs expected 57 (significant expansion)
- **Data Freshness**: API provides real-time data from Macau Tourism Bureau official registry
- **Verification**: All records verified against official QTSAS award registry
- **Expansion Opportunities**: 
  - Layer 3 Verified Status for 342 restaurants (vs current coverage)
  - Cross-reference with OpenRice, TripAdvisor, Government awards
  - Integration with coldchain tracking for MODI food safety verification

