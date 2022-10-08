/**
 * The API object.
 */
export const API = {
    /**
     * Fetch the date range for the data type.
     *
     * @param dataType The data type.
     * @returns {Promise<Response>}
     */
    async dateRage(dataType) {
        return await fetch(`${API_URL}/dateRange/${dataType}`);
    },

    /**
     * Fetch the daily country data.
     *
     * @param startDate The start date of the data to fetch, as an ISO date string.
     * @param endDate The end date of the data to fetch, as an ISO date string.
     * @returns {Promise<Response>}
     */
    async dailyCountryData(startDate, endDate) {
        let url = `${API_URL}/data/daily/country`;
        let queryString = '';
        if (startDate) {
            queryString += `start_date=${startDate}`
        }
        if (endDate) {
            if (queryString) {
                queryString += '&';
            }
            queryString += `end_date=${endDate}`
        }
        if (queryString) {
            url += `?${queryString}`;
        }

        return await fetch(url);
    },

    /**
     * Fetch the country data per prefecture.
     *
     * @param date The date.
     * @returns {Promise<Response>}
     */
    async countryData(date) {
        let url = `${API_URL}/data/country/${date}`;

        return await fetch(url);
    }
}
