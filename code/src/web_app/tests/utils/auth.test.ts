import { describe, it, expect } from "vitest";
import { getUser, setUser } from "../../src/utils/auth";
import { UserType } from "../../src/types/auth";

describe('tests for auth utils', () => {
    describe('getUser', () => {
        it('should return null if no user is in sessionStorage', () => {
            sessionStorage.clear();
            expect(getUser()).toBeNull();
        });
        it('should return the parsed user if user is present', () => {
            sessionStorage.setItem('user', JSON.stringify({a: 1}));
            expect(getUser()).toStrictEqual({a: 1});
        });
    });

    describe('setUser', () => {
        it('should remove user from sessionStorage if given null', () => {
            sessionStorage.setItem('user', JSON.stringify({a: 1}));
            setUser(null);
            expect(sessionStorage.getItem('user')).toBeNull();
        });

        it('should replace user', () => {
            sessionStorage.setItem('user', JSON.stringify({a: 1}));
            setUser({username: "test", id: 2, type: UserType.Customer});
            expect(sessionStorage.getItem("user")).toEqual(JSON.stringify({username: "test", id: 2, type: UserType.Customer}));
        });
    })
})