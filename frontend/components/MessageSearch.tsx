"use client";

import { useState, useEffect } from "react";
import type { Message, ClassifyMessageResponse } from "../lib/types";
import { getMessages, classifyMessage } from "../lib/api";
import styles from "../app/page.module.css";

/// Helper to get date strings in YYYY-MM-DD format
const toDateInputString = (date: Date) => {
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, "0");
    const day = date.getDate().toString().padStart(2, "0");
    return `${year}-${month}-${day}`;
};

interface MessageSearchProps {
    initialPhysicianId: number | null;
}

export default function MessageSearch({ initialPhysicianId }: MessageSearchProps) {
    const [physicianId, setPhysicianId] = useState("");

    const [startDate, setStartDate] = useState<Date | null>(null);
    const [endDate, setEndDate] = useState<Date | null>(new Date());

    const [messages, setMessages] = useState<Message[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const [classifying, setClassifying] = useState<Record<number, boolean>>({});
    const [classificationResults, setClassificationResults] = useState<
        Record<number, ClassifyMessageResponse | null>
    >({});

    const [lastSearched, setLastSearched] = useState<{
        physicianId: string;
        startDate: Date | null;
        endDate: Date | null;
    } | null>(null);

    useEffect(() => {
        if (initialPhysicianId !== null) {
            setPhysicianId(initialPhysicianId.toString());
        }
    }, [initialPhysicianId]);

    const handleSearch = async () => {
        try {
            setLoading(true);
            setError(null);
            setMessages([]);
            setClassificationResults({});
            const physicianIdNum = physicianId ? parseInt(physicianId, 10) : null;

            if (physicianId && isNaN(physicianIdNum!)) {
                setError("Invalid Physician ID.");
                setLoading(false);
                return;
            }
            const data = await getMessages(physicianIdNum, startDate, endDate);
            setMessages(data);
            setLastSearched({ physicianId, startDate, endDate });
        } catch (err) {
            setError("Failed to load messages.");
            setLastSearched(null);
        } finally {
            setLoading(false);
        }
    };

    const handleClassify = async (messageId: number) => {
        setClassifying((prev) => ({ ...prev, [messageId]: true }));
        try {
            const result = await classifyMessage(messageId);
            setClassificationResults((prev) => ({ ...prev, [messageId]: result }));
        } catch (err) {
            setError(`Failed to classify message ${messageId}.`);
            setClassificationResults((prev) => ({ ...prev, [messageId]: null }));
        } finally {
            setClassifying((prev) => ({ ...prev, [messageId]: false }));
        }
    };

    return (
        <div className={styles.messageView}>
            <h2>Message Search</h2>
            <div className={styles.controls}>
                <input
                    type="text"
                    name="physicianId"
                    placeholder="Physician ID"
                    value={physicianId}
                    onChange={(e) => setPhysicianId(e.target.value)}
                />
                <label htmlFor="start-date">From:</label>
                <input
                    type="date"
                    id="start-date"
                    value={startDate ? toDateInputString(startDate) : ""}
                    onChange={(e) => setStartDate(e.target.value ? new Date(e.target.value + "T00:00:00") : null)}
                />
                <label htmlFor="end-date">To:</label>
                <input
                    type="date"
                    id="end-date"
                    value={endDate ? toDateInputString(endDate) : ""}
                    onChange={(e) => setEndDate(e.target.value ? new Date(e.target.value + "T00:00:00") : null)}
                />
                <button type="button" onClick={handleSearch} disabled={loading}>
                    {loading ? "Searching..." : "Search Messages"}
                </button>
            </div>

            {error && <p className={styles.error}>{error}</p>}

            {lastSearched && !loading && (
                <div className={styles.searchResultsInfo}>
                    <p>
                        Results for:
                        <strong>{lastSearched.physicianId ? ` Physician ID ${lastSearched.physicianId}` : ' All Physicians'}</strong> Messages
                        {lastSearched.startDate && lastSearched.endDate ? (
                            <> from <strong>{toDateInputString(lastSearched.startDate)}</strong> to <strong>{toDateInputString(lastSearched.endDate)}</strong></>
                        ) : lastSearched.startDate ? (
                            <> after or on <strong>{toDateInputString(lastSearched.startDate)}</strong></>
                        ) : lastSearched.endDate ? (
                            <> before or on <strong>{toDateInputString(lastSearched.endDate)}</strong></>
                        ) : null}
                    </p>
                </div>
            )}

            {loading ? (
                <p>Loading messages...</p>
            ) : messages.length > 0 ? (
                <table>
                    <thead>
                        <tr>
                            <th>Timestamp</th>
                            <th>Topic</th>
                            <th>Sentiment</th>
                            <th>Message</th>
                            <th>Classification</th>
                        </tr>
                    </thead>
                    <tbody>
                        {messages.map((msg) => (
                            <tr key={msg.message_id}>
                                <td>{new Date(msg.timestamp).toLocaleString()}</td>
                                <td>{msg.topic ?? "N/A"}</td>
                                <td>{msg.sentiment ?? "N/A"}</td>
                                <td>{msg.message_text}</td>
                                <td>
                                    {!classifying[msg.message_id] &&
                                        !classificationResults[msg.message_id] && (
                                            <button
                                                onClick={() => handleClassify(msg.message_id)}
                                                disabled={classifying[msg.message_id]}
                                            >
                                                {classifying[msg.message_id]
                                                    ? "Classifying..."
                                                    : "Classify"}
                                            </button>
                                        )}
                                    {classificationResults[msg.message_id] && (
                                        <div className={styles.classificationResult}>
                                            {classificationResults[msg.message_id]!
                                                .matched_rules.length > 0 ? (
                                                <ul>
                                                    {classificationResults[
                                                        msg.message_id
                                                    ]!.matched_rules.map((rule) => (
                                                        <li key={rule.id}>
                                                            <strong>{rule.name} ({rule.result_type}):</strong>{" "}
                                                            {rule.result_text} {" "}
                                                            Matched:{" "}<u>
                                                                {rule.matched_keywords.join(", ")}
                                                            </u>
                                                        </li>
                                                    ))}
                                                </ul>
                                            ) : (
                                                <p>No rules triggered.</p>
                                            )}
                                        </div>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                lastSearched && <p>No messages found for the selected criteria.</p>
            )}
        </div>
    );
}

