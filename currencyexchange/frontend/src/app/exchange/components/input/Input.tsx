import Image from "next/image";
import { StaticImport } from "next/dist/shared/lib/get-img-props";
import CurrenciesDropdown from "../dropdown/Dropdown";
import "./styles.scss";

interface InputProps {
  label: string;
  value: string | number | readonly string[] | undefined;
  icon: string | StaticImport;
  iconPosition: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

export default function Input({label, value, icon, iconPosition, onChange }: InputProps) {
  const flexDirection = iconPosition == "end" ? "flex-row-reverse" : "flex-row";

  return (
    <div className={`input-group flex ${flexDirection} p-3 border-2 border-slate-300 rounded-full font-medium bg-transparent`}>
      <CurrenciesDropdown dropdownTrigger={
        <Image src={icon} alt={label} width={40} height={40} className="cursor-pointer" />
      } />
      <div className="flex justify-center items-center mx-5 border-b-2 border-slate-300">
        <input className="w-full text-slate-800 bg-transparent focus:outline-0" type="number" id={label} name={label} value={value} autoComplete="false" onChange={onChange} />
        <label className="px-2 ml-2 pt-0.5 border-l-2 border-slate-300 text-sm text-slate-400 pointer-events-none" htmlFor={label}>{label}</label>
      </div>
    </div>
  )
}
