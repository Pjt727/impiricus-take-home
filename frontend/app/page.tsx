"use client";

import { useState } from "react";
import { Physician } from "../lib/types";
import styles from "./page.module.css";
import PhysicianSearch from "../components/PhysicianSearch";
import MessageSearch from "../components/MessageSearch";

export default function Home() {
    const [selectedPhysician, setSelectedPhysician] = useState<Physician | null>(
        null
    );


    return (
        <main className={styles.container}>
            <h1>Message Classifier</h1>

            <PhysicianSearch
                onSelectPhysician={setSelectedPhysician}
                selectedPhysician={selectedPhysician}
            />


            <hr className={styles.divider} />

            <MessageSearch
                initialPhysicianId={selectedPhysician ? selectedPhysician.physician_id : null}
            />
        </main>
    );
}

