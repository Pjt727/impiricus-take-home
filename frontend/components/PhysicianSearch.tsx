"use client";

import { useRef } from "react";
import { useState } from "react";
import type { Physician } from "../lib/types";
import styles from "../app/page.module.css";
import { getPhysicians } from "../lib/api";

interface PhysicianSearchProps {
    onSelectPhysician: (physician: Physician) => void;
    selectedPhysician: Physician | null;
}

export default function PhysicianSearch({
    onSelectPhysician,
    selectedPhysician,
}: PhysicianSearchProps) {
    const specialtyRef = useRef<HTMLInputElement>(null);
    const stateRef = useRef<HTMLInputElement>(null);
    const [physicians, setPhysicians] = useState<Physician[]>([]);
    const [loading, setLoadingPhysicians] = useState(false);
    const [error, setError] = useState<string | null>(null);


    const handleSearch = async () => {
        const specialty = specialtyRef.current?.value || "";
        const state = stateRef.current?.value || "";
        try {
            setLoadingPhysicians(true);
            setError(null);
            const data = await getPhysicians(state, specialty);
            setPhysicians(data);
        } catch (err) {
            setError("Failed to load physicians.");
        } finally {
            setLoadingPhysicians(false);
        }
    };

    return (
        <div className={styles.physicianSearch}>
            <h2>Physician Search</h2>
            <div className={styles.controls}>
                <input
                    type="text"
                    name="specialty"
                    placeholder="Specialty (e.g., Oncology)"
                    ref={specialtyRef}
                />
                <input
                    type="text"
                    name="state"
                    placeholder="State (e.g., NY)"
                    ref={stateRef}
                />
                <button type="button" onClick={handleSearch} disabled={loading}>
                    {loading ? "Searching..." : "Search Physicians"}
                </button>
            </div>
            {loading && <p>Loading physicians...</p>}
            {
                <ul className={styles.physicianList}>
                    {physicians.length == 0 && (
                        <li>No results</li>
                    )}
                    {physicians.map((p) => (
                        <li
                            key={p.physician_id}
                            className={
                                selectedPhysician?.physician_id === p.physician_id
                                    ? styles.selectedPhysician
                                    : ""
                            }
                            onClick={() => onSelectPhysician(p)}
                        >
                            {p.physician_id} {p.first_name} {p.last_name} ({p.specialty} | {p.state})
                        </li>
                    ))}
                </ul>
            }
            {error && <p className={styles.error}>{error}</p>}
        </div>
    );
}

