export interface KPI {
    amount: number;
}

export interface ProductKPI extends KPI {
    product_name: string;
}

export interface ModeKPI extends KPI {
    mode: string;
}

export interface KPIData {
    products: ProductKPI[];
    payment_mode: ModeKPI[];
}
