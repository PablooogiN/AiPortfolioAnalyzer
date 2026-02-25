import { useEffect, useState } from "react";
import { getCash, updateCash } from "../api/client";
import type { CashPositions as CashPositionsType } from "../types";

interface Props {
  onUpdated: () => void;
}

export default function CashPositions({ onUpdated }: Props) {
  const [preTaxCash, setPreTaxCash] = useState("");
  const [postTaxCash, setPostTaxCash] = useState("");
  const [saving, setSaving] = useState(false);
  const [dirty, setDirty] = useState(false);

  useEffect(() => {
    getCash().then((data: CashPositionsType) => {
      setPreTaxCash(data.pre_tax_cash.toString());
      setPostTaxCash(data.post_tax_cash.toString());
    });
  }, []);

  const handleSave = async () => {
    setSaving(true);
    try {
      const data = await updateCash({
        pre_tax_cash: parseFloat(preTaxCash) || 0,
        post_tax_cash: parseFloat(postTaxCash) || 0,
      });
      setPreTaxCash(data.pre_tax_cash.toString());
      setPostTaxCash(data.post_tax_cash.toString());
      setDirty(false);
      onUpdated();
    } finally {
      setSaving(false);
    }
  };

  const totalCash =
    (parseFloat(preTaxCash) || 0) + (parseFloat(postTaxCash) || 0);

  return (
    <div className="flex flex-wrap gap-3 items-end">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Pre-Tax Cash (401k/IRA)
        </label>
        <input
          type="number"
          value={preTaxCash}
          onChange={(e) => {
            setPreTaxCash(e.target.value);
            setDirty(true);
          }}
          placeholder="0.00"
          min="0"
          step="any"
          className="w-40 rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Post-Tax Cash (Brokerage)
        </label>
        <input
          type="number"
          value={postTaxCash}
          onChange={(e) => {
            setPostTaxCash(e.target.value);
            setDirty(true);
          }}
          placeholder="0.00"
          min="0"
          step="any"
          className="w-40 rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <div className="text-sm text-gray-600 self-center">
        Total Cash:{" "}
        <span className="font-semibold">
          ${totalCash.toLocaleString(undefined, { minimumFractionDigits: 2 })}
        </span>
      </div>
      {dirty && (
        <button
          onClick={handleSave}
          disabled={saving}
          className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {saving ? "Saving..." : "Save"}
        </button>
      )}
    </div>
  );
}
