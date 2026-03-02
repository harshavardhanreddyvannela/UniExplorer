#!/usr/bin/env zsh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p \
  scrapers/regions/north_america/us \
  scrapers/regions/north_america/canada \
  scrapers/regions/europe \
  scrapers/regions/asia_pacific

for dir in \
  scrapers/regions \
  scrapers/regions/north_america \
  scrapers/regions/north_america/us \
  scrapers/regions/north_america/canada \
  scrapers/regions/europe \
  scrapers/regions/asia_pacific
do
  [[ -f "$dir/__init__.py" ]] || : > "$dir/__init__.py"
done

us_states=(
  alabama alaska arizona arkansas california colorado connecticut delaware district_of_columbia
  florida georgia hawaii idaho illinois indiana iowa kansas kentucky louisiana maine maryland
  massachusetts michigan minnesota mississippi missouri montana nebraska nevada new_hampshire
  new_jersey new_mexico new_york north_carolina north_dakota ohio oklahoma oregon pennsylvania
  rhode_island south_carolina south_dakota tennessee texas utah vermont virginia washington
  west_virginia wisconsin wyoming
)

canada_divisions=(
  alberta british_columbia manitoba new_brunswick newfoundland_and_labrador northwest_territories
  nova_scotia nunavut ontario prince_edward_island quebec saskatchewan yukon
)

europe=(
  uk ireland spain portugal italy france netherlands belgium luxembourg malta greece bulgaria
  romania iceland denmark norway sweden finland estonia latvia lithuania czechia slovakia
  hungary austria switzerland germany poland
)

asia_pacific=(
  japan south_korea taiwan singapore hong_kong australia new_zealand
)

write_placeholder() {
  local file_path="$1"
  local scraper_name="$2"

  cat > "$file_path" <<EOF
from scrapers.template.scraper_template import BaseGeographyScraper


class GeographyScraper(BaseGeographyScraper):
    name = "${scraper_name}"

    def get_source_descriptors(self) -> list[dict]:
        return []

    def parse_source(self, source: dict, payload):
        return []
EOF
}

for state in "${us_states[@]}"; do
  write_placeholder "scrapers/regions/north_america/us/${state}.py" "north_america.us.${state}"
done

for division in "${canada_divisions[@]}"; do
  write_placeholder "scrapers/regions/north_america/canada/${division}.py" "north_america.canada.${division}"
done

for country in "${europe[@]}"; do
  write_placeholder "scrapers/regions/europe/${country}.py" "europe.${country}"
done

for country in "${asia_pacific[@]}"; do
  write_placeholder "scrapers/regions/asia_pacific/${country}.py" "asia_pacific.${country}"
done

echo "Generated scraper placeholders successfully."
