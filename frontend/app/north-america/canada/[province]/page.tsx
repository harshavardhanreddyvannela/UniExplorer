import { PageShell } from "../../../../components/page-shell";
import { humanizeSlug } from "../../../../lib/format";

type Props = {
  params: Promise<{ province: string }>;
};

export default async function NorthAmericaCanadaProvincePage({ params }: Props) {
  const { province } = await params;
  const provinceLabel = humanizeSlug(province);

  return (
    <PageShell
      title={`Canada: ${provinceLabel}`}
      description="University listing for this Canadian province/territory will be populated from backend data."
    />
  );
}
