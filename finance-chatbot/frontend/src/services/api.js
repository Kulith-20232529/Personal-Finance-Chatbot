import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const getDashboard = () => API.get("/dashboard");
export const sendMessage = (message) =>
  API.post("/chat", { message });