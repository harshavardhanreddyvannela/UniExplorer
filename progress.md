# University Scrapers - Progress

| Region           | Completed | Total  | Status |
| ---------------- | --------- | ------ | ------ |
| Asia-Pacific     | 0         | 6      | ⏳     |
| British Isles    | 0         | 2      | ⏳     |
| Eastern Europe   | 2         | 2      | ✅     |
| North America    | 0         | 2      | ⏳     |
| Nordic Countries | 3         | 3      | ✅     |
| Southern Europe  | 1         | 3      | 🔄     |
| Western Europe   | 3         | 6      | 🔄     |
| **TOTAL**        | **9**     | **24** | **38%**|

---

## Asia-Pacific (0/6)

- [ ] Australia
- [ ] Japan
- [ ] New Zealand
- [ ] Singapore
- [ ] South Korea
- [ ] Taiwan

## British Isles (0/2)

- [ ] Ireland
- [ ] United Kingdom

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

## Southern Europe (1/3) 🔄

- [ ] Italy
- [ ] Portugal
- [x] Spain

## Western Europe (3/6) 🔄

- [x] Austria
- [x] Belgium
- [ ] France
- [ ] Germany
- [ ] Netherlands
- [x] Switzerland

---

## Summary

### Completed: 9/24 countries

### Key Technical Features Implemented

1. **Austria**: Multi-category extraction with regex type filtering (4 pages)
2. **Czechia**: Dual-path extraction (list items + fallback anchors), translation cleanup
3. **Denmark**: Multi-page list extraction with URL cleaning
4. **Belgium**: Combined Flanders JSON API + Wallonia section-heading extraction with dedupe
5. **Norway**: Section-indexed extraction (skip designated 4th section "Høgskular")
6. **Sweden**: Section-based h2 tracking with name cleanup (webbplats suffix, genitive 's' removal)
7. **Switzerland**: Generalized section-structure handling for complex federations and accordion-based organizations
8. **Poland**: RAD-on/POL-on API integration with token pagination and filtered extraction
9. **Spain**: RUCT Excel export download and parsing with filtered extraction

### Remaining: 15/24 countries

Stubs to implement: Australia, Canada, France, Germany, Ireland, Italy, Japan, Netherlands, New Zealand, Portugal, Singapore, South Korea, Taiwan, USA, United Kingdom

---

## Notes

### Spain: Universities Without Websites

The following 4 Spanish universities passed all RUCT filters but have no website listed in the official source Excel:

- Universidad de Valladolid
- Universidad de Zaragoza
- Universidad Internacional de Andalucía
- Universitat de Girona
