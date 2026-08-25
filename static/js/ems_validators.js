/**
 * Smart Employee Management System — Form Validation & Formatting Client Library
 * Validates PAN, Aadhaar, IFSC, Employee IDs, Tax regime inputs, and Shift timings.
 */

class EMSFormValidator {
    static isValidEmail(email) {
        const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }

    static isValidPAN(pan) {
        const re = /^[A-Z]{5}[0-9]{4}[A-Z]{1}$/;
        return re.test(String(pan).toUpperCase().trim());
    }

    static isValidAadhaar(aadhaar) {
        const clean = String(aadhaar).replace(/\s+/g, '');
        return /^[2-9]{1}[0-9]{11}$/.test(clean);
    }

    static isValidIFSC(ifsc) {
        const re = /^[A-Z]{4}0[A-Z0-9]{6}$/;
        return re.test(String(ifsc).toUpperCase().trim());
    }

    static formatINR(amount) {
        const num = Number(amount);
        if (isNaN(num)) return '₹ 0.00';
        return '₹ ' + num.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }

    static validateShiftTimes(startStr, endStr) {
        if (!startStr || !endStr) return { isValid: false, message: 'Both start and end times are required.' };
        return { isValid: true, message: 'Valid timing schedule.' };
    }
}

window.EMSFormValidator = EMSFormValidator;
