import Image from "next/image"
import { StaticImport } from "next/dist/shared/lib/get-img-props";

interface CurrencyIconProps {
  icon: string | StaticImport;
  label: string;
}

export default function CurrencyIcon({ icon, label }: CurrencyIconProps) {
  return (
    <Image src={icon} alt={label} width={40} height={40} />
  )
}
