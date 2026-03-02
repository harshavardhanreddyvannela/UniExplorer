import { PageShell } from "../../../components/page-shell";
import { humanizeSlug } from "../../../lib/format";

type Props = {
  params: Promise<{ region: string; country: string }>;
};

export default async function RegionCountryPage({ params }: Props) {
  const { region, country } = await params;
  const regionLabel = humanizeSlug(region);
  const countryLabel = humanizeSlug(country);

  return (
    <PageShell
      title={countryLabel}
      description={`University listing for ${regionLabel} → ${countryLabel} will be populated from backend data.`}
    />
  );
}
