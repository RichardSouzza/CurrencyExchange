import React from "react";
import { Dropdown, DropdownTrigger, DropdownMenu, DropdownItem } from "@nextui-org/react";
import CurrencyIcon from "../currencyicon/CurrencyIcon";

interface CurrenciesDropdownProps {
  dropdownTrigger: React.ReactNode;
}

export default function CurrenciesDropdown({ dropdownTrigger }: CurrenciesDropdownProps) {
  const currencies = ["AUD", "BGN", "BRL", "CAD", "CHF", "CNY", "DKK", "USD"];
  
  return (
    <Dropdown>
      <DropdownTrigger>
        {dropdownTrigger}
      </DropdownTrigger>
      <DropdownMenu variant="faded" aria-label="Currencies Dropdown" classNames={{list: "grid grid-cols-2 gap-4"}} onAction={(key) => alert(key)}>
        {currencies.map((currency) => (
          <DropdownItem
            key={currency}
            startContent={<CurrencyIcon icon={`/assets/icons/${currency}.png`} label={currency} />}
          >
            {currency}
          </DropdownItem>
        ))}
      </DropdownMenu>
    </Dropdown>
  );
}
