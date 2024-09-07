import axios from "axios";
import dotenv from "dotenv";

dotenv.config();

export const handler = async (event, context) => {
    const NEWS_API_URL = "https://newsapi.org/v2/everything";
    const API_KEY = process.env.API_KEY;
    const response = await axios.get(`${NEWS_API_URL}?q=keyword&apiKey=${API_KEY}`);
    // Unwind source and flatten it.
    const texts = response.data.articles.map((news) => {
        return [...Object.values(news.source), ...Object.values(news).slice(1)];
    });
    return {
        statusCode: 200,
        body: JSON.stringify(texts),
    };
}


handler(null, null);