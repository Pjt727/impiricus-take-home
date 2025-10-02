import type { Physician, Message, ClassifyMessageResponse } from './types';

const API_BASE_URL = 'http://localhost:8000';

export async function getPhysicians(
    state?: string,
    specialty?: string
): Promise<Physician[]> {
    const params = new URLSearchParams();
    if (state) params.append('state', state);
    if (specialty) params.append('specialty', specialty);
    const response = await fetch(`${API_BASE_URL}/physicians?${params.toString()}`);
    if (!response.ok) {
        throw new Error('Failed to fetch physicians');
    }
    return response.json();
}

export async function getMessages(
    physicianId?: number | null,
    startDate?: Date | null,
    endDate?: Date | null
): Promise<Message[]> {
    const params = new URLSearchParams();
    if (physicianId) {
        params.append('physician_id', physicianId.toString());
    }
    if (startDate) {
        params.append('start_date', (<string>startDate.toISOString().split('T')[0]));
    }

    // for simplicity the frontend works in date's instead of datetime
    // it is better in this case to be inclusive
    if (endDate) {
        const end = new Date(endDate);
        end.setDate(end.getDate() + 1);
        params.append('end_date', (<string>end.toISOString().split('T')[0]));
    };
    const response = await fetch(`${API_BASE_URL}/messages?${params.toString()}`);
    if (!response.ok) {
        throw new Error('Failed to fetch messages');
    }
    return response.json();
}

export async function classifyMessage(messageId: number): Promise<ClassifyMessageResponse> {
    const response = await fetch(`${API_BASE_URL}/classify/${messageId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({}), // Assuming default compliance_version is fine
    });
    if (!response.ok) {
        throw new Error('Failed to classify message');
    }
    return response.json();
}
