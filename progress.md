# University Scrapers - Progress

| Region           | Completed | Total  | Status |
| ---------------- | --------- | ------ | ------ |
| Asia-Pacific     | 0         | 6      | ⏳     |
| British Isles    | 0         | 5      | ⏳     |
| Eastern Europe   | 2         | 2      | ✅     |
| North America    | 0         | 2      | ⏳     |
| Nordic Countries | 3         | 3      | ✅     |
| Southern Europe  | 0         | 3      | ⏳     |
| Western Europe   | 4         | 7      | 🔄     |
| **TOTAL**        | **9**     | **28** | **32%**|

---

## Asia-Pacific (0/6)

- [ ] Australia
- [ ] Japan
- [ ] New Zealand
- [ ] Singapore
- [ ] South Korea
- [ ] Taiwan

## British Isles (0/5)

- [ ] England
- [ ] Ireland
- [ ] Northern Ireland
- [ ] Scotland
- [ ] Wales

## Eastern Europe (2/2) ✅

- [x] Czechia
- [x] Poland

## North America (0/2)

- [ ] Canada
- [ ] USA

## Nordic Countries (3/3) ✅

- [x] Denmark
- [x] Norway
- [x] Sweden

## Southern Europe (0/3)

- [ ] Italy
- [ ] Portugal
- [ ] Spain

## Western Europe (4/7) 🔄

- [x] Austria
- [x] Flanders
- [ ] France
- [ ] Germany
- [ ] Netherlands
- [x] Switzerland
- [x] Wallonia

---

## Summary

### Completed: 9/28 countries

### Key Technical Features Implemented

1. **Austria**: Multi-category extraction with regex type filtering (4 pages)
2. **Czechia**: Dual-path extraction (list items + fallback anchors), translation cleanup
3. **Denmark**: Multi-page list extraction with URL cleaning
4. **Flanders**: JSON API parsing with type exclusions
5. **Norway**: Section-indexed extraction (skip designated 4th section "Høgskular")
6. **Sweden**: Section-based h2 tracking with name cleanup (webbplats suffix, genitive 's' removal)
7. **Switzerland**: Generalized section-structure handling for complex federations like HES-SO
   - Detects multi-section organizations via multiple P+UL patterns
   - Extracts heading links for sections WITH links
   - Extracts all sub-links for sections WITHOUT links
   - Works for any accordion-based organization with this pattern
8. **Wallonia**: Section-by-heading extraction (h2/h3 grouping)
9. **Poland**: RAD-on/POL-on API integration with token pagination and post-scrape filtering
   - Filters: institution kinds (church/private/public) + operating status
   - Maps official `www` field to `website`
   - Drops church institutions that do not provide a website

### Remaining: 19/28 countries

Stubs to implement: Australia, Canada, England, France, Germany, Ireland, Italy, Japan, Netherlands, New Zealand, Northern Ireland, Portugal, Scotland, Singapore, South Korea, Spain, Taiwan, USA, Wales
