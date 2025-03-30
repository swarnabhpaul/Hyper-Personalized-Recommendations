export interface Spend {
    spend: number;
}

export interface CategorySpend extends Spend {
    category: string;
}

export interface ModeSpend extends Spend {
    mode: string;
}

export interface SpendData {
    category: CategorySpend[];
    payment_mode: ModeSpend[];
}