export interface Physician {
    physician_id: number;
    npi: string;
    first_name: string;
    last_name: string;
    specialty: string;
    state: string;
    consent_opt_in: boolean;
    preferred_channel: string;
}

export interface Message {
    message_id: number;
    physician_id: number;
    channel: string;
    direction: string;
    timestamp: string;
    message_text: string;
    campaign_id?: string;
    topic?: string;
    compliance_tag?: string;
    sentiment?: string;
    delivery_status?: string;
    response_latency_sec?: number;
}

export interface RuleResponse {
    id: string;
    name: string;
    result_type: string;
    result_text: string;
    matched_keywords: string[];
}

export interface ClassifyMessageResponse {
    message_id: number;
    message_text: string;
    compliance_version: string;
    matched_rules: RuleResponse[];
}
