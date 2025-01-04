"use client";

import { useEffect, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import Image from "next/image";
import Input from "./components/input/Input";

export default function Exchange() {
  const currencies = {
    "usd": {}
  };  
  const from = {"code": "USD", "symbol": "$", "rate": 1.00};
  const to = {"code": "BRL", "symbol": "R$", "rate": 6.00};

  const [currentFromRate, setFromRate] = useState<number>(from.rate);
  const [currentToRate, setToRate] = useState<number>(to.rate);

  useEffect(() => {
    setToRate(currentFromRate * to.rate);
  }, [currentFromRate, to.rate]);

  useEffect(() => {
    setFromRate(currentToRate / to.rate);
  }, [currentToRate, to.rate]);

  const [isSwapped, setIsSwapped] = useState<boolean>(false);

  const handleSwap = () => {
    setIsSwapped(!isSwapped);
  };

  const inputFrom = (
    <motion.div
      key="inputFrom"
      initial={{ opacity: 0, x: -50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 50 }}
    >
      <Input
        label="USD"
        value={currentFromRate}
        icon="/assets/icons/USD.png"
        iconPosition={isSwapped ? "end" : "start"}
        onChange={(event) => setFromRate(parseFloat(event.target.value))}
      />
    </motion.div>
  );

  const inputTo = (
    <motion.div
      key="inputTo"
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -50 }}
    >
      <Input
        label="BRL"
        value={currentToRate}
        icon="/assets/icons/BRL.png"
        iconPosition={isSwapped ? "start" : "end"}
        onChange={(event) => setToRate(parseFloat(event.target.value))}
      />
    </motion.div>
  );

  return (
    <div className="min-h-96 flex justify-center items-center">
      <form action="" className="flex justify-center items-center gap-16">
        <div className="basis-2/5">
          <AnimatePresence mode="wait">
            {isSwapped ? inputTo : inputFrom}
          </AnimatePresence>
        </div>

        <div id="swap" className="cursor-pointer" onClick={handleSwap}>
          <Image src="/assets/icons/swap-horiz.svg" alt="Swap" width={40} height={40} />
        </div>

        <div className="basis-2/5">
          <AnimatePresence mode="wait">
            {isSwapped ? inputFrom : inputTo}
          </AnimatePresence>
        </div>
      </form>
    </div>
  );
};
