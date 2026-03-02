import { PageShell } from "../../../components/page-shell";
import { humanizeSlug } from "../../../lib/format";

type Props = {
  params: Promise<{ region: string }>;
};

export default async function RegionCountriesPage({ params }: Props) {
  const { region } = await params;
  const regionLabel = humanizeSlug(region);

  return (
    <PageShell
      title={`${regionLabel} Countries`}
      description="Country list for this region will be populated from backend data."
    />
  );
}
