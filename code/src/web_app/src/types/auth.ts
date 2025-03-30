export enum UserType {
    Customer,
    Business
}

export interface User {
    username: string
    id: number
    type: UserType
}

export interface Customer extends User {
    cid: number;
    name: string;
    age: number;
    gender: string;
    location: string;
    annual_income: number;
    education: string;
    occupation: string;
}

export interface Business extends User {
    bid: number;
    category: string;
    business_name: string;
    revenue: number;
    num_employees: number;
}